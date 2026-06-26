# QuoteContext API 参考

## 初始化

```python
from longport.openapi import QuoteContext, Config

config = Config.from_env()
ctx = QuoteContext(config)
```

## 方法列表

### quote — 获取实时行情

```python
ctx.quote(symbols: list[str]) -> list[SecurityQuote]
```

返回值关键字段：
- `symbol`, `last_done`（最新价）, `prev_close`（昨收）
- `open`, `high`, `low`, `volume`, `turnover`
- `change_rate`（涨跌幅%）, `change_value`（涨跌额）
- `timestamp`

### realtime_quote — 实时报价（含盘前盘后）

```python
ctx.realtime_quote(symbols: list[str]) -> list[RealtimeQuote]
```

### static_info — 标的基础信息

```python
ctx.static_info(symbols: list[str]) -> list[SecurityStaticInfo]
```

返回：`symbol`, `name_cn`, `name_en`, `name_hk`, `exchange`, `currency`, `lot_size`, `board` 等。

### depth — 盘口数据

```python
ctx.depth(symbol: str) -> SecurityDepth
```

返回 `asks[]` 和 `bids[]`，每个包含 `price`, `volume`, `order_num`。

### realtime_depth — 实时盘口

```python
ctx.realtime_depth(symbol: str) -> SecurityDepth
```

### brokers — 经纪队列

```python
ctx.brokers(symbol: str) -> SecurityBrokers
```

### realtime_brokers — 实时经纪队列

```python
ctx.realtime_brokers(symbol: str) -> SecurityBrokers
```

### trades — 成交明细

```python
ctx.trades(symbol: str, count: int) -> list[Trade]
```

### realtime_trades — 实时成交明细

```python
ctx.realtime_trades(symbol: str, count: int = 500) -> list[Trade]
```

### candlesticks — K线数据

```python
ctx.candlesticks(
    symbol: str,
    period: Period,
    count: int,
    adjust_type: AdjustType,
) -> list[Candlestick]
```

每根 K 线包含：`open`, `close`, `high`, `low`, `volume`, `turnover`, `timestamp`。

### realtime_candlesticks — 实时K线

```python
ctx.realtime_candlesticks(symbol: str, period: Period, count: int = 500) -> list[Candlestick]
```

### history_candlesticks_by_date — 按日期查历史K线

```python
ctx.history_candlesticks_by_date(
    symbol: str,
    period: Period,
    adjust_type: AdjustType,
    start: date = None,
    end: date = None,
) -> list[Candlestick]
```

### history_candlesticks_by_offset — 按偏移查历史K线

```python
ctx.history_candlesticks_by_offset(
    symbol: str,
    period: Period,
    adjust_type: AdjustType,
    forward: bool,
    count: int,
    time: datetime = None,
) -> list[Candlestick]
```

### intraday — 分时数据

```python
ctx.intraday(symbol: str) -> list[IntradayLine]
```

### capital_flow — 资金流向

```python
ctx.capital_flow(symbol: str) -> list[CapitalFlowLine]
```

### capital_distribution — 资金分布

```python
ctx.capital_distribution(symbol: str) -> CapitalDistributionResponse
```

### calc_indexes — 计算指标

```python
ctx.calc_indexes(
    symbols: list[str],
    indexes: list[CalcIndex],
) -> list[SecurityCalcIndex]
```

### option_chain_expiry_date_list — 期权到期日列表

```python
ctx.option_chain_expiry_date_list(symbol: str) -> list[date]
```

### option_chain_info_by_date — 期权链信息

```python
ctx.option_chain_info_by_date(symbol: str, expiry_date: date) -> list[StrikePriceInfo]
```

### option_quote — 期权行情

```python
ctx.option_quote(symbols: list[str]) -> list[OptionQuote]
```

### warrant_quote — 轮证行情

```python
ctx.warrant_quote(symbols: list[str]) -> list[WarrantQuote]
```

### warrant_list — 轮证筛选

```python
ctx.warrant_list(
    symbol: str,
    sort_by: WarrantSortBy,
    sort_order: SortOrderType,
    warrant_type: list[WarrantType] = None,
    issuer: list[int] = None,
    expiry_date: list[FilterWarrantExpiryDate] = None,
    price_type: list[FilterWarrantInOutBoundsType] = None,
    status: list[WarrantStatus] = None,
) -> list[WarrantInfo]
```

### warrant_issuers — 轮证发行商

