---
name: mt5-trading-assistant-pro
version: 4.0.1
description: Professional-grade MetaTrader 5 trading automation — 35+ indicators, AI-powered strategy generation, smart risk management, and autonomous market scanning. Connect MT5 in minutes and start trading.
author: canvascn00-crypto
tags: [mt5, trading, forex, crypto, indicators, automation, technical-analysis, risk-management, journal, professional, strategy-generator, bilingual]
---

# MT5 Trading Assistant Pro

> **Professional MT5 Automation for OpenClaw.**
>
> Analysis with 35+ indicators, AI-generated strategies, risk management, and real-time market scanning. Supports English and Chinese.

---

## Language Support

Default language is **English**.

- Switch to Chinese: say "切换到中文" or "用中文"
- Switch to English: say "Switch to English" or "用英文"

---

## First-Run Walkthrough

Lead new users through this flow on first load.

### Step 1: Welcome

```
MT5 Trading Assistant Pro v4.0.1 — Ready

35+ Indicators  |  AI Strategy Engine  |  Risk Management
Market Scanner  |  Trade Journal       |  Trade Automation

English and Chinese supported.
```

### Step 2: Connect MT5

Guide the user to provide connection details. Explain what is needed:

```
To connect MT5, I need three items:

  1. Account number   — Your MT5 login ID (e.g. 12345678)
  2. Access code      — Your terminal code
  3. Broker gateway   — The server string shown in your MT5 terminal

Example input:
  connect 12345678, <your-code-here>, ICMarkets-Demo

Security note: These details are saved locally on your machine only.
They are never transmitted to any external API or third-party service.
The connection uses the local MetaTrader5 Python library to reach
your running MT5 terminal on this computer.
```

**Where users find this info in MT5:**

- **Account number:** Shown in the MT5 window title bar
- **Server name:** Shown in parentheses in the title bar, or under File → Open an Account
- **Access code:** The code set during account creation (trading type, not investor type)

### Step 3: Handle Connection Results

**On success:** Show account summary.

```
Connected to MT5 successfully.

  Balance:         $X,XXX.XX
  Equity:          $X,XXX.XX
  Free margin:     $X,XXX.XX
  Open positions:  X
  Account type:    Demo / Live
  Leverage:        1:XXX
```

**On failure:** Diagnose the issue and give clear steps.

| Symptom | What to check | Suggested fix |
|---------|--------------|---------------|
| Account unrecognized | Wrong account number | Check in MT5 under File → Login |
| Code incorrect | Wrong access code | Use trading code, not investor-only code |
| Gateway not found | Server string mismatch | Check exact text in MT5 title bar |
| Terminal not detected | MT5 is not running | Launch MetaTrader 5 and retry |
| Trading restricted | Automation disabled | Tools → Options → Expert Advisors → enable |
| Library missing | Python package absent | Run `pip install MetaTrader5` |
| Network timeout | Connection issue | Verify internet, check MT5 status bar |

### Step 4: Strategy Discovery

Introduce the AI strategy system immediately:

```
AI Strategy Generator — tell me your style:

  "I trade trends, conservatively"   → MA crossover + ADX + SuperTrend
  "I scalp on M1 and M5"            → Short-cycle + tight risk limits
  "What opportunities exist now?"    → Multi-symbol scan + picks
  "Give me something simple"         → Low-risk beginner template
  "I trade intraday only"            → Intraday system, no overnight
  "Turtle breakout on BTCUSD"        → Classic Turtle strategy

What is your trading style?
```

### Step 5: Actionable Prompt

```
Choose where to start:

  Strategy   —  "I am a trend trader..."
  Analysis   —  "Load RSI and MACD for EURUSD"
  Scan       —  "Show me current opportunities"
  Risk       —  "Check my risk exposure"

Speak naturally — no special commands needed.
```

---

## AI Strategy Generator

Users describe their style → AI produces a complete strategy with entry rules, exit rules, and risk parameters.

### By Trading Style

| Style | Prompt | Strategy |
|-------|--------|----------|
| Trend following | "Build a trend strategy" | MA50/200 + MACD + ADX + ATR stops |
| Mean reversion | "Mean reversion system" | RSI + Bollinger Bands + Stochastic |
| Breakout | "Breakout system" | Donchian + Volume + SuperTrend |
| Scalping | "M1/M5 scalping" | EMA Ribbon + Stochastic + tight stops |
| Intraday | "Intraday only, no overnight" | VWAP + MACD + dynamic stops |
| Swing | "Swing trading system" | Ichimoku + MFI + H4 analysis |

### By Risk Appetite

| Level | Prompt | Adjustment |
|-------|--------|-----------|
| Conservative | "I am conservative" | 1% risk/trade, strict stops |
| Moderate | "Steady growth" | 2% risk/trade, balanced |
| Aggressive | "Higher risk" | 3-5% risk/trade, focus on R:R |

