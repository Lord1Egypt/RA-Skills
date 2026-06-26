---
name: moneysharks
description: Fully autonomous 24/7 Aster DEX perpetual futures trading agent. Manages the complete lifecycle — onboarding, live execution, bracket orders, trailing stop management, position monitoring, risk enforcement, journaling, and self-learning from past trades — with zero per-trade approval required once the user gives explicit consent at onboarding. Use when the user wants to set up autonomous live trading on Aster DEX, onboard API credentials, run real-money trades continuously, manage open positions, enforce hard risk limits, review trade outcomes, or inspect adaptive learning metrics. Maximises ROI and profit within strictly configured risk bounds.
metadata:
  clawdis:
    primaryEnv: ASTER_API_KEY
    requires:
      env:
        - ASTER_API_KEY
        - ASTER_API_SECRET
---

# MoneySharks

Autonomous 24/7 Aster Futures perpetual trading agent. Purpose: generate the largest sustainable ROI from live leveraged futures trading on Aster DEX, operating continuously without per-trade human intervention, learning from every completed trade.

---

## Core rules

- **Require onboarding before any private API action.** Never use credentials that haven't been verified.
- **Default mode is `paper`** until the user completes onboarding and types `ACCEPT` at the consent gate.
- **In `autonomous_live` mode**: execute orders immediately — do NOT pause for per-trade human approval.
- **All hard risk limits are permanent**: daily loss cap, max exposure, max notional, leverage ceiling, stop-loss and take-profit requirements, circuit breakers. None can be overridden by configuration changes, learning, or performance.
- **Never hardcode secrets.** API key and secret live only in environment variables.
- **Never silently expand risk.** Never raise leverage above `max_leverage`, never change mode to a riskier mode without explicit user instruction.
- **Never self-modify hard risk rules.** The learning system adjusts confidence and leverage within bounds — it cannot rewrite the rules that define those bounds.
- **Journal every decision**, including `wait` decisions. No silent cycles.

---

## Modes

| Mode | Real Orders | Approval Per Trade | Description |
|---|---|---|---|
| `paper` | No | N/A | Full pipeline simulation. Real market data, no API writes. |
| `approval` | No | Yes | Generates proposals and waits for per-trade confirmation before submitting. |
| `live` | Yes | Configurable | Live execution. Per-trade approval gate controlled by `execution.require_human_approval_for_live_orders`. |
| `autonomous_live` | Yes | **No** | Full autonomy. Consent locked in once at onboarding. Executes every decision immediately 24/7. |

---

## Files in this skill

### Core skill file
- `SKILL.md` — this file

### Documentation
- `documentation-moneysharks.md` — **comprehensive human-readable documentation**: architecture, all config options, pipeline deep-dives, API integration details, operational runbook, FAQ. Read this for context before explaining anything to the user.

### References (read when needed)
- `references/onboarding.md` — onboarding flow, consent gate text, defaults, post-ACCEPT steps
- `references/strategy-framework.md` — multi-TF strategy principles (4H trend, 1H signal, 5M timing)
- `references/confluence-model.md` — 9-point confluence check definitions and confidence thresholds
- `references/leverage-policy.md` — leverage selection rules and volatility adjustments
- `references/risk-policy.md` — hard risk rules, circuit breaker conditions
- `references/execution-playbook.md` — step-by-step execution cycle for each mode
- `references/live-execution-boundary.md` — exactly what is and isn't gated in autonomous_live
- `references/review-and-learning.md` — what the learning system may and may not adapt
- `references/emergency-controls.md` — halt sequence, resume, circuit breaker, trigger phrases
- `references/cron-automation.md` — cron job intervals, 24/7 continuity rules
- `references/aster-readonly-integration.md` — API integration scope and guidance
- `references/aster-skill-map.md` — Aster skill family map
- `references/approval-execution.md` — approval mode flow
- `references/proposal-flow.md` — proposal generation and approval handoff
- `references/websocket-loop.md` — real-time data feed (advanced / optional)
- `references/deployment.md` — systemd / launchd deployment
- `references/packaging.md` — skill packaging
- `openclaw-cron-templates.json` — ready-to-use OpenClaw cron job definitions (paths substituted by `register_crons.py`)

