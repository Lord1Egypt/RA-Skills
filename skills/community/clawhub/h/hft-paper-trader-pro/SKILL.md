---
name: hft-paper-trader
version: 1.1.0
description: High-frequency paper trading framework for crypto. Multi-indicator TA scoring (RSI/MACD/EMA/BB/OBV/StochRSI), dual-regime filter (15m fast + 4h macro), position sizing (Kelly criterion), correct stop-loss management (3% max risk cap), auto-observation logging, and trade ledger. Use for paper trading, backtesting trading logic, HFT simulation, or building an autonomous trading agent.
author: JamieRossouw
tags: [trading, paper-trading, hft, crypto, kelly, backtesting, autonomous-agent, regime-filter]
---

# HFT Paper Trader — Autonomous Crypto Trading Framework

A complete high-frequency paper trading system for building and testing autonomous crypto trading agents.

## Architecture

```
Market Data (Binance public API)
    ↓
TA Engine (RSI + MACD + EMA + BB + OBV + StochRSI)
    ↓
Signal Score (-10 to +10)
    ↓
Dual Regime Filter (15m EMA8/21 fast + 4h EMA20/50 macro)
    ↓
Kelly Position Sizer (3% max risk per trade)
    ↓
Paper Portfolio Manager (portfolio.json)
    ↓
Trade Ledger (journal.json) + Auto-Observation Logger (observations.md)
```

## Features

- **Multi-indicator confluence**: 7 indicators combined into one score
- **Dual regime filter**: 15m EMA8/21 (fast) gates entries alongside 4h EMA20/50 (macro) — prevents trading against short-term trend
- **OBV divergence detection**: hidden accumulation/distribution
- **Quarter-Kelly sizing**: conservative risk management
- **Correct SL placement**: Math.max caps risk at 3% — fixes bug where SL ran 5–11% instead of 3%
- **Drawdown controls**: auto-pause at 2% daily NAV
- **Full audit trail**: every trade logged with entry/stop/target/outcome
- **Auto-observation logging**: losses and SL hits automatically appended to `observations.md` for strategy learning
- **Self-improvement loop**: lessons captured after each loss

## Usage

```
Use hft-paper-trader to run TA on BTC and place a paper trade

Use hft-paper-trader to check portfolio performance

Use hft-paper-trader to scan the watchlist and trade all signals

Use hft-paper-trader to check today's observations and lessons
```

## Regime Filter Logic

Entries are only allowed when BOTH regimes are bullish:
- **Fast (15m)**: EMA8 > EMA21
- **Macro (4h)**: EMA20 > EMA50

This gates out counter-trend entries that otherwise pass signal scoring. When either regime is bearish, new positions are blocked regardless of score.

## Stop-Loss Placement (Fixed v1.1.0)

```js
// CORRECT — caps SL at 3% below entry
stopLoss = entry * (1 - MAX_RISK);   // Math.max not used here — direct cap

// Bug in v1.0.0 — Math.min let SL run to 5-11%
// Fix: use direct percentage cap on entry price, not min of wick distance
```

## Watchlist
BTC ETH SOL XRP TRX DOGE ADA AVAX BNB LINK LTC SUI ARB OP NEAR DOT ATOM UNI MATIC

## File Layout

```
trading/
  paper-dashboard/portfolio.json   ← live portfolio state
  journal.json                     ← full trade ledger
  observations.md                  ← auto-logged trade lessons
```

## Performance
Starting capital: $1,000. Runs hourly (XX:01 UTC). Max 5 concurrent positions at 10% each.
