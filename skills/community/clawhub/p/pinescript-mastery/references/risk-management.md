# Risk Management — Position Sizing, SL/TP & Drawdown Control

Professional risk management for Pine Script strategies.

---

## The Cardinal Rules

1. **Never risk more than 1-2% of equity per trade**
2. **Always define SL before entry — no exceptions**
3. **Risk:Reward must be at least 1:1.5. Aim for 1:2+**
4. **Drawdown above 15% = pause and review the system**
5. **Correlation kills — don't run 5 strategies on correlated assets**

---

## Position Sizing Methods

### Method 1 — Fixed Percent of Equity (Simplest)
```pine
risk_pct    = input.float(1.0, "Risk per Trade %",
     minval=0.1, maxval=5.0, step=0.1, group="Risk")

// Size is set in strategy() declaration:
// default_qty_type = strategy.percent_of_equity
// default_qty_value = 1.0
// This risks 1% of equity per trade
```

### Method 2 — ATR-Based Sizing (Professional Standard)
```pine
// Risk exactly N% of equity based on ATR stop distance
risk_pct    = input.float(1.0, "Risk per Trade %", group="Risk")
sl_mult     = input.float(1.5, "SL ATR Multiplier", group="Risk")
atr_len     = input.int(14, "ATR Length", group="Risk")

atr_val     = ta.atr(atr_len)
sl_distance = atr_val * sl_mult

// Dollar risk per trade
dollar_risk = strategy.equity * (risk_pct / 100)

// Shares/units = dollar risk / distance to stop
qty         = dollar_risk / (sl_distance * syminfo.pointvalue)

if long_signal
    strategy.entry("Long", strategy.long, qty=qty)
    strategy.exit("Long Exit", "Long",
         stop  = close - sl_distance,
         limit = close + sl_distance * rr_ratio)
```

### Method 3 — Kelly Criterion (Advanced — Use with Caution)
```pine
// Kelly fraction = (W * R - L) / R
// W = win rate, L = loss rate, R = average win/loss ratio
// Use half-Kelly (divide by 2) for real trading — full Kelly is too aggressive

float total_trades  = strategy.closedtrades
float wins          = strategy.wintrades
float losses        = strategy.losstrades

win_rate    = wins / math.max(total_trades, 1)
loss_rate   = losses / math.max(total_trades, 1)
avg_win     = strategy.grossprofit / math.max(wins, 1)
avg_loss    = math.abs(strategy.grossloss) / math.max(losses, 1)
rr          = avg_win / math.max(avg_loss, 1)

kelly       = (win_rate * rr - loss_rate) / rr
half_kelly  = kelly / 2  // use this — safer

// Cap at 5% regardless of Kelly output
safe_size   = math.min(half_kelly * 100, 5.0)
```

### Method 4 — Volatility-Scaled Sizing
```pine
// Scale position size inversely to current volatility
// High volatility → smaller position, Low volatility → larger position
target_vol  = input.float(2.0, "Target Volatility %", group="Risk")

current_vol = ta.stdev(close / close[1] - 1, 20) * 100 * math.sqrt(252)
vol_scalar  = target_vol / math.max(current_vol, 0.01)
adj_size    = math.min(base_size * vol_scalar, max_size)  // cap at max
```

---

## Stop Loss Systems

### Type 1 — Fixed ATR Stop (Standard)
```pine
atr     = ta.atr(14)
sl_pct  = input.float(1.5, "SL ATR Multiplier")

long_sl  = strategy.position_avg_price - atr * sl_pct
short_sl = strategy.position_avg_price + atr * sl_pct
```

### Type 2 — Structure Stop (Most Logical)
```pine
// SL just below recent swing low (for longs)
lookback  = input.int(10, "Swing Lookback")
swing_low = ta.lowest(low, lookback)
buffer    = ta.atr(14) * 0.3  // small buffer below swing

long_sl   = swing_low - buffer
```

### Type 3 — Trailing Stop
```pine
// Manual trailing stop implementation
var float trail_stop = na

if strategy.position_size > 0
    trail_stop := na(trail_stop) ?
         strategy.position_avg_price - ta.atr(14) * trail_mult :
         math.max(trail_stop, close - ta.atr(14) * trail_mult)

    if low < trail_stop
        strategy.close("Long", comment="Trail Hit")
```

### Type 4 — Chandelier Exit
```pine
// Trail from highest high since entry
var float entry_bar_high = na
var float chandelier_stop = na

if long_entry
    entry_bar_high  := high
    chandelier_stop := high - ta.atr(14) * chandelier_mult

if strategy.position_size > 0
    entry_bar_high  := math.max(entry_bar_high, high)
    chandelier_stop := entry_bar_high - ta.atr(14) * chandelier_mult

    if close < chandelier_stop
        strategy.close("Long", comment="Chandelier")
```