### Scripts — live trading core (29 scripts total)

#### Entry point
- `scripts/autonomous_runner.py` — **main 24/7 entry point**. Called by cron every 2 min. Validates config + credentials, checks halt/circuit-breaker, runs `position_monitor.py` for all known open positions, runs `trade_loop.py` per symbol, runs trailing stop management for open positions, triggers post-trade review every 5 new trades. Writes `state.json` after every cycle.

#### Per-symbol execution loop
- `scripts/trade_loop.py` — single-symbol execution cycle. Enforces cooldown after close, duplicate position guard, learning-adjusted confidence threshold, and learning-capped leverage. Calls the full scan → risk → execute → journal pipeline. Handles `paper`, `live`, and `autonomous_live` execution branches. Updates `known_open_positions` in state on successful entry.

#### Market data and feature computation
- `scripts/market_scan_from_aster.py` — fetches real multi-TF klines (5m/1h/4h), ticker, mark price + funding rate, order book depth, and account bundle from Aster API. Computes all features, signal, confluence, leverage, and position size. Applies exchange precision rounding via `round_quantity()` / `round_price()`. Enforces `MIN_NOTIONAL` from exchangeInfo. Performs order-book liquidity check. Returns a complete order proposal or `null` for non-entry signals.
- `scripts/compute_features.py` — from a kline array: computes EMA20, EMA50, EMA12, EMA26, RSI14, ATR14, MACD line, MACD signal, volume ratio, trend (`up`/`down`/`neutral`), momentum (`up`/`down`/`neutral`), high_volatility flag. Accepts optional `funding_rate` passthrough.
- `scripts/compute_signal.py` — multi-TF weighted scoring for long and short. 7 factors each: 4H trend (weight 2), 1H trend (weight 2), RSI zone (1.5), MACD crossover (1), 5M timing (0.5), volume (1), EMA20 position (1). Incorporates funding rate bias (+0.5 weight). In high volatility raises the entry bar to 0.70. Generates `close` signal on trend reversal or extreme RSI with existing position.
- `scripts/compute_confluence.py` — 9-point binary check system: `trend_alignment`, `momentum_confirmation`, `volume_confirmation`, `rsi_zone`, `macd_alignment`, `reward_risk_ok`, `exposure_capacity_ok`, `position_capacity_ok`, `timeframe_confluence`. Confidence = checks_passed/9. Requires ≥ 0.55 for new entries (configurable via learning).

#### Sizing and risk
- `scripts/recommend_leverage.py` — maps confidence to leverage (min at < 0.60, midpoint at 0.60–0.79, max at ≥ 0.80). Steps down by 1 in high volatility. Result is further capped by `effective_leverage_cap` from learning metrics.
- `scripts/size_position.py` — risk-based position sizing: `notional = (equity × risk_pct) / stop_distance_pct`. Returns `risk_usd`, `stop_distance_pct`, `notional`, `margin`, `quantity`.
- `scripts/risk_checks.py` — four hard enforcement checks: daily loss limit hit, total exposure after trade vs `max_total_exposure`, per-trade notional vs `max_notional_per_trade`, available margin vs required margin. Also guards against zero notional. Only enforces limits that are set > 0.
- `scripts/prepare_order.py` — constructs the final order dict from sizing outputs (symbol, side, type, quantity, leverage, stop_loss, take_profit).

#### Execution
- `scripts/live_execution_adapter.py` — gated live execution. Checks credentials, enforces mode guard (only `live` or `autonomous_live`), enforces approval gate in `live` mode, skips gate in `autonomous_live`. Calls `aster.place_bracket()` → entry MARKET + STOP_MARKET + TAKE_PROFIT_MARKET. Returns full order result JSON.
- `scripts/aster_readonly_client.py` — **complete Aster DEX API client**. HMAC-SHA256 signing, retry logic (3 retries, exponential backoff, 429 `Retry-After` respect, 5xx retry). Exchange info cache (1h TTL). `round_quantity()`, `round_price()`, `get_symbol_filters()`. Public endpoints: ticker, mark price, depth, klines, funding rate, exchangeInfo. Private reads: account, positions, open orders, income history, user trades. Private writes: set_leverage, set_margin_type, place_order (MARKET / STOP_MARKET / TAKE_PROFIT_MARKET), cancel_order, cancel_all_orders, close_position_market, `place_bracket()`. CLI modes: `market`, `market_bundle`, `klines`, `account`, `mark_price`, `funding`, `set_leverage`, `cancel_all`, `income`, `trades`, `positions`.

