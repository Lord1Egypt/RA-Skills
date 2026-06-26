# Language Mastery — Pine Script v5 & v6

Complete reference for production-grade Pine Script development.
Covers syntax, built-ins, common patterns, and critical gotchas.

---

## Script Declaration

### Indicator
```pine
//@version=5
indicator(
     title             = "My Indicator",
     shorttitle        = "MI",
     overlay           = true,          // true = on chart, false = separate pane
     max_bars_back     = 500,           // increase if "Index out of bounds" errors
     max_lines_count   = 500,
     max_labels_count  = 500,
     max_boxes_count   = 500,
     explicit_plot_zorder = true        // predictable z-order for plots
     )
```

### Strategy
```pine
//@version=5
strategy(
     title             = "My Strategy",
     shorttitle        = "MS",
     overlay           = true,
     initial_capital   = 10000,
     default_qty_type  = strategy.percent_of_equity,
     default_qty_value = 2,             // 2% per trade
     commission_type   = strategy.commission.percent,
     commission_value  = 0.05,          // 0.05% per side (realistic for crypto)
     slippage          = 2,             // 2 ticks slippage
     calc_on_every_tick= false,         // use false for accurate backtesting
     max_bars_back     = 500
     )
```

---

## Variable Declaration

```pine
// Simple assignment (reassignable with :=)
length = 14
src    = close

// Typed declaration
float myFloat = na
int   myInt   = 0
bool  myBool  = false
color myColor = color.blue

// var — persists across bars (only initialized once)
var float runningMax = 0.0
var int   tradeCount = 0

// varip — updates on every tick within a bar (real-time)
varip float tickHigh = 0.0

// Reassign with :=
myFloat := close * 1.5
```

---

## Inputs — Full Pattern Library

```pine
grp_main = "═══ Main Settings ═══"
grp_risk = "═══ Risk Management ═══"
grp_vis  = "═══ Visual ═══"

// Integer
length = input.int(14, "RSI Length",
     minval=2, maxval=100,
     tooltip="Period for RSI calculation. Lower = more sensitive, higher = smoother.",
     group=grp_main)

// Float
mult = input.float(1.5, "ATR Multiplier",
     minval=0.1, maxval=10.0, step=0.1,
     group=grp_risk)

// Boolean
use_filter = input.bool(true, "Enable Trend Filter",
     tooltip="When enabled, only takes signals in the direction of the trend.",
     group=grp_main)

// Source
src = input.source(close, "Source", group=grp_main)

// Timeframe
htf = input.timeframe("D", "Higher Timeframe", group=grp_main)

// Symbol
sym = input.symbol("BTCUSDT", "Symbol", group=grp_main)

// Color
bull_color = input.color(color.new(#26a69a, 0), "Bull Color", group=grp_vis)
bear_color = input.color(color.new(#ef5350, 0), "Bear Color", group=grp_vis)

// Dropdown
mode = input.string("Aggressive", "Mode",
     options=["Conservative", "Moderate", "Aggressive"],
     group=grp_main)
```

---

## Built-in Technical Analysis (ta namespace)

### Trend
```pine
ta.sma(src, length)           // Simple Moving Average
ta.ema(src, length)           // Exponential Moving Average
ta.wma(src, length)           // Weighted Moving Average
ta.vwma(src, length)          // Volume Weighted Moving Average
ta.hma(src, length)           // Hull Moving Average (smoother, less lag)
ta.alma(src, length, 0.85, 6) // Arnaud Legoux MA
ta.linreg(src, length, 0)     // Linear Regression
ta.supertrend(factor, atrLen) // Returns [supertrend, direction]
ta.dema(src, length)          // Double EMA
ta.tema(src, length)          // Triple EMA
```

### Momentum
```pine
ta.rsi(src, length)           // RSI — returns 0-100
ta.macd(src, fast, slow, sig) // Returns [macd, signal, histogram]
ta.stoch(close, high, low, k) // Stochastic %K — returns 0-100
ta.cci(src, length)           // Commodity Channel Index
ta.mom(src, length)           // Momentum (price change over length)
ta.roc(src, length)           // Rate of Change (%)
ta.mfi(hlc3, length)          // Money Flow Index (volume-weighted RSI)
```