### Type 5 — Breakeven Stop (Move to Cost)
```pine
// Move SL to breakeven after price reaches R1
var float sl_price = na
var bool  be_moved = false

if long_entry
    sl_price := close - ta.atr(14) * sl_mult
    be_moved := false

if strategy.position_size > 0 and not be_moved
    r1_reached = high >= strategy.position_avg_price + ta.atr(14) * sl_mult
    if r1_reached
        sl_price := strategy.position_avg_price  // move to entry price
        be_moved := true
```

---

## Take Profit Systems

### Single Target
```pine
tp = strategy.position_avg_price + ta.atr(14) * tp_mult
strategy.exit("Exit", "Long", limit=tp)
```

### Scaled Exit (Professional)
```pine
// 50% at TP1, 50% at TP2
tp1 = strategy.position_avg_price + atr * 1.5
tp2 = strategy.position_avg_price + atr * 3.0

strategy.exit("TP1", "Long", qty_percent=50, limit=tp1,
     stop=sl, comment="TP1")
strategy.exit("TP2", "Long", qty_percent=100, limit=tp2,
     trail_offset=atr * 0.5 / syminfo.mintick, comment="TP2+Trail")
```

### Dynamic R:R Target
```pine
rr_ratio = input.float(2.0, "Risk:Reward Ratio")
sl_dist  = math.abs(close - sl_price)
tp_price = close + sl_dist * rr_ratio  // always maintains target RR
```

---

## Drawdown Control System

```pine
// ─── DRAWDOWN MONITOR ─────────────────────────────
max_dd_pct = input.float(15.0, "Max Drawdown % to Halt Trading",
     minval=5.0, maxval=50.0, step=0.5, group="Risk")

var float peak_equity = strategy.initial_capital
peak_equity := math.max(peak_equity, strategy.equity)

current_dd  = (peak_equity - strategy.equity) / peak_equity * 100
dd_breached = current_dd >= max_dd_pct

// Stop all trading when max DD hit
trading_ok  = not dd_breached

// Apply to all entry conditions
final_long  = long_signal  and trading_ok
final_short = short_signal and trading_ok

// Close open positions if DD breached
if dd_breached and strategy.position_size != 0
    strategy.close_all(comment="Max DD Protection")
```

---

## Risk Metrics Dashboard

```pine
// Display live risk metrics in a table
var table risk_table = table.new(position.bottom_right, 2, 6,
     bgcolor=color.new(color.black, 80),
     border_color=color.new(color.gray, 50), border_width=1)

if barstate.islast
    float win_rate_pct = strategy.wintrades /
         math.max(strategy.closedtrades, 1) * 100

    float pf = strategy.grossprofit /
         math.max(math.abs(strategy.grossloss), 1)

    // Headers
    table.cell(risk_table, 0, 0, "Metric",
         text_color=color.gray, text_size=size.small)
    table.cell(risk_table, 1, 0, "Value",
         text_color=color.gray, text_size=size.small)

    // Win Rate
    table.cell(risk_table, 0, 1, "Win Rate",
         text_color=color.gray, text_size=size.small)
    table.cell(risk_table, 1, 1,
         str.tostring(win_rate_pct, "#.##") + "%",
         text_color=win_rate_pct > 50 ? color.green : color.red,
         text_size=size.small)

    // Profit Factor
    table.cell(risk_table, 0, 2, "Profit Factor",
         text_color=color.gray, text_size=size.small)
    table.cell(risk_table, 1, 2,
         str.tostring(pf, "#.##"),
         text_color=pf > 1.5 ? color.green : color.orange,
         text_size=size.small)

    // Drawdown
    table.cell(risk_table, 0, 3, "Drawdown",
         text_color=color.gray, text_size=size.small)
    table.cell(risk_table, 1, 3,
         str.tostring(current_dd, "#.##") + "%",
         text_color=current_dd < 10 ? color.green :
                    current_dd < max_dd_pct ? color.orange : color.red,
         text_size=size.small)

    // Trades
    table.cell(risk_table, 0, 4, "Trades",
         text_color=color.gray, text_size=size.small)
    table.cell(risk_table, 1, 4,
         str.tostring(strategy.closedtrades),
         text_color=color.white, text_size=size.small)

    // Status
    table.cell(risk_table, 0, 5, "Status",
         text_color=color.gray, text_size=size.small)
    table.cell(risk_table, 1, 5,
         trading_ok ? "✓ Active" : "✗ Halted",
         text_color=trading_ok ? color.green : color.red,
         text_size=size.small)
```