#### Position lifecycle management
- `scripts/position_monitor.py` — runs at the start of every cycle. Compares `state.json → known_open_positions` to live Aster positions. When a position disappears: queries `/fapi/v1/income` for REALIZED_PNL, classifies outcome (`win`/`loss`/`breakeven`), detects close reason (`stop_loss_hit`/`take_profit_hit`/`unknown`), updates the matching journal entry in `trades.json` with `outcome`, `realised_pnl`, `close_reason`, `closed_at`, `lesson_tags`, `regime`. Adds to `daily_loss` on losses. Cleans up `known_open_positions`.
- `scripts/trailing_stop.py` — calculates updated stop-loss for an open position. Two modes: `atr` (trail = current_price ± ATR × 1.5) and `breakeven` (move SL to entry + buffer when PnL ≥ 0.5%). Never moves against the position. Called by `autonomous_runner.py` after trade loops. When `moved=true`, `autonomous_runner.py` cancels the old STOP_MARKET order and places a new one via `aster_readonly_client`.

#### Learning pipeline
- `scripts/fetch_trade_outcomes.py` — **backbone of the self-learning loop**. Queries `/fapi/v1/income` (REALIZED_PNL) for each symbol with unresolved journal entries. Matches income records by symbol and time. Writes `outcome`, `realised_pnl`, and `lesson_tags` into `trades.json`. For paper mode (with `--paper` flag): estimates outcome from current mark price vs recorded SL/TP levels. Returns counts of updated entries.
- `scripts/review_trades.py` — analyses `trades.json`: win rate, avg PnL, total PnL, max loss streak, lesson tag frequency, performance by symbol, performance by market regime (trending_up, trending_down, high_volatility, ranging), high-confidence trade win rate. Generates `lessons` list.
- `scripts/update_metrics.py` — applies learning adaptations from review to `state.json → metrics`. Adaptations: `confidence_multiplier` (lowered after ≥4 loss streak, recovered after winning), `effective_leverage_cap` (lowered after ≥3 streak or win_rate < 35%, recovered slowly), `recommended_min_confidence` (raised when high-confidence trades outperform), `underperforming_symbols` flag. All bounded by config limits — never raises leverage above `max_leverage`.
- `scripts/journal_trade.py` — appends one entry to `trades.json`. Sets `ts` if missing.

#### Setup and operations
- `scripts/onboarding.py` — interactive CLI onboarding. Step 1: reads/prompts credentials, verifies against Aster `/fapi/v2/account` live call (fails hard on bad creds). Step 2: collects symbols, base investment, leverage range, exposure limits, daily loss limit, allow_short. Step 3: presents consent gate — must type `ACCEPT` to enable `autonomous_live`. Step 4: writes `config.json`, calls `register_crons.py`, prints next steps.
- `scripts/register_crons.py` — substitutes `/ABSOLUTE/PATH/TO/moneysharks` placeholder in `openclaw-cron-templates.json` with the real skill root path. Selects which jobs to enable based on mode. Writes `register_crons.json`. Called automatically by `onboarding.py`.
- `scripts/validate_config.py` — validates `config.json`: all required fields present, valid mode, consent set for `autonomous_live`, leverage bounds sensible, notional vs exposure consistency, cron scan interval, symbols non-empty. Returns `{"ok": bool, "errors": [...], "warnings": [...]}`.
- `scripts/reconcile_state.py` — two modes. **Stdin mode** (`-`): accepts `{"account": {...}, "positions": [...], "orders": [...]}` JSON and returns a reconciled summary. **CLI mode**: fetches live account bundle from Aster API and updates `state.json → account` + `positions_snapshot` fields. Use at startup and after resume.
- `scripts/halt.py` — emergency halt CLI. Sets `halt=true` + `circuit_breaker=true` in `state.json`. Cancels all orders for each allowed symbol if `--cancel-orders` or `execution.cancel_on_halt=true`. Optionally flattens all open positions with `--flatten`. Accepts `--reason "text"`. Journals a `halt_event` entry. Prints confirmation.
- `scripts/resume.py` — resume from halt. Clears `halt=false`, `circuit_breaker=false`, `consecutive_errors=0`. Optionally switches mode (`--mode paper|autonomous_live`). Guards: cannot resume into `autonomous_live` without `autonomous_live_consent=true` in config. Fetches live account reconciliation. Journals a `resume_event`. Optionally runs first cycle (`--run-now`).
- `scripts/status.py` — live status report. Fetches account + positions from Aster API. Reads `state.json` and `trades.json`. Outputs: mode, halt, circuit breaker, consecutive errors, daily loss vs limit, last cycle age, credentials status, equity, available margin, today PnL, open positions with uPnL, trade stats (total/executed/closed, win rate, total PnL), adaptive metrics (win rate, avg PnL, eff leverage cap, confidence multiplier), active lessons, config summary. Human-readable by default; `--json` for machine output.

