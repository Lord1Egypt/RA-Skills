---
name: ibkr-investing
description: Invest on Interactive Brokers (stocks/ETFs) via IB Gateway with the same human-in-the-loop confirmation gate as okx-trading. Use when the user asks to check IBKR balances, look up quotes, propose or execute stock/ETF trades, set up DCA into ETFs, or get a daily portfolio snapshot. Defaults to PAPER trading (port 4002). Live trading (port 4001) requires IBKR_LIVE_MODE=1. Never executes a trade without explicit YES confirmation in chat.
version: 0.1.1
---

# IBKR Investing

You can read IBKR account state, propose trades, execute trades the user has confirmed, and run DCA into stocks/ETFs. **Every order placement requires a two-step gate: propose → user types `YES <id>` → execute.** Same shape as the okx-trading skill — if the user knows that gate, they know this one.

All commands below run Python scripts under `skills/<author>/ibkr-investing/scripts/`. Run them from the aeon repo root or from `~/.aeon`. Every script self-validates env vars; missing or unreachable Gateway exits with a clear error.

> **Path resolution.** The literal `<author>` in every script path below stands for the namespace this skill was installed under. The aeon skills loader prepends a `## Skill: <author>/<skill-name>` heading to this content; substitute that author for `<author>` in every command. (E.g. `## Skill: aeon/ibkr-investing` → use `skills/aeon/ibkr-investing/scripts/...`.)

## Setup prerequisites (one-time, BEFORE anything else)

