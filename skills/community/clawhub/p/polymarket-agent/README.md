# Polymarket Agent 🎰

An [OpenClaw](https://openclaw.ai) skill for **prediction-market research** on
Polymarket — whale tracking, smart-money rankings, and optional order execution
behind deterministic guard-rails.

> ⚠️ **This skill can move real money.** It can custody a Polygon wallet private
> key and sign irreversible transactions. Read [SECURITY.md](SECURITY.md)
> before configuring a wallet.

## What it does

**With no credential at all:**
- 🔍 search active markets, prices, spread and volume;
- 🐋 **track large trades (whales)** with server-side value filtering;
- 🏆 **rank profitable traders** (smart money) by category and period;
- 👤 profile any wallet: bankroll, positions and recent trades;
- 👥 largest holders of each market outcome;
- ⏰ recurring alerts via cron, deduplicated and silent when nothing happened.

**With a wallet configured:**
- read balance, positions and open orders;
- place limit buy/sell orders — always validated by the guard-rails.

## Install

```bash
./install.sh
.venv/bin/poly markets --limit 5     # works immediately, no credential
```

To operate a wallet (optional):

```bash
.venv/bin/poly setup      # key read hidden → encrypted keystore (0600)
.venv/bin/poly doctor     # check install and active limits
```

**Dry-run ships enabled.** Orders are validated and journaled, but not sent,
until you deliberately turn it off.

## Commands

| Command | What it does |
|---|---|
| `poly whales` | 🐋 Recent large trades (`--min`, `--hours`, `--alert`) |
| `poly leaderboard` | 🏆 Most profitable traders (`--category`, `--period`) |
| `poly trader <0x…>` | 👤 A wallet's bankroll, positions and trades |
| `poly holders <conditionId>` | 👥 Largest holders per outcome |
| `poly quote <id\|slug>` | 💹 Spread and top of book |
| `poly markets [query]` | List/search markets (`--tokens` shows token_ids) |
| `poly market <id\|slug>` | Market detail with token_id and implied probability |
| `poly balance` · `positions` · `orders` | Wallet state |
| `poly buy/sell <TOKEN_ID> <PRICE> <SIZE>` | Limit order (asks for confirmation) |
| `poly cancel <ID>` · `--all` | Cancel orders |
| `poly halt` · `poly resume` | **Emergency stop** / release |
| `poly history` | Audit trail of everything that touched money |
| `poly config --list` | Active risk limits |
| `poly revoke` | Delete the local keystore |

## Guard-rails

Enforced by code before any order leaves — the agent cannot disable them:

| Limit | Default |
|---|---|
| Notional per order | $25 |
| Share of bankroll | 5% |
| Spend per 24h | $100 |
| Open orders | 10 |
| Price range | 0.01–0.99 |
| Dry-run | on |
| Human confirmation | required |

Autonomous mode requires `--i-understand-the-risk`, **expires on its own**
(max 24h) and stays subject to every cap. `poly halt` overrides everything.

## 🐋 Whale alerts

`--alert` returns only **unseen** trades and prints `NO_REPLY` when there is
nothing — OpenClaw's cron suppresses delivery in that case, so you are notified
only when something real happened.

```bash
# test without consuming the dedup state
poly whales --alert --min 50000 --hours 1 --preview

# schedule every 15 min (deterministic, no model turn)
openclaw cron create "*/15 * * * *" \
  --name "Polymarket whales" \
  --command "$PWD/.venv/bin/poly whales --alert --min 50000 --hours 1" \
  --announce
```

Use a window larger than the cron interval: indexing lags and deduplication
prevents repeats. `poly alerts-reset` clears the history.

## Using it with OpenClaw

```
"analyze Polymarket opportunities"
"are any whales buying right now?"
"who are the most profitable traders this month?"
"what is wallet 0x69c5… doing?"
"alert me when someone bets more than $100k"
"is X worth betting on?"
```

The agent researches news, compares against the odds and recommends — **without
executing**. Execution only happens when you ask for a specific order.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Requirements

- Python 3.10+
- A Polygon wallet with USDC (only for trading; research needs none)

## License

MIT
