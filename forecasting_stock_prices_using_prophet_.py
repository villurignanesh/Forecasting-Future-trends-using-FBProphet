# -*- coding: utf-8 -*-
"""Forecasting Stock Prices using Prophet..ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HglePpqSSzPPMFyifDI0QbArOhwb_Ngl

Notebook from [Predicting the ‘Future’ with Facebook’s Prophet](https://towardsdatascience.com/predicting-the-future-with-facebook-s-prophet-bdfe11af10ff)

## Installation

`conda install pystan`

`conda install -c conda-forge fbprophet`

## Importing the dataset
"""

import pandas as pd
import numpy as np
from fbprophet import Prophet
import matplotlib.pyplot as plt
import pandas_datareader.data as pdr
# from google.colab import files
# uploaded=files.upload()
plt.style.use("fivethirtyeight")# for pretty graphs
# df = pd.read_excel('monthly_csv.xlsx')
# df.head()

"""## Analysing the datatypes"""

df=pdr.DataReader('TSLA',start='2015-1-1',end='2021-1-31',data_source='yahoo')
df

df=df.reset_index()

df=df.drop(labels=['High','Low','Open','Volume','Adj Close'],axis=1)

df

df['Date']=pd.to_datetime(df['Date'],infer_datetime_format=True)

df.dtypes

df

"""## Plotting to get insights"""

plt.figure(figsize=(20,16))
plt.plot(df.set_index(['Date'])['Close'])
# plt.legend(['Price'])

## Removing the Outliers: Optional



"""## Converting Views column to its log value"""

df['Close'] = np.log(df['Close'])
plt.figure(figsize=(10,6))
plt.plot(df.set_index(['Date'])['Close'])
plt.legend(['Price'])

"""## Making the dataset 'Prophet' compliant."""

df.columns = ['ds','y']
df.head()

"""## Making Predictions

Prophet follows the sklearn model API wherein an instance of the Prophet class is created and then the fit and predict methods are called. The model is instantiated by a new Prophet object and followed by calling its fit method and passing in the historical dataframe.
"""

m1 = Prophet(daily_seasonality=True)
m1.fit(df)

"""Prophet will by default fit weekly and yearly seasonalities if the time series is more than two cycles long. It will also fit daily seasonality for a sub-daily time series. You can add other seasonalities (monthly, quarterly, hourly)if required."""

future1 = m1.make_future_dataframe(periods=60)
forecast1 = m1.predict(future1)
forecast1.tail().T

forecast1[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

"""Since we took the log of Price, let's convert back to original values """

forecast_upscale=np.exp(forecast1[['yhat', 'yhat_lower', 'yhat_upper']])

"""## Plotting the Forecast"""

m1.plot(forecast1);

"""## Plotting the forecast components"""

m1.plot_components(forecast1);

"""## Holiday Effect"""

# Stocks = pd.DataFrame({
#   'holiday': 'Price',
#   'ds': pd.to_datetime(['2018-07-02', '2018-07-06', '2018-07-08',
#                         '2018-07-09', '2018-07-12', '2018-07-19', '2018-07-26', '2018-07-31',
#                         '2018-08-06', '2018-08-15', '2018-07-19', '2018-08-26', '2018-08-31',
#                         '2018-09-01', '2018-09-04', '2018-09-11', '2018-09-17', '2018-09-23',
#                         '2018-10-02', '2018-10-09', '2018-10-18', '2018-10-19', '2018-10-26',
#                         '2018-11-02', '2018-11-08', '2018-11-24', '2018-12-05', '2018-12-13',
#                         '2018-12-19', '2018-12-24', '2018-12-27', '2019-01-08', '2019-01-11',
#                         '2019-01-22', '2019-01-24', '2019-01-28', '2019-02-01', '2019-02-04',
#                         '2019-02-07', '2019-02-12', '2019-02-15', '2019-02-21', '2019-03-03',
#                         '2019-03-07', '2019-03-12', '2019-03-18', '2019-03-23' ]),
#   'lower_window': 0,
#   'upper_window': 5,
# })
# Stocks.head()

# m2 = Prophet(holidays=Stocks,daily_seasonality=True).fit(df)
# future2 = m2.make_future_dataframe(periods=90)
# forecast2 = m2.predict(future2)
# m2.plot(forecast2);

# m2.plot_components(forecast2);

"""## Predicting Views for the next 15 days"""

# m3 = Prophet(holidays=Stocks, mcmc_samples=300).fit(df)
# future3 = m3.make_future_dataframe(periods=60)
# forecast3 = m3.predict(future3)
# forecast3["Price"] = np.exp(forecast3.yhat).round()
# forecast3["Price_lower"] = np.exp(forecast3.yhat_lower).round()
# forecast3["Price_upper"] = np.exp(forecast3.yhat_upper).round()
# forecast3[(forecast3.ds > "3-22-2019") &
#           (forecast3.ds < "4-07-2019")][["ds","Price_lower",
#                                         "Price", "Price_upper"]]

# forecast3.head()

"""## Exporting the results to Excel"""

forecast1.to_excel('Predicted_Prices.xlsx')

forecast1.tail(10)