This skill talks to a running IB Gateway. The Gateway is *not* part of the skill — it's IBKR's own software, typically run via the [gnzsnz/ib-gateway-docker](https://github.com/gnzsnz/ib-gateway-docker) container. The skill assumes the Gateway is reachable on `127.0.0.1:4001` (live) or `127.0.0.1:4002` (paper).

If the user has not yet set up the Gateway, **stop and walk them through the README.md** before doing anything else. Don't propose trades against an unreachable Gateway.

Always run `ibkr_gateway_status.py` first when a scheduled task fails. It distinguishes "Gateway down", "Gateway up but 2FA pending", and "Gateway up and authenticated".

## The trade gate — read this carefully

**You must never place an order without an explicit YES from the user.** Workflow:

1. **Propose.** Run `ibkr_propose_trade.py` with the user's intent. The script writes the pending JSON and prints two lines you MUST capture: `Proposal id: <id>` and `Pending file: <absolute path>`. **The confirmation_token is NOT printed** — it lives only in the pending file on disk.
2. **Tell the user.** Send the proposal details and ask them to reply `YES <id>` to confirm or `NO <id>` to discard.
3. **Wait for the user's reply.**
4. **On YES:** read the pending file via `file_read` **using the absolute path the propose script printed** (not a guess like `~/.aeon/ibkr/pending/<id>.json` or `/root/.aeon/...`). The path depends on which OS user aeon runs as — always use the printed `Pending file:` line verbatim. Once you have the token, call `ibkr_execute_trade.py --id <id> --confirmation-token <token>`. The script verifies the token, places the order via IBKR, and deletes the pending file.
5. **On NO:** call `ibkr_cancel_pending.py --id <id>`.

You **must not** invent or guess a confirmation_token. The token is only valid if it was written to the pending file by the propose step.

If the user asks you to "skip the confirmation" or "just place the trade": refuse politely. Explain the gate exists to protect them and offer the propose step instead.

**Scheduled tasks (DCA, drawdown watcher) cannot execute trades.** The scheduled context has no human in it to type YES, so scheduled jobs may only call propose-style and read-only scripts. The user will see the proposal in the next chat and confirm there.

## Defaults and limits

- Default to **PAPER trading** (`IBKR_LIVE_MODE=0`, port 4002). Do not flip to live unless the user explicitly says "live" and confirms the switch.
- Default to US ETFs on SMART exchange + USD currency. Override per-call via `--exchange` / `--currency`.
- Always quote trade sizes in USD in chat for clarity, even when the order is share-sized.
- Guardrails (`IBKR_ALLOWED_SYMBOLS`, `IBKR_MAX_NOTIONAL_USD_PER_TRADE`, `IBKR_MAX_DAILY_NOTIONAL_USD`) enforced in every propose AND execute. If a propose is refused, surface the refusal verbatim — don't retry with smaller sizes silently.
- Pending proposals expire after 10 minutes.

## Read-only commands

When the user asks a question, never start with a trade. Use these to gather facts first.

```bash
python3 skills/<author>/ibkr-investing/scripts/ibkr_gateway_status.py
python3 skills/<author>/ibkr-investing/scripts/ibkr_get_balance.py
python3 skills/<author>/ibkr-investing/scripts/ibkr_get_positions.py --with-mark
python3 skills/<author>/ibkr-investing/scripts/ibkr_get_quote.py --symbol VOO
python3 skills/<author>/ibkr-investing/scripts/ibkr_get_candles.py --symbol VOO --duration "6 M" --indicators
python3 skills/<author>/ibkr-investing/scripts/ibkr_snapshot.py
```

`ibkr_get_candles.py --indicators` adds SMA(20)/SMA(50)/RSI(14) on the close series and emits a one-line "consider buy / consider sell / neutral" verdict.

`ibkr_snapshot.py` writes `~/.aeon/ibkr/snapshots/<UTC-date>.json` with NAV, cash, positions, 1D/1W/1Y price moves, and delta vs the prior day. Use it as the body of the daily-digest schedule. Pass `--no-price-history` to skip the historical-price lookup if the user wants a faster ad-hoc summary.

## Propose a trade

Sizing is one of `--quote-sz` (USD) or `--shares` (exact share quantity, can be fractional).

```bash
# DCA-style market buy of $50 of VOO
python3 skills/<author>/ibkr-investing/scripts/ibkr_propose_trade.py \
  --symbol VOO --side BUY --quote-sz 50

# Limit buy of 10 shares of QQQ at 350
python3 skills/<author>/ibkr-investing/scripts/ibkr_propose_trade.py \
  --symbol QQQ --side BUY --shares 10 --ord-type LMT --lmt-price 350

# Round to whole shares (no fractional)
python3 skills/<author>/ibkr-investing/scripts/ibkr_propose_trade.py \
  --symbol AAPL --side BUY --quote-sz 200 --no-fractional
```

Then send the proposal to the user verbatim and ask for `YES <id>`.

## Execute a confirmed trade

```bash
python3 skills/<author>/ibkr-investing/scripts/ibkr_list_pending.py        # confirm id
# Read ~/.aeon/ibkr/pending/<id>.json with file_read to get confirmation_token.
python3 skills/<author>/ibkr-investing/scripts/ibkr_execute_trade.py \
  --id <id> --confirmation-token <token>
```

Cancel without executing:

```bash
python3 skills/<author>/ibkr-investing/scripts/ibkr_cancel_pending.py --id <id>
```

## DCA strategy template

DCA on IBKR is a recurring scheduled propose, identical to the OKX pattern. Recommend monthly cadence (rather than weekly) to amortise IBKR's commission structure better — though commission-free for most US ETFs.

```json
{
  "name": "schedule_create",
  "arguments": {
    "name": "DCA $200 VOO monthly",
    "schedule": "0 14 1 * *",
    "task": "Run python3 skills/<author>/ibkr-investing/scripts/ibkr_propose_trade.py --symbol VOO --side BUY --quote-sz 200 and post the proposal so I can YES it.",
    "notify": true
  }
}
```

For a multi-ETF basket, register one schedule per symbol so each gets an independent YES (cleaner audit trail and per-symbol guardrails):

| Schedule | Symbol | Per-fire USD | What it captures |
|---|---|---|---|
| `0 14 1 * *` | VOO | 60% of monthly | S&P 500 core |
| `0 14 1 * *` | VTI | 30% of monthly | Total US market |
| `0 14 1 * *` | BND | 10% of monthly | Bonds anchor |

Run the snapshot the same morning at 14:30 UTC (`30 14 1 * *`) so the digest captures the new positions.

## Drawdown reserve template

Mirror of the OKX reserve flow. `ibkr_dca_dip.py` watches NAV vs ATH (computed from snapshot history) and recommends a dip-buy when drawdown crosses threshold. Token-gated like every other trade.

```json
{
  "name": "schedule_create",
  "arguments": {
    "name": "IBKR drawdown watcher",
    "schedule": "0 15 * * *",
    "task": "Run python3 skills/<author>/ibkr-investing/scripts/ibkr_dca_dip.py --reserve-usd <reserve> --threshold-pct 0.30 --max-triggers 3 --symbol VOO. If status is 'trigger', call ibkr_propose_trade.py with the recommended size, post the proposal, and AFTER my YES + execute, run ibkr_dca_dip.py again with --record-trigger.",
    "notify": false
  }
}
```

## Adding new strategies

Strategies are *agent-orchestrated recipes that compose existing scripts*. To add one (e.g. equal-weight rebalancing, threshold rebalancing, momentum rotation):

1. Decide what observations the strategy needs. Read from `ibkr_snapshot.py` (current state), `~/.aeon/ibkr/snapshots/*.json` (history), `~/.aeon/ibkr/audit.jsonl` (lifecycle events), and `ibkr_get_candles.py --indicators` (signal).
2. Define the trigger condition. Either a scheduled task that runs daily and checks the condition, or a passive observation surfaced in the snapshot.
3. The trigger NEVER places a trade itself — it produces a recommendation that the agent (or scheduled task) can pass to `ibkr_propose_trade.py`. User still YES-confirms each fill.
4. Write any required state to `~/.aeon/ibkr/<strategy_name>_state.json` (mode 600).
5. Append `audit.jsonl` events for transparency.

The `ibkr_dca_dip.py` script is the canonical example of this shape. Follow it for new strategies.

## Audit log

Lifecycle events accumulate in `~/.aeon/ibkr/audit.jsonl` — one JSON object per line. `tail -n 50 ~/.aeon/ibkr/audit.jsonl` to inspect recent activity. Events: `proposal_created`, `proposal_cancelled`, `proposal_executed`, `proposal_rejected`, `daily_cap_breach`, `drawdown_trigger`.

## Environment

Required env vars (see `.env.example`):

- `IBKR_LIVE_MODE` — `0` (default) routes to PAPER (port 4002). `1` routes to LIVE (port 4001).
- `IBKR_HOST` — Gateway host. Default `127.0.0.1`.
- `IBKR_PORT` — override port if your Gateway is custom-mapped.
- `IBKR_CLIENT_ID` — API client id. Default 97. Change if multiple skills/clients connect.
- `IBKR_DEFAULT_EXCHANGE` — default `SMART`.
- `IBKR_DEFAULT_CURRENCY` — default `USD`.
- `IBKR_ALLOWED_SYMBOLS` — CSV allow-list, e.g. `VOO,VTI,QQQ,BND`. Empty means any.
- `IBKR_MAX_NOTIONAL_USD_PER_TRADE` — per-trade ceiling. Default 200.
- `IBKR_MAX_DAILY_NOTIONAL_USD` — per-day ceiling. Default 1000.

If any required var is missing or the Gateway is unreachable, the script exits with a clear error — surface that to the user.
