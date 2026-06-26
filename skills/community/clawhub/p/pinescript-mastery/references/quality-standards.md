# Quality Standards — Code Structure, Anti-Patterns & Publication

Every Pine Script output must meet these standards before delivery.

---

## Code Structure Template

Every script follows this exact section order:

```pine
// ============================================================
// SCRIPT NAME — Short Description
// ============================================================
// Author      : [name]
// Version     : v1.0
// Pine Script : v5
// Description :
//   [What this script does in 2-3 sentences]
//   [What makes it useful / different]
//   [How to use it — brief]
// ============================================================

//@version=5
indicator("Script Name", shorttitle="SN", overlay=true)

// ─── INPUT GROUPS ──────────────────────────────────
// All inputs, organized by group

// ─── CONSTANTS ─────────────────────────────────────
// Named constants instead of magic numbers

// ─── CORE CALCULATIONS ─────────────────────────────
// Primary calculations

// ─── SIGNAL LOGIC ──────────────────────────────────
// Entry/exit conditions

// ─── RISK MANAGEMENT ───────────────────────────────
// SL/TP/sizing calculations

// ─── PLOTS & VISUALS ───────────────────────────────
// All plots, shapes, lines, labels, tables

// ─── ALERTS ────────────────────────────────────────
// All alertcondition() declarations
```

---

## Naming Conventions

```pine
// Variables: camelCase
fastEma    = ta.ema(close, fast_len)
isBullish  = close > open

// Constants: UPPER_SNAKE_CASE
MAX_BARS   = 500
MIN_LENGTH = 2

// Inputs: snake_case with descriptive names
rsi_length  = input.int(14, "RSI Length")
sl_mult     = input.float(1.5, "SL Multiplier")
use_filter  = input.bool(true, "Enable Filter")

// Functions: camelCase + verb
calcVolatility(src, len) =>
    ta.stdev(src, len)

isAboveTrend(src, len) =>
    src > ta.ema(src, len)
```

---

## Input Quality Standards

Every input must have:
1. **Descriptive title** — not "Length", but "RSI Length"
2. **Tooltip** — explains what it does and effect of changing it
3. **Sensible defaults** — tested values, not arbitrary
4. **Min/max limits** — prevent nonsensical values
5. **Group** — organized, not scattered

```pine
// BAD input
len = input.int(14, "Length")

// GOOD input
rsi_len = input.int(14, "RSI Period",
     minval=2, maxval=100,
     tooltip="Number of bars for RSI calculation. " +
             "Lower values = more sensitive but more noise. " +
             "Higher values = smoother but slower to react.",
     group="Signal Settings")
```

---

## Plot Quality Standards

Every plot must have:
1. **Title** — for data window and status line
2. **Color** — meaningful color (green = bull, red = bear, gray = neutral)
3. **Style** — appropriate for data type

```pine
// BAD plot
plot(fastEma)

// GOOD plot
plot(fastEma,
     title="Fast EMA",
     color=color.new(color.blue, 0),
     linewidth=2,
     style=plot.style_line)

// Signal markers — always use plotshape with labels
plotshape(longSignal,
     title="Long Signal",
     style=shape.labelup,
     location=location.belowbar,
     color=color.new(color.green, 0),
     textcolor=color.white,
     text="L",
     size=size.small)
```

---

## Strategy-Specific Requirements

Every strategy must include:

```pine
// 1. Realistic commission and slippage
strategy(commission_type=strategy.commission.percent,
         commission_value=0.05, slippage=2)

// 2. Position size based on risk
default_qty_type=strategy.percent_of_equity, default_qty_value=2

// 3. Comment on every entry/exit for clarity in backtest log
strategy.entry("Long", strategy.long, comment="EMA Cross + Vol")
strategy.exit("Long Exit", "Long", stop=sl, limit=tp, comment="SL/TP")

// 4. Always exit conflicting position before entering opposite
if short_signal and strategy.position_size > 0
    strategy.close("Long", comment="Reverse to Short")
if short_signal
    strategy.entry("Short", strategy.short)

// 5. Check position_size before entry to avoid pyramiding (unless intended)
if long_signal and strategy.position_size == 0
    strategy.entry("Long", strategy.long)
```

---