#### Approval / proposal mode helpers
- `scripts/aster_proposal_runner.py` — generates an approval-gated order proposal using real Aster market data. Calls `market_scan_from_aster.py` for the symbol, extracts price and order params, emits a `PENDING_APPROVAL` proposal with confidence, leverage, entry, SL, TP, and signal context.
- `scripts/approval_runner.py` — constructs a `PENDING_APPROVAL` proposal dict from order inputs. Used in `approval` mode trade loop.
- `scripts/approval_watch_runner.py` — returns a monitoring status dict indicating scan-journal-propose mode. Stub for approval watcher loop.
- `scripts/paper_runner.py` — legacy paper simulation runner (static file inputs). Main paper flow uses `autonomous_runner.py` with `mode=paper`.

### Config and data files
- `config.json` — your active configuration. Written by `onboarding.py`. Never commit with real credentials.
- `config.example.json` — annotated reference config with all fields and sensible defaults.
- `state.json` — live agent state: `halt`, `circuit_breaker`, `consecutive_errors`, `daily_loss`, `last_run`, `account`, `known_open_positions`, `last_close_ts`, `metrics`.
- `state.example.json` — state schema reference.
- `trades.json` — complete trade journal. Append-only during operation. Every decision logged.
- `trades.example.json` — trades schema reference.
- `register_crons.json` — generated by `register_crons.py` at onboarding. Contains ready-to-register OpenClaw cron job defs with real paths substituted.

### Setup
- `install.sh` — setup verification: Python 3.10+ check, all 21 required scripts present, all scripts syntax-valid, config validation, credentials check.
- `requirements.txt` — no pip dependencies (stdlib only). Documents optional advanced integrations.

### Deployment
- `deploy.systemd.service` / `deploy.systemd.timer` — Linux systemd unit files for 24/7 background deployment.
- `deploy.launchd.plist` — macOS launchd plist for 24/7 background deployment.
- `logrotate.moneysharks.conf` — Linux log rotation config.
- `newsyslog.moneysharks.conf` — macOS log rotation config.

---

## Workflow

### Per-cycle execution (called by cron every 2 min)

