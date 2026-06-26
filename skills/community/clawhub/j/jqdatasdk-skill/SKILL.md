---
name: jqdatasdk
description: |
  JoinQuant (聚宽) 量化交易数据SDK开发技能。基于jqdatasdk官方库提供行情数据获取、财务数据查询、因子数据等API。用于开发量化交易策略、进行jqdatasdk二次开发、API问题排查。
  适用于需要使用聚宽数据接口进行策略开发、回测验证、数据分析的场景。
compatibility: Python 3.10+, jqdatasdk, pandas, sqlalchemy
---

# jqdatasdk 量化开发技能

本技能基于 JoinQuant (聚宽) 官方 jqdatasdk SDK，帮助开发者使用 Python 进行量化交易策略开发和数据分析。

## 参考项目

- **官方 jqdatasdk**: `https://github.com/JoinQuant/jqdatasdk.git` - 官方 Python SDK 源码
- **类型定义**: `https://github.com/stairclimber/joinquant_api.git` - 第三方 API 类型定义 (TypeScript 风格)

## 快速开始

### 1. 安装 jqdatasdk

```bash
pip install jqdatasdk
```

### 2. 账号认证

```python
import jqdatasdk as jq

# 使用用户名密码认证
jq.auth('username', 'password')

# 或使用 token 认证
jq.auth_by_token('your_token')

# 检查认证状态
print(jq.is_auth())  # True/False
```

### 3. 基础数据获取

```python
import jqdatasdk as jq
from jqdatasdk import finance

# 获取股票行情数据
df = jq.get_price('000001.XSHE', start_date='2024-01-01', end_date='2024-12-31')

# 获取财务数据
from sqlalchemy import func
q = jq.query(
    finance.indicator.code,
    finance.indicator.pub_date,
    finance.indicator.eps
).filter(finance.indicator.code == '000001.XSHE')
df = jq.get_fundamentals(q, date='2024-12-31')

# 获取指数成分股
stocks = jq.get_index_stocks('000300.XSHG')  # 沪深300

# 获取交易日历
trade_days = jq.get_trade_days(start_date='2024-01-01', end_date='2024-12-31')
```

## 核心API分类

### 认证与配置

| 函数 | 说明 |
|------|------|
| `jq.auth(username, password, host=None, port=None)` | 账号密码认证 |
| `jq.auth_by_token(token, host=None, port=None)` | Token认证 |
| `jq.logout()` | 退出登录 |
| `jq.is_auth()` | 检查认证状态 |
| `jq.set_params(**params)` | 设置请求参数 |

### 行情数据

| 函数 | 说明 |
|------|------|
| `get_price(security, ...)` | 获取行情数据(日/分钟) |
| `get_bars(security, count, unit, ...)` | 获取K线数据 |
| `get_ticks(security, ...)` | 获取Tick数据 |
| `get_current_tick(security)` | 获取实时Tick |
| `get_extras(info, security_list, ...)` | 获取额外数据(ST/净值等) |

### 财务数据

| 函数 | 说明 |
|------|------|
| `get_fundamentals(query_object, ...)` | 查询财务数据 |
| `get_fundamentals_continuously(...)` | 连续查询财务数据 |
| `get_valuation(security_list, ...)` | 获取市值数据 |
| `get_history_fundamentals(...)` | 获取历史财报数据 |

### 标的信息

| 函数 | 说明 |
|------|------|
| `get_all_securities(types, date)` | 获取所有证券信息 |
| `get_security_info(code, date)` | 获取证券详细信息 |
| `get_index_stocks(index_symbol, date)` | 获取指数成分股 |
| `get_industry_stocks(industry_code, date)` | 获取行业股票 |
| `get_concept_stocks(concept_code, date)` | 获取概念股票 |

### 行业与概念

| 函数 | 说明 |
|------|------|
| `get_industries(name, date)` | 获取行业列表 |
| `get_concepts()` | 获取概念板块列表 |
| `get_concept(security, date)` | 获取股票所属概念 |
| `get_industry(security, date)` | 获取股票所属行业 |

### 资金流向

| 函数 | 说明 |
|------|------|
| `get_money_flow(security_list, ...)` | 获取资金流向数据 |
| `get_money_flow_pro(security_list, ...)` | 获取专业资金流向 |

### 融资融券

| 函数 | 说明 |
|------|------|
| `get_mtss(security_list, ...)` | 融资融券数据 |
| `get_margincash_stocks(date)` | 可融资标的列表 |
| `get_marginsec_stocks(date)` | 可融券标的列表 |