### Volatility
```pine
ta.atr(length)                // Average True Range — key for dynamic SL/TP
ta.tr                         // True Range (single bar)
ta.bb(src, length, mult)      // Bollinger Bands — returns [upper, basis, lower]
ta.kc(src, length, mult)      // Keltner Channels — returns [upper, basis, lower]
ta.historical_volatility(src, length, ann) // Historical Volatility
```

### Volume
```pine
ta.obv                        // On-Balance Volume
ta.pvt                        // Price Volume Trend
ta.vwap                       // VWAP (session)
ta.vwap(src, anchor, stdev)  // VWAP with anchor and bands
```

### Structure
```pine
ta.highest(src, length)       // Highest value in last N bars
ta.lowest(src, length)        // Lowest value in last N bars
ta.highestbars(src, length)   // Bars since highest
ta.lowestbars(src, length)    // Bars since lowest
ta.pivothigh(src, left, right) // Pivot High (repaints — use carefully)
ta.pivotlow(src, left, right)  // Pivot Low (repaints — use carefully)
ta.crossover(a, b)            // True when a crosses above b
ta.crossunder(a, b)           // True when a crosses below b
ta.cross(a, b)                // True when either cross occurs
ta.valuewhen(cond, src, n)    // Value of src on nth most recent true condition
ta.barssince(cond)            // Bars since condition was last true
ta.cum(src)                   // Cumulative sum
ta.change(src, length)        // Change from N bars ago
```

### DMI / ADX
```pine
[diplus, diminus, adx] = ta.dmi(diLen, adxSmoothing)
// diplus > diminus = bullish, diminus > diplus = bearish
// adx > 25 = trending market
```

---

## Multi-Timeframe (MTF) Requests

### Correct MTF Pattern (No Lookahead Bias)
```pine
// CORRECT — no repainting
htf_close = request.security(syminfo.tickerid, "D", close,
     lookahead=barmerge.lookahead_off)

// CORRECT — request a calculation from higher TF
htf_ema  = request.security(syminfo.tickerid, "D",
     ta.ema(close, 50),
     lookahead=barmerge.lookahead_off)

// CORRECT — boolean condition from higher TF
htf_bull = request.security(syminfo.tickerid, "D",
     close > ta.ema(close, 200),
     lookahead=barmerge.lookahead_off)
```

### v6 Dynamic Requests (NEW — December 2024)
```pine
//@version=6
// Can now use series string — timeframe can change bar by bar
dynamic_tf = condition ? "D" : "W"
result = request.security(syminfo.tickerid, dynamic_tf, close)

// Can now call inside loops (v6 only)
for i = 0 to 4
    tf_data = request.security(syminfo.tickerid, timeframes.get(i), close)
```

### Minimize request.security() Calls
```pine
// WRONG — multiple calls for same symbol/TF
htf_high  = request.security(syminfo.tickerid, "D", high)
htf_low   = request.security(syminfo.tickerid, "D", low)
htf_close = request.security(syminfo.tickerid, "D", close)

// RIGHT — tuple return in one call
[htf_high, htf_low, htf_close] = request.security(syminfo.tickerid, "D",
     [high, low, close],
     lookahead=barmerge.lookahead_off)
```

---

## Plotting

### plot()
```pine
plot(value,
     title="My Line",
     color=color.new(color.blue, 0),
     linewidth=2,
     style=plot.style_line,        // line / circles / histogram / area / columns / cross / stepline
     display=display.all)          // all / none / data_window / status_line / pane_title

// Conditional color
plot(src,
     color=src > src[1] ? color.green : color.red)
```

### plotshape() — Signals on Chart
```pine
plotshape(long_signal,
     title="Long",
     style=shape.labelup,           // triangleup / labelup / arrowup / circle / flag / xcross
     location=location.belowbar,    // belowbar / abovebar / absolute
     color=color.new(color.green, 0),
     textcolor=color.white,
     text="L",
     size=size.small)               // tiny / small / normal / large / huge
```

