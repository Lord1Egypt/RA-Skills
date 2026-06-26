# Orderbook, Ticker, Broker

核心接口：
- `/quotes/get_order_book`
- `/quotes/get_rt_ticker`
- `/quotes/get_broker_queue`

## Order Book

适用问法：
- 看摆盘
- 看五档
- 看买卖盘

默认摘要：
- 买一 / 卖一价
- 买一 / 卖一量
- 盘口是否偏强
- 时间戳

只有用户明确要求时，再展开更多档位。

## Ticker

适用问法：
- 看逐笔
- 最近成交明细

默认摘要：
- 最近成交方向分布
- 价格区间
- 成交笔数
- 是否有放量特征

枚举翻译：
- `BUY` → 外盘
- `SELL` → 内盘
- `NEUTRAL` → 中性盘

## Broker Queue

适用问法：
- 经纪队列
- 经纪席位

默认摘要：
- 前几档经纪买盘 / 卖盘
- 主要经纪席位分布

避免把整张经纪队列原样抛出，除非用户明确要求完整数据。
