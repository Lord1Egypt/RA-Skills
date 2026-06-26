# 数据获取函数说明

## 1. 历史行情数据

### 1.1 get_price 函数

```python
def get_price(
    security,  # 股票代码，单个代码或代码列表
    start_date=None,  # 开始日期
    end_date=None,  # 结束日期
    frequency='daily',  # 数据频率：'daily', '1m', '5m', '15m', '30m', '60m'
    fields=None,  # 返回字段，默认为 ['open', 'close', 'high', 'low', 'volume', 'money']
    skip_paused=False,  # 是否跳过停牌日期
    fq='pre'  # 复权方式：'pre' 前复权, 'post' 后复权, None 不复权
):
    """获取历史行情数据"""
    pass
```

**参数说明**：
- `security`：股票代码，可以是单个代码或代码列表
- `start_date`：开始日期，格式为 'YYYY-MM-DD'
- `end_date`：结束日期，格式为 'YYYY-MM-DD'
- `frequency`：数据频率，可选 'daily', '1m', '5m', '15m', '30m', '60m'
- `fields`：返回字段，默认为 ['open', 'close', 'high', 'low', 'volume', 'money']
- `skip_paused`：是否跳过停牌日期，默认为 False
- `fq`：复权方式，可选 'pre' 前复权, 'post' 后复权, None 不复权

**返回值**：
- DataFrame，包含指定股票的历史行情数据

**示例**：
```python
# 获取单只股票的日线数据
df = get_price('600000.XSHG', start_date='2020-01-01', end_date='2020-12-31')

# 获取多只股票的分钟数据
df = get_price(['600000.XSHG', '600519.XSHG'], start_date='2020-01-01', end_date='2020-01-02', frequency='1m')
```

## 2. 财务数据

### 2.1 get_fundamentals 函数

```python
def get_fundamentals(
    query_object,  # 查询对象
    date=None,  # 查询日期
    statDate=None  # 财报统计日期
):
    """获取财务数据"""
    pass
```

**参数说明**：
- `query_object`：查询对象，使用 query() 函数构建
- `date`：查询日期，格式为 'YYYY-MM-DD'
- `statDate`：财报统计日期，格式为 'YYYY-MM'

**返回值**：
- DataFrame，包含查询的财务数据

**示例**：
```python
# 查询市盈率和市净率
df = get_fundamentals(
    query(valuation.code, valuation.pe_ratio, valuation.pb_ratio),
    date='2020-12-31'
)

# 带筛选条件的查询
df = get_fundamentals(
    query(valuation.code, valuation.pe_ratio)
    .filter(valuation.pe_ratio < 20)
    .order_by(valuation.pe_ratio.asc())
    .limit(10),
    date='2020-12-31'
)
```

### 2.2 query 函数

```python
query(
    indicator.roe,  # 要查询的字段
    valuation.pe_ratio
).filter(
    indicator.roe > 0.1  # 筛选条件
).order_by(
    indicator.roe.desc()  # 排序方式
).limit(
    10  # 限制返回数量
)
```

**功能**：
- 构建财务数据查询对象

## 3. 股票列表

### 3.1 get_all_securities 函数

```python
def get_all_securities(
    types=['stock'],  # 证券类型，可选 'stock', 'fund', 'index', 'futures', 'option'
    date=None  # 查询日期
):
    """获取所有证券列表"""
    pass
```

**参数说明**：
- `types`：证券类型列表
- `date`：查询日期，格式为 'YYYY-MM-DD'

**返回值**：
- DataFrame，包含证券列表及基本信息

**示例**：
```python
# 获取所有股票列表
stock_list = get_all_securities(['stock'], date='2020-01-01')

# 获取所有基金列表
fund_list = get_all_securities(['fund'], date='2020-01-01')
```

### 3.2 get_index_stocks 函数

```python
def get_index_stocks(
    index_symbol,  # 指数代码
    date=None  # 查询日期
):
    """获取指数成分股"""
    pass
```

**参数说明**：
- `index_symbol`：指数代码
- `date`：查询日期，格式为 'YYYY-MM-DD'

**返回值**：
- 列表，包含指数成分股代码

