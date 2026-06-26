# Live Execution Boundary

MoneySharks may execute live orders when all of the following are true:
- Credentials are loaded and valid (`ASTER_API_KEY` + `ASTER_API_SECRET` in environment).
- Config validates (passes `scripts/validate_config.py`).
- Mode is `live` or `autonomous_live`.
- `autonomous_live_consent=true` in config (required for `autonomous_live`).
- State is not halted (`state.json → halt=false`).
- Circuit breakers are not active (`state.json → circuit_breaker=false`).
- Risk checks pass (all hard limits respected by `scripts/risk_checks.py`).
- Daily loss limit has not been hit.

## Per-trade approval requirement

| Mode | Approval required per trade? |
|---|---|
| `paper` | N/A (simulation) |
| `approval` | Yes — always |
| `live` | Yes — unless `execution.require_human_approval_for_live_orders=false` |
| `autonomous_live` | **No** — user gave explicit consent at onboarding; approval gate permanently bypassed |

## What stays locked at all times (cannot be bypassed by any mode or learning)

- `max_daily_loss` — trading halts immediately when daily loss reaches this value
- `max_total_exposure` — hard cap on total notional across all positions
- `max_notional_per_trade` — hard cap per order
- `max_leverage` — never exceeded, not even under performance pressure
- `require_stop_loss` — every bracket trade places a STOP_MARKET order
- `require_take_profit` — every bracket trade places a TAKE_PROFIT_MARKET order
- Circuit breakers — API errors, rate-limit violations, unreconcilable state
- Emergency halt controls — always available regardless of mode
- `autonomous_live_consent` — cannot be set to true by self-modification; requires user to type ACCEPT at onboarding

## Execution path in autonomous_live

```
autonomous_runner.py (cron, every 2 min)
  └─ trade_loop.py (per symbol)
       ├─ market_scan_from_aster.py  ← real klines + account data
       ├─ compute_features.py        ← EMA, RSI, ATR, MACD
       ├─ compute_signal.py          ← long/short/wait/hold/close
       ├─ compute_confluence.py      ← confluence score
       ├─ recommend_leverage.py      ← volatility-adjusted leverage
       ├─ size_position.py           ← risk-based sizing
       ├─ risk_checks.py             ← hard limit enforcement
       └─ live_execution_adapter.py  ← place_bracket() → Aster API
            ├─ set_leverage()        ← POST /fapi/v1/leverage
            ├─ set_margin_type()     ← POST /fapi/v1/marginType (ISOLATED)
            ├─ place_order() MARKET  ← POST /fapi/v1/order (entry)
            ├─ place_order() STOP_MARKET ← POST /fapi/v1/order (SL)
            └─ place_order() TAKE_PROFIT_MARKET ← POST /fapi/v1/order (TP)
```

## Autonomous live mode: operating principles

- The agent treats every scan cycle as an autonomous decision point.
- It does not wait for user input between scan → signal → execution.
- Every decision (including `wait`) is journaled before the cycle completes.
- On any hard-limit breach, execution halts and the circuit breaker is set.
- State and trades are persisted after every cycle.
- On position close: review_trades.py + update_metrics.py run for learning.

## Do not

- Do not remove or weaken hard risk limits through self-learning or performance pressure.
- Do not silently raise leverage caps above configured maximums.
- Do not disable circuit breakers.
- Do not suppress journaling to speed up execution.
- Do not place unhedged orders without stop-loss when `require_stop_loss=true`.