## Anti-Patterns — Never Do These

### Anti-Pattern 1 — Repainting Without Disclosure
```pine
// BAD — repaints because it uses current bar's high/low
signal = ta.pivothigh(high, 3, 0)  // right offset = 0 → repaint

// GOOD — confirmed pivot (waits for 3 bars right of pivot)
signal = ta.pivothigh(high, 3, 3)  // right offset = 3 → confirmed, no repaint
```

### Anti-Pattern 2 — Lookahead Bias in request.security
```pine
// BAD — uses future bar data (lookahead_on is default in some contexts)
htf_ema = request.security(syminfo.tickerid, "D",
     ta.ema(close, 50), lookahead=barmerge.lookahead_on)

// GOOD
htf_ema = request.security(syminfo.tickerid, "D",
     ta.ema(close, 50), lookahead=barmerge.lookahead_off)
```

### Anti-Pattern 3 — Magic Numbers
```pine
// BAD
if ta.rsi(close, 14) > 70 and ta.atr(14) * 1.5 > sl_dist

// GOOD
RSI_OVERBOUGHT = 70
atr_period     = 14
sl_multiplier  = 1.5

rsi_val = ta.rsi(close, rsi_period)
atr_val = ta.atr(atr_period)
if rsi_val > RSI_OVERBOUGHT and atr_val * sl_multiplier > sl_dist
```

### Anti-Pattern 4 — Plot Inside Conditional
```pine
// BAD — Pine Script error: cannot call plot() in local scope
if condition
    plot(value)  // ERROR

// GOOD — use na to hide the plot when not needed
plot(condition ? value : na, "My Line")
```

### Anti-Pattern 5 — No Error Handling for na
```pine
// BAD — crashes when highest returns na
ratio = close / ta.highest(close, 100)

// GOOD
highest_val = ta.highest(close, 100)
ratio = not na(highest_val) ? close / highest_val : na
```

### Anti-Pattern 6 — Recalculating Inside Loops
```pine
// BAD — extremely slow, recalculates atr every loop iteration
for i = 0 to 100
    atr_val = ta.atr(14)  // recalculates 100 times!
    arr.push(arr, close[i] / atr_val)

// GOOD — calculate once outside loop
atr_val = ta.atr(14)
for i = 0 to 100
    arr.push(arr, close[i] / atr_val)
```

### Anti-Pattern 7 — Overfit Strategy (Flag This Explicitly)
Strategies with >8 inputs optimized together are usually overfit.
Always mention this when delivering complex strategies:

```
⚠️ Optimization note: This strategy has [N] optimizable parameters.
Optimizing all simultaneously risks curve-fitting to historical data.
Recommended approach: optimize signal parameters first, then risk
parameters separately. Validate on out-of-sample data before live use.
```

---

## TradingView Publication Checklist

For scripts intended for public publication:

```
REQUIRED
[ ] Script compiles without errors or warnings
[ ] No security vulnerabilities (no external data calls to untrusted sources)
[ ] All inputs have titles and tooltips
[ ] All plots have titles
[ ] Strategy includes realistic commission and slippage
[ ] Repainting behavior is disclosed in description if present
[ ] Risk warning included for strategies

DESCRIPTION FORMAT (TradingView requires this structure)
[ ] Overview paragraph — what it does, who it's for
[ ] How It Works — key components explained
[ ] Settings — each input explained
[ ] Usage Guide — how to interpret signals
[ ] Alerts — how to set up alerts
[ ] Risk Disclaimer — required for strategies

VISUAL QUALITY
[ ] Clean chart — not cluttered with unnecessary plots
[ ] Colors accessible (consider colorblind users)
[ ] Dashboard readable at small size
[ ] Screenshot shows clear signal examples
```

---

## Indicator vs Strategy — When to Use Which

**Use `indicator()` when:**
- Visualizing market data
- Creating a signal overlay
- Building a tool for manual decision-making
- Publishing a standalone indicator

**Use `strategy()` when:**
- Backtesting a complete trading system
- Need position tracking (position_size, avg_price)
- Testing risk management systems
- Building for automated trading via alerts

**Key difference in output:**
- indicator() — can be applied to any chart, shows on all historical bars
- strategy() — shows backtest results, strategy tester panel, trade log
