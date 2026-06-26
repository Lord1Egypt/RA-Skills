# TradeContext API 参考

## 初始化

```python
from longport.openapi import TradeContext, Config

config = Config.from_env()
ctx = TradeContext(config)
```

## 方法列表

### submit_order — 提交订单

```python
ctx.submit_order(
    symbol: str,                    # 标的代码，如 "US.AAPL"
    order_type: OrderType,          # 订单类型
    side: OrderSide,                # 买卖方向
    submitted_quantity: Decimal,    # 委托数量
    time_in_force: TimeInForceType, # 有效期类型
    submitted_price: Decimal = None,     # 委托价格（限价单必填）
    trigger_price: Decimal = None,       # 触发价（LIT/MIT 必填）
    limit_offset: Decimal = None,        # 限价偏移（跟踪止损限价单）
    trailing_amount: Decimal = None,     # 跟踪金额（TSLPAMT/TSMAMT）
    trailing_percent: Decimal = None,    # 跟踪百分比（TSLPPCT/TSMPCT）
    expire_date: date = None,            # 到期日（GoodTilDate 时填）
    outside_rth: OutsideRTH = None,      # 盘前盘后（美股）
    remark: str = None,                  # 备注
) -> SubmitOrderResponse  # 返回 order_id
```

### cancel_order — 撤单

```python
ctx.cancel_order(order_id: str)
```

### replace_order — 改单

```python
ctx.replace_order(
    order_id: str,
    quantity: Decimal,
    price: Decimal = None,
    trigger_price: Decimal = None,
    limit_offset: Decimal = None,
    trailing_amount: Decimal = None,
    trailing_percent: Decimal = None,
    remark: str = None,
)
```

### today_orders — 今日订单

```python
ctx.today_orders(
    symbol: str = None,           # 筛选标的
    status: list[OrderStatus] = None,  # 筛选状态
    side: OrderSide = None,       # 筛选方向
    market: Market = None,        # 筛选市场
    order_id: str = None,         # 筛选订单ID
) -> list[Order]
```

### today_executions — 今日成交

```python
ctx.today_executions(
    symbol: str = None,
    order_id: str = None,
) -> list[Execution]
```

### history_orders — 历史订单

```python
ctx.history_orders(
    symbol: str = None,
    status: list[OrderStatus] = None,
    side: OrderSide = None,
    market: Market = None,
    start_at: datetime = None,
    end_at: datetime = None,
) -> list[Order]
```

### history_executions — 历史成交

```python
ctx.history_executions(
    symbol: str = None,
    start_at: datetime = None,
    end_at: datetime = None,
) -> list[Execution]
```

### order_detail — 订单详情

```python
ctx.order_detail(order_id: str) -> OrderDetail
```

### account_balance — 账户余额

```python
ctx.account_balance(currency: str = None) -> list[AccountBalance]
```

返回值关键字段：
- `currency` — 币种
- `total_cash` — 现金总额
- `net_assets` — 净资产
- `buy_power` — 购买力
- `risk_level` — 风控等级（0安全 1中风险 2预警 3危险）
- `cash_infos` — 现金明细（available_cash, frozen_cash, settling_cash, withdraw_cash）

### stock_positions — 股票持仓

```python
ctx.stock_positions(symbols: list[str] = None) -> StockPositionsResponse
```

返回值结构：`resp.channels[].positions[]`，每个 position 包含：
- `symbol`, `quantity`, `available_quantity`
- `cost_price`, `currency`

### fund_positions — 基金持仓

```python
ctx.fund_positions(symbols: list[str] = None) -> FundPositionsResponse
```

### cash_flow — 现金流

```python
ctx.cash_flow(
    start_at: datetime,
    end_at: datetime,
    business_type: BalanceType = None,
    symbol: str = None,
    page: int = None,
    size: int = None,
) -> list[CashFlow]
```

### estimate_max_purchase_quantity — 估算最大可买数量

```python
ctx.estimate_max_purchase_quantity(
    symbol: str,
    order_type: OrderType,
    side: OrderSide,
    price: Decimal,
    currency: str = None,
    order_id: str = None,
) -> EstimateMaxPurchaseQuantityResponse
```

返回 `cash_max_qty` 和 `margin_max_qty`。

### margin_ratio — 保证金比率

```python
ctx.margin_ratio(symbol: str) -> MarginRatio
```

返回 `im_factor`（初始保证金比率）和 `mm_factor`（维持保证金比率）。

### subscribe / unsubscribe — 订阅/取消订阅订单推送

```python
ctx.subscribe(topics: list[TopicType])
ctx.unsubscribe(topics: list[TopicType])
```

### set_on_order_changed — 订单变更回调

```python
ctx.set_on_order_changed(callback)
# callback 接收 PushOrderChanged 对象
```

---

## 枚举值参考

### OrderType — 订单类型

| 值 | 说明 |
|---|---|
| `LO` | 限价单 |
| `MO` | 市价单 |
| `ELO` | 增强限价单（港股） |
| `ALO` | 竞价限价单（港股） |
| `ODD` | 碎股单（港股） |
| `SLO` | 特别限价单（港股） |
| `LIT` | 触价限价单（美股） |
| `MIT` | 触价市价单（美股） |
| `TSLPAMT` | 跟踪止损限价单-金额（美股） |
| `TSLPPCT` | 跟踪止损限价单-百分比（美股） |
| `TSMAMT` | 跟踪止损市价单-金额（美股） |
| `TSMPCT` | 跟踪止损市价单-百分比（美股） |
| `AO` | 竞价单 |

### OrderSide — 买卖方向

| 值 | 说明 |
|---|---|
| `Buy` | 买入 |
| `Sell` | 卖出 |

### TimeInForceType — 有效期

| 值 | 说明 |
|---|---|
| `Day` | 当日有效 |
| `GoodTilCanceled` | 撤单前有效 |
| `GoodTilDate` | 到期日前有效 |

### OrderStatus — 订单状态

| 值 | 说明 |
|---|---|
| `New` | 已报 |
| `Filled` | 已成交 |
| `PartialFilled` | 部分成交 |
| `Canceled` | 已撤单 |
| `Rejected` | 已拒绝 |
| `Expired` | 已过期 |
| `PendingCancel` | 待撤单 |
| `PendingReplace` | 待改单 |
| `Replaced` | 已改单 |
| `WaitToNew` | 等待报盘 |
| `WaitToReplace` | 等待改单 |
| `WaitToCancel` | 等待撤单 |

### Market — 市场

| 值 | 说明 |
|---|---|
| `US` | 美股 |
| `HK` | 港股 |
| `CN` | A股 |
| `SG` | 新加坡 |

### OutsideRTH — 盘前盘后（美股）

| 值 | 说明 |
|---|---|
| `RTHOnly` | 仅盘中 |
| `AnyTime` | 任意时段 |
| `Overnight` | 夜盘 |

### BalanceType — 余额类型

| 值 | 说明 |
|---|---|
| `Cash` | 现金 |
| `Stock` | 股票 |
| `Fund` | 基金 |

### TopicType — 推送主题

| 值 | 说明 |
|---|---|
| `Private` | 私有（订单变更） |