### plotcandle() — Custom Candles
```pine
plotcandle(open, high, low, close,
     title="Custom Candles",
     color=close > open ? color.green : color.red,
     wickcolor=color.gray)
```

### bgcolor() — Background Highlights
```pine
bgcolor(condition ? color.new(color.green, 90) : na)
```

### Lines and Labels
```pine
// Persistent horizontal line
var line sl_line = na
if long_entry
    sl_line := line.new(bar_index, stop_price, bar_index + 50, stop_price,
         color=color.red, style=line.style_dashed, width=1)

// Label with price
label.new(bar_index, high,
     text="🎯 " + str.tostring(close, format.mintick),
     style=label.style_label_down,
     color=color.new(color.green, 20),
     textcolor=color.white,
     size=size.small)
```

---

## Strategy Functions

### Entries
```pine
strategy.entry("Long",  strategy.long,
     qty=qty_shares,           // optional — overrides default
     limit=price,              // limit order price
     stop=price,               // stop order price
     comment="Signal name")

strategy.entry("Short", strategy.short)
```

### Exits
```pine
// Full exit
strategy.close("Long", comment="Exit")

// Partial exit
strategy.close("Long", qty_percent=50, comment="TP1 — 50%")

// Exit with SL/TP
strategy.exit("Long Exit", "Long",
     qty_percent=100,
     stop=sl_price,
     limit=tp_price,
     trail_price=trail_activation,    // price where trailing activates
     trail_offset=trail_ticks,        // trail distance in ticks
     comment="SL/TP")

// Close all
strategy.close_all(comment="Close All")
```

### Position Info
```pine
strategy.position_size          // current position (+ = long, - = short, 0 = flat)
strategy.position_avg_price     // average entry price
strategy.equity                 // current equity
strategy.netprofit              // net profit
strategy.openprofit             // open trade P&L
strategy.grossprofit            // total gross profit
strategy.grossloss              // total gross loss
strategy.wintrades              // winning trades count
strategy.losstrades             // losing trades count
strategy.closedtrades           // total closed trades
```

---

## Arrays and Matrices

```pine
// Create
arr = array.new_float(0)

// Add / remove
array.push(arr, value)
array.pop(arr)
array.shift(arr)               // remove first element
array.unshift(arr, value)      // add to beginning
array.insert(arr, index, value)
array.remove(arr, index)

// Read
array.get(arr, index)
array.size(arr)
array.first(arr)
array.last(arr)

// Math
array.max(arr)
array.min(arr)
array.sum(arr)
array.avg(arr)
array.stdev(arr)

// Sort
array.sort(arr, order.ascending)
array.sort(arr, order.descending)
```

---

## Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `Cannot call 'plot' in local scope` | plot() inside if/for block | Move plot() to global scope, use na conditionally |
| `Index -1 out of bounds` | Accessing history before bar 0 | Add `max_bars_back = 500` to indicator() |
| `Security context error` | Using alert() inside request.security() | Move alert outside request |
| `Repainting` | Future data leaking into past | Add `lookahead=barmerge.lookahead_off` |
| `Variable 'X' already declared` | Using = twice | Use := for reassignment |
| `Loop is too slow` | Heavy calculation inside loop | Pre-calculate outside loop, use array operations |
| `Cannot modify read-only var` | Trying to change built-in | Assign to a new variable first |

---

## Performance Optimization

```pine
// SLOW — recalculates every bar
slowFn() =>
    sum = 0.0
    for i = 0 to 100
        sum += close[i]
    sum

// FAST — use built-in
ta.sum(close, 100)

// AVOID — calling request.security() in loops
// USE — request outside loop, access array inside

// AVOID — re-creating objects every bar
// USE — var to persist objects

// AVOID — complex calculations when not needed
// USE — barstate.islast for single-bar calculations (dashboard, etc.)
```
