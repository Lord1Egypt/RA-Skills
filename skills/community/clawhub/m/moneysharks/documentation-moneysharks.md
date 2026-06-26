# 🦈 MoneySharks — Complete Documentation

> Autonomous 24/7 Aster DEX perpetual futures trading agent for OpenClaw.  
> Purpose: generate maximum sustainable ROI from live leveraged trading, learning from every trade.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Installation](#3-installation)
4. [Onboarding](#4-onboarding)
5. [Configuration Reference](#5-configuration-reference)
6. [Trading Modes](#6-trading-modes)
7. [The Trading Pipeline](#7-the-trading-pipeline)
   - 7.1 [Market Data & Features](#71-market-data--features)
   - 7.2 [Signal Generation](#72-signal-generation)
   - 7.3 [Confluence Scoring](#73-confluence-scoring)
   - 7.4 [Leverage Recommendation](#74-leverage-recommendation)
   - 7.5 [Position Sizing](#75-position-sizing)
   - 7.6 [Risk Checks](#76-risk-checks)
   - 7.7 [Order Execution](#77-order-execution)
   - 7.8 [Position Management](#78-position-management)
8. [Self-Learning System](#8-self-learning-system)
9. [Cron Automation (24/7 Operation)](#9-cron-automation-247-operation)
10. [State & Journal Files](#10-state--journal-files)
11. [Emergency Controls](#11-emergency-controls)
12. [Script Reference](#12-script-reference)
13. [Aster DEX API Integration](#13-aster-dex-api-integration)
14. [Hard Safety Rules](#14-hard-safety-rules)
15. [Monitoring & Status](#15-monitoring--status)
16. [Operational Runbook](#16-operational-runbook)
17. [Frequently Asked Questions](#17-frequently-asked-questions)

---

## 1. Overview

MoneySharks is a fully autonomous 24/7 perpetual futures trading agent that runs inside OpenClaw. Once you complete a one-time onboarding — providing your Aster DEX API credentials, base investment, leverage limits, and explicit consent — the agent trades continuously without requiring per-trade approval from you.

**What it does:**
- Scans Aster DEX futures markets every 2 minutes (configurable)
- Analyses multi-timeframe market data using technical indicators
- Decides whether to go long, short, hold, or wait — with strict confluence requirements
- Places bracket orders (entry + stop-loss + take-profit) automatically
- Manages open positions with trailing stops and close logic
- Learns from every completed trade, adapting confidence thresholds and leverage caps
- Sends daily summaries and alerts when intervention is needed

**What it does NOT do:**
- Trade without your explicit consent (given once at onboarding)
- Override hard risk limits under any circumstances
- Raise leverage above your configured maximum
- Trade symbols outside your approved list
- Remove stop-losses or take-profits from orders

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw (cron host)                  │
│                                                          │
│  Every 2 min ──────► autonomous_runner.py               │
│                            │                            │
│                    ┌───────┴────────┐                   │
│                    │                │                    │
│            position_monitor.py   trade_loop.py × N      │
│            (detect closes)       (per symbol)           │
│                    │                │                    │
│                    │         ┌──────▼──────────────┐    │
│                    │         │  market_scan_from_   │    │
│                    │         │  aster.py            │    │
│                    │         │  (multi-TF klines +  │    │
│                    │         │   account + depth)   │    │
│                    │         └──────┬───────────────┘    │
│                    │                │                    │
│                    │    compute_features.py              │
│                    │    compute_signal.py                │
│                    │    compute_confluence.py            │
│                    │    recommend_leverage.py            │
│                    │    size_position.py                 │
│                    │    risk_checks.py                   │
│                    │                │                    │
│                    │    live_execution_adapter.py        │
│                    │         │                           │
└────────────────────┼─────────┼───────────────────────── ┘
                     │         │
              ┌──────▼─────────▼──────────────────────────┐
              │           Aster DEX Futures API            │
              │  POST /fapi/v1/leverage                     │
              │  POST /fapi/v1/marginType                   │
              │  POST /fapi/v1/order  (entry MARKET)        │
              │  POST /fapi/v1/order  (STOP_MARKET SL)      │
              │  POST /fapi/v1/order  (TAKE_PROFIT_MARKET)  │
              └────────────────────────────────────────────┘
```

**Data persistence:**
- `config.json` — your settings (written once at onboarding, read every cycle)
- `state.json` — live agent state: halt flags, daily loss, metrics, open positions
- `trades.json` — complete journal of every decision and outcome

---

## 3. Installation

### Requirements

- Python 3.10+
- OpenClaw installed
- Aster DEX account with Futures trading enabled and API key created

No pip dependencies. Everything uses Python's standard library.

### Steps

```bash
# 1. Copy the skill to your OpenClaw skills directory or a standalone folder
cp -r moneysharks-skill/ ~/my-moneysharks/

# 2. Run the install verification script
cd ~/my-moneysharks
bash install.sh

# 3. Set your credentials in your shell profile
echo 'export ASTER_API_KEY="your-api-key"' >> ~/.zshrc
echo 'export ASTER_API_SECRET="your-api-secret"' >> ~/.zshrc
source ~/.zshrc

# 4. Run onboarding
python3 scripts/onboarding.py
```

The `install.sh` script verifies:
- Python 3.10+ is available
- All 21 required scripts are present
- All scripts pass syntax check
- `config.json` validates (if it exists)
- Environment credentials are set

---

## 4. Onboarding

Onboarding is a one-time interactive setup that configures and activates the agent.

### Via OpenClaw Agent (recommended)

Tell your OpenClaw agent:
> "Set up MoneySharks" or "Onboard moneysharks"

The agent will guide you through the consent flow conversationally, write `config.json`, and register all four cron jobs automatically.

### Via CLI

```bash
python3 scripts/onboarding.py [--output /path/to/config.json]
```

**Onboarding flow:**

```
Step 1: Aster API Credentials
  → Reads ASTER_API_KEY / ASTER_API_SECRET from environment
  → If not set: prompts you to enter them (not written to config.json)
  → Verifies credentials with a live read-only API call (/fapi/v2/account)
  → Fails hard if credentials are invalid

Step 2: Trading Configuration
  → Symbols to trade (default: BTCUSDT ETHUSDT SOLUSDT)
  → Base investment per trade in USD (default: 100)
  → Max leverage (default: 10)
  → Min leverage (default: 2)
  → Max total exposure in USD
  → Max daily loss in USD
  → Allow short positions? (default: yes)

Step 3: Consent Gate (ACCEPT / DECLINE)
  → Shows full summary of what the agent will do
  → Requires you to type ACCEPT to enable live trading
  → DECLINE starts in paper mode (safe simulation, no real orders)

Step 4: Post-ACCEPT Setup
  → Writes config.json with mode=autonomous_live
  → Runs register_crons.py to generate ready-to-register cron job JSON
  → OpenClaw agent registers the 4 cron jobs automatically
  → Runs first cycle immediately to verify everything works
  → Shows status report
```

### Consent Gate Text

The consent gate you see before ACCEPT:

```
⚠️  AUTONOMOUS LIVE TRADING — READ CAREFULLY BEFORE ACCEPTING

By typing ACCEPT below, you authorise MoneySharks to:

  • Place and manage REAL leveraged orders on Aster DEX
    using your API credentials, 24 hours a day, 7 days a week.
  • Execute trades automatically WITHOUT asking for your
    approval on each individual trade.
  • Manage, modify, and close open positions autonomously.
  • Operate continuously via background cron until you halt it.

Hard safeguards always active:
  • Max daily loss cap            ✓
  • Stop-loss on every trade      ✓
  • Take-profit on every trade    ✓
  • Leverage capped at max        ✓
  • Circuit breakers              ✓

⚠  Futures trading is HIGH RISK. You may lose your entire
    deposit. Past performance does not guarantee future results.
```

> **Important:** `autonomous_live_consent=true` cannot be set by the agent itself. You must physically type `ACCEPT` at this prompt or confirm to the conversational agent. This is a deliberate one-way gate.

---

## 5. Configuration Reference

The `config.json` file controls every aspect of the agent's behaviour.

```json
{
  "mode": "autonomous_live",
  "autonomous_live_consent": true,

  "allowed_symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],

  "base_value_per_trade": 100,
  "risk_pct_per_trade": 0.01,

  "min_leverage": 2,
  "max_leverage": 10,
  "max_notional_per_trade": 500,
  "max_total_exposure": 2000,
  "max_concurrent_positions": 3,
  "max_daily_loss": 100,

  "allow_short": true,
  "require_stop_loss": true,
  "require_take_profit": true,
  "min_reward_risk": 1.5,
  "cooldown_after_close_sec": 120,
  "minimum_hold_sec": 60,

  "cron": {
    "enabled": true,
    "scan_interval_minutes": 2,
    "review_interval_minutes": 30,
    "daily_summary_hour": 0
  },

  "sentiment": {
    "enabled": false,
    "weight": 0.1
  },

  "execution": {
    "cancel_on_halt": true,
    "flatten_on_emergency_stop": false,
    "require_human_approval_for_live_orders": false
  }
}
```

### Field Reference

#### Core

| Field | Type | Default | Description |
|---|---|---|---|
| `mode` | string | `"paper"` | Trading mode. See [Trading Modes](#6-trading-modes). |
| `autonomous_live_consent` | bool | `false` | Must be `true` for `autonomous_live` mode. Set only via ACCEPT at onboarding. |

#### Symbols

| Field | Type | Default | Description |
|---|---|---|---|
| `allowed_symbols` | array | — | **Required.** List of Aster futures symbols to trade. E.g. `["BTCUSDT", "ETHUSDT"]`. The agent only ever touches symbols on this list. |

#### Position Sizing

| Field | Type | Default | Description |
|---|---|---|---|
| `base_value_per_trade` | float | — | **Required.** Reference value in USD per trade. Used as input for position sizing when risk-based sizing would produce zero or near-zero. |
| `risk_pct_per_trade` | float | `0.01` | Percentage of account equity to risk per trade. `0.01` = 1%. Position size is calculated so that hitting the stop-loss costs exactly this fraction of equity. |

#### Leverage

| Field | Type | Default | Description |
|---|---|---|---|
| `min_leverage` | int | — | **Required.** Minimum leverage to use. Applied when confidence is low or volatility is high. |
| `max_leverage` | int | — | **Required.** Maximum leverage the agent is ever allowed to use. Hard ceiling — never exceeded even under performance pressure or by the learning system. |

#### Risk Limits (all hard — cannot be bypassed)

| Field | Type | Default | Description |
|---|---|---|---|
| `max_notional_per_trade` | float | — | **Required.** Maximum USD notional value of any single trade (position size × price). Orders exceeding this are scaled down. |
| `max_total_exposure` | float | — | **Required.** Maximum total USD notional across all open positions simultaneously. New entries are blocked when `current_exposure + new_notional > max_total_exposure`. |
| `max_concurrent_positions` | int | — | **Required.** Maximum number of open positions at the same time across all symbols. |
| `max_daily_loss` | float | — | **Required.** Maximum USD loss allowed in a single UTC calendar day. When this is hit, all new entries are blocked until midnight UTC. |

#### Trade Structure

| Field | Type | Default | Description |
|---|---|---|---|
| `allow_short` | bool | `true` | If `false`, the agent only considers long setups. Short signals are suppressed. |
| `require_stop_loss` | bool | `true` | If `true`, every bracket order must include a STOP_MARKET order. Trades without a valid stop-loss level are skipped. |
| `require_take_profit` | bool | `true` | If `true`, every bracket order must include a TAKE_PROFIT_MARKET order. |
| `min_reward_risk` | float | `1.5` | Minimum reward-to-risk ratio required for a trade to pass confluence. With ATR-based stops, this means take-profit must be at least `min_reward_risk × stop_distance` away from entry. |
| `cooldown_after_close_sec` | int | `120` | Seconds to wait after closing a position on a symbol before opening a new one. Prevents immediate re-entry into unstable markets. |
| `minimum_hold_sec` | int | `60` | Minimum time a position must be held before the close signal can trigger (not currently enforced on SL/TP fills, which happen via exchange). |

#### Cron

| Field | Type | Default | Description |
|---|---|---|---|
| `cron.enabled` | bool | `true` | Master switch for cron-driven operation. Set to `false` to pause all automated cycles without halting existing positions. |
| `cron.scan_interval_minutes` | int | `2` | How often the main execution cycle runs. Minimum recommended: 1. Lower values increase API usage. |
| `cron.review_interval_minutes` | int | `30` | How often the learning review runs. |
| `cron.daily_summary_hour` | int | `0` | UTC hour at which the daily summary cron fires. `0` = midnight UTC. |

#### Sentiment

| Field | Type | Default | Description |
|---|---|---|---|
| `sentiment.enabled` | bool | `false` | Enable sentiment as a weak signal input. Currently reserved for future integration. |
| `sentiment.weight` | float | `0.1` | Weight of sentiment in the overall confidence score when enabled. |

#### Execution

| Field | Type | Default | Description |
|---|---|---|---|
| `execution.cancel_on_halt` | bool | `true` | If `true`, all open orders are cancelled via Aster API when a halt is triggered. Positions are NOT closed unless `flatten_on_emergency_stop=true`. |
| `execution.flatten_on_emergency_stop` | bool | `false` | If `true`, halt also closes all open positions at market price. **Use with caution** — market orders in volatile conditions may have significant slippage. |
| `execution.require_human_approval_for_live_orders` | bool | `false` | In `live` mode only: if `true`, every proposed order waits for per-trade user confirmation before submission. In `autonomous_live`, this field is ignored. |

---

## 6. Trading Modes

| Mode | Live Orders | Approval Required | Use Case |
|---|---|---|---|
| `paper` | No | N/A | Safe simulation. Full pipeline runs but no real API writes. Good for validating strategy before going live. |
| `approval` | No | Per-trade | Agent prepares proposals and waits for your confirmation each time. No automatic execution. |
| `live` | Yes | Configurable | Live orders with optional per-trade approval gate (`require_human_approval_for_live_orders`). |
| `autonomous_live` | Yes | **None** | Full autonomy. Consent given once at onboarding. Agent executes every decision immediately 24/7. |

### Switching Modes

**To switch to paper mode immediately:**
```bash
python3 scripts/resume.py config.json --mode paper
# Or say: "switch to paper mode"
```

**To return to autonomous live (requires re-confirming consent):**
```bash
python3 scripts/resume.py config.json --mode autonomous_live
# autonomous_live_consent must already be true in config.json
```

**To change mode manually:**
Edit `config.json` → change `"mode"` field → restart the next cron cycle.

> **Note:** Switching to paper mode does NOT automatically close live positions. You must manage existing positions manually or use `--flatten`.

---

## 7. The Trading Pipeline

Every execution cycle runs the complete pipeline below, per symbol.

### 7.1 Market Data & Features

**Script:** `market_scan_from_aster.py` + `compute_features.py`

The scan fetches six API responses per symbol:
- **5m klines** (50 bars) — entry timing
- **1h klines** (100 bars) — primary signal timeframe
- **4h klines** (100 bars) — trend context
- **Ticker** — current last price
- **Mark price** — mark price + funding rate
- **Order book depth** (top 5 bids + asks) — liquidity check
- **Account bundle** — equity, available margin, open positions, open orders

From kline data, `compute_features.py` derives:

| Feature | Method | Description |
|---|---|---|
| `ema20` | EMA(close, 20) | Fast moving average — trend proximity |
| `ema50` | EMA(close, 50) | Slow moving average — structural trend |
| `rsi14` | RSI(close, 14) | Momentum oscillator — entry zone filter |
| `atr14` | ATR(high, low, close, 14) | Average True Range — stop/target sizing |
| `macd` | EMA(12) − EMA(26) | MACD line — momentum direction |
| `macd_signal` | EMA(macd, 9) | Signal line — MACD crossover trigger |
| `volume_ratio` | current_vol / avg_vol(20) | Relative volume — confirms moves |
| `trend` | `up` / `down` / `neutral` | Price vs EMA20 vs EMA50 |
| `momentum` | `up` / `down` / `neutral` | RSI > 55 = up, RSI < 45 = down |
| `high_volatility` | ATR / price > 2% | Flags explosive / risky market conditions |
| `funding_rate` | From mark price endpoint | Positive = longs pay shorts; negative = shorts pay longs |

All features are computed independently for 5m, 1h, and 4h — giving the strategy three timeframe views.

**Precision:** Before any order is placed, `round_quantity()` and `round_price()` query the exchange's `exchangeInfo` endpoint (cached for 1 hour) and floor quantity to the symbol's `LOT_SIZE.stepSize` and round price to `PRICE_FILTER.tickSize`. Orders that fall below `MIN_NOTIONAL` are suppressed with a `wait` decision.

**Liquidity check:** If the proposed notional exceeds 10% of the top-5 book depth, `liquidity_ok` is flagged `false`. This is logged but does not currently hard-block execution — it's a signal quality warning.

---

### 7.2 Signal Generation

**Script:** `compute_signal.py`

The signal engine scores long and short setups independently and picks the winner.

#### Long scoring (7 factors, total weight 9)

| Factor | Weight | Condition for points |
|---|---|---|
| 4H trend up | 2 | `features_4h.trend == "up"` |
| 1H trend up | 2 | `features_1h.trend == "up"` |
| RSI long zone | 1.5 | RSI 45–68 (ideal entry, not overbought) |
| MACD bullish | 1 | MACD line > signal line |
| 5M timing up | 0.5 | 5m trend or momentum is up |
| Volume ok | 1 | volume_ratio ≥ 0.8 |
| Price above EMA20 | 1 | last_price > ema20 |
| Funding favours long | 0.5 | funding_rate < −0.0001 (shorts paying longs) |

#### Short scoring (mirrored)

| Factor | Weight | Condition |
|---|---|---|
| 4H trend down | 2 | `features_4h.trend == "down"` |
| 1H trend down | 2 | `features_1h.trend == "down"` |
| RSI short zone | 1.5 | RSI 32–55 |
| MACD bearish | 1 | MACD line < signal line |
| 5M timing down | 0.5 | 5m trend or momentum is down |
| Volume ok | 1 | volume_ratio ≥ 0.8 |
| Price below EMA20 | 1 | last_price < ema20 |
| Funding favours short | 0.5 | funding_rate > +0.0001 (longs paying shorts) |

**Decision logic:**
```
long_score  = (points earned) / (total possible points)
short_score = (points earned) / (total possible points)

if high_volatility and max(long_score, short_score) < 0.70:
    signal = "wait"  ← protect capital in volatile, unclear markets

elif long_score >= short_score and long_score >= 0.55:
    signal = "long"

elif allow_short and short_score > long_score and short_score >= 0.55:
    signal = "short"

else:
    signal = "wait"
```

#### Existing position signals

If the agent is already in a position on this symbol:

| Condition | Signal |
|---|---|
| Long position AND 1H + 4H both now trending down | `close` |
| Long position AND RSI > 78 | `close` (overbought exit) |
| Short position AND 1H + 4H both now trending up | `close` |
| Short position AND RSI < 22 | `close` (oversold exit) |
| None of the above | `hold` |

---

### 7.3 Confluence Scoring

**Script:** `compute_confluence.py`

Nine binary checks. Each either passes or fails. Confidence = `checks_passed / 9`.

| # | Check | What it verifies |
|---|---|---|
| 1 | `trend_alignment` | 1H trend matches signal; 4H at least neutral |
| 2 | `momentum_confirmation` | RSI-based momentum matches signal |
| 3 | `volume_confirmation` | volume_ratio ≥ 0.75 |
| 4 | `rsi_zone` | RSI in valid entry zone (long: 40–70, short: 30–60) |
| 5 | `macd_alignment` | MACD crossover matches direction |
| 6 | `reward_risk_ok` | `(take_profit − entry) / (entry − stop_loss) ≥ min_reward_risk` |
| 7 | `exposure_capacity_ok` | `current_exposure < max_total_exposure × 0.90` |
| 8 | `position_capacity_ok` | `open_positions < max_concurrent_positions` |
| 9 | `timeframe_confluence` | Both 1H AND 4H trend agree with direction |

**Stop and target calculation (used for checks 6 and 9):**

When ATR is available (normal):
```
stop_loss  = entry − (1.5 × ATR)   for longs
           = entry + (1.5 × ATR)   for shorts

take_profit = entry + (2.5 × ATR)  for longs
            = entry − (2.5 × ATR)  for shorts
```

Natural R:R = 2.5/1.5 = **1.67×** — above the default `min_reward_risk` of 1.5.

Fallback (no ATR):
```
stop_loss   = entry × 0.985  (longs) / entry × 1.015  (shorts)
take_profit = entry × 1.025  (longs) / entry × 0.975  (shorts)
```

**Entry threshold:** Confluence confidence must be ≥ **0.55** (5/9 passing) for a new trade. In high volatility, the bar rises to **0.70**.

---

### 7.4 Leverage Recommendation

**Script:** `recommend_leverage.py`

Leverage scales linearly with confidence, then steps down in high volatility:

| Confidence | Leverage |
|---|---|
| < 0.60 | `min_leverage` |
| 0.60 – 0.79 | `(min_leverage + max_leverage) / 2` |
| ≥ 0.80 | `max_leverage` |

If `high_volatility = true`: subtract 1 from the above result, floored at `min_leverage`.

**Learning cap:** The `effective_leverage_cap` from `state.json` (set by the learning system after loss streaks) further limits this. Effective leverage = `min(recommended, effective_leverage_cap)`.

---

### 7.5 Position Sizing

**Script:** `size_position.py`

Risk-based sizing: the stop-loss distance defines how much of your equity you're risking.

```
risk_usd         = equity × risk_pct_per_trade
stop_distance    = |entry_price − stop_loss| / entry_price  (as a fraction)
notional         = risk_usd / stop_distance
quantity         = notional / entry_price
margin_required  = notional / leverage
```

**Example:** equity=$1,000, risk=1%, entry=$85,000, SL=$84,412 (0.69% away), leverage=10×:
```
risk_usd       = $10
stop_distance  = 0.0069
notional       = $10 / 0.0069 = $1,449
→ capped at max_notional_per_trade ($500)
quantity       = $500 / $85,000 = 0.00588 BTC
margin         = $500 / 10 = $50
```

The notional is always capped at `max_notional_per_trade`. Quantity is then rounded down to the exchange's lot size precision.

---

### 7.6 Risk Checks

**Script:** `risk_checks.py`

Four hard checks that block execution regardless of signal quality:

| Check | Condition to BLOCK |
|---|---|
| Daily loss limit | `daily_loss_accumulated >= max_daily_loss` |
| Total exposure | `current_exposure + new_notional > max_total_exposure` (when limit set) |
| Per-trade notional | `new_notional > max_notional_per_trade` (when limit set) |
| Margin availability | `available_margin < required_margin` |

**Additional guards in the trade loop:**
- **Duplicate position guard:** If the agent already has an open position on a symbol (tracked in `state.json`), it will not open a new one — no position stacking.
- **Cooldown guard:** After closing a position on a symbol, new entries are blocked for `cooldown_after_close_sec` seconds.
- **Halt/circuit breaker check:** If `state.json` has `halt=true` or `circuit_breaker=true`, no execution happens at all.

---

### 7.7 Order Execution

**Script:** `live_execution_adapter.py` → `aster_readonly_client.py`

In `autonomous_live` mode, execution is immediate with no approval gate. Every trade is a **bracket order**:

```
place_bracket(symbol, entry_side, quantity, stop_loss_price, take_profit_price, leverage)
  │
  ├─ POST /fapi/v1/leverage       ← set leverage for symbol
  ├─ POST /fapi/v1/marginType     ← set ISOLATED margin (no cross-margin risk)
  ├─ POST /fapi/v1/order          ← entry MARKET order
  ├─ POST /fapi/v1/order          ← STOP_MARKET (reduce-only, opposite side)
  └─ POST /fapi/v1/order          ← TAKE_PROFIT_MARKET (reduce-only, opposite side)
```

All prices are rounded to the exchange's tick size. Quantities are floored to the step size. If any component of the bracket fails, it is logged; the learning system tracks the error toward the circuit breaker threshold.

---

### 7.8 Position Management

#### Trailing Stops

**Script:** `trailing_stop.py`

After each execution cycle, the agent checks all open positions and adjusts stop-losses upward (for longs) or downward (for shorts) as price moves in favour.

Two modes:

**ATR trail (default):**
```
new_stop = current_price − (ATR × 1.5)   (for longs)
new_stop = current_price + (ATR × 1.5)   (for shorts)
```
Only moves if `new_stop > old_stop` (for longs) — never moves against you.

**Breakeven trigger:**
When position PnL reaches 0.5%:
```
new_stop = entry_price × 1.001  (long: entry + 0.1% buffer)
new_stop = entry_price × 0.999  (short: entry − 0.1% buffer)
```

When the stop needs updating, the agent:
1. Cancels all existing `STOP_MARKET` orders for the symbol
2. Places a new `STOP_MARKET` order at the new level (reduce-only)
3. Updates `known_open_positions[symbol].stop_loss` in `state.json`

#### Position Monitoring

**Script:** `position_monitor.py`

Runs at the start of every cycle, before the trade loop. Compares `state.json`'s `known_open_positions` to live exchange data. When a position disappears (SL or TP hit):

1. Queries `/fapi/v1/income` to get the realised PnL
2. Classifies the trade as `win` (PnL > 0), `loss` (PnL < 0), or `breakeven`
3. Detects close reason: `stop_loss_hit`, `take_profit_hit`, or `unknown`
4. Updates the corresponding journal entry in `trades.json` with `outcome`, `realised_pnl`, `close_reason`, `closed_at`, and `lesson_tags`
5. Adds to `daily_loss` counter if it was a loss
6. Removes from `known_open_positions` in state

---

## 8. Self-Learning System

MoneySharks learns from every completed trade and adapts its behaviour without ever touching hard risk limits.

### What gets tracked

Every journal entry stores:
- Signal that triggered the trade
- Confluence score and which checks passed/failed
- Confidence at entry
- Market regime at entry time (`trending_up`, `trending_down`, `high_volatility`, `ranging`)
- Technical indicator values (RSI, MACD, trend, funding rate)
- Outcome: `win` / `loss` / `breakeven`
- Realised PnL
- Close reason
- Lesson tags generated by position_monitor

### Review cycle

**Script:** `fetch_trade_outcomes.py` + `review_trades.py` + `update_metrics.py`

Runs every 30 minutes (via cron) and also after every 5 new trades within the main runner.

**Step 1 — Fetch outcomes** (`fetch_trade_outcomes.py`):
- Queries `/fapi/v1/income` for REALIZED_PNL records
- Matches income records to open journal entries by symbol and time
- Writes `outcome`, `realised_pnl`, and `lesson_tags` back to `trades.json`

**Step 2 — Review** (`review_trades.py`):
Computes from the complete trade history:
- Win rate (wins / total closed)
- Average PnL per trade
- Total PnL
- Maximum consecutive loss streak
- Win rate on high-confidence trades (confidence ≥ 0.7)
- Performance by symbol
- Performance by market regime
- Lesson tags frequency

**Step 3 — Update metrics** (`update_metrics.py`):
Applies learning adaptations and writes to `state.json → metrics`:

| Adaptation | Trigger | Effect |
|---|---|---|
| Confidence multiplier (lower) | Loss streak ≥ 4 consecutive | Multiplies raw confidence by < 1.0, making it harder to reach the entry threshold |
| Confidence multiplier (recover) | Streak ≤ 1 AND win rate ≥ 55% | Restores multiplier toward 1.0 at 0.05/review |
| Effective leverage cap (lower) | Streak ≥ 3 OR win rate < 35% | Reduces the leverage ceiling by 1x per review |
| Effective leverage cap (recover) | Win rate ≥ 60%, streak = 0, ≥ 5 closed trades | Restores cap by 0.5x per review, never above `max_leverage` |
| Confidence threshold (raise) | High-confidence win rate > overall win rate by 10%+ | Raises `recommended_min_confidence` by 0.02, max 0.75 |
| Underperforming symbols | Symbol PnL < −$100 | Flags symbol in `metrics.underperforming_symbols` |

### What learning cannot do

The learning system has hard constraints:
- **Cannot raise leverage above `config.max_leverage`** — ever
- **Cannot remove stop-loss requirements**
- **Cannot change mode to a riskier mode**
- **Cannot modify hard risk limits**
- **Cannot suppress journaling**
- **Cannot rewrite the decision rules**

---

## 9. Cron Automation (24/7 Operation)

Four cron jobs drive continuous operation. They are registered automatically by the onboarding process.

### Jobs

| Job | Schedule | Description |
|---|---|---|
| `moneysharks-autonomous-live-scan` | Every 2 minutes | Main execution cycle. Calls `autonomous_runner.py`. The heartbeat of the system. |
| `moneysharks-post-trade-review` | Every 30 minutes | Fetches outcomes, runs review, updates learning metrics. |
| `moneysharks-daily-summary` | Daily at 00:00 UTC | Generates and announces a complete day summary with PnL, win rate, lessons, and any alerts. |
| `moneysharks-halt-check` | Every 15 minutes | Health check. Announces immediately if halt, circuit breaker, or ≥3 consecutive errors. Also warns if daily loss ≥ 80% of limit. |

### Cron Templates

All job definitions are in `openclaw-cron-templates.json`. The `/ABSOLUTE/PATH/TO/moneysharks` placeholder is substituted with the real skill path by `scripts/register_crons.py` during onboarding.

**To regenerate cron JSON manually:**
```bash
python3 scripts/register_crons.py config.json \
  --skill-root /path/to/moneysharks \
  --mode autonomous_live \
  --output register_crons.json
```

**To register a job manually (via OpenClaw agent):**
```
Read register_crons.json and call cron(action="add", job=<job dict>) for each active job.
```

### Cron behaviour on halt

When `halt=true` in `state.json`, the main scan cron job checks this at the start of every cycle and exits immediately (no execution). The health-check cron independently detects the halt and announces it.

---

## 10. State & Journal Files

### `state.json` — Live Agent State

```json
{
  "halt": false,
  "circuit_breaker": false,
  "consecutive_errors": 0,
  "daily_loss": 0.0,
  "last_run": "2026-03-17T22:00:00Z",
  "account": {
    "equity": 1250.50,
    "available_margin": 900.00,
    "daily_pnl": 45.20
  },
  "known_open_positions": {
    "BTCUSDT": {
      "side": "BUY",
      "quantity": 0.00588,
      "entry_price": 85000.0,
      "leverage": 10,
      "stop_loss": 84000.0,
      "take_profit": 87000.0,
      "opened_at": "2026-03-17T21:15:00Z"
    }
  },
  "last_close_ts": {
    "ETHUSDT": "2026-03-17T20:30:00Z"
  },
  "metrics": {
    "win_rate": 0.6667,
    "avg_pnl": 18.03,
    "total_pnl": 54.10,
    "max_loss_streak": 1,
    "confidence_multiplier": 1.0,
    "effective_leverage_cap": 10.0,
    "recommended_min_confidence": 0.55,
    "leverage_reduction_active": false,
    "lessons": []
  }
}
```

**Key fields:**

| Field | Description |
|---|---|
| `halt` | When `true`, all execution is blocked. Set by halt.py or emergency phrases. |
| `circuit_breaker` | Automatically set when `consecutive_errors >= 5`. Blocks execution until cleared. |
| `consecutive_errors` | Count of consecutive cycle errors. Resets to 0 on any successful cycle. |
| `daily_loss` | USD lost today. Resets at UTC midnight. |
| `known_open_positions` | The agent's record of open trades including stop/target levels for trailing stop management. |
| `last_close_ts` | Per-symbol timestamp of last close — used for cooldown enforcement. |
| `metrics` | Adaptive learning metrics updated by `update_metrics.py`. |

### `trades.json` — Complete Trade Journal

Every decision — including `wait` decisions — is journaled. A full entry looks like:

```json
{
  "ts": "2026-03-17T21:15:23Z",
  "symbol": "BTCUSDT",
  "mode": "autonomous_live",
  "decision": "long",
  "signal": "long",
  "signal_reason": "4H_trend_up, 1H_trend_up, RSI_long_zone:56.0, MACD_bullish, volume_ok:1.05",
  "confidence": 0.89,
  "adjusted_confidence": 0.89,
  "regime": "trending_up",
  "confluence": {
    "passed": ["trend_alignment", "momentum_confirmation", "volume_confirmation",
               "rsi_zone", "macd_alignment", "reward_risk_ok",
               "exposure_capacity_ok", "position_capacity_ok", "timeframe_confluence"],
    "failed": [],
    "count": 9,
    "total": 9,
    "confidence": 1.0
  },
  "order": {
    "entry_price": 85000.0,
    "stop_loss": 84412.0,
    "take_profit": 86980.0,
    "leverage": 10,
    "quantity": 0.00588,
    "notional": 499.80,
    "side": "BUY"
  },
  "exec_result": {
    "ok": true,
    "status": "EXECUTED",
    "order_result": {
      "entry": {"orderId": 123456789, "status": "FILLED"},
      "stop_loss": {"orderId": 123456790, "status": "NEW"},
      "take_profit": {"orderId": 123456791, "status": "NEW"}
    }
  },
  "status": "live_executed",
  "market": {
    "last_price": 85000.0,
    "mark_price": 85010.0,
    "funding_rate": -0.0001
  },
  "features_1h": {
    "rsi14": 56.0,
    "ema20": 84800.0,
    "ema50": 84200.0,
    "atr14": 392.0,
    "volume_ratio": 1.05,
    "trend": "up",
    "momentum": "up",
    "funding_rate": -0.0001
  },
  "outcome": "win",
  "realised_pnl": 31.20,
  "close_reason": "take_profit_hit",
  "closed_at": "2026-03-17T23:44:00Z",
  "lesson_tags": ["target-hit", "uptrend", "trending_up"]
}
```

---

## 11. Emergency Controls

### Halt phrases (say to OpenClaw agent)

Any of these immediately triggers a full halt:

```
halt moneysharks
stop trading
kill switch
emergency stop
```

### CLI halt

```bash
python3 scripts/halt.py config.json [OPTIONS]

Options:
  --cancel-orders    Cancel all open orders on Aster for each allowed symbol
  --flatten          Close all open positions at market price (CAUTION: slippage risk)
  --reason "text"    Custom reason string for the halt journal entry
  --data-dir <path>  Custom data directory (default: same as config.json)
```

### Halt sequence (automatic on any halt command)

1. `state.json → halt = true` — blocks all future cycle execution immediately
2. `state.json → circuit_breaker = true` — additional safety layer
3. Cron jobs check halt state at start of each run and exit immediately
4. If `execution.cancel_on_halt = true` (default): cancel all open orders for each allowed symbol via Aster API
5. If `--flatten` or `execution.flatten_on_emergency_stop = true`: market-close all open positions
6. Journal the halt event with timestamp and reason
7. Confirmation announced to user

### Resume

```bash
python3 scripts/resume.py config.json [OPTIONS]

Options:
  --mode paper|live|autonomous_live   Mode to resume in (default: paper — safer)
  --run-now                           Run first cycle immediately after resuming
  --data-dir <path>                   Custom data directory
```

**Resume sequence:**
1. Clears `halt = false`, `circuit_breaker = false`, `consecutive_errors = 0`
2. Updates `config.json` if mode changed
3. Fetches live account state from Aster (reconcile)
4. Journals the resume event
5. Runs first cycle if `--run-now`

> **Important:** Resuming into `autonomous_live` requires `autonomous_live_consent = true` already in config. You cannot resume into live mode if you declined at onboarding.

### Individual symbol controls

```
cancel orders for BTCUSDT    → cancels all orders for BTCUSDT only
close BTCUSDT position        → market-closes your BTCUSDT position
switch to paper mode          → changes mode to paper, no positions touched
```

### Circuit breaker

Auto-trips when `consecutive_errors >= 5`. Causes:
- API errors (network, auth, malformed response) — each counts as 1 error
- Any successful cycle resets the counter to 0

To clear manually:
```bash
python3 scripts/resume.py config.json --mode paper
```

Or by editing `state.json`:
```json
{ "circuit_breaker": false, "consecutive_errors": 0 }
```

---

## 12. Script Reference

### Core execution pipeline

| Script | Role | Called by |
|---|---|---|
| `autonomous_runner.py` | Main 24/7 entry point. Validates config, checks halt/CB state, runs position monitor + trade loops + trailing stops + post-trade review. | Cron (every 2 min) |
| `trade_loop.py` | Single-symbol execution cycle. Cooldown check, duplicate guard, full signal pipeline, execution by mode, journaling. | `autonomous_runner.py` |
| `market_scan_from_aster.py` | Fetches real multi-TF klines, account state, computes all features and the full order proposal. | `trade_loop.py` |
| `compute_features.py` | EMA, RSI, ATR, MACD, volume ratio, trend, momentum, high_volatility from kline array. | `market_scan_from_aster.py` |
| `compute_signal.py` | Long/short/wait/hold/close signal from multi-TF features, with funding rate bias. | `market_scan_from_aster.py` |
| `compute_confluence.py` | 9-point confluence check → confidence score. | `market_scan_from_aster.py` |
| `recommend_leverage.py` | Confidence + volatility → leverage recommendation within configured bounds. | `market_scan_from_aster.py` |
| `size_position.py` | Risk-based position sizing (equity × risk_pct / stop_distance). | `market_scan_from_aster.py` |
| `risk_checks.py` | Hard limit enforcement: daily loss, exposure, notional, margin. Blocks execution on failure. | `trade_loop.py` |
| `live_execution_adapter.py` | Gated live order submission. Calls `place_bracket()`. In autonomous_live: no approval gate. | `trade_loop.py` |
| `aster_readonly_client.py` | Full Aster DEX API client: market reads, account reads, order writes, precision rounding. | Many scripts |
| `position_monitor.py` | Detects position closes, queries income history for PnL, updates journal. | `autonomous_runner.py` |
| `trailing_stop.py` | ATR-trail and breakeven stop calculation. | `autonomous_runner.py` |

### Learning pipeline

| Script | Role |
|---|---|
| `fetch_trade_outcomes.py` | Queries `/fapi/v1/income` to match realised PnL to open journal entries. Writes outcome + lesson tags to `trades.json`. |
| `review_trades.py` | Analyses complete trade history: win rate, PnL, streaks, regime performance, lesson tag frequency. |
| `update_metrics.py` | Applies learning adaptations (confidence multiplier, leverage cap, confidence threshold) from review output. Writes to `state.json`. |
| `journal_trade.py` | Appends a single trade entry to `trades.json`. |

### Operations

| Script | Usage |
|---|---|
| `onboarding.py` | Interactive setup. Credential verification, config generation, consent gate, cron registration. |
| `register_crons.py` | Generates `register_crons.json` with real paths substituted. Called by onboarding. |
| `validate_config.py` | Validates `config.json`: required fields, mode, leverage bounds, notional vs exposure. Returns errors + warnings. |
| `reconcile_state.py` | Syncs `state.json` account fields with live Aster data. Stdin mode for pipeline use; CLI mode for startup reconciliation. |
| `halt.py` | Emergency halt: sets halt flag, cancels orders, optionally flattens positions, journals event. |
| `resume.py` | Resume from halt: clears state, optionally changes mode, reconciles. |
| `status.py` | Full status report: mode, halt, daily loss, open positions, win rate, metrics, lessons. Human-readable or `--json`. |
| `install.sh` | Verifies Python version, all scripts present and syntactically valid, config, credentials. |

### Approval / proposal mode

| Script | Usage |
|---|---|
| `aster_proposal_runner.py` | Generates an approval-gated order proposal using real Aster market data. For manual use in approval mode. |
| `approval_runner.py` | Emits a `PENDING_APPROVAL` proposal dict for a given order. |
| `approval_watch_runner.py` | Watcher stub for approval flows. |
| `paper_runner.py` | Paper simulation runner (legacy; main paper flow uses `autonomous_runner.py` with `mode=paper`). |

---

## 13. Aster DEX API Integration

### Base URL

```
https://fapi.asterdex.com
```

Override with `ASTER_BASE_URL` environment variable if needed.

### Authentication

Binance-compatible HMAC-SHA256 signing:
```
signature = HMAC_SHA256(secret, urlencode(params + timestamp))
```

Every authenticated request includes:
- `timestamp` millisecond Unix timestamp
- `signature` HMAC-SHA256 of the URL-encoded parameter string
- `X-MBX-APIKEY` header with your API key

### Endpoints used

**Public (no auth):**
- `GET /fapi/v1/ticker/price` — last traded price
- `GET /fapi/v1/premiumIndex` — mark price + funding rate
- `GET /fapi/v1/depth` — order book
- `GET /fapi/v1/klines` — OHLCV candlestick data
- `GET /fapi/v1/fundingRate` — funding rate history
- `GET /fapi/v1/exchangeInfo` — symbol filters (lot size, tick size, min notional)

**Private reads:**
- `GET /fapi/v2/account` — balances, margins, positions
- `GET /fapi/v2/positionRisk` — detailed position info
- `GET /fapi/v1/openOrders` — active orders
- `GET /fapi/v1/income` — realised PnL history
- `GET /fapi/v1/userTrades` — fill history

**Private writes:**
- `POST /fapi/v1/leverage` — set leverage per symbol
- `POST /fapi/v1/marginType` — set ISOLATED margin (always)
- `POST /fapi/v1/order` — place order (MARKET, STOP_MARKET, TAKE_PROFIT_MARKET)
- `DELETE /fapi/v1/order` — cancel specific order
- `DELETE /fapi/v1/allOpenOrders` — cancel all orders for symbol

### Retry logic

All API calls use `_request_with_retry()` with:
- Up to 3 retries
- **429 (rate limited):** exponential backoff, respects `Retry-After` header, max 30s wait
- **5xx (server error):** exponential backoff
- **4xx (client error):** no retry, error surfaced immediately

### Exchange precision

Before placing any order, quantities and prices are rounded to exchange-required precision using data from `exchangeInfo`:
- `round_quantity(symbol, qty)` — floors to `LOT_SIZE.stepSize`, uses `quantityPrecision` decimal places
- `round_price(symbol, price)` — rounds to `PRICE_FILTER.tickSize`, uses `pricePrecision` decimal places
- Exchange info is cached in-process for 1 hour to minimise API calls

### Credentials

Set as environment variables — **never** written to `config.json`:
```bash
export ASTER_API_KEY="your-api-key"
export ASTER_API_SECRET="your-api-secret"
```

---

## 14. Hard Safety Rules

These rules are enforced in every cycle and **cannot be overridden** by configuration, learning, or the agent's own decisions.

| Rule | Where enforced |
|---|---|
| `max_daily_loss` — trading halts when limit is hit | `risk_checks.py`, `trade_loop.py` |
| `max_total_exposure` — total open notional is capped | `risk_checks.py` |
| `max_notional_per_trade` — single trade size is capped | `market_scan_from_aster.py` (scaling), `risk_checks.py` (block) |
| `max_leverage` — leverage ceiling never exceeded | `recommend_leverage.py`, `update_metrics.py` |
| `require_stop_loss` — every bracket has a STOP_MARKET | `live_execution_adapter.py` |
| `require_take_profit` — every bracket has a TAKE_PROFIT_MARKET | `live_execution_adapter.py` |
| Stop-loss is always `reduce_only=true` — closes only, never opens | `aster_readonly_client.py.place_bracket()` |
| Margin type is always `ISOLATED` — position loss can't drain full account | `aster_readonly_client.py.set_margin_type()` |
| `halt=true` blocks all execution | `autonomous_runner.py`, `trade_loop.py` |
| `circuit_breaker=true` blocks all execution | `autonomous_runner.py` |
| Learning cannot raise leverage above `max_leverage` | `update_metrics.py` |
| Learning cannot change mode to a riskier mode | `update_metrics.py` |
| `autonomous_live_consent` cannot be set by the agent itself | `onboarding.py` consent gate |

---

## 15. Monitoring & Status

### Status command

```bash
python3 scripts/status.py config.json
python3 scripts/status.py config.json --json   # machine-readable
```

**Output example:**
```
🦈  MoneySharks Status
──────────────────────────────────────────────────
  Mode:              🤖 autonomous_live
  Halt:              no
  Circuit breaker:   clear
  Consecutive errors:0
  Daily loss:        $12.50 / $100.00 (12.5%)
  Last cycle:        3m ago
  Credentials:       ✓ loaded

  Account:
    Equity:          $1,250.50
    Available:       $900.00
    Today PnL:       $45.20

  Open Positions (1):
    BTCUSDT       LONG   qty=0.0059  entry=85000.0000  uPnL=$12.30

  Trade History:
    Total trades:    47  (executed=23, closed=18)
    Win rate:        66.7%  (12W / 6L)
    Total PnL:       $87.42
    Today:           3 trades  $45.20

  Adaptive Metrics:
    Win rate:        66.7%
    Avg PnL/trade:   $4.86
    Eff. lev cap:    10×
    Confidence mult: 1.00

  Config:
    Symbols:         BTCUSDT, ETHUSDT, SOLUSDT
    Base value:      $100.00 / trade
    Leverage:        2×–10×
    Max daily loss:  $100.00
    Cron:            enabled
```

### Daily summary

The `moneysharks-daily-summary` cron fires at 00:00 UTC and announces to your configured OpenClaw channel:

```
🦈 MoneySharks Daily Summary — 2026-03-17

Trades: 8 executed, 6 closed
Win rate: 66.7% (4W / 2L)
Today's PnL: +$45.20
Best trade: BTCUSDT long +$31.20 (TP hit)
Worst trade: ETHUSDT short −$18.50 (SL hit)

Symbols: BTCUSDT (3 trades), ETHUSDT (2 trades), SOLUSDT (1 trade)
Leverage used: 5×–10×

Lessons applied: None
Circuit breaker: clear
Halt events: 0
```

### Health alerts

The `moneysharks-halt-check` cron runs every 15 minutes and announces **only if there's a problem**:

- `halt = true` → 🛑 urgent alert
- `circuit_breaker = true` → ⚡ circuit breaker alert
- `consecutive_errors >= 3` → ⚠ error accumulation warning
- `daily_loss >= 80% of max_daily_loss` → ⚠ approaching daily limit

---

## 16. Operational Runbook

### Starting for the first time

```bash
# 1. Install and verify
bash install.sh

# 2. Set credentials
export ASTER_API_KEY="..."
export ASTER_API_SECRET="..."

# 3. Run onboarding
python3 scripts/onboarding.py

# 4. Verify first cycle runs clean
python3 scripts/autonomous_runner.py config.json

# 5. Check status
python3 scripts/status.py config.json
```

### Switching from paper to live

```bash
# Re-run onboarding (will show consent gate again)
python3 scripts/onboarding.py

# Type ACCEPT at the consent gate
# Onboarding re-writes config.json with mode=autonomous_live
```

### Temporarily pausing (no positions touched)

```bash
# Halt all execution (cancels orders, does NOT close positions)
python3 scripts/halt.py config.json --cancel-orders

# To resume in paper mode (safe)
python3 scripts/resume.py config.json --mode paper

# To resume in autonomous_live
python3 scripts/resume.py config.json --mode autonomous_live
```

### Emergency: close everything and stop

```bash
python3 scripts/halt.py config.json --cancel-orders --flatten --reason "emergency"
```

### Changing allowed symbols

1. Edit `config.json` → update `allowed_symbols`
2. Validate: `python3 scripts/validate_config.py < config.json`
3. The change takes effect on the next cron cycle automatically

### Adjusting leverage after bad streak

The learning system does this automatically. If you want to do it manually:
1. Edit `config.json` → lower `max_leverage`
2. Optionally also lower `min_leverage`
3. Changes take effect next cycle

### Checking what the agent is doing

```bash
# Full status
python3 scripts/status.py config.json

# Review recent trades
python3 scripts/review_trades.py < trades.json | python3 -m json.tool

# Tail the last 20 journal entries
python3 -c "
import json
trades = json.load(open('trades.json'))
for t in trades[-20:]:
    print(t.get('ts',''), t.get('symbol',''), t.get('decision',''), 
          t.get('status',''), t.get('outcome',''), t.get('realised_pnl',''))
"
```

### Resetting the learning system

If you want to start learning fresh (e.g. after changing strategy config):
```bash
# Edit state.json and reset metrics block
python3 -c "
import json
s = json.load(open('state.json'))
s['metrics'] = {
    'win_rate': 0.0, 'avg_pnl': 0.0, 'total_pnl': 0.0,
    'confidence_multiplier': 1.0, 'effective_leverage_cap': None,
    'recommended_min_confidence': 0.55, 'leverage_reduction_active': False, 'lessons': []
}
json.dump(s, open('state.json','w'), indent=2)
print('Metrics reset.')
"
```

### Deploying 24/7 on a Linux server (systemd)

```bash
# Copy the provided service file
sudo cp deploy.systemd.service /etc/systemd/system/moneysharks.service
sudo cp deploy.systemd.timer   /etc/systemd/system/moneysharks.timer

# Edit paths and user in the service file
sudo nano /etc/systemd/system/moneysharks.service

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable moneysharks.timer
sudo systemctl start moneysharks.timer

# Check status
sudo systemctl status moneysharks.timer
journalctl -u moneysharks.service -f
```

### Deploying 24/7 on macOS (launchd)

```bash
# Edit the plist with your paths
nano deploy.launchd.plist

# Install
cp deploy.launchd.plist ~/Library/LaunchAgents/com.moneysharks.scan.plist
launchctl load ~/Library/LaunchAgents/com.moneysharks.scan.plist

# Check
launchctl list | grep moneysharks
```

---

## 17. Frequently Asked Questions

**Q: Does MoneySharks guarantee profit?**  
A: No. Futures trading is inherently risky. MoneySharks is a mechanical system that acts on technical signals — it can and will have losing trades. The learning system and risk limits are designed to protect capital and improve performance over time, but past performance of the system does not guarantee future results.

**Q: Can I run MoneySharks on multiple accounts?**  
A: Yes — deploy separate instances in separate directories, each with their own `config.json` and `ASTER_API_KEY`/`ASTER_API_SECRET`. They operate independently.

**Q: How many API calls does it make?**  
A: Per symbol, per 2-minute cycle: approximately 9 API reads (ticker, mark price, depth, 3× klines, account, positions, orders). For 3 symbols: ~27 reads per cycle, ~810 reads per hour. Well within Aster's rate limits.

**Q: What happens if my machine restarts while there are open positions?**  
A: Positions on the exchange stay open regardless. When MoneySharks restarts, `position_monitor.py` reconciles `state.json` against the live exchange on the first cycle. Any positions opened before the restart are detected and tracked. New trailing stops are set if needed.

**Q: What if the API is down during a cycle?**  
A: The API client retries up to 3 times with exponential backoff. If all retries fail, the cycle exits with an error (logged). The `consecutive_errors` counter increments. After 5 consecutive errors, the circuit breaker trips and all execution pauses until you clear it.

**Q: Can the learning system make the agent more aggressive over time?**  
A: Only up to your configured `max_leverage`. The learning system can recover from a reduced leverage cap back toward your maximum if performance improves, but it cannot go beyond `max_leverage`. Confidence thresholds can be raised (making it harder to enter) but never lowered below their starting point.

**Q: Can I add new symbols while the agent is running?**  
A: Yes. Edit `config.json → allowed_symbols` and add the new symbol. The change takes effect on the next cron cycle without restart. Make sure the symbol exists on Aster Futures.

**Q: What is ISOLATED margin mode?**  
A: Every position uses only the margin allocated to it. If a position hits its stop-loss, only the margin for that position is at risk — it cannot drain your full account balance. MoneySharks always sets `ISOLATED` margin on every symbol before placing an order.

**Q: How do I know if a trade was a win or loss?**  
A: Check `trades.json`. After `fetch_trade_outcomes.py` runs (every 30 minutes or after each position close), entries with `status=live_executed` get populated with `outcome`, `realised_pnl`, and `close_reason`. You can also check the daily summary announcement or run `python3 scripts/status.py config.json`.

**Q: Can I run in paper mode and autonomous_live simultaneously?**  
A: No — there's one `config.json` and one `mode` setting. If you want to compare paper vs live, run two separate instances.

**Q: What does "circuit breaker" mean?**  
A: When 5 consecutive execution cycles fail with errors (API errors, parse errors, etc.), the circuit breaker trips automatically. All execution stops until you manually clear it with `resume.py`. This prevents the agent from hammering a broken API or placing erratic orders during instability.

**Q: Is my API key stored anywhere?**  
A: Only in your environment variables. It is never written to `config.json`, `state.json`, `trades.json`, or any file in the skill directory. Log output masks all keys (only last 4 characters shown).

---

*MoneySharks — Built for OpenClaw. Trade responsibly.*
