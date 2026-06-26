---
name: panda-data-skill
version: 3.0.0
description: PandaAI 金融数据 API 的 LLM Tool 封装多个数据查询方法，支持A股行情、A股基本面，期货，指数等
author: PandaAI
homepage: https://pypi.org/project/panda-data-tools/
user-invocable: true
metadata:
  categories:
    - financial
    - market-data
    - llm-tools
---

# Panda Data Skill

PandaAI 金融数据 API 的 OpenClaw 技能封装，将 35 个数据查询方法封装为符合 LLM function calling 规范的 tools，支持行情数据、市场参考、财务因子、交易工具、期货等全品类查询。

## Quick Start

```python
from panda_tools.credential import CredentialManager
from panda_tools.registry import ToolRegistry

CredentialManager.init_from_env()
registry = ToolRegistry()
tools = registry.get_all_tools()
result = registry.call_tool("get_market_data", start_date="20250101", end_date="20250110", symbol="000001.SZ")
```

## Key Notes

- 需配置环境变量 `PANDA_DATA_USERNAME` 和 `PANDA_DATA_PASSWORD` 作为 API 凭证
- 需安装 PandaData SDK：`pip install panda_data`
- 需安装 PandaDataSkill SDK：`pip install panda-data-tools`
- 完整安装步骤（ClawHub、pip、凭证）见同目录 **[INSTALL_GUIDE.md](INSTALL_GUIDE.md)**
- 日期格式统一为 YYYYMMDD（如 20250101）
- 股票代码格式：A股 `000001.SZ`、指数 `000300.SH`、期货 `A2501.DCE`

## Rules

1. 调用任何数据接口前必须先执行 `CredentialManager.init_from_env()` 初始化凭证
2. 日期参数使用 YYYYMMDD 格式，不要使用 YYYY-MM-DD
3. 股票/指数/期货代码需带交易所后缀（.SZ/.SH/.DCE 等）
4. 查询日期范围注意 API 限制（如日线不超过 5 年）

## 代码示例

```python
# 获取日线行情
registry.call_tool("get_market_data", start_date="20250101", end_date="20250110", symbol="000001.SZ")

# 获取交易日历
registry.call_tool("get_trade_cal", start_date="20250101", end_date="20250131")

# 获取最新交易日
registry.call_tool("get_last_trade_date")
```

## API 方法列表

完整参数说明见 [api_reference.md](api_reference.md)。

#### 1. `get_market_data(start_date, end_date, symbol, ...)` — 获取日线行情数据

获取股票、指数、期货的日线行情，返回开高低收、成交量等字段。

#### 2. `get_market_min_data(start_date, end_date, symbol, ...)` — 获取分钟级行情数据

获取分钟级行情，支持 1m/5m/15m/60m 频率。

#### 3. `get_stock_detail(symbol, fields, ...)` — 获取股票基本信息

获取 A 股、港股、美股的股票基本信息。

#### 4. `get_index_detail(symbol, fields, ...)` — 获取指数基本信息

获取指数代码、名称、上市日期等。

#### 5. `get_concept_list(concept, start_date, end_date)` — 获取概念列表

获取概念板块列表及纳入日期。

#### 6. `get_concept_constituents(concept, concept_stock, ...)` — 获取概念成分股

获取指定概念的成分股列表。

#### 7. `get_industry_detail(fields, level)` — 获取行业基本信息

获取申万行业分类的行业列表。

#### 8. `get_industry_constituents(industry_code, stock_symbol, ...)` — 获取行业成分股

获取指定行业的成分股数据。

#### 9. `get_stock_industry(stock_symbol, level)` — 获取股票所属行业

查询指定股票所属的行业信息。

#### 10. `get_index_indicator(symbol, start_date, end_date, ...)` — 获取指数估值指标

获取指数市净率、市盈率等估值指标。

#### 11. `get_index_weights(index_symbol, stock_symbol, start_date, end_date, ...)` — 获取指数权重

获取指数成分股权重信息。

#### 12. `get_lhb_list(symbol, type, start_date, end_date, ...)` — 获取龙虎榜数据

获取股票龙虎榜上榜数据。

#### 13. `get_lhb_detail(symbol, type, start_date, end_date, ...)` — 获取龙虎榜明细

获取龙虎榜买卖明细及营业部信息。

#### 14. `get_repurchase(symbol, start_date, end_date, ...)` — 获取回购数据

获取上市公司回购数据。

#### 15. `get_margin(symbol, start_date, end_date, ...)` — 获取融资融券信息

获取融资买入、融券卖出等两融数据。

#### 16. `get_hsgt_hold(symbol, start_date, end_date, ...)` — 获取沪深股通持股

获取北向资金持股信息。

#### 17. `get_investor_activity(symbol, start_date, end_date, ...)` — 获取投资者关系活动

获取 A 股投资者关系活动记录。

#### 18. `get_restricted_list(symbol, start_date, end_date, ...)` — 获取限售解禁明细

获取股票限售解禁数据。

#### 19. `get_holder_count(symbol, start_date, end_date, ...)` — 获取股东数量

获取股东户数及户均持股等。

#### 20. `get_top_holders(symbol, start_date, end_date, ...)` — 获取股东信息

获取十大股东、十大流通股东等。

#### 21. `get_block_trade(symbol, start_date, end_date, ...)` — 获取大宗交易

获取 A 股大宗交易信息。

#### 22. `get_share_float(symbol, start_date, end_date, ...)` — 获取股本数据

