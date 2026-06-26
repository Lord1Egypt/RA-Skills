---
name: ibkr-autonomous-trader
description: >
  Autonomous paper trading research agent for Interactive Brokers (IBKR). Use this skill whenever
  the user wants to connect to IBKR, execute trades, manage positions, analyze strategies, run
  paper trading workflows, backtest signals, or build any automated trading system with TWS or
  IBKR Gateway. Triggers on: "trade", "IBKR", "Interactive Brokers", "paper trading",
  "order execution", "position management", "quant strategy", "bracket order", "stop loss",
  "ib_insync", or any mention of automated trading. Always use this skill for trading-related
  tasks — even exploratory ones.
compatibility: "Python >=3.9 | pip: ib_insync pandas numpy pyyaml loguru | IBKR TWS or IB Gateway with API enabled (port 7497 paper / 7496 live)"
---

# IBKR Autonomous Trader Skill

A modular, safe, self-improving paper trading agent for Interactive Brokers.

> ⚠️ **Safety First**: `ENABLE_LIVE_TRADING` defaults to `False`. The agent operates in paper
> trading mode unless explicitly toggled and confirmed. Never flip this flag without user
> confirmation.

---

## Quick Start

```bash
pip install ib_insync pandas numpy pyyaml loguru
# Ensure TWS or IB Gateway is running with API enabled on port 7497 (paper)
python skills/ibkr-autonomous-trader/scripts/trader.py
```

---

## File Map

| File | Purpose |
|---|---|
| `scripts/trader.py` | Main trading loop — entry point |
| `scripts/strategy_engine.py` | Signal generation, indicator logic |
| `scripts/risk_manager.py` | Position sizing, kill switch, daily loss limit |
| `scripts/execution_engine.py` | Order placement, modification, cancellation |
| `scripts/performance.py` | Trade logging, PnL, Sharpe, self-improvement |
| `config/settings.yaml` | All tunable parameters |
| `memory/trades.json` | Full trade history |
| `memory/strategies.json` | Strategy parameter versions |
| `memory/performance.json` | Rolling performance metrics |

---

## Agent Workflow (One Loop Iteration)

```
1. Connect to IBKR
2. Load config + memory
3. Fetch market data (bars + live quotes)
4. Scan watchlist assets
5. Run strategy_engine → generate signals
6. Run risk_manager → validate each signal
7. Size position
8. Execute order via execution_engine (bracket with stop loss)
9. Monitor open positions
10. Log trade details to memory/trades.json
11. Periodically: run performance.py → evaluate + tune parameters
12. Sleep → repeat
```

---

## Safety Controls

- `ENABLE_LIVE_TRADING = False` in `config/settings.yaml` — paper only by default
- Kill switch triggers if daily drawdown exceeds `MAX_DAILY_LOSS_PCT`
- Max concurrent positions enforced via `MAX_POSITIONS`
- Every order validated by `risk_manager.py` before submission
- Duplicate order detection prevents double-fills
- All actions logged via `loguru`

---

## Key Functions (see individual scripts for full signatures)

### execution_engine.py
- `execute_trade(signal)` — Places bracket order with auto stop loss
- `close_trade(position)` — Market-closes an open position
- `adjust_stop(position, new_stop)` — Modifies trailing stop
- `cancel_trade(order_id)` — Cancels a pending order
- `get_positions()` — Returns all open positions
- `get_open_orders()` — Returns all pending orders

### risk_manager.py
- `validate_signal(signal, portfolio_state)` — Returns (approved: bool, reason: str)
- `size_position(signal, account_value)` — Returns share quantity
- `check_kill_switch(daily_pnl, account_value)` — Halts trading if threshold breached

### strategy_engine.py
- `generate_signals(bars_dict)` — Returns list of Signal objects
- `compute_indicators(bars)` — RSI, MACD, ATR, EMA
- `score_signal(signal)` — Confidence 0–1

### performance.py
- `log_trade(trade)` — Appends to trades.json
- `evaluate_performance()` — Returns stats dict (win rate, Sharpe, drawdown, profit factor)
- `suggest_improvements(stats)` — Returns parameter adjustment recommendations
- `apply_improvements(recommendations)` — Updates strategies.json

---

## Reading the Reference Files

When implementing or modifying any module, read the corresponding reference:

- Connection + auth patterns → `references/ibkr_connection.md`
- Order types and bracket logic → `references/order_types.md`
- Indicator formulas → `references/indicators.md`
- Self-improvement algorithm → `references/self_improvement.md`

---

## Adding a New Strategy

1. Add a function `strategy_<name>(bars) -> list[Signal]` in `strategy_engine.py`
2. Register it in `config/settings.yaml` under `strategies.enabled`
3. Add parameter defaults under `strategies.params.<name>`
4. The self-improvement loop will automatically tune its parameters over time

---

## Extending Order Types

To add OCO (One-Cancels-Other) or trailing stops, see `references/order_types.md`.
`execution_engine.py` is structured to accept any `ib_insync` Order object.

---

## News Intelligence & Decision System (v2)

Two new modules extend the base skill with multi-factor decision making.

### news_engine.py
- Fetches Google News RSS for 8 market topics + per-symbol feeds (no API key needed)
- Scores each item: **sentiment** (bullish/bearish/neutral/risk_event), **event type**, **impact level**, **time sensitivity**
- `fetch_all()` → list of `NewsItem` (cached for 5 min)
- `get_market_sentiment(items)` → aggregate score dict used by decision engine
- `get_symbol_sentiment(symbol, items)` → float score for a specific ticker
- `evaluate_news_utility()` → learns which news types predict trade outcomes
- All items logged to `memory/news_log.json`

### decision_engine.py
- **Never** lets a trade fire from news alone — technical signal always required
- Combines 4 scores with configurable weights:
  - `technical` (default 50%) — strategy_engine confidence
  - `news` (default 25%) — directional alignment with sentiment
  - `risk` (default 15%) — inverse portfolio exposure
  - `volatility` (default 10%) — ATR/price regime penalty
- Returns a `Decision` with: action, confidence, `position_size_modifier`, `stop_modifier`
- **Risk event override**: any `risk_event` news → `REDUCE_RISK`, no new entries
- **Conflict rule**: strong opposing news + weak tech signal → `NO_TRADE`
- Weights auto-tune after `min_trades_for_weight_update` closed trades

### Updated Trading Loop (trader.py v2)

```
1. Fetch market data
2. Fetch + analyze news → market_sentiment
3. Generate technical signals
4. For each signal:
   a. risk_manager.validate_signal()
   b. news_engine.get_symbol_sentiment()
   c. decision_engine.decide() → Decision
   d. Apply position_size_modifier + stop_modifier
   e. execution_engine.execute_trade()
5. Monitor positions
6. Periodic eval → parameter tuning + news utility learning
```

### Defensive Mode Triggers

| Event | Response |
|---|---|
| `risk_event` in news | REDUCE_RISK — no new entries, stops tightened |
| `high_impact` news | Position size × 0.6, stops × 0.85 |
| News opposes signal AND tech < 0.8 | NO_TRADE |
| Final confidence < 0.45 | NO_TRADE |
| Extreme volatility regime | Volatility score = 0.20 |

### Install

```bash
pip install feedparser  # Only new dependency
```
