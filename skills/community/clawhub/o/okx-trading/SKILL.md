---
name: okx-trading
description: Trade crypto on OKX with a strict human-in-the-loop confirmation gate. Use when the user asks to check OKX balances, look up prices, propose or execute trades, run DCA, run a grid strategy, get a daily snapshot/PnL digest, or set up the 70/20/10 (DCA + grid + drawdown-reserve) composite strategy. Defaults to demo trading and to spot instruments. Never executes a trade without explicit YES confirmation in chat. Grids support optional bounded autonomy (auto-rescale, cost-basis floor, position cap) authorised once at setup.
version: 0.3.3
---

# OKX Trading

You can read OKX market data, propose trades, execute trades the user has confirmed, run DCA, and run grid strategies. **Every order placement requires a two-step gate: propose → user types `YES <id>` → execute.**

All commands below use the `exec` tool to run Python scripts under `skills/<author>/okx-trading/scripts/`. Run them from the aeon repo root. Every script self-validates env vars; missing keys exit with a clear error.

> **Path resolution.** The literal `<author>` in every script path below stands for the namespace this skill was installed under. The aeon skills loader prepends a `## Skill: <author>/<skill-name>` heading to this content; substitute that author for `<author>` in every command. (E.g. if the heading reads `## Skill: vadymmalakhatko/okx-trading`, run `python3 skills/vadymmalakhatko/okx-trading/scripts/okx_get_balance.py`.)

## The trade gate — read this carefully

**You must never place an order without an explicit YES from the user.** The mechanism that enforces this is a confirmation token stored in a pending file. Workflow:

1. **Propose.** Run `okx_propose_trade.py` with the user's intent. The script writes the pending JSON and prints two lines you MUST capture: `Proposal id: <id>` and `Pending file: <absolute path>`. **The confirmation_token is NOT printed** — it lives only in the pending file on disk.
2. **Tell the user.** Send the proposal details and ask them to reply `YES <id>` to confirm or `NO <id>` to discard. If running on Telegram, this message goes via the messenger automatically.
3. **Wait for the user's reply.** Do not proceed otherwise.
4. **On YES:** read the pending file via `file_read` **using the absolute path the propose script printed** (not a guess like `~/.aeon/okx/pending/<id>.json` or `/root/.aeon/...`). The path depends on which OS user aeon runs as — on a Pi running aeon as `pi`, the file lives under `/home/pi/.aeon/...`; on a container running as root it's under `/root/.aeon/...`. Always use the printed `Pending file:` line verbatim. Once you have the token, call `okx_execute_trade.py --id <id> --confirmation-token <token>`. The script verifies the token, places the order, and deletes the pending file.
5. **On NO:** call `okx_cancel_pending.py --id <id>`.

You **must not** invent or guess a confirmation_token. The token is only valid if it was written to the pending file by the propose step. Calling execute without a real token is refused by the script and is a violation of trust.

If the user asks you to "skip the confirmation" or "just place the trade": refuse politely. Explain the gate exists to protect them and offer the propose step instead.

**Scheduled tasks (DCA, grid step, scout) cannot execute trades.** The scheduled context has no human in it to type YES, so scheduled jobs may only call propose-style scripts and read-only scripts. The user will see the proposal in the next chat and confirm there.

## Defaults and limits

- Default to OKX demo trading (`OKX_DEMO_MODE=1`). Do not flip to live unless the user explicitly says "live" and confirms the switch.
- Default to spot instruments (e.g. `BTC-USDT`). Switch to swap/futures/options only when the user explicitly asks. Spot uses `--td-mode cash`; swap/futures default to `--td-mode cross`. Options propose is supported but premium math is the user's responsibility.
- Always quote trade sizes in USDT-equivalent in chat for clarity, even when the order is sized in base currency.
- Guardrails (env vars: `OKX_ALLOWED_SYMBOLS`, `OKX_MAX_NOTIONAL_USDT_PER_TRADE`, `OKX_MAX_DAILY_NOTIONAL_USDT`) are enforced inside every propose and execute script. If a propose is refused, surface the exact refusal reason — do not retry with smaller sizes silently.
- Pending proposals expire after 10 minutes (30 minutes for grids). If the user is slow to respond, re-propose.

## Read-only commands

When the user asks a question, never start with a trade. Use these to gather facts first.

