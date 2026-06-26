# Strategy Design — Architecture & Signal Logic

Professional trading strategy design methodology for Pine Script.

---

## The Strategy Design Process

Never start with code. Start with these questions:

### 1. What is the edge?
The strategy must exploit a specific, repeatable market inefficiency.
Common edges:
- **Momentum**: Markets that move tend to keep moving
- **Mean reversion**: Prices that deviate from equilibrium tend to return
- **Breakout**: Price escaping from consolidation often continues
- **Pattern**: Specific price formations have predictive value
- **Flow**: Volume/order flow precedes price movement

### 2. What market conditions does it work in?
Every strategy has ideal conditions and conditions where it fails.
Define both before writing a line of code.

### 3. What is the signal stack?
A robust strategy uses multiple confirming signals, not a single indicator.

---

## Signal Stack Architecture

### Tier Structure
```
TIER 1 — Market Regime (Macro Context)
  Is this a trending or ranging market?
  Is volatility high or low?
  What direction is the dominant trend?
  → Use: ADX, ATR percentile, Supertrend, 200 EMA

TIER 2 — Setup (Condition to Watch)
  Price approaching a key level?
  Indicator in oversold/overbought zone?
  Structure forming?
  → Use: Support/Resistance, RSI extremes, Bollinger Band squeeze

TIER 3 — Trigger (Entry Signal)
  The actual entry event — must be specific and unambiguous
  → Use: Crossovers, candle closes above/below, volume spike

TIER 4 — Confirmation (Reduce False Signals)
  Secondary evidence that validates the trigger
  → Use: Volume, divergence, second indicator alignment
```

### Example Signal Stack — Trend Following System
```
T1 Regime   : ADX > 25 (trending market confirmed)
              Price > EMA(200) for longs only
T2 Setup    : RSI pulled back to 40-50 zone (not overbought)
T3 Trigger  : EMA(9) crosses above EMA(21)
T4 Confirm  : Volume above 20-bar average
```

### Example Signal Stack — Mean Reversion System
```
T1 Regime   : ADX < 20 (ranging market confirmed)
              Price within Bollinger Bands
T2 Setup    : Price touches lower BB (for longs)
T3 Trigger  : RSI crosses above 30 (from oversold)
T4 Confirm  : Bullish candle close on trigger bar
```

---

## Entry Logic Patterns

### Pattern 1 — Crossover Entry
```pine
// Fast EMA crosses above slow EMA
bull_cross  = ta.crossover(ta.ema(close, 9), ta.ema(close, 21))
bear_cross  = ta.crossunder(ta.ema(close, 9), ta.ema(close, 21))

long_entry  = bull_cross and adx > 20 and close > ema200
short_entry = bear_cross and adx > 20 and close < ema200
```

### Pattern 2 — Zone Bounce Entry
```pine
// RSI bouncing from oversold with price at support
[upper, basis, lower] = ta.bb(close, 20, 2)
rsi = ta.rsi(close, 14)

at_support  = low <= lower
rsi_bounce  = ta.crossover(rsi, 30)
long_entry  = at_support and rsi_bounce
```

### Pattern 3 — Breakout Entry
```pine
// Price breaking above N-bar high with volume confirmation
n = 20
breakout_level = ta.highest(high, n)[1]  // [1] = previous bar's value (no repaint)
vol_confirm    = volume > ta.sma(volume, 20) * 1.5

long_entry = close > breakout_level and vol_confirm
```

### Pattern 4 — Multi-Timeframe Entry
```pine
// Higher TF trend filter + lower TF entry signal
htf_bull = request.security(syminfo.tickerid, "4H",
     ta.ema(close, 50) > ta.ema(close, 200),
     lookahead=barmerge.lookahead_off)

ltf_entry = ta.crossover(ta.rsi(close, 14), 50)

long_entry = htf_bull and ltf_entry
```

### Pattern 5 — Divergence Entry
```pine
// Price makes lower low but RSI makes higher low = bullish divergence
rsi = ta.rsi(close, 14)
pl_price = ta.pivotlow(low, 5, 5)
pl_rsi   = ta.pivotlow(rsi, 5, 5)

// Track recent pivot values
var float prev_price_pivot = na
var float prev_rsi_pivot   = na

if not na(pl_price)
    bull_div = low < prev_price_pivot and rsi > prev_rsi_pivot
    prev_price_pivot := low
    prev_rsi_pivot   := rsi
```

---

## Exit Logic Systems

### System 1 — Fixed ATR Exits (Most Common)
```pine
atr_val  = ta.atr(14)
entry_px = strategy.position_avg_price

sl_long  = entry_px - atr_val * sl_mult
tp1_long = entry_px + atr_val * tp1_mult
tp2_long = entry_px + atr_val * tp2_mult

// Partial exit at TP1, full exit at TP2
strategy.exit("TP1", "Long", qty_percent=50, limit=tp1_long, stop=sl_long)
strategy.exit("TP2", "Long", qty_percent=100, limit=tp2_long, stop=sl_long)
```

### System 2 — Trailing Stop
```pine
// Trail activates after TP1, trails by ATR distance
strategy.exit("Trail", "Long",
     trail_price  = tp1_long,              // activate when price hits TP1
     trail_offset = atr_val * trail_mult / syminfo.mintick)  // trail distance in ticks
```

### System 3 — Indicator-Based Exit
```pine
// Exit when RSI becomes overbought (for momentum strategy)
rsi = ta.rsi(close, 14)
exit_signal = rsi > 70 and strategy.position_size > 0
if exit_signal
    strategy.close("Long", comment="RSI Exit")
```

### System 4 — Time-Based Exit
```pine
// Exit after N bars if still in trade
bars_in_trade = ta.barssince(long_entry)
time_exit     = bars_in_trade >= max_bars_in_trade

if time_exit and strategy.position_size > 0
    strategy.close("Long", comment="Time Exit")
```

