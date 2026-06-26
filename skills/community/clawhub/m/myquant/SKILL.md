---
name: myquant
description: 掘金量化Python SDK - 事件驱动量化平台，支持A股、期货、期权、ETF、可转债回测与实盘交易。
version: 1.2.0
homepage: https://www.myquant.cn
metadata: {"clawdbot":{"emoji":"⛏️","requires":{"bins":["python3"]}}}
---

# 掘金量化（MyQuant / GoldMiner）

[掘金量化](https://www.myquant.cn) 是专业量化交易平台，提供事件驱动策略开发、回测、模拟交易和实盘交易。支持A股、期货、期权、ETF、可转债和融资融券，通过统一的Python SDK（`gm.api`）操作。

> 需要在 https://www.myquant.cn 注册获取Token进行认证。实盘交易需要通过掘金终端连接券商账户。

## 安装

```bash
pip install gm
```

也可从官网下载：https://www.myquant.cn/docs/downloads/698

## 架构概述

```
你的Python脚本（strategy.py）
    ↓ gm SDK（from gm.api import *）
    ├── 回测模式  → 掘金回测引擎（云端/本地）
    ├── 模拟交易   → 掘金模拟交易服务器
    └── 实盘交易    → 掘金终端 → 券商网关
```

## 策略程序结构

所有策略遵循**事件驱动**架构，包含生命周期函数：

```python
from gm.api import *

def init(context):
    """Initialization function — called once when the strategy starts, used to set up subscriptions and parameters"""
    # Subscribe to 30-second bars for two stocks, keeping the most recent 5 historical bars
    subscribe(symbols='SHSE.600000,SZSE.000001', frequency='30s', count=5)
    context.my_param = 0.8  # Custom context attribute

def on_bar(context, bars):
    """Bar event — triggered at each bar close, write main trading logic here"""
    bar = bars[0]
    if bar['close'] > bar['open']:
        # Close price above open price, place a limit buy order for 1000 shares
        order_volume(symbol=bar['symbol'], volume=1000,
                     side=OrderSide_Buy, order_type=OrderType_Limit,
                     position_effect=PositionEffect_Open, price=bar['close'])

def on_tick(context, tick):
    """Tick event — triggered on each tick push (real-time mode)"""
    print(tick['symbol'], tick['price'])

def on_order_status(context, order):
    """Order status event — triggered when order status changes"""
    print(f"Order {order['cl_ord_id']}: status={order['status']}")

def on_execution_report(context, execrpt):
    """Execution report event — triggered on trade execution"""
    print(f"Executed: {execrpt['symbol']} {execrpt['filled_volume']}@{execrpt['filled_vwap']}")

if __name__ == '__main__':
    run(strategy_id='your_strategy_id',
        filename='main.py',
        mode=MODE_BACKTEST,                          # Run mode: backtest
        token='your_token',
        backtest_start_time='2024-01-01 09:30:00',   # Backtest start time
        backtest_end_time='2024-06-30 15:00:00',     # Backtest end time
        backtest_initial_cash=1000000,                # Initial capital 1,000,000
        backtest_commission_ratio=0.0003,             # Commission rate 0.03%
        backtest_slippage_ratio=0.001,                # Slippage 0.1%
        backtest_adjust=ADJUST_PREV)                  # 前复权
```

---

## 基本函数

### init — 策略初始化

```python
def init(context):
    # Subscribe to daily bars, keeping the most recent 20
    subscribe(symbols='SHSE.600000', frequency='1d', count=20)
    context.ratio = 0.8  # Custom parameter
```

- 策略启动时调用一次
- 用于设置订阅、定义参数和初始化状态
- **回测模式下init中不允许下单**（模拟/实盘模式允许）

### schedule — 定时任务

```python
def init(context):
    # Execute algo_1 function at 09:40:00 on each trading day
    schedule(schedule_func=algo_1, date_rule='1d', time_rule='09:40:00')
    # Execute algo_2 function at 14:30:00 on the 1st trading day of each month
    schedule(schedule_func=algo_2, date_rule='1m', time_rule='14:30:00')

def algo_1(context):
    # Stock selection / rebalancing logic
    pass

def algo_2(context):
    # Market order to buy 200 shares
    order_volume(symbol='SHSE.600000', volume=200,
                 side=OrderSide_Buy, order_type=OrderType_Market,
                 position_effect=PositionEffect_Open)
```

- `date_rule`: `'1d'` (daily), `'1w'` (weekly, backtest only), `'1m'` (monthly, backtest only)
- `time_rule`: `'HH:MM:SS'` format, must be zero-padded (e.g., `'09:40:00'`, not `'9:40:0'`)

### run — 运行策略

```python
run(strategy_id='strategy_1',
    filename='main.py',
    mode=MODE_BACKTEST,       # MODE_BACKTEST=2 (backtest), MODE_LIVE=1 (live/paper)
    token='your_token',
    backtest_start_time='2024-01-01 09:30:00',
    backtest_end_time='2024-06-30 15:00:00',
    backtest_initial_cash=1000000,          # Initial capital
    backtest_transaction_ratio=1,           # Transaction fill ratio
    backtest_commission_ratio=0.0003,       # Commission rate
    backtest_slippage_ratio=0.001,          # Slippage ratio
    backtest_adjust=ADJUST_PREV)  # ADJUST_NONE=0 (unadjusted), ADJUST_PREV=1 (forward-adjusted), ADJUST_POST=2 (backward-adjusted)
```

### stop — 停止策略

```python
stop()  # Gracefully stop and exit the strategy
```

---

## 数据订阅

### subscribe — 订阅行情数据

```python
subscribe(symbols='SHSE.600000,SZSE.000001',
          frequency='60s',    # Frequency: tick, 1s~300s, 60s, 300s, 900s, 1800s, 3600s, 1d
   
          count=5,            # Number of historical bars to keep in context.data
          wait_group=True,    # Wait for all symbols in the group before triggering callback
          wait_group_timeout='5s')  # Wait timeout duration
```

### unsubscribe — 取消订阅

```python
unsubscribe(symbols='SHSE.600000', frequency='60s')
```

---

## 数据事件

| 事件 | 触发条件 | 参数 |
|---|---|---|
| `on_tick(context, tick)` | 每次Tick推送 | 包含价格、买卖盘、成交量的Tick字典 |
| `on_bar(context, bars)` | 每根K线收盘 | K线字典列表 |
| `on_l2transaction(context, l2transaction)` | Level 2逐笔成交 | L2Transaction字典 |
| `on_l2order(context, l2order)` | Level 2逐笔委托 | L2Order字典 |
| `on_l2order_queue(context, l2order_queue)` | Level 2委托队列 | L2OrderQueue字典 |

---

## 数据查询函数

### current — 实时快照

```python
data = current(symbols='SZSE.000001')
# 收益率: [{'symbol': 'SZSE.000001', 'price': 16.56, 'open': 16.20, 'high': 16.92, 'low': 16.15,
#            'quotes': [{'bid_p': 16.55, 'bid_v': 209200, 'ask_p': 16.56, 'ask_v': 296455}, ...],
#            'cum_volume': 160006232, 'cum_amount': 2654379585.66, 'created_at': ...}]
```

- 回测模式：仅返回 `symbol`、`price`、`created_at`
- 实盘模式：返回完整tick字段，包含5档买卖盘

### history — 历史K线/Tick

```python
df = history(symbol='SHSE.000300', frequency='1d',
             start_time='2024-01-01', end_time='2024-06-30',
             fields='open,close,high,low,volume,eob',
             skip_suspended=True,          # 跳过停牌日
             fill_missing=None,            # Missing value fill: None, 'NaN', 'Last'
             adjust=ADJUST_PREV,           # 0=unadjusted, 1=forward-adjusted, 2=backward-adjusted
             df=True)                      # True returns DataFrame, False returns list[dict]
```

### history_n — 最近N根K线

```python
df = history_n(symbol='SHSE.600000', frequency='1d', count=20,
               end_time='2024-06-30', fields='close,volume',
               adjust=ADJUST_PREV, df=True)
```

### context.data — 订阅数据缓存

```python
# Access the subscribed data buffer (set by the count parameter in subscribe)
bars = context.data(symbol='SHSE.600000', frequency='60s', count=10)
```

### Level 2历史数据

```python
get_history_l2ticks(symbol, start_time, end_time, fields, skip_suspended, fill_missing, adjust, df)
get_history_l2bars(symbol, frequency, start_time, end_time, fields, skip_suspended, fill_missing, adjust, df)
get_history_l2transactions(symbol, start_time, end_time, fields, df)
get_history_l2orders(symbol, start_time, end_time, fields, df)
get_history_l2orders_queue(symbol, start_time, end_time, fields, df)
```

### 基本面数据

```python
# Retrieve financial indicator data with filtering and sorting support
df = get_fundamentals(
    table='trading_derivative_indicator',    # Data table name
    symbols='SHSE.600000,SZSE.000001',       # Stock symbols
    start_date='2024-01-01',
    end_date='2024-06-30',
    fields='TCLOSE,NEGOTIABLEMV,TOTMKTCAP,TURNRATE,PETTM',  # Field list
    limit=1000,                              # Result count limit
    df=True
)

# Retrieve the most recent N records
df = get_fundamentals_n(
    table='trading_derivative_indicator',
    symbols='SHSE.600000',
    end_date='2024-06-30',
    count=10,
    fields='TCLOSE,PETTM',
    df=True
)
```

可用的基本面数据表：参见[财务数据文档](https://www.myquant.cn/docs/l3333/913)

### 合约信息

```python
# Get all A-share instruments on the Shenzhen exchange
instruments = get_instruments(exchanges='SZSE', sec_types=1, df=True)

# Get information for specific instruments
info = get_instruments(symbols='SHSE.600000,SZSE.000001', df=True)
# Fields: symbol, sec_name, exchange, listed_date, delisted_date, sec_type,
#         pre_close, upper_limit, lower_limit, adj_factor, is_st, is_suspended, ...

# Get historical instrument information
hist_info = get_history_instruments(symbols='SHSE.600000', start_date='2024-01-01', end_date='2024-06-30')

# Get basic instrument information (static)
basic_info = get_instrumentinfos(symbols='SHSE.600000', df=True)
```

### 指数成分股

```python
# Get current constituents
stocks = get_constituents(index='SHSE.000300')  # CSI 300

# Get historical constituents
hist = get_history_constituents(index='SHSE.000300', start_date='2024-01-01', end_date='2024-06-30')
```

### 行业成分股

```python
# Get the stock list for a specified industry code
stocks = get_industry(code='J66')  # 收益率 stocks in industry J66 (Banking)
```

### 分红数据

```python
divs = get_dividend(symbol='SHSE.600000', start_date='2020-01-01', end_date='2024-12-31', df=True)
```

### 交易日历

```python
dates = get_trading_dates(exchange='SZSE', start_date='2024-01-01', end_date='2024-06-30')
prev = get_previous_trading_date(exchange='SHSE', date='2024-03-15')   # Previous trading date
next_d = get_next_trading_date(exchange='SHSE', date='2024-03-15')     # Next trading date
```

### 连续合约（期货）

```python
contracts = get_continuous_contracts(csymbol='CFFEX.IF', start_date='2024-01-01', end_date='2024-06-30')
```

### 新股申购函数

```python
quota = ipo_get_quota()                  # Query IPO subscription quota
instruments = ipo_get_instruments()      # Query today's IPO list
match_nums = ipo_get_match_number()      # Query allotment numbers
lot_info = ipo_get_lot_info()            # Query winning lot information
```

---

## 交易函数

### 按数量下单

```python
order = order_volume(
    symbol='SHSE.600000',
    volume=10000,                               # Order quantity
    side=OrderSide_Buy,                         # Side: OrderSide_Buy=1 (buy), OrderSide_Sell=2 (sell)
    order_type=OrderType_Limit,                 # Order type: OrderType_Limit=1 (limit), OrderType_Market=2 (market)
    position_effect=PositionEffect_Open,        # Position effect: Open=1 (open), Close=2 (close), CloseToday=3 (close today), CloseYesterday=4 (close yesterday)
    price=11.0,                                 # Order price
    account=''                                  # Optional: specify account for multi-account setups
)
```

### 按金额下单

```python
order = order_value(
    symbol='SHSE.600000',
    value=100000,                   # Target order value (CNY)
    side=OrderSide_Buy,
    order_type=OrderType_Limit,
    position_effect=PositionEffect_Open,
    price=11.0
)
# Actual quantity = value / price, truncated to valid lot size
```

### 按比例下单

```python
order = order_percent(
    symbol='SHSE.600000',
    percent=0.1,                    # 10% of total assets
    side=OrderSide_Buy,
    order_type=OrderType_Limit,
    position_effect=PositionEffect_Open,
    price=11.0
)
```

### 目标仓位函数

```python
# Adjust to target volume
order_target_volume(symbol='SHSE.600000', volume=10000,
                    position_side=PositionSide_Long,
                    order_type=OrderType_Limit, price=13.0)

# Adjust to target value
order_target_value(symbol='SHSE.600000', value=130000,
                   position_side=PositionSide_Long,
                   order_type=OrderType_Limit, price=13.0)

# Adjust to target percentage (percentage of total assets)
order_target_percent(symbol='SHSE.600000', percent=0.1,
                     position_side=PositionSide_Long,
                     order_type=OrderType_Limit, price=13.0)
```

### 批量下单

```python
orders = [
    {'symbol': 'SHSE.600000', 'volume': 1000, 'side': OrderSide_Buy,
     'order_type': OrderType_Limit, 'position_effect': PositionEffect_Open, 'price': 11.0},
    {'symbol': 'SZSE.000001', 'volume': 2000, 'side': OrderSide_Buy,
     'order_type': OrderType_Limit, 'position_effect': PositionEffect_Open, 'price': 15.0},
]
results = order_batch(orders)  # Submit orders in batch
```

### 撤单与全部平仓

```python
# 撤销指定订单
order_cancel(wait_cancel_orders=[
    {'cl_ord_id': order1['cl_ord_id'], 'account_id': order1['account_id']}
])
order_cancel_all()        # Cancel all unfilled orders
order_close_all()         # Close all positions (limit orders)
```

### 查询委托

```python
unfinished = get_unfinished_orders()    # Query unfinished orders (pending/partially filled)
all_orders = get_orders()               # Query all orders today
executions = get_execution_reports()    # Query all execution reports today
```

### 特殊交易

```python
ipo_buy(symbol)                                       # IPO subscription
fund_etf_buy(symbol, volume, price)                   # ETF purchase
fund_etf_redemption(symbol, volume, price)             # ETF redemption
fund_subscribing(symbol, volume, price)                # Fund initial subscription
fund_buy(symbol, volume, price)                        # Fund purchase
fund_redemption(symbol, volume, price)                 # Fund redemption
bond_reverse_repurchase_agreement(symbol, volume, price) # Treasury reverse repo
```

---

## 账户与持仓查询

```python
# Query cash information
cash = context.account().cash
# Attributes: nav (net asset value), fpnl (floating P&L), pnl (realized P&L), available (available funds),
#             order_frozen (order frozen), balance (balance), market_value (position market value), cum_trade (cumulative trade amount), ...

# Query all positions
positions = context.account().positions()
# Each position contains: symbol, side, volume, available_now, cost, vwap, market_value, fpnl, ...

# Query a specific position
pos = context.account().position(symbol='SHSE.600000', side=PositionSide_Long)
```

---

## 融资融券

```python
# Margin buy
credit_buying_on_margin(symbol, volume, price, side=OrderSide_Buy, order_type=OrderType_Limit)

# Short sell
credit_short_selling(symbol, volume, price, side=OrderSide_Sell, order_type=OrderType_Limit)

# Repayment
credit_repay_cash_directly(amount)              # Direct cash repayment
credit_repay_share_directly(symbol, volume)      # Direct share repayment
credit_repay_share_by_buying_share(symbol, volume, price)  # Buy shares to repay
credit_repay_cash_by_selling_share(symbol, volume, price)  # Sell shares to repay cash

# Collateral operations
credit_buying_on_collateral(symbol, volume, price)   # Buy collateral
credit_selling_on_collateral(symbol, volume, price)   # Sell collateral
credit_collateral_in(symbol, volume)                  # Transfer collateral in
credit_collateral_out(symbol, volume)                 # Transfer collateral out

# Queries
credit_get_collateral_instruments()          # Query collateral instruments
credit_get_borrowable_instruments()          # Query borrowable instruments
credit_get_borrowable_instruments_positions() # Query broker's lending positions
credit_get_contracts()                       # Query margin trading contracts
credit_get_cash()                            # Query margin trading funds
```

---

## 算法交易

```python
# Submit an algorithmic order (e.g., TWAP, VWAP)
algo_order(symbol, volume, side, order_type, position_effect, price, algo_name, algo_param)

# Cancel an algorithmic order
algo_order_cancel(cl_ord_id, account_id)

# Query algorithmic orders
get_algo_orders()

# Pause/resume an algorithmic order
algo_order_pause(cl_ord_id, account_id, status)  # AlgoOrderStatus_Pause / AlgoOrderStatus_Resume

# Query child orders of an algorithmic order
get_algo_child_orders(cl_ord_id, account_id)

# Algorithmic order status event
def on_algo_order_status(context, order):
    print(f"Algo order {order['cl_ord_id']}: status={order['status']}")
```

---

## 交易事件

| 事件 | 触发条件 | 关键字段 |
|---|---|---|
| `on_order_status(context, order)` | 订单状态变化 | `cl_ord_id`, `symbol`, `status`, `filled_volume`, `filled_vwap` |
| `on_execution_report(context, execrpt)` | 成交回报 | `cl_ord_id`, `symbol`, `filled_volume`, `filled_vwap`, `price` |
| `on_account_status(context, account)` | 账户状态变化 | `account_id`, `status` |

---

## 动态参数

```python
def init(context):
    # Add a parameter that can be dynamically modified in the terminal UI
    add_parameter(key='threshold', value=0.05, min=0.01, max=0.2, name='买入阈值', intro='触发买入的比例')

def on_parameter(context, parameter):
    """Triggered when a parameter is modified in the terminal UI"""
    print(f"Parameter changed: {parameter['key']} = {parameter['value']}")

# Modify parameter at runtime
set_parameter(key='threshold', value=0.08)

# Read all parameters
params = context.parameters
```

---

## 连接事件

| 事件 | 触发条件 |
|---|---|
| `on_backtest_finished(context, indicator)` | 回测完成，接收绩效统计 |
| `on_error(context, code, info)` | 发生错误 |
| `on_market_data_connected(context)` | 行情数据连接建立 |
| `on_trade_data_connected(context)` | 交易连接建立 |
| `on_market_data_disconnected(context)` | 行情数据连接断开 |
| `on_trade_data_disconnected(context)` | 交易连接断开 |

---

## 代码格式

格式：`交易所代码.证券代码`

| 交易所代码 | 说明 | 示例 |
|---|---|---|
| `SHSE` | 上海证券交易所 | `SHSE.600000`（浦发银行） |
| `SZSE` | 深圳证券交易所 | `SZSE.000001`（平安银行） |
| `CFFEX` | 中国金融期货交易所 | `CFFEX.IF2401`（沪深300期货） |
| `SHFE` | 上海期货交易所 | `SHFE.ag2407`（白银期货） |
| `DCE` | 大连商品交易所 | `DCE.m2405`（豆粕期货） |
| `CZCE` | 郑州商品交易所 | `CZCE.CF405`（棉花期货） |
| `INE` | 上海国际能源交易中心 | `INE.sc2407`（原油期货） |
| `GFEX` | 广州期货交易所 | `GFEX.si2407`（工业硅期货） |

## 枚举常量参考

### OrderSide — 委托方向

| 常量 | 值 | 说明 |
|---|---|---|
| `OrderSide_Buy` | 1 | 买入 |
| `OrderSide_Sell` | 2 | 卖出 |

### OrderType — 委托类型

| 常量 | 值 | 说明 |
|---|---|---|
| `OrderType_Limit` | 1 | 限价单 |
| `OrderType_Market` | 2 | 市价单 |

### PositionEffect — 开平标志

| 常量 | 值 | 说明 |
|---|---|---|
| `PositionEffect_Open` | 1 | 开仓 |
| `PositionEffect_Close` | 2 | 平仓 |
| `PositionEffect_CloseToday` | 3 | 平今仓 |
| `PositionEffect_CloseYesterday` | 4 | 平昨仓 |

### PositionSide — 持仓方向

| 常量 | 值 | 说明 |
|---|---|---|
| `PositionSide_Long` | 1 | 多头 |
| `PositionSide_Short` | 2 | 空头 |

### OrderStatus — 订单状态

| 常量 | 值 | 说明 |
|---|---|---|
| `OrderStatus_New` | 1 | 已报 |
| `OrderStatus_PartiallyFilled` | 2 | 部分成交 |
| `OrderStatus_Filled` | 3 | 已成 |
| `OrderStatus_Canceled` | 5 | 已撤 |
| `OrderStatus_PendingCancel` | 6 | 待撤 |
| `OrderStatus_Rejected` | 8 | 废单 |
| `OrderStatus_PendingNew` | 10 | 待报 |
| `OrderStatus_Expired` | 12 | 过期 |

### ADJUST — 复权方式

| 常量 | 值 | 说明 |
|---|---|---|
| `ADJUST_NONE` | 0 | 不复权 |
| `ADJUST_PREV` | 1 | 前复权 |
| `ADJUST_POST` | 2 | 后复权 |

---

## 完整示例 — 双均线回测策略

```python
from gm.api import *

def init(context):
    # Subscribe to daily bars, keeping the most recent 21
    subscribe(symbols='SHSE.600000', frequency='1d', count=21)
    context.symbol = 'SHSE.600000'

def on_bar(context, bars):
    # Get the most recent 20 daily bars
    hist = context.data(symbol=context.symbol, frequency='1d', count=20)
    closes = [bar['close'] for bar in hist]

    if len(closes) < 20:
        return  # Insufficient data, skip

    # Calculate 5-day and 20-day moving averages
    ma5 = sum(closes[-5:]) / 5
    ma20 = sum(closes) / 20
    price = bars[0]['close']

    # Query current position
    pos = context.account().position(symbol=context.symbol, side=PositionSide_Long)

    # 金叉 signal: 5-day MA > 20-day MA and no position, buy
    if ma5 > ma20 and (pos is None or pos['volume'] == 0):
        order_percent(symbol=context.symbol, percent=0.9,
                      side=OrderSide_Buy, order_type=OrderType_Limit,
                      position_effect=PositionEffect_Open, price=price)
    # 死叉 signal: 5-day MA < 20-day MA and has position, close all
    elif ma5 < ma20 and pos is not None and pos['volume'] > 0:
        order_close_all()

def on_order_status(context, order):
    if order['status'] == OrderStatus_Filled:
        print(f"Executed: {order['symbol']} volume={order['filled_volume']} avg_price={order['filled_vwap']}")

def on_backtest_finished(context, indicator):
    print(f"Backtest completed: return={indicator['pnl_ratio']:.2%}, "
          f"Sharpe ratio={indicator['sharpe_ratio']:.2f}, "
          f"max drawdown={indicator['max_drawdown']:.2%}")

if __name__ == '__main__':
    run(strategy_id='ma_cross',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='your_token',
        backtest_start_time='2023-01-01 09:30:00',
        backtest_end_time='2024-06-30 15:00:00',
        backtest_initial_cash=1000000,
        backtest_commission_ratio=0.0003,
        backtest_slippage_ratio=0.001,
        backtest_adjust=ADJUST_PREV)
```

## 完整示例 — 定时调仓策略

```python
from gm.api import *

def init(context):
    # Rebalance at 09:35 on each trading day
    schedule(schedule_func=rebalance, date_rule='1d', time_rule='09:35:00')
    context.target_stocks = ['SHSE.600000', 'SZSE.000001', 'SHSE.601318']

def rebalance(context):
    # Equal-weight allocation, each stock gets 1/N of total assets
    target_pct = 1.0 / len(context.target_stocks)
    for sym in context.target_stocks:
        order_target_percent(symbol=sym, percent=target_pct * 0.95,
                             position_side=PositionSide_Long,
                             order_type=OrderType_Market)

if __name__ == '__main__':
    run(strategy_id='equal_weight',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='your_token',
        backtest_start_time='2024-01-01 09:30:00',
        backtest_end_time='2024-06-30 15:00:00',
        backtest_initial_cash=1000000,
        backtest_adjust=ADJUST_PREV)
```

## 完整示例 — 纯数据研究（无交易）

```python
from gm.api import *

# Set Token (can query data without starting a strategy)
set_token('your_token')

# Get historical bar data
df = history(symbol='SHSE.000300', frequency='1d',
             start_time='2024-01-01', end_time='2024-06-30',
             fields='open,close,high,low,volume',
             adjust=ADJUST_PREV, df=True)
print(df.head())

# Get financial indicator data
fund = get_fundamentals(table='trading_derivative_indicator',
                        symbols='SHSE.600000',
                        start_date='2024-01-01',
                        end_date='2024-06-30',
                        fields='TCLOSE,PETTM,TURNRATE',
                        df=True)
print(fund)

# 获取沪深300成分股
constituents = get_constituents(index='SHSE.000300')
print(f'CSI 300 has {len(constituents)} constituent stocks')

# Get banking industry stocks
bank_stocks = get_industry(code='J66')
print(f'Banking industry has {len(bank_stocks)} stocks')
```

---

## 支持的数据频率

| 频率 | 说明 | 模式 |
|---|---|---|
| `tick` | Tick级数据 | 实时 & 回测 |
| `1s` ~ `300s` | N秒K线 | 实时 & 回测 |
| `60s` | 1分钟K线 | 实时 & 回测 |
| `300s` | 5分钟K线 | 实时 & 回测 |
| `900s` | 15分钟K线 | 实时 & 回测 |
| `1800s` | 30分钟K线 | 实时 & 回测 |
| `3600s` | 60分钟K线 | 实时 & 回测 |
| `1d` | 日K线 | 实时 & 回测 |

## 运行模式

| 模式 | 常量 | 说明 |
|---|---|---|
| 回测 | `MODE_BACKTEST` (2) | 历史数据模拟，可配置参数 |
| 实盘/模拟 | `MODE_LIVE` (1) | 实时模拟交易或通过掘金终端实盘交易 |

---

## 使用技巧

- **需要Token**：在 https://www.myquant.cn 注册获取。使用 `set_token()` 或在 `run()` 中传入。
- **事件驱动**：所有策略逻辑由事件触发（`on_bar`、`on_tick`、`on_order_status`），无需轮询。
- **先订阅再交易**：在 `init()` 中使用 `subscribe()` 确保 `on_bar`/`on_tick` 触发前数据已就绪。
- **回测模式init中不可下单**：回测模式下 `init()` 仅允许订阅和参数设置。
- **定期调仓用schedule**：使用 `schedule()` 而非 `on_bar` 实现定期调仓策略。
- **df=True**：大多数数据查询函数支持 `df=True` 返回pandas DataFrame，便于分析。
- **多账户**：在下单函数中传入 `account=''` 参数指定账户。
- **期货平仓**：上期所需要用 `PositionEffect_CloseToday` / `PositionEffect_CloseYesterday` 区分平今仓和平昨仓。
- **回测默认值**：初始资金=1,000,000，手续费=0，滑点=0。请设置合理值。
- Documentation: https://www.myquant.cn/docs/python/41

---

## 进阶示例

### 多因子选股策略

```python
from gm.api import *
import numpy as np

def init(context):
    # Execute stock selection and rebalancing at 10:00 on the 1st trading day of each month
    schedule(schedule_func=multi_factor_rebalance, date_rule='1m', time_rule='10:00:00')
    context.hold_num = 10          # 持股数量
    context.target_index = 'SHSE.000300'  # Selection universe: CSI 300 constituents

def multi_factor_rebalance(context):
    """Multi-factor stock selection + equal-weight rebalancing"""
    # 获取沪深300成分股
    constituents = get_constituents(index=context.target_index)
    symbols = [c['symbol'] for c in constituents]

    # Get financial indicator data (PE, PB, ROE, turnover rate)
    fund_data = get_fundamentals(
        table='trading_derivative_indicator',
        symbols=','.join(symbols),
        end_date=context.now.strftime('%Y-%m-%d'),
        count=1,
        fields='PETTM,PB,TURNRATE',
        df=True
    )

    if fund_data is None or len(fund_data) == 0:
        return

    # Data cleaning: remove missing values and outliers
    fund_data = fund_data.dropna(subset=['PETTM', 'PB'])
    fund_data = fund_data[(fund_data['PETTM'] > 0) & (fund_data['PETTM'] < 100)]
    fund_data = fund_data[(fund_data['PB'] > 0) & (fund_data['PB'] < 20)]

    # Factor scoring: lower PE is better, lower PB is better (higher rank = higher score)
    fund_data['PE_rank'] = fund_data['PETTM'].rank(ascending=True)
    fund_data['PB_rank'] = fund_data['PB'].rank(ascending=True)
    # Composite score = PE rank * 0.5 + PB rank * 0.5
    fund_data['score'] = fund_data['PE_rank'] * 0.5 + fund_data['PB_rank'] * 0.5
    # Sort by composite score, select top N
    selected = fund_data.nsmallest(context.hold_num, 'score')
    target_symbols = selected['symbol'].tolist()

    print(f"Selected {len(target_symbols)} stocks this period: {target_symbols}")

    # First close positions not in the target list
    positions = context.account().positions()
    for pos in positions:
        if pos['symbol'] not in target_symbols and pos['volume'] > 0:
            order_target_volume(symbol=pos['symbol'], volume=0,
                                position_side=PositionSide_Long,
                                order_type=OrderType_Market)
            print(f"  Closing: {pos['symbol']}")

    # 等权重买入目标股票
    target_pct = 0.95 / len(target_symbols)  # Keep 5% cash
    for sym in target_symbols:
        order_target_percent(symbol=sym, percent=target_pct,
                             position_side=PositionSide_Long,
                             order_type=OrderType_Market)
        print(f"  Rebalancing: {sym} -> {target_pct*100:.1f}%")

if __name__ == '__main__':
    run(strategy_id='multi_factor',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='your_token',
        backtest_start_time='2023-01-01 09:30:00',
        backtest_end_time='2024-06-30 15:00:00',
        backtest_initial_cash=1000000,
        backtest_commission_ratio=0.0003,
        backtest_slippage_ratio=0.001,
        backtest_adjust=ADJUST_PREV)
```

### 配对交易策略（统计套利）

```python
from gm.api import *
import numpy as np

def init(context):
    # Pair: China Merchants Bank vs Industrial Bank (same industry, high correlation)
    context.stock_a = 'SHSE.600036'
    context.stock_b = 'SHSE.601166'
    context.lookback = 60          # Lookback window (trading days)
    context.entry_z = 2.0          # Entry Z-score threshold
    context.exit_z = 0.5           # Exit Z-score threshold
    context.position_pct = 0.4     # Single-side position ratio

    # Subscribe to daily bars for both stocks
    subscribe(symbols=f'{context.stock_a},{context.stock_b}', frequency='1d', count=context.lookback + 1)

def on_bar(context, bars):
    # Get historical close prices
    hist_a = context.data(symbol=context.stock_a, frequency='1d', count=context.lookback)
    hist_b = context.data(symbol=context.stock_b, frequency='1d', count=context.lookback)

    if len(hist_a) < context.lookback or len(hist_b) < context.lookback:
        return

    closes_a = np.array([bar['close'] for bar in hist_a])
    closes_b = np.array([bar['close'] for bar in hist_b])

    # Calculate price ratio (spread)
    ratio = closes_a / closes_b
    ratio_mean = np.mean(ratio)
    ratio_std = np.std(ratio)

    if ratio_std == 0:
        return

    # Calculate current Z-score
    current_ratio = bars[0]['close'] / bars[1]['close'] if len(bars) >= 2 else ratio[-1]
    z_score = (current_ratio - ratio_mean) / ratio_std

    # Query current positions
    pos_a = context.account().position(symbol=context.stock_a, side=PositionSide_Long)
    pos_b = context.account().position(symbol=context.stock_b, side=PositionSide_Long)
    has_pos_a = pos_a is not None and pos_a['volume'] > 0
    has_pos_b = pos_b is not None and pos_b['volume'] > 0

    print(f"Z-score={z_score:.2f}, ratio={current_ratio:.4f}, mean={ratio_mean:.4f}")

    if z_score > context.entry_z and not has_pos_b:
        # Z-score too high: A overvalued relative to B → sell A, buy B
        if has_pos_a:
            order_close_all()  # Close reverse positions first
        order_percent(symbol=context.stock_b, percent=context.position_pct,
                      side=OrderSide_Buy, order_type=OrderType_Market,
                      position_effect=PositionEffect_Open)
        print(f"  Open position: buy {context.stock_b}")

    elif z_score < -context.entry_z and not has_pos_a:
        # Z-score too low: A undervalued relative to B → buy A, sell B
        if has_pos_b:
            order_close_all()
        order_percent(symbol=context.stock_a, percent=context.position_pct,
                      side=OrderSide_Buy, order_type=OrderType_Market,
                      position_effect=PositionEffect_Open)
        print(f"  Open position: buy {context.stock_a}")

    elif abs(z_score) < context.exit_z and (has_pos_a or has_pos_b):
        # Z-score reverts to mean → close positions
        order_close_all()
        print(f"  Close positions: Z-score reverted")

if __name__ == '__main__':
    run(strategy_id='pair_trading',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='your_token',
        backtest_start_time='2023-01-01 09:30:00',
        backtest_end_time='2024-06-30 15:00:00',
        backtest_initial_cash=1000000,
        backtest_commission_ratio=0.0003,
        backtest_adjust=ADJUST_PREV)
```

### 期货CTA趋势跟踪策略（海龟交易）

```python
from gm.api import *
import numpy as np

def init(context):
    context.symbol = 'CFFEX.IF2401'   # CSI 300 index futures
    context.entry_period = 20          # 入场通道周期 (20-day high/low)
    context.exit_period = 10           # 出场通道周期 (10-day high/low)
    context.atr_period = 20            # ATR calculation period
    context.risk_ratio = 0.01          # Per-trade risk ratio (1% of total assets)

    subscribe(symbols=context.symbol, frequency='1d', count=context.entry_period + 1)

def on_bar(context, bars):
    hist = context.data(symbol=context.symbol, frequency='1d', count=context.entry_period)
    if len(hist) < context.entry_period:
        return

    highs = np.array([bar['high'] for bar in hist])
    lows = np.array([bar['low'] for bar in hist])
    closes = np.array([bar['close'] for bar in hist])

    # Calculate Donchian Channel
    entry_high = np.max(highs[-context.entry_period:])    # 20-day high (breakout long)
    entry_low = np.min(lows[-context.entry_period:])      # 20-day low (breakout short)
    exit_high = np.max(highs[-context.exit_period:])      # 10-day high (short stop-loss)
    exit_low = np.min(lows[-context.exit_period:])        # 10-day low (long stop-loss)

    # Calculate ATR (Average True Range)
    tr_list = []
    for i in range(1, len(highs)):
        tr = max(highs[i] - lows[i],
                 abs(highs[i] - closes[i-1]),
                 abs(lows[i] - closes[i-1]))
        tr_list.append(tr)
    atr = np.mean(tr_list[-context.atr_period:]) if len(tr_list) >= context.atr_period else 0

    current_price = bars[0]['close']
    pos_long = context.account().position(symbol=context.symbol, side=PositionSide_Long)
    pos_short = context.account().position(symbol=context.symbol, side=PositionSide_Short)
    has_long = pos_long is not None and pos_long['volume'] > 0
    has_short = pos_short is not None and pos_short['volume'] > 0

    # 计算仓位大小（基于ATR的风险管理）
    if atr > 0:
        nav = context.account().cash['nav']
        unit_size = int(nav * context.risk_ratio / (atr * 300))  # IF contract multiplier 300
        unit_size = max(unit_size, 1)
    else:
        unit_size = 1

    # Entry signals
    if current_price > entry_high and not has_long:
        if has_short:
            # Close short position first
            order_volume(symbol=context.symbol, volume=pos_short['volume'],
                         side=OrderSide_Buy, order_type=OrderType_Market,
                         position_effect=PositionEffect_Close)
        # Open long position
        order_volume(symbol=context.symbol, volume=unit_size,
                     side=OrderSide_Buy, order_type=OrderType_Market,
                     position_effect=PositionEffect_Open)
        print(f"Breakout long: price={current_price}, upper channel={entry_high}, lots={unit_size}")

    elif current_price < entry_low and not has_short:
        if has_long:
            order_volume(symbol=context.symbol, volume=pos_long['volume'],
                         side=OrderSide_Sell, order_type=OrderType_Market,
                         position_effect=PositionEffect_Close)
        # Open short position
        order_volume(symbol=context.symbol, volume=unit_size,
                     side=OrderSide_Sell, order_type=OrderType_Market,
                     position_effect=PositionEffect_Open)
        print(f"Breakout short: price={current_price}, lower channel={entry_low}, lots={unit_size}")

    # Exit signals
    elif has_long and current_price < exit_low:
        order_volume(symbol=context.symbol, volume=pos_long['volume'],
                     side=OrderSide_Sell, order_type=OrderType_Market,
                     position_effect=PositionEffect_Close)
        print(f"Long stop-loss: price={current_price}, exit lower channel={exit_low}")

    elif has_short and current_price > exit_high:
        order_volume(symbol=context.symbol, volume=pos_short['volume'],
                     side=OrderSide_Buy, order_type=OrderType_Market,
                     position_effect=PositionEffect_Close)
        print(f"Short stop-loss: price={current_price}, exit upper channel={exit_high}")

def on_backtest_finished(context, indicator):
    print(f"\nBacktest results:")
    print(f"  Return: {indicator['pnl_ratio']:.2%}")
    print(f"  Annualized return: {indicator['pnl_ratio_annual']:.2%}")
    print(f"  Sharpe ratio: {indicator['sharpe_ratio']:.2f}")
    print(f"  Max drawdown: {indicator['max_drawdown']:.2%}")
    print(f"  Win rate: {indicator['win_ratio']:.2%}")

if __name__ == '__main__':
    run(strategy_id='turtle_cta',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='your_token',
        backtest_start_time='2023-01-01 09:30:00',
        backtest_end_time='2024-06-30 15:00:00',
        backtest_initial_cash=2000000,
        backtest_commission_ratio=0.000023,
        backtest_slippage_ratio=0.0005,
        backtest_adjust=ADJUST_PREV)
```

### 风险管理模块 — 仓位控制与回撤监控

```python
from gm.api import *

def init(context):
    subscribe(symbols='SHSE.600000,SZSE.000001,SHSE.601318', frequency='1d', count=21)
    context.max_drawdown_limit = 0.10   # Max drawdown limit 10%
    context.max_single_position = 0.30  # Max single stock position 30%
    context.max_total_position = 0.90   # Max total position 90%
    context.peak_nav = 0                # Historical peak NAV
    context.is_stopped = False          # Whether risk control has stopped trading

def on_bar(context, bars):
    # Update historical peak NAV
    nav = context.account().cash['nav']
    if nav > context.peak_nav:
        context.peak_nav = nav

    # Calculate current drawdown
    current_drawdown = (context.peak_nav - nav) / context.peak_nav if context.peak_nav > 0 else 0

    # Check if max drawdown limit is triggered
    if current_drawdown >= context.max_drawdown_limit:
        if not context.is_stopped:
            print(f"⚠️ Max drawdown limit triggered: drawdown={current_drawdown:.2%}, closing all positions!")
            order_close_all()
            context.is_stopped = True
        return

    context.is_stopped = False

    # Check if any single stock position exceeds the limit
    positions = context.account().positions()
    total_position_value = sum(p['market_value'] for p in positions)
    total_asset = context.account().cash['nav']

    for pos in positions:
        single_pct = pos['market_value'] / total_asset if total_asset > 0 else 0
        if single_pct > context.max_single_position:
            # Single stock position exceeds limit, reduce to the limit
            target_value = total_asset * context.max_single_position
            order_target_value(symbol=pos['symbol'], value=target_value,
                               position_side=PositionSide_Long,
                               order_type=OrderType_Market)
            print(f"  Reducing: {pos['symbol']} position {single_pct:.1%} -> {context.max_single_position:.1%}")

    # Output risk control status
    total_pct = total_position_value / total_asset if total_asset > 0 else 0
    print(f"NAV={nav:.2f}, drawdown={current_drawdown:.2%}, total position={total_pct:.1%}")

if __name__ == '__main__':
    run(strategy_id='risk_mgmt',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='your_token',
        backtest_start_time='2023-01-01 09:30:00',
        backtest_end_time='2024-06-30 15:00:00',
        backtest_initial_cash=1000000,
        backtest_adjust=ADJUST_PREV)
```

### 数据研究 — 行业轮动分析

```python
from gm.api import *
import pandas as pd

# Set Token (pure data research, no strategy needed)
set_token('your_token')

# Define industry ETF list (using ETFs instead of industry indices for easier data access)
industry_etfs = {
    'SHSE.510050': '上证50',
    'SHSE.510300': '沪深300',
    'SHSE.510500': '中证500',
    'SZSE.159915': '创业板',
    'SHSE.512010': '医药ETF',
    'SHSE.512880': '证券ETF',
    'SHSE.512800': '银行ETF',
    'SHSE.515030': '新能源车ETF',
    'SZSE.159995': '芯片ETF',
    'SHSE.512690': '白酒ETF',
}

# Get daily bar data for each industry ETF over the past year
results = []
for symbol, name in industry_etfs.items():
    df = history(symbol=symbol, frequency='1d',
                 start_time='2024-01-01', end_time='2024-12-31',
                 fields='close,volume,eob',
                 adjust=ADJUST_PREV, df=True)
    if df is not None and len(df) > 20:
        # Calculate returns over various periods
        ret_5d = (df['close'].iloc[-1] / df['close'].iloc[-6] - 1) * 100    # 5-day return
        ret_20d = (df['close'].iloc[-1] / df['close'].iloc[-21] - 1) * 100  # 20-day return
        ret_60d = (df['close'].iloc[-1] / df['close'].iloc[-61] - 1) * 100 if len(df) > 60 else None
        avg_volume = df['volume'].tail(20).mean()  # 20-day average volume

        results.append({
            '行业': name,
            '代码': symbol,
            '近5日收益(%)': round(ret_5d, 2),
            '近20日收益(%)': round(ret_20d, 2),
            '近60日收益(%)': round(ret_60d, 2) if ret_60d else None,
            '20日均量': int(avg_volume),
        })

# Sort by 20-day return
df_result = pd.DataFrame(results).sort_values('近20日收益(%)', ascending=False)
print("\nIndustry rotation analysis (sorted by 20-day return):")
print(df_result.to_string(index=False))

# Find industries with strongest momentum (ranked top 3 in both 5-day and 20-day returns)
top5d = set(df_result.nlargest(3, '近5日收益(%)')['行业'].tolist())
top20d = set(df_result.nlargest(3, '近20日收益(%)')['行业'].tolist())
momentum_leaders = top5d & top20d
if momentum_leaders:
    print(f"\nMomentum leaders (strong in both short-term and mid-term): {momentum_leaders}")
```

---

---

## 🤖 AI Agent 高阶使用指南

对于 AI Agent，在使用该量化/数据工具时应遵循以下高阶策略和最佳实践，以确保任务的高效完成：

### 1. 数据校验与错误处理
在获取数据或执行操作后，AI 应当主动检查返回的结果格式是否符合预期，以及是否存在缺失值（NaN）或空数据。
* **示例策略**：在通过 API 获取数据框（DataFrame）后，使用 `if df.empty:` 进行校验；捕获 `Exception` 以防网络或接口错误导致进程崩溃。

### 2. 多步组合分析
AI 经常需要进行宏观经济分析或跨市场对比。应善于将当前接口与其他数据源或工具组合使用。
* **示例策略**：先获取板块或指数的宏观数据，再筛选成分股，最后对具体标的进行深入的财务或技术面分析，形成完整的决策链条。

### 3. 构建动态监控与日志
对于交易和策略类任务，AI 可以定期拉取数据并建立监控机制。
* **示例策略**：使用循环或定时任务检查特定标的的异动（如涨跌停、放量），并在发现满足条件的信号时输出结构化日志或触发预警。

---

## 社区与支持

由 **大佬量化** 维护 — 量化交易教学与策略研发团队。

微信客服: **bossquant1** · [Bilibili](https://space.bilibili.com/48693330) · 搜索 **大佬量化** — 微信公众号 / Bilibili / 抖音