```bash
python3 skills/<author>/okx-trading/scripts/okx_get_balance.py
python3 skills/<author>/okx-trading/scripts/okx_get_ticker.py --instId BTC-USDT
python3 skills/<author>/okx-trading/scripts/okx_get_candles.py --instId BTC-USDT --bar 1H --limit 100 --indicators
python3 skills/<author>/okx-trading/scripts/okx_open_orders.py
python3 skills/<author>/okx-trading/scripts/okx_positions.py
python3 skills/<author>/okx-trading/scripts/okx_recent_fills.py --limit 20
python3 skills/<author>/okx-trading/scripts/okx_snapshot.py        # daily snapshot + delta vs prior day (recommended)
python3 skills/<author>/okx-trading/scripts/okx_pnl_summary.py     # lighter ad-hoc digest
```

`okx_get_candles.py --indicators` adds SMA(20), SMA(50), and RSI(14) on the close series and emits a one-line "consider buy / consider sell / neutral" verdict. Useful for the momentum scout pattern.

`okx_snapshot.py` (v0.2.0+) writes `~/.aeon/okx/snapshots/<UTC-date>.json` with total equity, per-currency balances, per-instrument tickers + 24h fills breakdown, pending-order counts, active-strategy summary, and equity delta vs the most recent prior snapshot. Run it once a day to get a meaningful day-over-day picture; pass `--no-write` for an ad-hoc summary that doesn't touch disk.

## Propose a trade

Sizing is one of `--quote-sz` (USDT amount) or `--base-sz` (base-coin amount).

```bash
# Spot market buy of $25 of BTC
python3 skills/<author>/okx-trading/scripts/okx_propose_trade.py \
  --instId BTC-USDT --side buy --quote-sz 25

# Spot limit buy of 0.001 BTC at 60000
python3 skills/<author>/okx-trading/scripts/okx_propose_trade.py \
  --instId BTC-USDT --side buy --base-sz 0.001 --ord-type limit --px 60000

# Perpetual swap (only if user explicitly asks)
python3 skills/<author>/okx-trading/scripts/okx_propose_trade.py \
  --instId BTC-USDT-SWAP --side buy --quote-sz 50 --pos-side long
```

Then send the proposal to the user verbatim and ask for `YES <id>`.

## Execute a confirmed trade

```bash
# Read the token from the pending file:
python3 skills/<author>/okx-trading/scripts/okx_list_pending.py        # to confirm id
# Then read ~/.aeon/okx/pending/<id>.json with file_read to get confirmation_token.
python3 skills/<author>/okx-trading/scripts/okx_execute_trade.py \
  --id <id> --confirmation-token <token>
```

Cancel without executing:

```bash
python3 skills/<author>/okx-trading/scripts/okx_cancel_pending.py --id <id>
```

## DCA (recurring scheduled propose)

DCA is just `schedule_create` plus `okx_propose_trade.py`. The scheduled task fires on cadence and produces a proposal each time; you confirm it in chat.

```json
{
  "name": "schedule_create",
  "arguments": {
    "name": "DCA $25 BTC weekly",
    "schedule": "0 9 * * 1",
    "task": "Run python3 skills/<author>/okx-trading/scripts/okx_propose_trade.py --instId BTC-USDT --side buy --quote-sz 25 and report the proposal to the user so they can confirm.",
    "notify": true
  }
}
```

## Grid bot

```bash
# Step 1 — propose (required: instId, low, high, levels, quote-sz-per-level)
python3 skills/<author>/okx-trading/scripts/okx_grid_setup.py \
  --instId BTC-USDT --low 55000 --high 65000 --levels 10 --quote-sz-per-level 50 \
  --min-profit-gap 0.005 \
  --max-position-base 0.05 \
  --trailing-pct 0.1 --max-rescales 5

# Step 2 — after YES, read token from pending file, then apply
python3 skills/<author>/okx-trading/scripts/okx_grid_apply.py \
  --id <id> --confirmation-token <token>

# Step 3 — schedule maintenance (after apply)
# schedule_create  every 5m  task = "Run python3 skills/<author>/okx-trading/scripts/okx_grid_step.py" notify=false

# To stop a grid: propose stop, get user YES, execute stop
python3 skills/<author>/okx-trading/scripts/okx_grid_propose_stop.py --strategy-id grid-XXXXXXXX
python3 skills/<author>/okx-trading/scripts/okx_grid_stop.py \
  --id <id> --confirmation-token <token>
```