```python
ctx.warrant_issuers() -> list[IssuerInfo]
```

### security_list — 标的列表

```python
ctx.security_list(market: Market, category: SecurityListCategory = None) -> list[Security]
```

### trading_session — 交易时段

```python
ctx.trading_session() -> list[MarketTradingSession]
```

### trading_days — 交易日

```python
ctx.trading_days(market: Market, begin: date, end: date) -> MarketTradingDays
```

### market_temperature — 市场温度

```python
ctx.market_temperature(market: Market) -> MarketTemperature
ctx.history_market_temperature(market: Market, start_date: date, end: date) -> HistoryMarketTemperatureResponse
```

### 自选股管理

```python
ctx.watchlist() -> list[WatchlistGroup]
ctx.create_watchlist_group(name: str, securities: list[str] = None)
ctx.update_watchlist_group(id: int, name: str = None, securities: list[str] = None, mode: SecuritiesUpdateMode = None)
ctx.delete_watchlist_group(id: int, purge: bool = False)
```

### 订阅/取消订阅

```python
ctx.subscribe(symbols: list[str], sub_types: list[SubType])
ctx.unsubscribe(symbols: list[str], sub_types: list[SubType])
ctx.subscriptions() -> list  # 已订阅列表
```

### 推送回调

```python
ctx.set_on_quote(callback)        # 价格推送
ctx.set_on_depth(callback)        # 盘口推送
ctx.set_on_brokers(callback)      # 经纪推送
ctx.set_on_trades(callback)       # 成交推送
ctx.set_on_candlestick(callback)  # K线推送
```

---

## 枚举值参考

### Period — K线周期

| 值 | 说明 |
|---|---|
| `Min_1` | 1分钟 |
| `Min_2` | 2分钟 |
| `Min_3` | 3分钟 |
| `Min_5` | 5分钟 |
| `Min_10` | 10分钟 |
| `Min_15` | 15分钟 |
| `Min_20` | 20分钟 |
| `Min_30` | 30分钟 |
| `Min_45` | 45分钟 |
| `Min_60` | 60分钟 |
| `Min_120` | 120分钟 |
| `Min_180` | 180分钟 |
| `Min_240` | 240分钟 |
| `Day` | 日K |
| `Week` | 周K |
| `Month` | 月K |
| `Quarter` | 季K |
| `Year` | 年K |

### AdjustType — 复权类型

| 值 | 说明 |
|---|---|
| `NoAdjust` | 不复权 |
| `ForwardAdjust` | 前复权 |

### SubType — 订阅类型

| 值 | 说明 |
|---|---|
| `Quote` | 行情报价 |
| `Depth` | 盘口 |
| `Brokers` | 经纪队列 |
| `Trade` | 成交明细 |

### TradeSession — 交易时段

| 值 | 说明 |
|---|---|
| `Intraday` | 盘中 |
| `Pre` | 盘前 |
| `Post` | 盘后 |
| `Overnight` | 夜盘 |

### WarrantSortBy — 轮证排序字段

| 值 | 说明 |
|---|---|
| `LastDone` | 最新价 |
| `ChangeRate` | 涨跌幅 |
| `ChangeValue` | 涨跌额 |
| `Volume` | 成交量 |
| `Turnover` | 成交额 |
| `ExpiryDate` | 到期日 |
| `StrikePrice` | 行使价 |
| `Premium` | 溢价 |
| `Delta` | Delta |
| `ImpliedVolatility` | 隐含波动率 |
| `EffectiveLeverage` | 有效杠杆 |
| `LeverageRatio` | 杠杆比率 |
| `ConversionRatio` | 换股比率 |
| `BalancePoint` | 打和点 |
| `CallPrice` | 收回价 |
| `ToCallPrice` | 距收回价 |
| `OutstandingQuantity` | 街货量 |
| `OutstandingRatio` | 街货比 |
| `ItmOtm` | 价内/价外 |
| `Status` | 状态 |
| `UpperStrikePrice` | 上限价 |
| `LowerStrikePrice` | 下限价 |

### WarrantType — 轮证类型

| 值 | 说明 |
|---|---|
| `Call` | 认购 |
| `Put` | 认沽 |
| `Bull` | 牛证 |
| `Bear` | 熊证 |
| `Inline` | 界内证 |

### SortOrderType — 排序方向

| 值 | 说明 |
|---|---|
| `Ascending` | 升序 |
| `Descending` | 降序 |