```
autonomous_runner.py config.json
 │
 ├─ 1. Validate config (validate_config.py)
 ├─ 2. Check credentials (ASTER_API_KEY / ASTER_API_SECRET)
 ├─ 3. Check halt + circuit_breaker → exit immediately if either is set
 ├─ 4. Reset daily_loss at UTC midnight
 │
 ├─ 5. Position monitoring (position_monitor.py)
 │       → compare known_open_positions vs live Aster positions
 │       → on close: fetch income, record outcome + PnL, tag lesson, update daily_loss
 │
 ├─ 6. Per symbol: trade_loop.py
 │       a. Halt / circuit_breaker check
 │       b. Daily loss limit check → block if hit
 │       c. Cooldown check → skip if closed recently
 │       d. Duplicate position guard → skip if already positioned
       ← cooldown_after_close_sec prevents immediate re-entry on same symbol
 │       e. market_scan_from_aster.py:
 │            - fetch klines (5m/1h/4h) + ticker + mark price + depth + account
 │            - compute_features.py (EMA/RSI/ATR/MACD, funding rate) for each TF
 │            - compute_signal.py (weighted scoring, funding rate bias, hold/close logic)
 │            - compute_confluence.py (9 checks → confidence)
 │            - recommend_leverage.py (confidence + volatility → leverage)
 │            - size_position.py (equity × risk_pct / stop_distance)
 │            - round_quantity + round_price (exchange precision)
 │            - min_notional check → suppress if too small
 │            - liquidity check (order vs order book depth)
 │       f. Apply learning feedback:
 │            - adjusted_confidence = confidence × confidence_multiplier
 │            - if adjusted_confidence < recommended_min_confidence → wait
 │            - cap leverage at effective_leverage_cap
 │       g. risk_checks.py (daily loss, exposure, notional, margin, zero notional guard)
 │       h. Execute by mode:
 │            paper         → simulate, record as paper_executed
 │            autonomous_live → live_execution_adapter.py → place_bracket() → Aster API
 │            live          → live_execution_adapter.py (with optional approval gate)
 │            approval      → approval_runner.py → emit PENDING_APPROVAL
 │       i. On successful autonomous_live entry: update known_open_positions in state
 │       j. Journal entry (always, including wait decisions)
 │       k. Save state.json
 │
 ├─ 7. Trailing stop management (open positions in autonomous_live):
 │       → trailing_stop.py for each known_open_position
 │       → if moved: cancel old STOP_MARKET, place new one via aster API
 │       → update known_open_positions[symbol].stop_loss in state
 │
 ├─ 8. Update state.json (last_run, consecutive_errors, circuit_breaker if errors ≥ 5)
 │
 └─ 9. Post-trade review (every 5 new trades):
         fetch_trade_outcomes.py → income history → resolve outcomes in trades.json
         review_trades.py       → win rate, PnL, streaks, regime performance
         update_metrics.py      → adapt confidence_multiplier, leverage cap, threshold
         save updated metrics to state.json
```

### Onboarding flow

```
onboarding.py
 │
 ├─ 1. Read ASTER_API_KEY + ASTER_API_SECRET from env (prompt if missing)
 ├─ 2. Verify credentials: GET /fapi/v2/account → fail hard if invalid
 ├─ 3. Collect: symbols, base_value, max_leverage, min_leverage,
 │              max_total_exposure, max_daily_loss, allow_short
 ├─ 4. Show consent gate with full risk summary
 ├─ 5. User types ACCEPT or DECLINE
 │
 ├─ On ACCEPT:
 │     - Write config.json (mode=autonomous_live, consent=true, cron.enabled=true)
 │     - register_crons.py → register_crons.json (paths substituted)
 │     - Agent calls cron(action="add", job=...) for each active job (see below)
 │     - Run first cycle: autonomous_runner.py config.json
 │     - Show status: status.py config.json
 │
 └─ On DECLINE:
       - Write config.json (mode=paper, consent=false, cron.enabled=false)
       - register_crons.py → register_crons.json (paper jobs only)
       - Instruct user to re-run onboarding when ready to go live
```

### Post-ACCEPT: register cron jobs (agent executes these steps)

After writing `config.json` and generating `register_crons.json`, the agent reads the file and calls `cron(action="add", job=...)` for each of the four active jobs:

| Job key | Schedule | sessionTarget | delivery |
|---|---|---|---|
| `autonomous_live_scan` | `*/2 * * * *` UTC | isolated | none |
| `autonomous_review` | `*/30 * * * *` UTC | isolated | none |
| `autonomous_daily_summary` | `0 0 * * *` UTC | isolated | announce |
| `halt_check` | `*/15 * * * *` UTC | isolated | announce |

The exact job JSON (with real paths) is already written to `register_crons.json` by `register_crons.py`. The agent reads each entry and passes it directly to `cron(action="add")`.

