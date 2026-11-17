---
name: mlb-live-trader
description: Use when comparing live MLB win probabilities with executable prediction-market prices through Simmer.
metadata:
  author: "kvzsolt"
  version: "2.2.1"
  displayName: "MLB Live Trader"
  difficulty: "intermediate"
---

# MLB Live Trader

MLB Live Trader compares ESPN's in-game home-win probability with executable MLB prediction-market prices available through Simmer.

> **Trading framework, not a verified edge.** Read [DISCLAIMER.md](DISCLAIMER.md) before use. Paper mode is the default; `--live` can submit real-money orders that may lose their full value.

> **This is a template.** Its signal, safeguards, and execution path are deterministic, but the thresholds have not been demonstrated to produce positive after-cost returns. Validate calibration, latency, fills, and drawdown out of sample before changing limits.

The strategy follows:

`scan → score → gate → size → execute`

It uses only `SimmerClient` for market access and trade execution. It never imports a Polymarket order client, never hardcodes a market ID, and never enables live execution without the explicit `--live` flag.

## Method

1. Scan in-progress MLB games from ESPN and require a usable in-game home-win probability.
2. Discover active Polymarket-backed MLB markets with Simmer's public `get_markets()` API, server-side MLB filters, and `sort="volume"`.
3. Reject props, totals, run lines, inning/series contracts, futures, ambiguous doubleheaders, foreign opponents, and resolution windows that do not match the current ESPN game.
4. Read the executable top of book. A real ask has priority; on standard binary markets `1 - best_bid` can supply the opposite outcome ask, while neg-risk NO orders require their own explicit executable ask. Midpoint pricing is fallback-only.
5. Score both YES and NO after reported fees, quote age, spread, inning, and source-quality penalties.
6. Gate paper candidates at a 2% clean late-game net edge and live candidates at 3%; weaker or older evidence raises the required edge.
7. Size approved candidates with `simmer_sdk.sizing.size_position()`, then apply the per-order, bankroll-fraction, daily-budget, and five-share minimum checks without rounding a small order upward.
8. Submit a bounded FAK buy tagged with `source=sdk:mlb-live-trader` and `skill_slug=mlb-live-trader`.

## Setup

Install the published skill:

```bash
npx clawhub@0.23.3 install @kvzsolt/mlb-live-trader
```

Or run a source checkout:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export SIMMER_API_KEY="your-simmer-api-key"
export TRADING_VENUE=polymarket
```

Keep credentials in an environment-managed secret. Do not write API or wallet keys to `config.json`, source files, shell history, issue reports, or logs.

## Paper mode

```bash
.venv/bin/python mlb_live_trader.py
```

Paper mode is the default. It uses Simmer's simulated trade path and never reads or writes the live risk-state file.

## Live mode

```bash
.venv/bin/python mlb_live_trader.py --initialize-live-state
.venv/bin/python mlb_live_trader.py --live
```

Live mode is explicit and requires `TRADING_VENUE=polymarket`; any other venue stops before client construction. Before the first live run, stop every older scheduler for this skill and run `--initialize-live-state` by itself. That command uses an SDK-enforced read-only live client. If no valid central or importable v2.1 ledger exists, it creates an empty ledger only when the entire Polymarket account has no open positions and no successful, failed, cancelled, or expired trade receipt in the preceding 96 hours. The proof is intentionally account-wide because the pinned SDK trade-history method has no source filter. There is no force flag: if the proof is not clean, reconcile the account or wait until it is clean.

After initialization, `--live` requires an ESPN timestamp no older than 90 seconds, an executable quote whose server age plus all local processing time is no older than 60 seconds, an exact team-and-game-window match, and available Simmer context. Signal and quote freshness are rechecked after durable reservation and immediately before the SDK POST; an expired candidate releases its reservation without submitting. `--no-safeguards` only skips optional context checks in paper mode. A whole-run lock blocks overlapping live processes. Missing, corrupt, future-dated, or inconsistent risk state stops the run instead of resetting spend limits.

Before each reservation, a Simmer preflight must confirm Polymarket live authorization, wallet readiness, available collateral, and account-wide cross-venue exposure. The configured live daily budget is also the conservative exposure cap. A blocker skips without reserving or posting; a failed or malformed preflight stops the live run.

Immediately before each live POST, the skill durably reserves the market, game, trade count, and amount in owner-only `live_state.json`. The order itself also carries an explicit `venue="polymarket"`. A confirmed rejection releases that reservation; a timeout or otherwise unconfirmed result keeps it and stops the run for manual order/position reconciliation. This prevents a lost response from permitting duplicate submissions or bypassing daily limits. It does not submit discretionary sell orders: positions are held to resolution unless an account-level Simmer control acts independently.

The default ledger lives outside the installed skill at `$XDG_STATE_HOME/simmer/mlb-live-trader/live_state.json` (or `~/.local/state/...`). A central `.initialized` generation marker prevents another installation from resurrecting an older ledger if the central JSON disappears. All local credentials conservatively share that lock and budget, so rotating an API key cannot reset live risk state.

For a source-checkout upgrade, v2.2 imports an existing installation-local v2.1 `live_state.json`, records its exact provenance, and moves the consumed snapshot to an owner-only `.migrated` archive. Stop the old scheduler before upgrading. The published ClawHub v1.0 used a different `.mlb-live-trader-state.json` inside its installation; ClawHub replaces that directory during an update, so v2.2 cannot safely recover the file afterward. A missing central ledger therefore blocks `--live` and requires the read-only initialization workflow above. Set one stable absolute `SIMMER_MLB_STATE_PATH` per account when separating accounts or when one account is scheduled across containers or hosts. Daily spend counters reset at UTC midnight, while unresolved submission reservations remain until their bounded settlement expiry.

## Configuration

Simmer resolves environment values before saved `config.json` values and defaults. Automaton tunables arrive through the same environment variables. Run `--config` to inspect every resolved setting.

| Setting | Environment variable | Default | Purpose |
| --- | --- | ---: | --- |
| `position_sizing` | `SIMMER_POSITION_SIZING` | `fractional_kelly` | SDK sizing method |
| `kelly_multiplier` | `SIMMER_KELLY_MULTIPLIER` | `0.20` | Fractional-Kelly multiplier |
| `min_ev` | `SIMMER_MIN_EV` | `0.00` | Additional SDK EV floor after the strategy gate |
| `paper_min_edge` | `SIMMER_MLB_PAPER_MIN_EDGE` | `0.02` | Clean paper net-edge gate |
| `live_min_edge` | `SIMMER_MLB_LIVE_MIN_EDGE` | `0.03` | Clean live net-edge gate |
| `max_position_usd` | `SIMMER_MLB_MAX_POSITION` | `5.00` | Hard per-order cap |
| `max_bankroll_fraction` | `SIMMER_MLB_MAX_BANKROLL_FRACTION` | `0.05` | Hard bankroll-fraction cap |
| `live_daily_budget_usd` | `SIMMER_MLB_DAILY_BUDGET` | `25.00` | Live daily spend cap |
| `max_quote_age_seconds` | `SIMMER_MLB_MAX_QUOTE_AGE` | `60` | Maximum executable quote age |
| `max_signal_age_seconds` | `SIMMER_MLB_MAX_SIGNAL_AGE` | `90` | Maximum live ESPN evidence age |
| `max_signal_future_skew_seconds` | `SIMMER_MLB_MAX_SIGNAL_FUTURE_SKEW` | `5` | Maximum future timestamp skew |
| `order_type` | `SIMMER_MLB_ORDER_TYPE` | `FAK` | Bounded live order type |

All published tunables and their ranges are declared in `clawhub.json`.

## Quick commands

```bash
# Show the resolved configuration without trading
.venv/bin/python mlb_live_trader.py --config

