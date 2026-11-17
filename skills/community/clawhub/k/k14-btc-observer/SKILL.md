---
name: k14-btc-observer
description: Run the complete BTC K14 strategy in paper mode with dynamic exits, a persistent ledger and a separate Simmer virtual SIM execution mirror.
metadata:
  version: "0.2.0"
  displayName: BTC K14 Paper Trader
  difficulty: advanced
---

# BTC K14 Paper Trader

This upgrades the former observation-only skill to the full, frozen K14 strategy in **paper trading only**. Read [DISCLAIMER.md](DISCLAIMER.md). No live trading switch, wallet signing, or real-money order endpoint is included. Never present hypothetical fills as exchange receipts or API connection-test trades as strategy performance.

## Run

Provide `SIMMER_API_KEY` through the runtime's secret environment and a persistent `K14_STATE_DIR`. Never put secrets in this package, messages, logs or ClawHub. Install the pip dependencies from `clawhub.json`, then run:

```sh
python paper_agent.py --action run
```

Default duration is 1800 seconds; `K14_RUN_SECONDS` accepts 10–86400. `--state-dir` and `--seconds` override those defaults. Reuse the same state directory across runs. A process lock rejects overlapping runs on the same filesystem. Managed runners with isolated disks must not run multiple copies for one API key; local locking does not establish distributed exclusivity.

`python paper_agent.py --action status` only reads the Simmer virtual portfolio and receipts. `--action smoke` spends up to **1 virtual SIM**, buys then sells on an active Bitcoin simulation market to verify connectivity. Smoke uses `sdk:k14-connection-test`, distinct from strategy `sdk:k14-paper-v020`; it is never strategy profit evidence. Do not run smoke on a schedule. No user money is spent.

Create a file named `STOP` inside the state directory to stop the running process cleanly. Remove it only when explicitly resuming. Publication and an automaton manifest do not prove a Simmer-hosted process exists: retrieve its actual run report first.

## Complete strategy

The bundled, hash-verified `TrialSession` and `ParallelExit` implement K14 on the last 14 completed Binance BTCUSDT 15-minute candles; frozen q=0.05 monthly thresholds; official Polymarket PTB; price/volatility/clock/book/fee validation; post-only Maker entry in the first 120 seconds; at most 5 shares and one entry window per persistent test account. Initial model cash is 50, daily risk 6 and total risk 20. Maximum entry price .48, minimum .30; opposite-leg price cap .50 and fee-inclusive paired cost cap .95.

Exit profile `continuous-decay-v1` compares passive sell, direct FOK sell and opposite-side FOK buy then Merge. Target net profit per share at window ages 0/180/360/540/720 seconds is .12/.09/.06/.03/.01. Replacement waits for terminal receipts; partial fills retain exact quantity. No new buying after 840 seconds. At 900 seconds cancel and reconcile, then Redeem only after an official resolved outcome. Losing unresolved single-sided positions can settle to zero; this strategy has no automatic below-cost stop-loss.

The frozen October 2026 threshold file is not valid in November. Missing or expired thresholds block new signals. Never silently retune gates to make an entry happen.

## Two distinct ledgers

1. `paper.sqlite`: complete-strategy model. Maker fills require a later fresh public book to cross strictly through the limit after a modeled 250 ms delay; touching a quote is not enough. Visible depth limits partial quantity. FOK is all-or-none on displayed depth. Cancellation/confirmation and Merge are simulated locally. Taker fees use the frozen model; Merge reserve is .00001/share. All receipts are labeled `LOCAL_HYPOTHETICAL_TRADE_THROUGH_V1`. These assumptions do not establish actual queue fills, latency or profitability.
2. `simmer.sqlite`: actual **virtual SIM** API requests and responses. On modeled BUY/SELL fills, the mirror submits `venue="sim"` with `execute=false`; it uses actual LMSR receipt quantities for later proportional sells. Source-market tokens must match. LMSR price, quantity, rounding and fills differ from Polymarket. Native Simmer simulation does not provide this strategy's Maker queue, cancel or Merge operations. A modeled Merge is recorded only in the local ledger; mirrored paired SIM positions remain for platform settlement. Do not add local Merge proceeds to the Simmer cash balance.

The mirror allows at most 2.5 SIM per buy and 6 SIM cumulative buys for this initial test, including the optional 1 SIM smoke. It pauses after ambiguous or rejected mirror execution for reconciliation; it never automatically resends an uncertain POST. Keys are attached only to `api.simmer.markets`; redirects are refused. Wallet/private-key endpoints and real venues are not exposed.

## Inspect evidence

`report.json` shows process status, public feed health, K14 signal, pending modeled orders, model cash/fees/payouts, mirror status and zero real-money orders. `simmer-status.json` contains the virtual portfolio and real API receipts for virtual trades. `paper.sqlite` retains commands, hypothetical fills and settlements atomically with checkpoints. `simmer.sqlite` persists each request before transmission and records idempotency keys and unknown outcomes. Restart preserves cash, open positions and the one-window budget.

The reviewed core is bundled in `vendor/`, so it needs no local source repository. `source-pins.json` verifies integrity. `portability-change.json` records the only platform-import adjustment; entry and exit logic remain identical. Network disconnects, stale feeds, unknown settlement, virtual API rejection and lack of a current K14 signal are observable states, not permission to fabricate trades.