### 期货数据

| 函数 | 说明 |
|------|------|
| `get_future_contracts(underlying_symbol, date)` | 期货合约列表 |
| `get_dominant_future(underlying_symbol, date)` | 主力合约 |
| `get_order_future_bar(symbol, future_type, ...)` | 连续合约行情 |

### 因子数据

| 函数 | 说明 |
|------|------|
| `get_factor_values(securities, factors, ...)` | 因子值 |
| `get_all_factors()` | 所有可用因子 |
| `get_factor_kanban_values(...)` | 因子面板数据 |
| `get_factor_style_returns(...)` | 风格因子收益 |
| `get_factor_stats(...)` | 因子历史收益统计 |

### Alpha因子

| 函数 | 说明 |
|------|------|
| `get_all_alpha_101(date, code, alpha)` | Alpha101因子 |
| `get_all_alpha_191(date, code, alpha)` | Alpha191因子 |

### 技术分析

| 函数 | 说明 |
|------|------|
| `jq.technical_analysis.*` | 技术指标函数 |

### 其他

| 函数 | 说明 |
|------|------|
| `get_trade_days(start_date, end_date, count)` | 交易日列表 |
| `get_all_trade_days()` | 所有交易日 |
| `get_billboard_list(...)` | 龙虎榜数据 |
| `get_locked_shares(...)` | 限售股解禁 |
| `get_table_info(table)` | 数据表字段信息 |

## 常用查询示例

### 查询股票财务指标

```python
import jqdatasdk as jq
from jqdatasdk import finance

# 使用 SQLAlchemy 查询
q = jq.query(
    finance.indicator.code,
    finance.indicator.pub_date,
    finance.indicator.eps,  # 每股收益
    finance.indicator.net_profits,  # 净利润
    finance.indicator.revenue,  # 营业收入
    finance.indicator.total_assets,  # 总资产
).filter(
    finance.indicator.code == '000001.XSHE'
).order_by(
    finance.indicator.pub_date.desc()
)

df = jq.get_fundamentals(q, date='2024-12-31')
print(df)
```

### 查询多个股票财务数据

```python
import jqdatasdk as jq
from jqdatasdk import finance

# 批量查询
stocks = ['000001.XSHE', '000002.XSHE', '600519.XSHG']
q = jq.query(
    finance.indicator.code,
    finance.indicator.eps,
    finance.indicator.roa,
    finance.indicator.roe
).filter(
    finance.indicator.code.in_(stocks)
)

df = jq.get_fundamentals(q, date='2024-12-31')
```

### 获取市值数据

```python
import jqdatasdk as jq

# 获取多只股票的市值数据
stocks = ['000001.XSHE', '000002.XSHE', '600519.XSHG']
df = jq.get_valuation(
    stocks,
    start_date='2024-01-01',
    end_date='2024-12-31',
    fields=['code', 'day', 'pe_ratio', 'pb_ratio', 'market_cap', 'circulating_market_cap']
)
```

### 因子策略示例

```python
import jqdatasdk as jq
import pandas as pd

# 获取因子数据
securities = jq.get_index_stocks('000300.XSHG')
factors_data = jq.get_factor_values(
    securities,
    factors=['pe_ratio', 'pb_ratio', 'roe'],
    start_date='2024-01-01',
    end_date='2024-12-31'
)

# 处理因子数据
for factor_name, df in factors_data.items():
    print(f"Factor: {factor_name}")
    print(df.head())
```

### 资金流向分析

```python
import jqdatasdk as jq

# 获取资金流向
stocks = ['000001.XSHE', '600519.XSHG']
df = jq.get_money_flow(
    stocks,
    start_date='2024-01-01',
    end_date='2024-12-31',
    fields=['date', 'sec_code', 'net_amount_main', 'net_pct_main']
)
```

### 连续财务数据查询

```python
import jqdatasdk as jq
from jqdatasdk import finance

# 获取连续多季度财务数据
q = jq.query(
    finance.indicator.code,
    finance.indicator.pub_date,
    finance.indicator.eps,
    finance.indicator.net_profits
)

df = jq.get_fundamentals_continuously(
    q,
    end_date='2024-12-31',
    count=8  # 最近8个季度
)
```

## SQLAlchemy 查询指南

### 常用表和字段

