# Visuals & Alerts

## Buy/Sell Labels
```pine
plotshape(buyCond, style=shape.labelup, location=location.belowbar,
     color=color.lime, text="BUY", textcolor=color.white, size=size.small)
plotshape(sellCond, style=shape.labeldown, location=location.abovebar,
     color=color.red, text="SELL", textcolor=color.white, size=size.small)
```

## TP/SL Boxes
```pine
var box tpBox = na
var box slBox = na
if buyCond and barstate.isconfirmed
    tpBox := box.new(bar_index, tp, bar_index + 10, entry,
         border_color=color.new(color.lime, 40), bgcolor=color.new(color.lime, 88))
    slBox := box.new(bar_index, entry, bar_index + 10, sl,
         border_color=color.new(color.red, 40), bgcolor=color.new(color.red, 88))
```

## Score Label
```pine
if buyCond and barstate.isconfirmed
    label.new(bar_index, low, str.tostring(score) + "%",
         style=label.style_label_up, color=color.lime, textcolor=color.black, size=size.small)
```

## Info Table (Top Right)
```pine
var table t = table.new(position.top_right, 2, 5,
     bgcolor=color.new(color.black, 70), border_color=color.new(color.gray, 60))
if barstate.isconfirmed
    table.cell(t, 0, 0, "Trend", text_color=color.gray, text_size=size.tiny)
    table.cell(t, 1, 0, "Bull", text_color=color.lime, text_size=size.tiny)
```

## Zone Background
```pine
bgcolor(highProb ? color.new(color.lime, 95) : na)
```

## EMA Color Fill
```pine
p1 = plot(ema9, color=color.lime, linewidth=1)
p2 = plot(ema21, color=color.orange, linewidth=1)
fill(p1, p2, color=color.new(color.lime, 90))
```

## Alert Conditions
```pine
alertcondition(buyCond, title="Buy Signal",
     message="🟢 BUY | Score: {{plot_0}}% | Price: {{close}}")

alertcondition(sellCond, title="Sell Signal",
     message="🔴 SELL | Score: {{plot_0}}% | Price: {{close}}")

alertcondition(exitCond, title="Exit Signal",
     message="🚪 EXIT | Price: {{close}}")
```

## Movement % (Live P&L)
```pine
if strategy.position_size != 0
    movePct = strategy.position_size > 0 ?
         ((close - strategy.position_avg_price) / strategy.position_avg_price) * 100 :
         ((strategy.position_avg_price - close) / strategy.position_avg_price) * 100
```

## Clean Plot Styling
```pine
plot(ema9, "EMA 9", color=color.new(color.lime, 0), linewidth=2)
plot(ema50, "EMA 50", color=color.new(color.orange, 0), linewidth=2)
plot(ema200, "EMA 200", color=color.new(color.red, 0), linewidth=3)
```

## Hline for Key Levels
```pine
hline(0, "Zero", color=color.gray, linestyle=hline.style_dotted)
```