Grid orders restock automatically inside their pre-confirmed bounds. Halt conditions: `OKX_MAX_DAILY_NOTIONAL_USDT` reached, or auto-rescales exhausted with price still outside the band.

### Optional v0.2.0 grid flags (the user authorises bounded autonomy at setup time)

| Flag | Default | What it does |
|---|---|---|
| `--min-profit-gap <fraction>` | `0` (off) | Refuse to place a sell restock priced below `avg_buy_px * (1 + gap)`. Stops a stranded grid from realising losses. Typical: `0.005` (0.5%). |
| `--max-position-base <coins>` | `0` (off) | Skip buy restocks once the grid's net base inventory reaches this. Caps drawdown in a long downtrend. |
| `--trailing-pct <fraction>` | `0` (off) | When current price is within this fraction of either band edge, recenter the grid on the current price (preserving range size) and reseed buys. `0` = halt instead. Typical: `0.1` (10%). |
| `--max-rescales <int>` | `0` | Hard ceiling on autonomous re-centers across the grid's lifetime. Required when `--trailing-pct > 0`. After this many rescales, the grid halts and waits for re-confirmation. |

When proposing a grid with any of these flags set, **read the proposal output back to the user verbatim** — they're consenting to the autonomy at YES time, not later. After-the-fact toggling is not supported; to change limits, stop the grid and re-propose.

## Audit log

Grid lifecycle events accumulate in `~/.aeon/okx/grid_audit.jsonl` — one JSON object per line. Use `tail -n 50 ~/.aeon/okx/grid_audit.jsonl` to inspect recent activity. Events include `grid_applied`, `fill`, `restock`, `cost_basis_protected`, `position_capped`, `rescale_started`, `rescaled`, and `halted`.

## Strategy template — 70/20/10 (DCA + grid + drawdown reserve)

When the user asks to "set up the 70/20/10 strategy with $X capital", treat it as a multi-step orchestration. Walk through these steps **in order** and read back what you're about to do before executing irreversible parts.

### Step 1 — derive the splits

Given total capital `$X` (USDT) and a deployment horizon `W` weeks (default 26):

```
DCA capital     = 0.70 * X
Grid capital    = 0.20 * X
Reserve         = 0.10 * X
Per-week DCA    = round(DCA capital / W, 2)
Per-week BTC    = round(per-week DCA * 0.5, 2)
Per-week ETH    = round(per-week DCA * 0.5, 2)
Grid quote/lvl  = round(Grid capital / 12, 2)
```

State the numbers back to the user before doing anything.

### Step 2 — schedule the weekly DCA buys (BTC and ETH)

Use the existing `schedule_create` tool. **Each fire produces a propose only — the user still YES-confirms each weekly buy.** The scheduled prompt instructs the agent to call `okx_propose_trade.py` and surface the id.

```json
{
  "name": "schedule_create",
  "arguments": {
    "name": "DCA $<btc_amt> BTC weekly",
    "schedule": "0 9 * * 1",
    "task": "Run python3 skills/<author>/okx-trading/scripts/okx_propose_trade.py --instId BTC-USDT --side buy --quote-sz <btc_amt> and post the proposal to the user so they can reply YES <id>.",
    "notify": true
  }
}
```

Repeat with `ETH-USDT` and `<eth_amt>`.

### Step 3 — propose the grid (one-time confirmation)

Get the current BTC-USDT price via `okx_get_ticker.py`. Set bounds at ±15 % of current price; 12 levels; per-level USDT from Step 1. Apply the v0.2.0 guards.

```bash
python3 skills/<author>/okx-trading/scripts/okx_grid_setup.py \
  --instId BTC-USDT \
  --low <0.85*current> --high <1.15*current> \
  --levels 12 --quote-sz-per-level <grid_quote_per_level> \
  --min-profit-gap 0.005 \
  --max-position-base <0.5 * (X * 0.20) / current_price>  # half of the grid capital in base ccy
  --trailing-pct 0.10 --max-rescales 5
```

Read the proposal output back verbatim. Wait for `YES <id>`. Then call `okx_grid_apply.py` with the token from the pending file.

