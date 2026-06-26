---
name: pine-script-strategy
description: Write, fix, test, and backtest Pine Script v5 strategies and indicators for TradingView. Use when asked to create trading strategies, indicators, Pine Script code, fix compilation errors, backtest ideas, optimize strategies, write SMC/scalping/trend-following systems, or anything related to TradingView Pine Script. Triggers on phrases like "pine script", "tradingview strategy", "tradingview indicator", "backtest this", "write a strategy", "fix my pine script", "pine script error", "create indicator", "trading strategy".
---

# Pine Script Strategy Builder

Write production-ready Pine Script v5 strategies and indicators for TradingView.

## Workflow

1. **Understand the request** — What instrument, timeframe, style (scalping/intraday/swing)?
2. **Choose type** — `strategy()` for backtesting + signals, `indicator()` for visual-only
3. **Follow architecture** — Data → Signal → Score → Filter → Risk → Execute → Visual
4. **Apply non-repaint rules** — MANDATORY, no exceptions
5. **Run pre-flight checklist** — Before finalizing ANY script
6. **Test mentally** — Walk through edge cases, verify logic on paper
7. **Deliver** — Complete script + explanation + suggested backtest settings

## Non-Negotiable Rules

### Non-Repaint (ALWAYS)
- Wrap signals in `barstate.isconfirmed`
- `strategy()` must have `calc_on_every_tick=false`, `process_orders_on_close=false`
- `request.security()` → use `barmerge.gaps_off, barmerge.lookahead_on` with `[1]` offset
- NEVER use current bar data for signal generation without confirmation

### Risk Management (ALWAYS)
- Every trade MUST have a stop loss — no naked positions
- Use ATR-based or swing-based SL
- RR ratio ≥ 1:2 preferred
- Max trades per day filter
- Cool-off after loss

### Quality Gates (ALWAYS)
- ADX chop filter (ADX > 20 to trade)
- Session filter for appropriate trading hours
- Volume confirmation (1.2x+ average)
- Score threshold ≥ 70 for entries

## Strategy Architecture

```
Layer 1: Data — Collect indicators (EMA, RSI, ATR, VWAP, ADX, Volume, BB, Pivots)
Layer 2: Signal — Generate signals (trend direction, breakouts, pullbacks, sweeps)
Layer 3: Score/Filter — Score + filter (multi-factor score, chop filter, session, cool-off)
Layer 4: Risk — SL/TP calculation (ATR/swing-based, partial exits, trailing)
Layer 5: Execute — Entry/exit logic (NON-REPAINT, barstate.isconfirmed)
Layer 6: Visual — Labels, boxes, tables, alerts, backgrounds
```

## Pre-Flight Checklist

Before delivering ANY strategy, verify:
- [ ] Non-repaint logic (`barstate.isconfirmed`)?
- [ ] Chop filter (ADX > 20)?
- [ ] Session filter?
- [ ] Cool-off after loss?
- [ ] Score threshold ≥ 70?
- [ ] Strong breakout confirmation?
- [ ] Full EMA alignment (3+ EMAs)?
- [ ] Volume confirmation (1.2x+)?
- [ ] RR ≥ 1:2?
- [ ] Max trades per day?
- [ ] SL always set?
- [ ] Partial exit or trailing?

## Templates

### Strategy Template
```pine
//@version=5
strategy("Name", overlay=true,
     initial_capital=10000,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=10,
     commission_type=strategy.commission.percent,
     commission_value=0.05,
     slippage=1,
     pyramiding=0,
     process_orders_on_close=false,
     calc_on_every_tick=false)
```

### Indicator Template
```pine
//@version=5
indicator("Name", overlay=true, max_lines_count=500, max_labels_count=500)
```

## Key Patterns

### Non-Repaint Entry
```pine
var bool longSignal = false
if barstate.isconfirmed
    longSignal := <conditions>
else
    longSignal := false

if longSignal and strategy.position_size == 0 and barstate.isconfirmed
    strategy.entry("Long", strategy.long)
```

### Multi-Timeframe Non-Repaint
```pine
htfClose = request.security(syminfo.tickerid, "60", close[1], barmerge.gaps_off, barmerge.lookahead_on)
```

### ATR-Based SL/TP
```pine
atrVal = ta.atr(14)
slLong = close - atrVal * 1.5
tpLong = close + atrVal * 1.5 * rrRatio
```

### Score System (0-100)
```pine
score = 0
if close > ema50 and close > ema200  // Trend: 0-25
    score += 25
if rsi > 60                          // Momentum: 0-20
    score += 20
if volume > ta.sma(volume, 10) * 1.2  // Volume: 0-15
    score += 15
if close > high[1] and close > open   // Breakout: 0-20
    score += 20
if ta.atr(14) > ta.atr(14)[1]        // Volatility: 0-10
    score += 10
if close > ta.vwap(hlc3)              // VWAP: 0-10
    score += 10
totalScore = math.min(score, 100)
```

### Cool-off After Loss
```pine
var int barsSinceLoss = 999
if strategy.closedtrades > 0
    if strategy.closedtrades.profit(strategy.closedtrades - 1) < 0
        barsSinceLoss := 0
barsSinceLoss += 1
coolOffOK = barsSinceLoss > 5
```

## Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `Cannot call ta.dmi().adx` | `[diPlus, diMinus, adxVal] = ta.dmi(len, len)` |
| `Undeclared identifier` | Declare with `var` before use |
| `Cannot call operator [] on bool` | Store in `var` variable first |
| `Script could not be translated` | Check commas, parentheses, v5 syntax |
| `Too many plot calls` | Max 64 plots — use tables/labels |
| `Loop takes too long` | Max 500K iterations — reduce loop |
| `Variable type mismatch` | Use `float()` or `int()` casting |

## Detailed References

- **SMC patterns (BOS, ChoCH, FVG, Order Blocks, Sweeps):** See [references/smc-patterns.md](references/smc-patterns.md)
- **All indicators cheat sheet:** See [references/indicators-cheatsheet.md](references/indicators-cheatsheet.md)
- **Entry patterns (proven):** See [references/entry-patterns.md](references/entry-patterns.md)
- **Risk management patterns:** See [references/risk-management.md](references/risk-management.md)
- **Visual & alert patterns:** See [references/visuals-alerts.md](references/visuals-alerts.md)
- **Performance tracking:** See [references/performance-tracking.md](references/performance-tracking.md)

## Output Format

When delivering a Pine Script:
1. Complete, copy-paste-ready code
2. Brief explanation of what it does
3. Suggested TradingView backtest settings (timeframe, dates, instrument)
4. Known limitations or things to watch for
5. Ideas for improvement

## Fixing Errors

When fixing Pine Script compilation errors:
1. Read the error message carefully
2. Match to known error patterns above
3. Fix the specific issue — don't rewrite the whole script
4. Verify the fix doesn't break other logic
5. Re-check non-repaint compliance

## Optimization Notes

- Don't overfit to historical data
- Test across multiple timeframes
- Verify with walk-forward (test on different date ranges)
- Keep strategies simple — complex ≠ profitable
- If win rate < 50% or profit factor < 1.3, strategy needs work
