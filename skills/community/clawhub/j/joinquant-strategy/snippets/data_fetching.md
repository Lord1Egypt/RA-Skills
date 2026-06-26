# 数据获取常用代码

## 1. 获取历史行情数据

### 基本用法

```python
# 获取单只股票的历史数据
df = get_price('600000.XSHG', start_date='2020-01-01', end_date='2020-12-31', frequency='daily')

# 获取多只股票的历史数据
df = get_price(['600000.XSHG', '600519.XSHG'], start_date='2020-01-01', end_date='2020-12-31', frequency='daily')

# 获取分钟级数据
df = get_price('600000.XSHG', start_date='2020-01-01', end_date='2020-01-02', frequency='1m')
```

### 聚宽特有函数

```python
# 获取单只股票历史数据（聚宽特有）
df = attribute_history('000001.XSHE', 20, '1d', 
                       ['close', 'volume', 'high', 'low'])

# 获取多只股票历史数据（聚宽特有）
df = history(20, '1d', 'close', 
             ['000001.XSHE', '600000.XSHG'])
```

### 参数说明
- `security`：股票代码，可以是单个代码或代码列表
- `start_date`：开始日期
- `end_date`：结束日期
- `frequency`：数据频率，可选 'daily', '1m', '5m', '15m', '30m', '60m'
- `fields`：返回字段，默认为 ['open', 'close', 'high', 'low', 'volume', 'money']

## 2. 获取财务数据

### 基本用法

```python
# 获取财务指标
df = get_fundamentals(query(indicator), date='2020-12-31')

# 获取估值指标
df = get_fundamentals(query(valuation), date='2020-12-31')

# 获取资产负债表
df = get_fundamentals(query(balance), date='2020-12-31')

# 获取利润表
df = get_fundamentals(query(income), date='2020-12-31')

# 获取现金流量表
df = get_fundamentals(query(cash_flow), date='2020-12-31')
```

### 高级查询

```python
# 筛选条件查询
df = get_fundamentals(
    query(valuation.code, valuation.pe_ratio, indicator.roe)
    .filter(valuation.pe_ratio < 20)
    .filter(indicator.roe > 0.1)
    .order_by(indicator.roe.desc())
    .limit(10),
    date='2020-12-31'
)
```

## 3. 获取股票列表

### 基本用法

```python
# 获取所有股票列表
stock_list = get_all_securities(['stock'], date='2020-01-01')

# 获取沪深300成分股
hs300 = get_index_stocks('000300.XSHG', date='2020-01-01')

# 获取中证500成分股
zz500 = get_index_stocks('000905.XSHG', date='2020-01-01')

# 获取创业板成分股
cyb = get_index_stocks('399006.XSHE', date='2020-01-01')
```

## 4. 获取实时数据

### 基本用法

```python
# 获取实时数据
current_data = get_current_data()

# 获取单只股票的实时价格
price = current_data['600000.XSHG'].last_price

# 获取多只股票的实时价格
for stock in ['600000.XSHG', '600519.XSHG']:
    price = current_data[stock].last_price
    log.info(f'{stock} 当前价格：{price}')
```

## 5. 获取行业数据

### 基本用法

```python
# 获取行业分类
industry = get_industry_stocks('801010', date='2020-01-01')  # 801010 为农林牧渔行业代码

# 获取概念板块
concept = get_concept_stocks('GN001', date='2020-01-01')  # GN001 为融资融券概念代码
```

## 6. 获取宏观经济数据

### 基本用法

```python
# 获取宏观经济指标
df = macro.MAC_INDUSTRY_GDP.get_data()

# 获取利率数据
df = macro.MAC_INTEREST_RATE.get_data()

# 获取汇率数据
df = macro.MAC_EXCHANGE_RATE.get_data()
```

## 7. 数据处理技巧

### 基本用法

```python
# 计算收益率
df['returns'] = df['close'].pct_change()

# 计算移动平均线
df['ma5'] = df['close'].rolling(window=5).mean()
df['ma20'] = df['close'].rolling(window=20).mean()

# 计算成交量指标
df['volume_ma5'] = df['volume'].rolling(window=5).mean()

# 处理缺失值
df = df.dropna()

# 数据合并
df1 = get_price('600000.XSHG', start_date='2020-01-01', end_date='2020-12-31')
df2 = get_price('600519.XSHG', start_date='2020-01-01', end_date='2020-12-31')
merged_df = pd.concat([df1['close'], df2['close']], axis=1, keys=['600000', '600519'])
```

## 8. 获取技术指标

```python
# 使用TA-Lib计算指标
import talib
close_prices = attribute_history('000001.XSHE', 30, '1d', ['close'])['close'].values
sma = talib.SMA(close_prices, timeperiod=20)
```