---

## Onboarding requirements

Collect only the essentials — everything else uses sensible defaults:

| Input | Required | Default | Notes |
|---|---|---|---|
| `ASTER_API_KEY` | Yes | — | Verified live against Aster API before proceeding |
| `ASTER_API_SECRET` | Yes | — | Never written to config.json |
| `allowed_symbols` | Yes | BTCUSDT, ETHUSDT, SOLUSDT | Must be valid Aster Futures symbols |
| `base_value_per_trade` | Yes | 100 | USD reference investment per trade |
| `max_leverage` | Yes | 10 | Hard ceiling — never exceeded |
| `min_leverage` | No | 2 | Floor for low-confidence setups |
| `max_total_exposure` | No | base_value × 10 | Total open notional cap |
| `max_daily_loss` | No | total_exposure × 10% | Daily loss hard stop |
| `allow_short` | No | true | Set false for long-only mode |
| Consent: ACCEPT | Yes | — | Cannot be set programmatically — user must type it |

Full config field reference: `documentation-moneysharks.md` § 5.

---

## Signal generation summary

Signals from `compute_signal.py` (weighted scoring, each factor contributes independently):

| Factor | Weight | Long condition | Short condition |
|---|---|---|---|
| 4H trend | 2.0 | trend == "up" | trend == "down" |
| 1H trend | 2.0 | trend == "up" | trend == "down" |
| RSI zone | 1.5 | RSI 45–68 | RSI 32–55 |
| MACD crossover | 1.0 | MACD > signal | MACD < signal |
| 5M timing | 0.5 | 5m trend/momentum up | 5m trend/momentum down |
| Volume | 1.0 | volume_ratio ≥ 0.8 | volume_ratio ≥ 0.8 |
| EMA20 position | 1.0 | price > EMA20 | price < EMA20 |
| Funding rate bias | 0.5 | funding < −0.0001 | funding > +0.0001 |

Entry threshold: score ≥ 0.55. High-volatility override: threshold raised to 0.70.  
`wait` if neither long nor short meets threshold.  
`hold` / `close` logic runs when a position is already open (trend reversal, extreme RSI).

---

## Confluence scoring (9-point system)

Implemented in `compute_confluence.py`. Confidence = checks_passed / 9.

| Check | Passes when |
|---|---|
| `trend_alignment` | 1H trend matches direction; 4H at least neutral |
| `momentum_confirmation` | RSI-based 1H momentum matches direction |
| `volume_confirmation` | volume_ratio ≥ 0.75 |
| `rsi_zone` | RSI in valid entry zone (long 40–70, short 30–60) |
| `macd_alignment` | MACD line above signal (long) / below signal (short) |
| `reward_risk_ok` | `(take_profit − entry) / (entry − stop_loss) ≥ min_reward_risk` |
| `exposure_capacity_ok` | current_exposure < max_total_exposure × 0.90 |
| `position_capacity_ok` | open_positions < max_concurrent_positions |
| `timeframe_confluence` | Both 1H AND 4H trend align with direction |

Minimum confidence to enter: **0.55** (5/9). Raises to **0.70** in high volatility.

Stop/target defaults (when ATR available): SL = entry ± 1.5×ATR, TP = entry ± 2.5×ATR → natural R:R 1.67×.

---

## Learning system summary

Three-step cycle after every set of closed trades:

1. `fetch_trade_outcomes.py` — pulls REALIZED_PNL from `/fapi/v1/income`, resolves `outcome` + `realised_pnl` + `lesson_tags` in `trades.json`
2. `review_trades.py` — computes win rate, avg PnL, loss streak, regime performance
3. `update_metrics.py` — applies bounded adaptations to `state.json → metrics`:

| Metric | What it does | Bounds |
|---|---|---|
| `confidence_multiplier` | Multiplied into raw confidence score before threshold check. < 1.0 makes entry harder. | 0.70 floor; recovers toward 1.0 |
| `effective_leverage_cap` | Caps the leverage recommended by `recommend_leverage.py`. | `min_leverage` floor; `max_leverage` ceiling — hard |
| `recommended_min_confidence` | Entry threshold. Raised when high-confidence trades outperform. | 0.55 default; 0.75 max |
| `leverage_reduction_active` | Flag indicating leverage has been reduced by learning. | Bool only |
| `underperforming_symbols` | Symbols with total PnL < −$100. Informational. | — |

