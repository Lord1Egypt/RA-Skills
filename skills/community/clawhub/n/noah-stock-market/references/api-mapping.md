# API Mapping

## Core Quote Queries

- 最新行情 / 市场快照
  - `/quotes/get_market_snapshot`
  - 返回：`MarketQuote`

- 订阅实时报价（受权限限制）
  - `/quotes/get_stock_quote`
  - 返回：扩展报价数据
  - 仅在用户明确要求订阅级实时数据且接口可用时使用

- 实时分时
  - `/quotes/get_rt_data`
  - 返回：`StockTimeData`

- 实时 K 线
  - `/quotes/get_cur_kline`
  - 返回：`KlineItem`

## Market Depth

- 实时摆盘
  - `/quotes/get_order_book`
  - 返回：`OrderBook`

- 实时逐笔
  - `/quotes/get_rt_ticker`
  - 返回：`TickerItem`

- 实时经纪队列
  - `/quotes/get_broker_queue`
  - 返回：`BrokerQueue`

## Market State

- 个股所属市场状态
  - `/infos/get_market_state`
  - 返回：`MarketStatus`

- 全局市场状态
  - `/quote/get_global_state`
  - 返回：`GlobalStateItem`

- 交易日历
  - `/quote/request_trading_days`
  - 返回：`TradingDayItem`

## Capital Flow

- 个股资金流向
  - `/infos/get_capital_flow`
  - 返回：`CapitalFlowItem`

## Plate / Basic Info

- 板块列表
  - `/quote/get_plate_list`
  - 返回：`PlateItem`

- 板块成分股
  - `/quote/get_plate_stock`
  - 返回：`PlateStockItem`

- 股票基础信息
  - `/quote/get_stock_basicinfo`
  - 返回：`StockBasicInfoItem`

## Derivatives

- 期权到期日
  - `/derivatives/get_option_expiration_date`
  - 返回：`OptionExpirationItem`

- 期权链
  - `/derivatives/get_option_chain`
  - 返回：`OptionChainItem`

- 窝轮 / 牛熊证 / 界内证
  - `/derivatives/get_warrant`
  - 返回：`WarrantItem`

## Advanced (Optional)

- 排行榜
  - `/rank/get_stock_rank`

- IPO 列表
  - `/quote/get_ipo_list`

## Routing Hints

- “现在多少钱 / 最新价 / 快照 / 行情” → `get_market_snapshot`
- “分时 / 实时走势” → `get_rt_data`
- “日K / 周K / 5分钟K / 30天走势” → `get_cur_kline`
- “摆盘 / 五档 / 买卖盘” → `get_order_book`
- “逐笔 / 成交明细” → `get_rt_ticker`
- “经纪队列” → `get_broker_queue`
- “港股/美股开盘了吗 / 市场状态” → `get_global_state` 或 `get_market_state`
- “资金流向 / 主力流入流出” → `get_capital_flow`
- “板块 / 板块成分股” → `get_plate_list` / `get_plate_stock`
- “基本信息 / 上市时间 / 每手股数” → `get_stock_basicinfo`
- “期权到期日 / 期权链” → `get_option_expiration_date` / `get_option_chain`