### System 5 — Composite Exit (Professional)
```pine
// Exit on ANY of: SL hit, TP hit, signal reversal, time limit
sl_hit      = low < sl_long
tp_hit      = high > tp2_long
reversal    = short_signal
time_limit  = ta.barssince(long_entry) >= 20

any_exit = sl_hit or tp_hit or reversal or time_limit
```

---

## Filter Systems

### Trend Filter
```pine
ema200      = ta.ema(close, 200)
above_trend = close > ema200    // only longs
below_trend = close < ema200    // only shorts

[_, _, adx] = ta.dmi(14, 14)
trending    = adx > 25          // strong trend present
```

### Volatility Filter
```pine
atr     = ta.atr(14)
atr_avg = ta.sma(atr, 50)

// Only trade when volatility is normal (not too low, not too high)
vol_ok = atr > atr_avg * 0.5 and atr < atr_avg * 2.0
```

### Volume Filter
```pine
vol_avg    = ta.sma(volume, 20)
vol_ok     = volume > vol_avg * 1.2    // at least 20% above average
```

### Session Filter
```pine
// Only trade during specific sessions (London + NY)
is_london  = not na(time(timeframe.period, "0800-1600", "Europe/London"))
is_new_york= not na(time(timeframe.period, "0930-1600", "America/New_York"))
in_session = is_london or is_new_york
```

### Drawdown Filter (Emergency Stop)
```pine
// Stop trading if drawdown exceeds threshold
peak_equity = 0.0
peak_equity := math.max(peak_equity, strategy.equity)
current_dd  = (peak_equity - strategy.equity) / peak_equity * 100
dd_ok       = current_dd < max_dd_pct    // e.g., 15%
```

---

## Backtesting Integrity Rules

### Rule 1 — Realistic Commission & Slippage
Always include. For crypto: 0.05-0.1% commission, 1-3 ticks slippage.
For forex: 1-3 pip spread equivalent. Without these, results are fantasy.

### Rule 2 — No Lookahead Bias
Never use future information. Every entry must be based on
the close of the signal bar (or confirmed on next bar open).

```pine
// WRONG — executes on same candle as signal
if crossover_signal
    strategy.entry("Long", strategy.long)

// RIGHT — execute on next bar open to avoid lookahead
if crossover_signal[1]
    strategy.entry("Long", strategy.long)
```

### Rule 3 — Sufficient Sample Size
Minimum 100 trades for statistical significance.
Under 50 trades = not enough data, regardless of win rate.

### Rule 4 — Out-of-Sample Validation
Optimize on 70% of data. Test on remaining 30% without touching.
If performance degrades dramatically on OOS data = overfitting.

### Rule 5 — Walk-Forward Analysis
Split data into rolling windows. Optimize on each window.
Test on next window. Average results. This is the gold standard.

### Rule 6 — Realistic Expectations
```
Good edge characteristics:
Win rate     : 45-65% (higher = often overfit)
Profit factor: >1.5 (gross profit / gross loss)
Max drawdown : <20% of capital
Sharpe ratio : >1.0
R:R ratio    : >1.5:1

Red flags:
Win rate > 75%     → likely curve-fitted
Profit factor > 5  → likely not realistic
Drawdown < 5%      → suspiciously good
< 50 trades        → insufficient data
```

---

## Strategy Template — Full Production Structure

```pine
//@version=5
strategy(
     title             = "Strategy Name v1.0",
     shorttitle        = "SN",
     overlay           = true,
     initial_capital   = 10000,
     default_qty_type  = strategy.percent_of_equity,
     default_qty_value = 2,
     commission_type   = strategy.commission.percent,
     commission_value  = 0.05,
     slippage          = 2,
     calc_on_every_tick= false,
     max_bars_back     = 500
     )

// ─── INPUTS ────────────────────────────────────────
grp_sig  = "Signal Settings"
grp_risk = "Risk Management"
grp_filt = "Filters"

// Signal inputs here...

// ─── CALCULATIONS ──────────────────────────────────
// Core indicator calculations...

// ─── FILTERS ───────────────────────────────────────
// Trend, volume, session, drawdown filters...

// ─── SIGNALS ───────────────────────────────────────
long_signal  = /* conditions */ and filter_1 and filter_2
short_signal = /* conditions */ and filter_1 and filter_2

// ─── RISK MANAGEMENT ───────────────────────────────
atr     = ta.atr(atr_len)
sl_dist = atr * sl_mult
tp_dist = atr * tp_mult

// ─── ENTRIES ───────────────────────────────────────
if long_signal and strategy.position_size == 0
    strategy.entry("Long", strategy.long, comment="L")

if short_signal and strategy.position_size == 0
    strategy.entry("Short", strategy.short, comment="S")

// ─── EXITS ─────────────────────────────────────────
long_sl  = strategy.position_avg_price - sl_dist
long_tp  = strategy.position_avg_price + tp_dist
short_sl = strategy.position_avg_price + sl_dist
short_tp = strategy.position_avg_price - tp_dist

if strategy.position_size > 0
    strategy.exit("Long Exit", "Long", stop=long_sl, limit=long_tp)

if strategy.position_size < 0
    strategy.exit("Short Exit", "Short", stop=short_sl, limit=short_tp)

// ─── VISUALS ───────────────────────────────────────
// Plots, shapes, lines, dashboard...

// ─── ALERTS ────────────────────────────────────────
alertcondition(long_signal  and barstate.isconfirmed, "Long",  "Long Signal — {{ticker}}")
alertcondition(short_signal and barstate.isconfirmed, "Short", "Short Signal — {{ticker}}")
```
