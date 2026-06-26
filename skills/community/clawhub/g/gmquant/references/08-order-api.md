# 交易下单 API

> 所有下单函数只能在策略事件回调中使用（`on_bar`、`on_tick`、`algo` 定时任务等）
> 回测模式下 `init` 中不支持交易操作

## 常用枚举常量

```python
# 买卖方向
OrderSide_Buy = 1   # 买入
OrderSide_Sell = 2  # 卖出

# 委托类型
OrderType_Limit = 1    # 限价
OrderType_Market = 2   # 市价

# 开平标志
PositionEffect_Open = 1   # 开仓
PositionEffect_Close = 2  # 平仓（平昨）
PositionEffect_Close_Today = 3  # 平今（期货）

# 持仓方向
PositionSide_Long = 1   # 多头
PositionSide_Short = 2  # 空头
```

---

## order_volume - 按数量下单

```python
order_volume(symbol, volume, side, order_type, position_effect,
             price=0, account=None)
```

```python
# 市价买入200股
order_volume(symbol='SHSE.600000', volume=200, side=OrderSide_Buy,
             order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)

# 限价卖出100股
order_volume(symbol='SZSE.000001', volume=100, side=OrderSide_Sell,
             order_type=OrderType_Limit, position_effect=PositionEffect_Close, price=16.5)
```

---

## order_value - 按金额下单

```python
order_value(symbol, value, side, order_type, position_effect,
            price=0, account=None)
```

```python
# 买入10000元的股票
order_value(symbol='SHSE.600000', value=10000, side=OrderSide_Buy,
            order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)
```

---

## order_percent - 按账户总资产比例下单

```python
order_percent(symbol, percent, side, order_type, position_effect,
              price=0, account=None)
```

```python
# 买入账户总资产的1%
order_percent(symbol='SHSE.600000', percent=0.01, side=OrderSide_Buy,
              order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)
```

---

## order_target_volume - 调仓到目标数量

> 自动计算差值，决定买入或卖出

```python
order_target_volume(symbol, volume, position_side=PositionSide_Long,
                    order_type=OrderType_Market, price=0, account=None)
```

```python
# 调整到持有500股（多头）
order_target_volume(symbol='SHSE.600000', volume=500,
                    position_side=PositionSide_Long,
                    order_type=OrderType_Market)
```

---

## order_target_value - 调仓到目标金额

```python
order_target_value(symbol, value, position_side=PositionSide_Long,
                   order_type=OrderType_Market, price=0, account=None)
```

---

## order_target_percent - 调仓到目标比例

```python
order_target_percent(symbol, percent, position_side=PositionSide_Long,
                     order_type=OrderType_Market, price=0, account=None)
```

```python
# 调整到账户总资产的10%
order_target_percent(symbol='SHSE.600000', percent=0.1,
                     position_side=PositionSide_Long,
                     order_type=OrderType_Market)
```

---

## order_cancel - 撤销委托

```python
order_cancel(wait_cancel_orders, account=None)
```

```python
# 撤销指定委托
orders = get_orders()  # 先获取委托列表
order_cancel(wait_cancel_orders=orders)
```

---

## order_close_all - 一键平仓

```python
order_close_all()
```

- 平掉当前账户所有持仓

---

## 实用组合示例

```python
def on_bar(context, bars):
    bar = bars[0]
    symbol = bar['symbol']
    
    # 获取当前持仓
    pos = context.account().position(symbol=symbol, side=PositionSide_Long)
    
    # 无持仓时买入
    if not pos:
        cash = context.account().cash
        available = cash['available']
        if available > 10000:
            order_percent(symbol=symbol, percent=0.1, side=OrderSide_Buy,
                          order_type=OrderType_Market,
                          position_effect=PositionEffect_Open)
    else:
        # 已有持仓时全部卖出
        order_target_volume(symbol=symbol, volume=0,
                            position_side=PositionSide_Long,
                            order_type=OrderType_Market)
```