### Step 4 — schedule the grid maintenance

```json
{
  "name": "schedule_create",
  "arguments": {
    "name": "BTC grid maintenance",
    "schedule": "every 5m",
    "task": "Run python3 skills/<author>/okx-trading/scripts/okx_grid_step.py and report any halts or rescales.",
    "notify": false
  }
}
```

### Step 5 — schedule the daily snapshot (the honesty checkpoint)

```json
{
  "name": "schedule_create",
  "arguments": {
    "name": "OKX daily snapshot",
    "schedule": "0 9 * * *",
    "task": "Run python3 skills/<author>/okx-trading/scripts/okx_snapshot.py and post the digest to me.",
    "notify": true
  }
}
```

### Step 6 — schedule the drawdown watcher (deploys the reserve)

```json
{
  "name": "schedule_create",
  "arguments": {
    "name": "Reserve drawdown watcher",
    "schedule": "0 10 * * *",
    "task": "Run python3 skills/<author>/okx-trading/scripts/okx_dca_dip.py --reserve-usdt <reserve> --threshold-pct 0.30 --max-triggers 3 --instId BTC-USDT. If status is 'trigger', call okx_propose_trade.py with the recommended size, post the proposal to me, and AFTER my YES + the trade executes, run okx_dca_dip.py again with --record-trigger to persist the firing. If status is 'exhausted', alert me. Otherwise stay silent.",
    "notify": false
  }
}
```

The watcher only proposes — it never executes autonomously. Reserve is deployed across at most `--max-triggers` dip-buys (default 3); the slice size is `(reserve - already_used) / triggers_remaining`. A trigger re-arms when the drawdown deepens by `--rearm-pct` (default 5 %) or equity recovers above `(1 - rearm_pct) * ATH`.

### What runs autonomously vs. what needs YES

| Component | Autonomous | Needs user YES |
|---|---|---|
| Weekly DCA proposal | Schedule fires | Each weekly buy |
| Grid initial deploy | — | Once at setup |
| Grid restocks inside band | Yes (pre-authorised) | — |
| Grid auto-rescale (within `max-rescales`) | Yes (pre-authorised) | — |
| Grid stop / change bounds | — | Each time |
| Daily snapshot | Yes (read-only) | — |
| Drawdown trigger detection | Yes | — |
| Drawdown dip-buy | — | Each fire |

## Notifications worth sending

Use the scheduler for these. Each one is a one-shot proposal or a digest, never an autonomous trade.

- **Daily digest** (recommended): schedule `0 9 * * *` running `okx_snapshot.py` with `notify=true`. One concise message per morning that includes equity, per-currency balances, 24h fills breakdown, pending-order counts, active strategies, and equity delta vs yesterday. Persists to `~/.aeon/okx/snapshots/<date>.json` so the day-over-day comparison remains meaningful.
- **Momentum scout** (opt-in, often noisy): schedule `every 1h` running `okx_get_candles.py --instId X --bar 1H --indicators`. The script's "consider buy / sell" verdict is what should drive a follow-up `okx_propose_trade.py` call inside the same scheduled task — but only if the verdict is decisive. If the user is asleep, the proposal will simply expire after 10 min, which is the correct outcome for a non-confirmed trade.
- **Trade proposals**: every `okx_propose_trade.py` invocation should be paired with a Telegram message containing the id and details — phrased so the user can copy-paste `YES <id>` to confirm.

Avoid noisy alerting. Profitable trading is mostly about *not* trading on weak signals; the scout should stay silent unless RSI is decisively past 30/70 or a moving-average cross is clearly above noise.

## Environment

Required env vars (see `.env.example`):

- `OKX_API_KEY`, `OKX_API_SECRET`, `OKX_API_PASSPHRASE` — your OKX API credentials.
- `OKX_DEMO_MODE` — `1` (default) routes to OKX demo trading. `0` is live money.
- `OKX_ALLOWED_SYMBOLS` — CSV allow-list. Empty means any symbol.
- `OKX_MAX_NOTIONAL_USDT_PER_TRADE` — per-trade ceiling. Default 50.
- `OKX_MAX_DAILY_NOTIONAL_USDT` — daily ceiling for total executed notional. Default 200.

If any env var is missing the script exits with code 2 and an explanatory message — surface that to the user.