获取流通股本、总股本等。

#### 23. `get_fina_forecast(symbol, fields, info_date, end_quarter)` — 获取业绩预告

获取业绩预告数据。

#### 24. `get_fina_performance(symbol, fields, info_date, end_quarter)` — 获取财务快报

获取财务快报数据。

#### 25. `get_fina_reports(symbol, start_date, end_date, start_quarter, end_quarter, ...)` — 获取财务报告

获取财务季度报告，含四大报表字段。

#### 26. `get_factor(start_date, end_date, factors, symbol, ...)` — 获取回测因子

获取股票或期货的回测因子数据。

#### 27. `get_adj_factor(symbol, start_date, end_date, ...)` — 获取复权因子

获取前复权、后复权因子。

#### 28. `get_trade_cal(start_date, end_date, exchange, ...)` — 获取交易日历

获取交易日历，支持 SH/HK/US。

#### 29. `get_prev_trade_date(date, exchange, n)` — 获取前第 n 个交易日

返回指定日期前第 n 个交易日的日期字符串。

#### 30. `get_last_trade_date(exchange)` — 获取最新交易日

返回最新交易日日期字符串。

#### 31. `get_stock_status_change(symbol, start_date, end_date, ...)` — 获取特殊处理数据

获取 ST、退市等状态变更数据。

#### 32. `get_trade_list(date)` — 获取在售股票列表

获取指定日期的可交易股票列表。

#### 33. `get_future_detail(symbol, fields, is_trading)` — 获取期货基本信息

获取期货合约基本信息。

#### 34. `get_future_market_post(start_date, end_date, symbol, ...)` — 获取期货后复权数据

获取期货后复权行情。

#### 35. `get_future_dominant(start_date, end_date, underlying_symbol)` — 获取期货主力合约

获取每日主力合约代码。

#### 38. `get_hk_daily(symbol, start_date, end_date, fields)` — 获取港股日线

获取港股日线行情数据。

#### 39. `get_us_daily(symbol, start_date, end_date, fields)` — 获取美股日线

获取美股日线行情数据。

#### 40. `get_stock_cash_dividend(symbol, start_date, end_date, market, fields)` — 获取现金分红

获取股票现金分红公告与金额信息。

#### 41. `get_stock_dividend_info(symbol, start_date, end_date, market, fields)` — 获取分红信息

获取股票分红方案及实施信息。

#### 42. `get_stock_split_info(symbol, start_date, end_date, market, fields)` — 获取拆合股信息

获取送股、转增、拆合股相关信息。

#### 43. `get_stock_dividend_amount(symbol, start_date, end_date, market, fields)` — 获取分红金额

获取股票累计分红金额与分红比例信息。

#### 44. `get_stock_private_placement(symbol, start_date, end_date, market, fields)` — 获取定向增发

获取股票定向增发相关信息。

#### 45. `get_stock_allotment(symbol, start_date, end_date, market, fields)` — 获取配股信息

获取股票配股方案与执行信息。

#### 46. `get_audit_opinion(symbol, start_quarter, end_quarter, market, fields)` — 获取审计意见

获取审计意见与审计机构信息。

#### 47. `get_future_netposi_rank(underlying_symbol, start_date, end_date, max_rank, fields, type)` — 获取净持仓排名

获取期货净持仓排名统计。

#### 48. `get_future_symbol_posi_rank(start_date, end_date, symbol, position_type, broker_name, rank_max, fields)` — 获取合约持仓排名

获取合约维度席位持仓排名。

#### 49. `get_future_variety_posi_rank(start_date, end_date, symbol, position_type, broker_name, rank_max, fields)` — 获取品种持仓排名

获取品种维度席位持仓排名。

#### 50. `get_future_contract_daily_indicators(start_date, end_date, symbol, fields)` — 获取合约日度指标

获取期货合约日度指标数据。

#### 51. `get_broker_variety_profit(start_date, end_date, symbol, fields, broker)` — 获取席位品种盈利

获取席位在品种维度的盈利统计。

#### 52. `get_broker_grade(grade)` — 获取席位评级

获取期货席位评级信息。

#### 53. `get_broker_net_margin(underlying_symbol, start_date, end_date, fields, broker)` — 获取净保证金

获取席位净保证金数据。

#### 54. `get_broker_net_margin_change(underlying_symbol, start_date, end_date, fields, broker)` — 获取净保证金变化

获取席位净保证金变动数据。

#### 55. `get_broker_total_margin(underlying_symbol, start_date, end_date, fields, broker)` — 获取总保证金

获取席位总保证金数据。

#### 56. `get_future_net_flow(start_date, end_date, symbol, fields, broker_name, position_type)` — 获取净资金流

获取期货净资金流向数据。

#### 57. `get_future_basis(underlying_symbol, start_date, end_date, fields)` — 获取期货基差

获取期货基差统计数据。

#### 58. `get_future_wr(underlying_symbol, start_date, end_date, fields)` — 获取仓单比率

获取期货仓单比率数据。

#### 59. `get_future_ls_ratio(symbol, start_date, end_date)` — 获取多空比

获取期货多空比数据。

#### 60. `get_future_net_cap_change(symbol, start_date, end_date, broker)` — 获取净资金变化

获取期货净资金变化数据。

#### 61. `get_future_contract_rank(symbol, underlying_symbol, start_date, end_date, type, max_rank, rank_type)` — 获取合约排名

获取期货合约席位排名数据。