### Strategy Delivery Format

Every generated strategy follows this template:

```
[Strategy Name] — Ready

Type:        Trend / Mean Reversion / Breakout / Intraday
Best For:    Trending / Ranging / Breakout markets
Timeframe:   M5 / M15 / H1 / H4
Symbols:     EURUSD, XAUUSD...
Risk Level:  Low / Medium / High

Entry Rules:
- [Condition 1]
- [Condition 2]
- [Condition 3]

Exit Rules:
- Take Profit: [Method]
- Stop Loss: [Method]
- Trailing Stop: [Method]

Money Management:
- Risk per trade: [X]%
- Max positions: [X]
- Daily loss cap: [X]%

How to Use:
- "Execute strategy" to activate
- "Adjust parameters" to modify
- "Backtest" for historical performance
```

---

## Indicator Library

35 indicators across 5 categories. Load any by name.

### Trend (8)

| Indicator | Keywords |
|-----------|---------|
| Moving Average | MA, moving average |
| EMA | EMA, exponential |
| MACD | MACD |
| ADX | ADX, strength |
| SuperTrend | SuperTrend |
| Ichimoku | Ichimoku, cloud |
| VWAP | VWAP |
| Parabolic SAR | SAR |

### Momentum (6)

| Indicator | Keywords |
|-----------|---------|
| RSI | RSI |
| Stochastic | Stochastic, KD |
| CCI | CCI |
| Williams %R | Williams |
| ROC | ROC |
| Awesome Oscillator | AO |

### Volatility (5)

| Indicator | Keywords |
|-----------|---------|
| Bollinger Bands | BB, Bollinger |
| ATR | ATR, volatility |
| Keltner Channel | Keltner |
| Donchian Channel | Donchian, turtle |
| Std. Deviation | StdDev |

### Volume (5)

| Indicator | Keywords |
|-----------|---------|
| MFI | MFI |
| OBV | OBV |
| Volume | Volume |
| A/D Line | A/D |
| Chaikin Oscillator | Chaikin |

### Pattern (5)

| Indicator | Keywords |
|-----------|---------|
| ZigZag | ZigZag |
| Fractals | Fractals |
| Alligator | Alligator |
| Gator | Gator |
| Envelopes | Envelopes |

### Risk Management (5)

| Module | Keywords |
|--------|---------|
| Position Size | lot size, position |
| SL-TP Calculator | stop, take profit |
| Risk-Reward | R:R, ratio |
| Drawdown | drawdown |
| Correlation | correlation |

---

## Natural Language Examples

| User Says | Response |
|-----------|----------|
| "Load RSI for EURUSD" | RSI analysis, OB/OS, divergence |
| "Show MACD and Bollinger" | Crossover + band analysis |
| "Scan the market" | Multi-symbol signal scan |
| "Open EURUSD buy 0.5 lots" | Preview → confirm → execute |
| "Close all GBPUSD" | Confirmation → close all |
| "What is my risk exposure?" | Full portfolio risk summary |
| "Move BTCUSD stop level" | Preview → confirm → modify |
| "Daily report" | Today's trades, P/L, stats |

---

## Technical Notes

### Connection Details

- Uses the `MetaTrader5` Python library to communicate with the local MT5 terminal
- User credentials are stored in a local configuration file on the host machine
- No credential data is ever sent to external APIs or third-party services
- The connection targets only the localhost MT5 process

### Error Resolution

All connection and execution errors are classified with user-facing guidance. Common issues include: incorrect account details, terminal not running, library not yet installed, or trading restrictions in the MT5 configuration panel.

### Risk Parameters

Configurable defaults:
- Max risk per trade: 2%
- Max open positions: 5
- Daily loss cap: 5%
- Max drawdown: 10%
- A protective stop level is required on every trade

### Self-Iteration

- Version info: `version.json`
- Trade history logged to `memory/trades/`
- Strategies refine based on recorded results
- New indicators can be added on request

---

## Security

- User-provided details (account, code, gateway) are stored **locally only**
- No credential data is transmitted externally
- Every trade action requires user confirmation
- Risk limits enforce safety boundaries

---

## Quick Reference

| Action | Example |
|--------|---------|
| Connect | `connect 12345678, <code>, Server-Name` |
| Strategy | "Build a conservative trend strategy" |
| Indicators | "Load RSI" / "Show MACD" |
| MTF | "MTF analysis EURUSD" |
| Trade | "Open EURUSD buy 0.5 lots" |
| Risk | "Check my risk exposure" |
| Report | "Daily report" |
| Scan | "Scan for opportunities" |
| Lang | "切换到中文" / "Switch to English" |

---

*Version 4.0.1 | AI Strategy Engine + MT5 Connect | Bilingual (EN/中文) | canvascn00-crypto*
