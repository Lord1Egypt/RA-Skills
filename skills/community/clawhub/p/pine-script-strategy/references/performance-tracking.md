# Performance Tracking

## Win Rate Counter
```pine
var int totalTrades = 0
var int wins = 0
var float totalPnL = 0.0

if strategy.closedtrades > 0 and barstate.isconfirmed
    lastPnL = strategy.closedtrades.profit(strategy.closedtrades - 1)
    totalTrades += 1
    if lastPnL > 0
        wins += 1
    totalPnL += lastPnL

winRate = totalTrades > 0 ? wins / totalTrades * 100 : 0
```

## Drawdown Tracking
```pine
var float peak = 0.0
var float maxDD = 0.0
equity = strategy.equity
if equity > peak
    peak := equity
dd = peak > 0 ? (peak - equity) / peak * 100 : 0
if dd > maxDD
    maxDD := dd
```

## Performance Table
```pine
var table perfTable = table.new(position.bottom_right, 2, 6,
     bgcolor=color.new(color.black, 80), border_color=color.new(color.gray, 70))

if barstate.islast
    table.cell(perfTable, 0, 0, "Win Rate", text_color=color.gray, text_size=size.tiny)
    table.cell(perfTable, 1, 0, str.tostring(winRate, "#.1") + "%", text_color=winRate > 50 ? color.lime : color.red, text_size=size.tiny)
    table.cell(perfTable, 0, 1, "Total Trades", text_color=color.gray, text_size=size.tiny)
    table.cell(perfTable, 1, 1, str.tostring(totalTrades), text_color=color.white, text_size=size.tiny)
    table.cell(perfTable, 0, 2, "Max DD", text_color=color.gray, text_size=size.tiny)
    table.cell(perfTable, 1, 2, str.tostring(maxDD, "#.1") + "%", text_color=color.red, text_size=size.tiny)
    table.cell(perfTable, 0, 3, "Net P&L", text_color=color.gray, text_size=size.tiny)
    table.cell(perfTable, 1, 3, str.tostring(totalPnL, "#.2"), text_color=totalPnL > 0 ? color.lime : color.red, text_size=size.tiny)
    table.cell(perfTable, 0, 4, "Profit Factor", text_color=color.gray, text_size=size.tiny)
    pf = strategy.grossloss != 0 ? math.abs(strategy.grossprofit / strategy.grossloss) : 0
    table.cell(perfTable, 1, 4, str.tostring(pf, "#.2"), text_color=pf > 1.3 ? color.lime : color.red, text_size=size.tiny)
```

## Consecutive Loss Tracking
```pine
var int consecLoss = 0
var int maxConsecLoss = 0

if strategy.closedtrades > 0 and barstate.isconfirmed
    lastPnL = strategy.closedtrades.profit(strategy.closedtrades - 1)
    if lastPnL < 0
        consecLoss += 1
        maxConsecLoss := math.max(maxConsecLoss, consecLoss)
    else
        consecLoss := 0
```

## Trade Duration Tracking
```pine
var int entryBar = na
if strategy.position_size != 0 and strategy.position_size[1] == 0
    entryBar := bar_index

if strategy.position_size == 0 and strategy.position_size[1] != 0
    tradeDuration = bar_index - nz(entryBar, bar_index)
```
