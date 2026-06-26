# Risk Management Patterns

## ATR-Based Stop Loss
```pine
atrVal = ta.atr(14)
slLong = close - atrVal * 1.5
slShort = close + atrVal * 1.5
```

## Swing-Based Stop Loss
```pine
swingLow = ta.lowest(low, 10)
swingHigh = ta.highest(high, 10)
slLong = swingLow
slShort = swingHigh
```

## Hybrid SL (Tighter of ATR or Swing)
```pine
slLong = math.max(close - atrVal * 1.5, swingLow)
slShort = math.min(close + atrVal * 1.5, swingHigh)
```

## Risk:Reward TP Calculation
```pine
slDist = close - slLong
tpLong = close + slDist * rrRatio  // rrRatio = 1.5, 2.0, etc.
```

## Partial Position Exit (Split TP)
```pine
tp1 = close + slDist * 1.0  // 1R
tp2 = close + slDist * 2.0  // 2R

strategy.entry("Long", strategy.long)
strategy.exit("TP1", "Long", qty_percent=50, limit=tp1, stop=slLong)
strategy.exit("TP2", "Long", limit=tp2, stop=slLong)
```

## Break-Even After TP1
```pine
var float entryPrice = 0.0
if strategy.position_size == 0
    entryPrice := close

if strategy.position_size > 0 and close >= tp1
    strategy.exit("BE", "Long", stop=entryPrice, limit=tp2)
```

## Trailing Stop (ATR-based)
```pine
var float trailStop = na
if strategy.position_size > 0
    trailStop := math.max(nz(trailStop, slLong), close - atrVal * 2.0)
    strategy.exit("Trail", "Long", stop=trailStop)
```

## Trailing Stop (Parabolic SAR)
```pine
sar = ta.sar(0.02, 0.02, 0.2)
strategy.exit("Trail", "Long", stop=sar)
```

## Cool-off After Loss
```pine
var int barsSinceLoss = 999
if strategy.closedtrades > 0
    if strategy.closedtrades.profit(strategy.closedtrades - 1) < 0
        barsSinceLoss := 0
barsSinceLoss += 1
coolOffOK = barsSinceLoss > 5
```

## Max Trades Per Day
```pine
var int tradesToday = 0
var int lastTradeDate = na
currentDate = dayofmonth
if currentDate != nz(lastTradeDate, -1)
    tradesToday := 0
    lastTradeDate := currentDate

if <entry_condition> and tradesToday < 3
    tradesToday += 1
    strategy.entry(...)
```

## Max Daily Loss
```pine
var float dailyPnL = 0.0
var int currentDay = na
if dayofmonth != nz(currentDay, -1)
    dailyPnL := 0.0
    currentDay := dayofmonth

if strategy.closedtrades > 0 and barstate.isconfirmed
    dailyPnL += strategy.closedtrades.profit(strategy.closedtrades - 1)

maxDailyLoss = dailyPnL < -maxLossAmount
if maxDailyLoss
    strategy.close_all()
```

## Position Sizing (Risk-Based)
```pine
riskPct = 2.0  // 2% risk per trade
riskAmount = strategy.equity * riskPct / 100
slDistance = close - slLong
qty = slDistance > 0 ? riskAmount / slDistance : 0
strategy.entry("Long", strategy.long, qty=qty)
```
