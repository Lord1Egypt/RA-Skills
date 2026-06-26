# Order Types Reference

## Basic Orders

```python
from ib_insync import MarketOrder, LimitOrder, StopOrder, StopLimitOrder

# Market order
order = MarketOrder("BUY", 100)

# Limit order
order = LimitOrder("BUY", 100, lmtPrice=150.00)

# Stop (stop-market)
order = StopOrder("SELL", 100, stopPrice=145.00)

# Stop-limit
order = StopLimitOrder("SELL", 100, lmtPrice=144.50, stopPrice=145.00)
```

## Bracket Orders (Recommended Pattern)

Bracket = Entry + Take Profit + Stop Loss, linked by parentId.
All three are placed atomically.

```python
from ib_insync import IB, Stock, LimitOrder, StopOrder

def place_bracket(ib, symbol, qty, entry, target, stop, direction="LONG"):
    contract = Stock(symbol, "SMART", "USD")
    ib.qualifyContracts(contract)

    action = "BUY" if direction == "LONG" else "SELL"
    close = "SELL" if direction == "LONG" else "BUY"

    # Parent entry order
    parent = LimitOrder(action, qty, entry)
    parent.transmit = False  # Don't send yet

    # Take profit (limit)
    tp = LimitOrder(close, qty, target)
    tp.parentId = parent.orderId
    tp.transmit = False

    # Stop loss (stop-market)
    sl = StopOrder(close, qty, stop)
    sl.parentId = parent.orderId
    sl.transmit = True  # Transmits all three

    parent_trade = ib.placeOrder(contract, parent)
    tp_trade = ib.placeOrder(contract, tp)
    sl_trade = ib.placeOrder(contract, sl)

    return parent_trade, tp_trade, sl_trade
```

## Trailing Stop

```python
from ib_insync import Order

trailing_stop = Order()
trailing_stop.action = "SELL"
trailing_stop.totalQuantity = 100
trailing_stop.orderType = "TRAIL"
trailing_stop.trailingPercent = 2.0   # 2% trailing
# OR: trailing_stop.auxPrice = 3.00  # Fixed dollar trail
trailing_stop.transmit = True
```

## OCO (One-Cancels-Other)

```python
# Both orders get the same OCA group name
tp = LimitOrder("SELL", 100, target)
tp.ocaGroup = "OCA_AAPL_001"
tp.ocaType = 1  # Cancel remaining with block

sl = StopOrder("SELL", 100, stop)
sl.ocaGroup = "OCA_AAPL_001"
sl.ocaType = 1
```

## Modifying an Order

```python
# Retrieve the order from open trades
for trade in ib.openTrades():
    if trade.order.orderId == target_id:
        trade.order.lmtPrice = new_price  # or auxPrice for stops
        ib.placeOrder(trade.contract, trade.order)  # Re-place to modify
        break
```

## Cancelling an Order

```python
for trade in ib.openTrades():
    if trade.order.orderId == target_id:
        ib.cancelOrder(trade.order)
        break
```

## Checking Fill Status

```python
trade = ib.placeOrder(contract, order)
ib.sleep(2)
print(trade.orderStatus.status)
# Possible: "Submitted", "PreSubmitted", "Filled", "Cancelled", "Inactive"
```

## Handling Partial Fills

```python
trade = ib.placeOrder(contract, order)
ib.sleep(2)
filled = trade.orderStatus.filled
remaining = trade.orderStatus.remaining
avg_fill_price = trade.orderStatus.avgFillPrice
```
