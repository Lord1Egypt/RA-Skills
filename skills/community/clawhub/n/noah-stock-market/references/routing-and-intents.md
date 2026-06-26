# Routing and Intents

## Price / Snapshot

触发示例：
- 腾讯控股现在多少钱
- AAPL 最新行情
- 看下 NVDA 今天涨跌

优先接口：
- `/quotes/get_market_snapshot`

## Intraday / Trend

触发示例：
- 给我看腾讯今天分时
- 看一下苹果最近走势
- 查下英伟达日K
- 看 5 分钟 K
- 看最近 10 根日K

优先接口：
- `/quotes/get_rt_data`
- `/quotes/get_cur_kline`

推荐脚本调用：
- `python3 scripts/run_query.py intraday HK-00700`
- `python3 scripts/run_query.py kline HK-00700 num=10 ktype=K_DAY`
- `python3 scripts/run_query.py kline US-AAPL num=20 ktype=K_5_M`
- 自然语言入口：
  - `python3 scripts/route_query.py 看腾讯最近10根日K`
  - `python3 scripts/route_query.py 看苹果5分钟K`
  - `python3 scripts/route_query.py 看腾讯资金流向`

## Market Depth

触发示例：
- 看下 00700 摆盘
- AAPL 最近逐笔成交
- 腾讯经纪队列

优先接口：
- `/quotes/get_order_book`
- `/quotes/get_rt_ticker`
- `/quotes/get_broker_queue`

## Market State

触发示例：
- 美股现在开盘了吗
- 港股现在什么状态

优先接口：
- `/quote/get_global_state`
- `/infos/get_market_state`

## Capital Flow

触发示例：
- 查下特斯拉资金流向
- 主力资金有没有流入

优先接口：
- `/infos/get_capital_flow`

## Plates / Basic Info

触发示例：
- 港股汽车板块有哪些股票
- 腾讯控股基础信息

优先接口：
- `/quote/get_plate_list`
- `/quote/get_plate_stock`
- `/quote/get_stock_basicinfo`

## Options

触发示例：
- AAPL 的期权到期日
- NVDA 的期权链

优先接口：
- `/derivatives/get_option_expiration_date`
- `/derivatives/get_option_chain`