**示例**：
```python
# 获取沪深300成分股
hs300 = get_index_stocks('000300.XSHG', date='2020-01-01')

# 获取中证500成分股
zz500 = get_index_stocks('000905.XSHG', date='2020-01-01')
```

### 3.3 get_industry_stocks 函数

```python
def get_industry_stocks(
    industry_code,  # 行业代码
    date=None  # 查询日期
):
    """获取行业成分股"""
    pass
```

**参数说明**：
- `industry_code`：行业代码
- `date`：查询日期，格式为 'YYYY-MM-DD'

**返回值**：
- 列表，包含行业成分股代码

**示例**：
```python
# 获取农林牧渔行业成分股
agriculture_stocks = get_industry_stocks('801010', date='2020-01-01')
```

### 3.4 get_concept_stocks 函数

```python
def get_concept_stocks(
    concept_code,  # 概念代码
    date=None  # 查询日期
):
    """获取概念成分股"""
    pass
```

**参数说明**：
- `concept_code`：概念代码
- `date`：查询日期，格式为 'YYYY-MM-DD'

**返回值**：
- 列表，包含概念成分股代码

**示例**：
```python
# 获取融资融券概念成分股
margin_stocks = get_concept_stocks('GN001', date='2020-01-01')
```

## 4. 实时数据

### 4.1 get_current_data 函数

```python
def get_current_data():
    """获取实时数据"""
    pass
```

**返回值**：
- 字典，包含所有股票的实时数据

**示例**：
```python
# 获取实时数据
current_data = get_current_data()

# 获取单只股票的实时价格
price = current_data['600000.XSHG'].last_price

# 获取股票是否停牌
is_paused = current_data['600000.XSHG'].paused

# 获取股票是否涨停
is_limit_up = current_data['600000.XSHG'].limit_up

# 获取股票是否跌停
is_limit_down = current_data['600000.XSHG'].limit_down
```

## 5. 宏观经济数据

### 5.1 macro 模块

```python
# 获取GDP数据
df = macro.MAC_INDUSTRY_GDP.get_data()

# 获取利率数据
df = macro.MAC_INTEREST_RATE.get_data()

# 获取汇率数据
df = macro.MAC_EXCHANGE_RATE.get_data()

# 获取CPI数据
df = macro.MAC_CPI.get_data()

# 获取PPI数据
df = macro.MAC_PPI.get_data()
```

**功能**：
- 获取宏观经济指标数据

## 6. 其他数据函数

### 6.1 get_dividend 函数

```python
def get_dividend(
    security,  # 股票代码
    start_date=None,  # 开始日期
    end_date=None  # 结束日期
):
    """获取分红数据"""
    pass
```

**参数说明**：
- `security`：股票代码
- `start_date`：开始日期，格式为 'YYYY-MM-DD'
- `end_date`：结束日期，格式为 'YYYY-MM-DD'

**返回值**：
- DataFrame，包含分红数据

**示例**：
```python
# 获取分红数据
df = get_dividend('600000.XSHG', start_date='2010-01-01', end_date='2020-12-31')
```

### 6.2 get_split 函数

```python
def get_split(
    security,  # 股票代码
    start_date=None,  # 开始日期
    end_date=None  # 结束日期
):
    """获取除权除息数据"""
    pass
```

**参数说明**：
- `security`：股票代码
- `start_date`：开始日期，格式为 'YYYY-MM-DD'
- `end_date`：结束日期，格式为 'YYYY-MM-DD'

**返回值**：
- DataFrame，包含除权除息数据

**示例**：
```python
# 获取除权除息数据
df = get_split('600000.XSHG', start_date='2010-01-01', end_date='2020-12-31')
```

### 6.3 get_money_flow 函数

```python
def get_money_flow(
    security_list,  # 股票代码列表
    start_date=None,  # 开始日期
    end_date=None  # 结束日期
):
    """获取资金流向数据"""
    pass
```

**参数说明**：
- `security_list`：股票代码列表
- `start_date`：开始日期，格式为 'YYYY-MM-DD'
- `end_date`：结束日期，格式为 'YYYY-MM-DD'

**返回值**：
- DataFrame，包含资金流向数据

**示例**：
```python
# 获取资金流向数据
df = get_money_flow(['600000.XSHG', '600519.XSHG'], start_date='2020-01-01', end_date='2020-01-31')
```