**Learning cannot**: raise leverage above `max_leverage`, change mode to riskier, suppress journaling, remove stop-loss requirements.

---

## Hard safety rules (always enforced, cannot be bypassed)

| Rule | Enforcement point |
|---|---|
| `max_daily_loss` — blocks ALL entries when daily loss hits limit | `trade_loop.py`, `risk_checks.py` |
| `max_total_exposure` — caps total open notional | `risk_checks.py` |
| `max_notional_per_trade` — scales down + hard blocks oversized trades | `market_scan_from_aster.py`, `risk_checks.py` |
| `max_leverage` — hard ceiling on all leverage | `recommend_leverage.py`, `update_metrics.py` |
| `require_stop_loss` — every live trade has STOP_MARKET | `live_execution_adapter.py` |
| `require_take_profit` — every live trade has TAKE_PROFIT_MARKET | `live_execution_adapter.py` |
| ISOLATED margin — per-position loss cannot drain full account | `aster_readonly_client.py → place_bracket()` |
| `reduceOnly=true` on SL/TP — closing orders never open new positions | `aster_readonly_client.py → place_order()` |
| `halt=true` blocks all execution | `autonomous_runner.py`, `trade_loop.py` |
| `circuit_breaker=true` blocks all execution | `autonomous_runner.py` |
| Consecutive errors ≥ 5 auto-trips circuit breaker | `autonomous_runner.py` |
| Learning cannot raise leverage above `max_leverage` | `update_metrics.py` |
| `autonomous_live_consent` cannot be set by agent self-action | `onboarding.py` consent gate only |

---

## Emergency controls

### Trigger phrases (say to OpenClaw agent)

```
halt moneysharks      stop trading       kill switch
emergency stop        cancel all orders  flatten all positions
switch to paper mode  disable cron
```

### Halt sequence (automatic on any trigger phrase)

1. Set `state.json → halt=true`, `circuit_breaker=true`
2. Cancel all open orders for each allowed symbol (if `execution.cancel_on_halt=true` — default)
3. Close all positions (only if `--flatten` flag or `execution.flatten_on_emergency_stop=true`)
4. Journal a `halt_event` entry in `trades.json`
5. Announce: "MoneySharks halted. Cycles stopped. Orders cancelled. Positions: [status]. Say 'resume moneysharks' to restart in paper mode."

**CLI:**
```bash
python3 scripts/halt.py config.json --cancel-orders [--flatten] [--reason "text"]
```

### Resume sequence

```bash
python3 scripts/resume.py config.json --mode paper       # safe default
python3 scripts/resume.py config.json --mode autonomous_live   # requires consent in config
```

1. Clear `halt=false`, `circuit_breaker=false`, `consecutive_errors=0`
2. Update `config.json` mode if changed
3. Fetch live account reconciliation from Aster
4. Journal `resume_event`
5. Run first cycle if `--run-now`

> Resuming into `autonomous_live` requires `autonomous_live_consent=true` already in `config.json`. It cannot be set by the resume script — only by onboarding ACCEPT.

### Circuit breaker

- Auto-trips when `consecutive_errors >= 5`
- Any successful cycle resets the counter to 0
- Clear via `resume.py` or by editing `state.json`

---

## Cron jobs (24/7 autonomous operation)

All defined in `openclaw-cron-templates.json`. Paths auto-substituted by `register_crons.py`.  
Registered automatically by the agent at the end of onboarding (on ACCEPT).

| Job | Schedule | What it runs | Delivery |
|---|---|---|---|
| `moneysharks-autonomous-live-scan` | every 2 min | `autonomous_runner.py config.json` | none (silent) |
| `moneysharks-post-trade-review` | every 30 min | `fetch_trade_outcomes.py` + `review_trades.py` | none (silent) |
| `moneysharks-daily-summary` | 00:00 UTC daily | `status.py` + `review_trades.py` → full day summary | **announce** |
| `moneysharks-halt-check` | every 15 min | `status.py --json` → alert if halt/CB/errors/daily loss approaching | **announce** (only on problem) |

