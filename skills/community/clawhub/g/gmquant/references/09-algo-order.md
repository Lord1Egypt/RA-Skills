# 算法委托（TWAP/VWAP 等）

## algo_order - 算法下单

```python
algo_order(symbol, volume, side, position_effect, order_type,
           price=0, algo_name='', algo_param={}, account=None)
```

| 参数 | 说明 |
|------|------|
| symbol | 标的代码 |
| volume | 委托量 |
| side | 买卖方向（OrderSide_Buy/Sell） |
| position_effect | 开平标志 |
| order_type | 委托类型 |
| algo_name | 算法名称，如 `'TWAP'`、`'VWAP'` |
| algo_param | 算法参数 dict |

```python
# TWAP 算法买入
algo_order(symbol='SHSE.600000', volume=1000, side=OrderSide_Buy,
           position_effect=PositionEffect_Open,
           order_type=OrderType_Market,
           algo_name='TWAP',
           algo_param={'start_time': '09:30:00', 'end_time': '15:00:00'})
```

## algo_order_cancel - 取消算法委托

```python
algo_order_cancel(wait_cancel_algo_orders, account=None)
```

---

# 账户与资金查询

## get_orders - 查询委托列表

```python
get_orders(account=None)
```

返回 `list[dict]`，每项为 Order 委托对象。

```python
from gm.api import *
set_token('YOUR_TOKEN')

orders = get_orders()
for order in orders:
    print(order['symbol'], order['status'], order['volume'])
```

**委托状态 OrderStatus**：
- 1=待报，2=已报，3=已报待撤，4=部成待撤，5=部撤，6=已撤，7=已成，8=废单，10=已报待改

---

## get_execution_reports - 查询成交回报

```python
get_execution_reports(account=None)
```

返回 `list[dict]`，每项为 ExecRpt 回报对象。

---

## get_cash - 查询账户资金

```python
get_cash(account=None)
```

返回资金 dict：

| 字段 | 说明 |
|------|------|
| nav | 总资产 |
| available | 可用资金 |
| fpnl | 浮动盈亏 |
| market_value | 持仓市值 |
| balance | 资金余额 |
| order_frozen | 冻结资金 |

```python
cash = get_cash()
print(f"总资产: {cash['nav']:.2f}")
print(f"可用资金: {cash['available']:.2f}")
```

---

## get_position - 查询持仓

```python
get_position(symbol=None, side=None, account=None)
```

```python
# 查询全部持仓
positions = get_position()

# 查询指定标的多头持仓
pos = get_position(symbol='SHSE.600000', side=PositionSide_Long)
if pos:
    print(f"持仓量: {pos[0]['volume']}")
    print(f"持仓均价: {pos[0]['vwap']}")
    print(f"浮动盈亏: {pos[0]['fpnl']}")
```

**Position 对象关键字段**：

| 字段 | 说明 |
|------|------|
| symbol | 标的代码 |
| side | 持仓方向 |
| volume | 总持仓量 |
| volume_today | 今日买入量 |
| available | 可用持仓（非冻结） |
| vwap | 持仓均价 |
| market_value | 持仓市值 |
| fpnl | 浮动盈亏 |
| amount | 持仓额 |

---

## context.account() - 在策略中查询账户

```python
# 获取所有持仓
all_positions = context.account().positions()

# 获取指定持仓
pos = context.account().position(symbol='SHSE.600519', side=PositionSide_Long)

# 获取资金
cash = context.account().cash

# 账户状态
status = context.account().status
```