```python
from jqdatasdk import finance

# 财务指标表 (indicator)
finance.indicator.code           # 股票代码
finance.indicator.pub_date       # 发布日期
finance.indicator.eps            # 每股收益
finance.indicator.net_profits    # 净利润
finance.indicator.revenue        # 营业收入
finance.indicator.total_assets   # 总资产
finance.indicator.total_liab     # 总负债
finance.indicator.roe            # 净资产收益率
finance.indicator.roa            # 总资产收益率
finance.indicator.gross_profit   # 毛利率
finance.indicator.net_profit_margin  # 净利率

# 资产负债表 (balance)
finance.balance.code
finance.balance.total_assets
finance.balance.total_liab
finance.balance.total_hldr_eqy_excl_min_int_shares  # 归属于母公司股东权益

# 利润表 (income)
finance.income.code
finance.income.total_revenue
finance.income.oper_cost
finance.income.net_profit

# 现金流量表 (cash_flow)
finance.cash_flow.code
finance.cash_flow.oper_cash_flow
finance.cash_flow.invest_cash_flow
finance.cash_flow.fin_cash_flow
```

### 查询条件

```python
from jqdatasdk import finance
import jqdatasdk as jq

# 基本过滤
q = jq.query(finance.indicator).filter(
    finance.indicator.code == '000001.XSHE'
)

# IN 查询
q = jq.query(finance.indicator).filter(
    finance.indicator.code.in_(['000001.XSHE', '000002.XSHE'])
)

# 多条件
q = jq.query(finance.indicator).filter(
    finance.indicator.code == '000001.XSHE',
    finance.indicator.pub_date >= '2024-01-01'
)

# 排序和限制
q = jq.query(finance.indicator).filter(
    finance.indicator.code == '000001.XSHE'
).order_by(finance.indicator.pub_date.desc()).limit(10)
```

## 二次开发指南

### 扩展新的API

参考官方 `jqdatasdk/api.py` 的实现模式：

```python
from jqdatasdk.utils import assert_auth
from jqdatasdk.client import JQDataClient

@assert_auth
def my_custom_api(param1, param2=None):
    """
    自定义API说明
    
    :param param1: 参数1说明
    :param param2: 参数2说明
    :return: 返回值说明
    """
    return JQDataClient.instance().my_custom_api(param1=param1, param2=param2)
```

### 添加新的财务表

参考 `jqdatasdk/finance_tables.py` 的结构：

```python
from sqlalchemy import Column, String, Numeric, Date
from jqdatasdk.finance_tables import Base

class MyCustomTable(Base):
    __tablename__ = 'my_custom_table'
    
    code = Column(String(20), primary_key=True)
    report_date = Column(Date)
    field1 = Column(Numeric(20, 4))
    field2 = Column(Numeric(20, 4))
```

### 缓存优化

使用内置缓存装饰器：

```python
from jqdatasdk.utils import hashable_lru

@hashable_lru(maxsize=3)
def my_cached_function(security, start_date, end_date):
    """带缓存的函数"""
    # 实际查询逻辑
    return JQDataClient.instance().query(...)
```

## 错误处理

### 常见错误

```python
import jqdatasdk as jq

try:
    jq.auth('username', 'password')
    df = jq.get_price('000001.XSHE')
except jq.exceptions.ParamsError as e:
    print(f"参数错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

### 认证错误

```python
if not jq.is_auth():
    jq.auth('username', 'password')
    print("认证成功")
else:
    print("已认证")
```

## 性能优化

1. **批量查询**: 尽量使用批量接口而非循环单个查询
2. **缓存使用**: 对不频繁变化的数据使用 `@hashable_lru` 缓存
3. **字段筛选**: 只查询需要的字段减少数据传输
4. **日期范围**: 使用 `count` 参数代替大范围日期查询

## 注意事项

1. **认证要求**: 绝大多数API需要先调用 `jq.auth()` 认证
2. **请求限制**: 注意API的调用频率限制
3. **数据延迟**: 财务数据可能有延迟,注意数据发布日期
4. **股票代码格式**: 使用聚宽标准格式如 `000001.XSHE` (深圳) 或 `600519.XSHG` (上海)

## 参考资源

- 聚宽官方文档: https://www.joinquant.com/help/api/
- 财务数据字典: https://www.joinquant.com/data/dict/fundamentals
- 指数数据: https://www.joinquant.com/indexData
- 行业分类: https://www.joinquant.com/data/dict/plateData