**In paper mode**: `autonomous_live_scan` and `autonomous_review` are replaced by:
- `moneysharks-paper-market-scan` (every 5 min)
- `moneysharks-paper-review-cycle` (every 30 min)

---

## Status and monitoring

```bash
python3 scripts/status.py config.json          # human-readable
python3 scripts/status.py config.json --json   # machine-readable JSON
```

Shows: mode, halt, circuit breaker, consecutive errors, daily loss %, last cycle age, credentials, equity, available margin, today PnL, open positions with uPnL, win rate, avg PnL, total PnL, adaptive metrics, active lessons, config summary.

---

## Key data files

### `state.json` structure

```json
{
  "halt": false,
  "circuit_breaker": false,
  "consecutive_errors": 0,
  "daily_loss": 0.0,
  "last_run": "2026-03-17T22:00:00Z",
  "account": { "equity": 1250.50, "available_margin": 900.00 },
  "known_open_positions": {
    "BTCUSDT": {
      "side": "BUY", "quantity": 0.00588, "entry_price": 85000.0,
      "leverage": 10, "stop_loss": 84000.0, "take_profit": 87000.0,
      "opened_at": "2026-03-17T21:15:00Z"
    }
  },
  "last_close_ts": { "ETHUSDT": "2026-03-17T20:30:00Z" },
  "metrics": {
    "win_rate": 0.6667, "avg_pnl": 18.03, "total_pnl": 54.10,
    "confidence_multiplier": 1.0, "effective_leverage_cap": 10.0,
    "recommended_min_confidence": 0.55, "leverage_reduction_active": false,
    "lessons": []
  }
}
```

### `trades.json` entry structure (executed trade)

```json
{
  "ts": "2026-03-17T21:15:23Z",
  "symbol": "BTCUSDT",
  "mode": "autonomous_live",
  "decision": "long",
  "signal": "long",
  "signal_reason": "4H_trend_up, 1H_trend_up, RSI_long_zone:56.0, MACD_bullish",
  "confidence": 0.89,
  "adjusted_confidence": 0.89,
  "regime": "trending_up",
  "confluence": { "passed": [...], "failed": [], "count": 9, "total": 9, "confidence": 1.0 },
  "order": {
    "entry_price": 85000.0, "stop_loss": 84412.0, "take_profit": 86980.0,
    "leverage": 10, "quantity": 0.00588, "notional": 499.80, "side": "BUY"
  },
  "exec_result": { "ok": true, "status": "EXECUTED", "order_result": { ... } },
  "status": "live_executed",
  "market": { "last_price": 85000.0, "mark_price": 85010.0, "funding_rate": -0.0001 },
  "features_1h": { "rsi14": 56.0, "ema20": 84800.0, "atr14": 392.0, "trend": "up" },
  "outcome": "win",
  "realised_pnl": 31.20,
  "close_reason": "take_profit_hit",
  "closed_at": "2026-03-17T23:44:00Z",
  "lesson_tags": ["target-hit", "uptrend", "trending_up"]
}
```

---

## Quick reference: when something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| No trades being placed | Confidence below threshold, or `wait` signal | Check `status.py`, review recent journal entries |
| Circuit breaker active | ≥5 consecutive API errors | `resume.py --mode paper`, investigate logs |
| Daily loss limit hit | Too many losses today | Waits for UTC midnight to reset, or lower `max_daily_loss` |
| Halt active | Manual or automatic halt | `resume.py config.json --mode paper` |
| Credential error | `ASTER_API_KEY`/`ASTER_API_SECRET` not set | Set env vars, re-run `install.sh` to verify |
| Trades have no outcome | `fetch_trade_outcomes.py` hasn't run yet | Run manually or wait for next 30-min review cron |
| Leverage too high in learning | Loss streak triggered `effective_leverage_cap` reduction | Wait for recovery, or reset metrics in `state.json` |

For full operational runbook, see `documentation-moneysharks.md` § 16.
