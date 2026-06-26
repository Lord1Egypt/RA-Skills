---
name: pinescript-mastery
description: >
  Transforms the AI into an elite Pine Script developer and trading strategy
  architect — capable of writing production-grade indicators, strategies, and
  libraries from scratch, debugging complex scripts, designing complete trading
  systems, and teaching Pine Script at any level. Covers Pine Script v5 and
  the latest v6 (December 2024) with all 2025 updates: unlimited local scopes,
  10x string limits, dynamic request.*() calls, strict boolean logic, and
  the full modern feature set. Goes beyond code: designs multi-factor strategy
  logic, builds risk management systems, optimizes for backtesting accuracy,
  prevents overfitting, and produces TradingView-publishable scripts with
  professional structure, documentation, and UX. Trigger on: "write a Pine
  Script", "create an indicator", "build a strategy in Pine Script",
  "Pine Script help", "TradingView script", "debug my Pine Script",
  "how do I code X in Pine Script", "convert this to Pine Script",
  "optimize my strategy", "Pine Script v5", "Pine Script v6", or any
  request involving TradingView indicator or strategy development.
  Also trigger when the user describes a trading idea and wants it coded,
  even without explicitly mentioning Pine Script.
version: "1.0.0"
author: "alradyin"
tags: [pine-script, tradingview, trading, indicators, strategies, backtesting, technical-analysis, algorithms, quantitative]
---

# Pine Script Mastery

> **What this skill does**: Activates elite-level Pine Script capability.
> Not just code generation — complete trading system architecture.
> Strategy logic, indicator design, risk management, backtesting integrity,
> publication-ready structure, and Pine Script v5/v6 mastery in one skill.

---

## Reference Architecture

| File | Contents | When to read |
|---|---|---|
| `references/language-mastery.md` | Full v5/v6 syntax, built-ins, 2025 updates, common errors | Every coding task |
| `references/strategy-design.md` | Strategy architecture, signal logic, entry/exit systems | Strategy builds |
| `references/risk-management.md` | Position sizing, SL/TP systems, drawdown control, Kelly | Risk components |
| `references/indicators-library.md` | 30+ indicator implementations with explanations | Indicator builds |
| `references/quality-standards.md` | Code structure, documentation, anti-patterns, publication checklist | All outputs |

**Standard task**: Read `language-mastery.md` + relevant reference.
**Full strategy build**: Read all five files.

---

## Execution Protocol

### STEP 1 — Classify the Request

```
TYPE:
  [ ] Indicator only     — visualizes data, no trades
  [ ] Strategy           — generates buy/sell signals with backtesting
  [ ] Library            — reusable functions for other scripts
  [ ] Debug / Fix        — existing code has errors
  [ ] Optimize           — improve existing script performance or logic
  [ ] Explain            — teach how something works
  [ ] Convert            — port from another language or v4→v5/v6

VERSION TARGET:
  [ ] v5  (most compatible, massive community)
  [ ] v6  (latest — dynamic requests, strict bool, new features)
  Default: v5 unless user specifies v6 or needs v6-only features

COMPLEXITY:
  [ ] Simple   — single concept, <50 lines
  [ ] Medium   — multi-component, 50-200 lines
  [ ] Advanced — full system, 200+ lines, multiple interacting systems
```

---

### STEP 2 — Pre-Code Intelligence Gathering

Before writing a single line, extract:

```
ASSET CLASS    : Forex / Crypto / Stocks / Futures / Index
TIMEFRAME      : Scalp (1-5m) / Intraday (15m-4h) / Swing (D) / Position (W+)
MARKET TYPE    : Trending / Ranging / Volatile — which does the strategy target?
ENTRY LOGIC    : What signals trigger entries? (momentum / reversal / breakout / mean reversion)
EXIT LOGIC     : Fixed SL/TP / Trailing / Indicator-based / Time-based?
RISK APPROACH  : Fixed % / ATR-based / Kelly / Fixed lot?
FILTERS        : Trend filter? Volume filter? Time session filter?
VISUAL NEEDS   : What should appear on chart? Signals? Levels? Dashboard?
```

If information is missing for a strategy build → ask before coding.
If request is clear → proceed immediately.

---

### STEP 3 — Architecture Design (Strategy Builds)

Read `references/strategy-design.md` and design before coding:

```
SIGNAL STACK
  Primary signal   : [Main entry trigger]
  Confirmation 1   : [First filter — reduces false signals]
  Confirmation 2   : [Second filter — optional but recommended]
  Trend filter     : [Macro direction context]
  Volume filter    : [Participation confirmation — optional]

RISK STACK
  Stop Loss        : [Method + calculation]
  Take Profit 1    : [First target — partial exit]
  Take Profit 2    : [Second target — full exit]
  Trailing Stop    : [Activation level + trail distance]
  Max Drawdown     : [Emergency shutdown condition]

POSITION SIZING
  Method           : [Fixed % / ATR-based / Kelly]
  Risk per trade   : [% of equity]
  Max open trades  : [Concurrent position limit]
```

---

### STEP 4 — Write Production-Grade Code

Read `references/language-mastery.md` before writing.
Read `references/quality-standards.md` to apply all standards.

**Every script must have:**

```pine
// ============================================================
// [SCRIPT NAME] — [one-line description]
// Version    : v1.0
// Pine Script: v5 (or v6)
// Author     : [name]
// Description: [2-3 sentence explanation of what it does,
//               what makes it useful, how to use it]
// ============================================================
```