# Read current positions
.venv/bin/python mlb_live_trader.py --positions
.venv/bin/python mlb_live_trader.py --positions --live

# One-time read-only proof before the first live run
.venv/bin/python mlb_live_trader.py --initialize-live-state

# Read the local/runtime status view
.venv/bin/python scripts/status.py

# Persist non-secret tuning changes through the Simmer config adapter
.venv/bin/python mlb_live_trader.py --set paper_min_edge=0.025
.venv/bin/python mlb_live_trader.py --set max_position_usd=5

# Explicit real-money opt-in
.venv/bin/python mlb_live_trader.py --live
```

`--no-safeguards` disables the optional Simmer context check in paper mode only. Live context validation remains mandatory. It never disables the edge gate, quote checks, SDK sizing, per-order cap, venue minimum, daily budget, duplicate protection, or live process lock.

## Example output

```text
MLB Live Trader — paper mode
Paper mode is the default. Nothing here touches the live state file.
PAPER YES New York Yankees — $5.00 at 0.600; net edge 10.0%
Done: 1 signals, 1 candidates, 1 trades.
```

Managed Automaton runs additionally emit one machine-readable `{"automaton": ...}` JSON line with signal, attempted-trade, executed-trade, skip, and execution-error counters.

## Troubleshooting

- **`SIMMER_API_KEY is not set`** — provide the key through the environment or managed secret store; do not place it in a tracked file.
- **No live games or signals** — confirm ESPN has an in-progress MLB game with a current, timestamped probability. Pregame/final games and unverifiable live rows are skipped.
- **No active markets** — inspect the Simmer catalog and confirm a full-game MLB winner market is active. Props, totals, partial-game, series, and ambiguous doubleheader markets are intentionally rejected.
- **Market context unavailable** — paper mode may continue without context; live mode always fails closed.
- **Simmer preflight blocked** — confirm real trading is enabled, the linked wallet and signer are ready, collateral is sufficient, and total live exposure remains below `SIMMER_MLB_DAILY_BUDGET`.
- **Position below venue minimum** — the SDK size was below the five-share or configured dollar minimum. The skill skips instead of increasing the stake.
- **Another live run is active** — wait for that cycle to finish. Do not delete the lock file while a process is running.
- **Live state is not initialized** — stop prior schedulers, then run `--initialize-live-state` alone. Any account-wide Polymarket position or receipt from the prior 96 hours intentionally blocks empty initialization.
- **Invalid live trade state or missing central state with an initialization marker** — restore or reconcile `live_state.json` deliberately. Do not delete the marker, `.migrated` archive, or damaged counters to bypass the stop.
- **Ambiguous submission** — stop automation and reconcile Simmer orders and positions. The reservation intentionally remains until an operator determines the real outcome.
- **Multiple hosts use one Simmer account** — point every instance at the same lock-capable filesystem with `SIMMER_MLB_STATE_PATH`, and run only one scheduler. Host-local state cannot coordinate independent machines.

## Remix points

Safe extensions include a separately validated probability source, pitcher/bullpen context, stricter game identity, a measured exit policy, or replay-based calibration. Keep external data authorization explicit, retain paper-first defaults, and add deterministic tests before changing the live path.
