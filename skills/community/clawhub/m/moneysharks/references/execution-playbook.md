# Execution Playbook

## Cycle (runs every scan interval, default 2 min in autonomous_live)

1. Validate config (`scripts/validate_config.py`)
2. Reconcile account, position, and order state (`scripts/reconcile_state.py`)
3. Fetch live market data (REST + optional websocket)
4. Compute features (`scripts/compute_features.py`)
5. Compute signal (`scripts/compute_signal.py`)
6. Compute confluence (`scripts/compute_confluence.py`)
7. Compute leverage (`scripts/recommend_leverage.py`)
8. Size position (`scripts/size_position.py`)
9. Run risk checks (`scripts/risk_checks.py`)
10. Choose decision: `long` / `short` / `wait` / `hold` / `close`
11. Execute by mode (see below)
12. Journal the decision and market context (`scripts/journal_trade.py`)
13. On close: run post-trade review (`scripts/review_trades.py` + `scripts/update_metrics.py`)
14. Persist `trades.json` and `state.json`

## Execution by mode

### `paper`
- Simulate the order. Record hypothetical fill, PnL, slippage.
- No Aster API write calls.

### `approval`
- Prepare the order proposal.
- Present to user for confirmation.
- Only submit after explicit approval token.

### `live`
- Prepare the order.
- If `require_human_approval_for_live_orders=true`: present for confirmation, submit after approval.
- If `require_human_approval_for_live_orders=false`: submit immediately via `scripts/live_execution_adapter.py`.

### `autonomous_live` ← primary production mode
- Prepare the order.
- **Skip approval gate entirely** (user consented at onboarding).
- Submit immediately via `scripts/live_execution_adapter.py`.
- Do not pause, do not prompt, do not wait.
- If risk checks fail → output `wait`, journal the block, return.
- If circuit breaker trips → halt execution, notify user.

## Real-data flow

- `scripts/aster_readonly_client.py` — live market and account reads
- `scripts/market_scan_from_aster.py` — build scan from live exchange data
- `scripts/live_execution_adapter.py` — gated handoff to Aster API write endpoints
- `scripts/aster_proposal_runner.py` — used only in `approval` mode

## Journaling (mandatory on every cycle)

Every cycle must produce a journal entry regardless of whether a trade is placed.
Journal schema: timestamp, symbol, decision, signal, confluence, confidence, leverage, size, stop, target, pnl (if close), regime, notes.

## Learning loop (post-close)

After every position close:
1. Record realised PnL, entry/exit prices, slippage.
2. Run `scripts/review_trades.py` to analyse the closed trade.
3. Run `scripts/update_metrics.py` to update win rate, avg PnL, regime performance.
4. Persist updated metrics to `state.json`.
5. Carry updated confidence weights forward to the next cycle.