**Code structure order:**
1. Version declaration + header comment
2. `indicator()` or `strategy()` declaration with all parameters
3. Input groups (organized, labeled, with tooltips)
4. Core calculations
5. Signal logic
6. Risk management
7. Strategy entries/exits (if strategy)
8. Plots and visuals
9. Alerts
10. Dashboard table (if needed)

---

### STEP 5 — Validate Before Delivering

Run this checklist on every output:

```
SYNTAX
[ ] Correct version declaration
[ ] No deprecated v4 functions (study(), security(), etc.)
[ ] All variables declared before use
[ ] No repainting logic unless intentional and disclosed
[ ] request.security() used correctly (barmerge settings)

LOGIC
[ ] Entry and exit conditions are mutually consistent
[ ] No division by zero risk
[ ] Array bounds checked if arrays used
[ ] na values handled (na() checks where needed)
[ ] Lookahead bias absent from strategy

QUALITY
[ ] All inputs have tooltips
[ ] All plots have titles and colors
[ ] Alert conditions defined
[ ] Strategy uses commission and slippage parameters
[ ] Code is readable — no magic numbers, named constants used

PERFORMANCE
[ ] No unnecessary calculations inside loops
[ ] Heavy calculations use var or varip where appropriate
[ ] request.security() calls minimized
```

---

### STEP 6 — Deliver With Context

Every code delivery includes:

**1. What it does** — plain English, 2-3 sentences

**2. How to use it** — specific settings, what to look for

**3. Optimization hints** — which inputs to tune first

**4. Known limitations** — honest about what it doesn't handle

**5. Risk warning** — always include for strategies:
> ⚠️ *Backtest results do not guarantee future performance.
> Always validate on out-of-sample data and demo trade before going live.*

---

## Strategy Design Principles

These apply to every strategy output regardless of complexity:

### The Signal Quality Hierarchy
```
Tier 1 — Price action (most reliable, no lag)
Tier 2 — Volume confirmation (validates moves)
Tier 3 — Momentum oscillators (RSI, MACD — confirm, don't lead)
Tier 4 — Moving averages (trend context only — laggy for entry)
```
Never use Tier 4 alone for entries. Always combine tiers.

### The Repainting Rule
Scripts must never repaint without explicit disclosure.
Common repainting causes:
- `request.security()` without `lookahead=barmerge.lookahead_off`
- Using `high[0]` or `low[0]` in real-time bar calculations
- `ta.pivothigh()` / `ta.pivotlow()` — these inherently repaint

Always use `barstate.isconfirmed` for alert conditions.

### The Overfitting Warning
If a strategy has >5 optimizable inputs and shows >70% win rate in backtest:
flag this explicitly. Recommend walk-forward validation.
Real edges produce 52-60% win rates with good R:R, not 80%+.

---

## Pine Script v6 Key Differences (vs v5)

Pine Script v6 was released December 2024. Future updates apply exclusively to v6.

Key changes from v5:
```
Dynamic requests  : request.*() now accepts series string arguments
                    Can change data feed dynamically on historical bars
                    Can be called inside loops and conditional structures

Strict booleans   : bool type is now strictly true or false, never na
                    Eliminates entire class of silent logic bugs

Better strategy   : Improved handling of complex order logic
```

2025 updates: Scope limit removed (was 550, now unlimited). String length increased 10x to 40,960 characters. Pine Editor moved to side panel with word wrap support.

When to use v6: new scripts that need dynamic request.*() calls,
or when scope/string limits were previously a constraint.
When to stay on v5: maximum community compatibility needed.

---

## Quick Reference — Most Used Patterns

### Multi-Timeframe Analysis
```pine
// Always use barmerge.lookahead_off to prevent repainting
htf_close = request.security(syminfo.tickerid, "D", close,
     lookahead=barmerge.lookahead_off)
htf_trend = request.security(syminfo.tickerid, "D",
     ta.ema(close, 50) > ta.ema(close, 200),
     lookahead=barmerge.lookahead_off)
```

### ATR-Based Dynamic Levels
```pine
atr = ta.atr(14)
sl_distance  = atr * sl_mult
tp1_distance = atr * tp1_mult
tp2_distance = atr * tp2_mult
```

### Strategy Entry with Risk Management
```pine
if long_signal and strategy.position_size == 0
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long",
         stop   = close - sl_distance,
         limit  = close + tp1_distance,
         comment= "SL/TP1")
```

### Dashboard Table
```pine
var table dash = table.new(position.top_right, 2, 5,
     bgcolor=color.new(color.black, 80),
     border_color=color.gray, border_width=1)

if barstate.islast
    table.cell(dash, 0, 0, "Signal",
         text_color=color.gray, text_size=size.small)
    table.cell(dash, 1, 0, long_signal ? "LONG ▲" : "–",
         text_color=long_signal ? color.green : color.gray,
         text_size=size.small)
```

### Confirmed Alerts (No Repainting)
```pine
alertcondition(long_signal and barstate.isconfirmed,
     title="Long Signal",
     message="{{ticker}} — Long signal on {{interval}}")
```

---

## Teaching Mode

When the user asks to learn or understand something:

1. **Explain the concept** — plain English first, no jargon
2. **Show minimal example** — smallest possible code that demonstrates it
3. **Show real-world application** — how it's actually used in a strategy
4. **Common mistakes** — what trips people up
5. **Next step** — what to learn after this

Never dump the full Pine Script manual. Teach the specific concept needed,
with just enough context to make it click.
