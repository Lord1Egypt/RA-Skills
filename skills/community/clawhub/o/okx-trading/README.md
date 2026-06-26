# okx-trading

Crypto trading on OKX, gated by an explicit human-in-the-loop confirmation. Defaults to OKX's demo (paper-trading) environment.

> Installed under your own ClawHub namespace, the skill lives at `skills/<your-handle>/okx-trading/`. Substitute your handle for `<author>` wherever you see it in `SKILL.md`.

## What it does

- Read-only: balances, tickers, OHLCV with RSI/SMA, open orders, positions, recent fills, daily snapshot with day-over-day delta + 24h fills breakdown.
- Trade-with-confirmation: propose → user replies `YES <id>` in chat → execute.
- DCA: scheduled recurring propose for fixed-size buys of majors.
- Grid bot (spot only): one-time confirm of the whole grid; subsequent fills restock automatically. Optional bounded autonomy at setup: cost-basis floor (refuse losing sells), position cap (refuse over-accumulation), auto-rescale with hard ceiling on re-centers.

## What's new in v0.3.3

- **Hotfix for the v0.3.2 httpx patch.** The previous release injected `timeout=N` into `httpx.Client.send()` — but httpx puts timeouts on the *client* (or *request*), not on `send()`. Every OKX call through httpx therefore raised `TypeError: Client.send() got an unexpected keyword argument 'timeout'`. v0.3.3 patches `httpx.Client.__init__` and `httpx.AsyncClient.__init__` instead, so new clients get the 15s default and `send()`'s signature is left alone. Verified locally with httpx 0.27+.

## What's new in v0.3.2

- `okx_propose_trade.py`, `okx_grid_setup.py`, `okx_grid_propose_stop.py` now print an absolute `Pending file: /...` line alongside the proposal id. The LLM must use that path verbatim with `file_read` rather than guessing `~/.aeon/okx/pending/<id>.json` — the tilde-expansion was ambiguous when aeon runs as a service user (`pi`, `root`, etc.) and previously caused YES-confirmation to fail with "permissions error" because the LLM tried `/root/.aeon/...` on a machine where aeon ran as `pi`.
- `_okx_client.py` enforces a **15-second default HTTP timeout** on `requests` / `httpx` so OKX rate-limits or stalled TCP no longer hang scheduled tasks until the 120s exec wall. Override with `OKX_HTTP_TIMEOUT_S`.

## What's new in v0.3.1

- `okx_snapshot.py` adds **1D / 1W / 1Y price-change context** per watched instrument. Pulls daily candles via OKX's history-candles endpoint (~2 API calls per instrument), reports `current  1D ±x%   1W ±y%   1Y ±z%` in the digest, persists `price_changes` block in the snapshot JSON. Pass `--no-price-history` to skip when you want a faster ad-hoc summary.

## What's new in v0.3.0

- **70/20/10 strategy template** — single-prompt orchestration for "DCA + grid + drawdown reserve". Documented as a recipe in `SKILL.md` so the agent can stand up the whole stack from one user request.
- `okx_dca_dip.py` — drawdown-triggered DCA-the-dip helper. Compares current equity to the all-time-high seen in snapshots; when drawdown crosses `--threshold-pct` (default 30%), recommends deploying a slice of the reserve. Idempotent via `~/.aeon/okx/dca_dip_state.json`; re-arms on deeper drawdown or equity recovery.

## What's new in v0.2.0

- `okx_snapshot.py` — persistent daily snapshots in `~/.aeon/okx/snapshots/<date>.json`, equity delta vs prior, 24h per-instrument fills (buy vol/avg, sell vol/avg, net USDT, fees), pending-order counts, active-strategy summary.
- `--min-profit-gap` flag on grid setup — refuses sell restocks below `avg_entry × (1 + gap)`.
- `--max-position-base` flag on grid setup — caps base-currency accumulation.
- `--trailing-pct` + `--max-rescales` flags — bounded auto-rescale: when price drifts to band edges, recenter and reseed; halts after the configured number of rescales.
- `~/.aeon/okx/grid_audit.jsonl` — append-only audit of grid lifecycle events (fills, restocks, protections, rescales, halts).

## One-time setup

1. **Install Python dependencies** (Python 3.9+):

   ```bash
   pip install -r skills/aeon/okx-trading/requirements.txt
   ```

2. **Get OKX demo API credentials.** Log in at <https://www.okx.com>, switch to "Demo trading" in the top-right account menu, then go to Account → API. Create a key with **Trade** permission, save the API key, secret, and passphrase. (Live keys go in the same place but on the live account; do NOT mix them.)

3. **Set environment variables** in `.env` (and `source` it before running aeon):

   ```bash
   export OKX_API_KEY=...
   export OKX_API_SECRET=...
   export OKX_API_PASSPHRASE=...
   export OKX_DEMO_MODE=1                              # 1 = demo, 0 = live
   export OKX_ALLOWED_SYMBOLS=BTC-USDT,ETH-USDT,SOL-USDT
   export OKX_MAX_NOTIONAL_USDT_PER_TRADE=50
   export OKX_MAX_DAILY_NOTIONAL_USDT=200
   ```

4. **Smoke test** that auth works:

   ```bash
   python3 skills/aeon/okx-trading/scripts/okx_get_balance.py
   ```

   You should see your demo USDT balance. If you see "Missing required environment variable", export the variables first.

## Going live

Flip `OKX_DEMO_MODE=0`, generate live API credentials on your real OKX account, lower your guardrail caps to whatever you're willing to lose to a bug, and re-run the smoke test. The same skill code runs against both environments — no other changes.

## State on disk

```text
~/.aeon/okx/
  pending/<id>.json         # proposed trades / grids / grid-stops awaiting YES
  strategies/<id>.json      # active grids
  notional_log.jsonl        # append-only log of executed notional (for daily cap)
  snapshots/<date>.json     # daily account snapshots (v0.2.0+)
  grid_audit.jsonl          # grid lifecycle audit log (v0.2.0+)
  dca_dip_state.json        # drawdown-trigger state (v0.3.0+)
```

Files are 0600 so the confirmation token is not world-readable. Pending proposals expire automatically (10 min for trades, 30 min for grids).

## What the user types in chat

- "Buy $25 of BTC." → agent runs `okx_propose_trade.py`, posts proposal, you reply `YES abc12345`.
- "What's my OKX balance?" → agent runs `okx_get_balance.py`, summarises.
- "Set up a BTC grid between 55k and 65k, 10 levels of $50." → `okx_grid_setup.py`, you `YES`, agent applies, schedules maintenance.
- "Stop the grid grid-abc12345." → `okx_grid_propose_stop.py`, you `YES`, agent stops.
- "DCA $25 of BTC every Monday at 9am." → agent calls `schedule_create` with the propose script.
