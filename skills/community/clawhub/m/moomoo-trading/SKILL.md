---
name: moomoo-trading
description: "Use OpenD-backed moomoo/Futu scripts for quotes, K-lines, price alerts, portfolio/account checks, and stock order execution. Triggers on moomoo, futu, OpenD, futu-api, moomoo-api, quotes, positions, orders, paper trading, or explicitly confirmed live trading."
---

# moomoo Trading

Use this skill when the user wants market data or stock trading through moomoo/Futu OpenAPI and a local OpenD gateway.

## Read This First

- Read [references/setup-guide.md](references/setup-guide.md) for installation, package choice (`futu-api` vs `moomoo-api`), OpenD login, and troubleshooting.
- Read [references/api-reference.md](references/api-reference.md) when you need exact method names, return shapes, or trade-query semantics.
- All bundled scripts lazy-load the SDK, so `--help` works even if neither Python package is installed yet.

## Safety Rules

- Default to simulated trading unless the user explicitly asks for live trading.
- Live order placement, modification, and cancellation require `--env real --confirm`.
- `scripts/trade.py` also requires a live-trading unlock password via `MOOMOO_UNLOCK_PASSWORD` by default, or another env var name passed with `--unlock-password-env`. The script unlocks for the requested action and then re-locks.
- For cancel/modify actions, pass `--market` unless you also provide a ticker so the script can infer the correct trade context.
- Do not put a raw trading password directly on the command line. Use an environment variable.

## Scripts

### Setup check

```bash
python3 scripts/setup_check.py
python3 scripts/setup_check.py --market HK --account-index 1
```

Checks quote connectivity, lists discovered trading accounts, and verifies simulated account access.

### Quotes and K-lines

```bash
python3 scripts/quote.py US.AAPL HK.00700
python3 scripts/quote.py US.TSLA --snapshot
python3 scripts/quote.py US.NVDA --kline --ktype K_DAY --count 10
python3 scripts/quote.py US.NVDA --kline --start 2026-03-01 --end 2026-04-01 --extended-time
```

### Trading

```bash
python3 scripts/trade.py --ticker US.AAPL --action buy --qty 10 --price 150 --type limit --env sim
python3 scripts/trade.py --ticker US.AAPL --action sell --qty 5 --type market --env sim
export MOOMOO_UNLOCK_PASSWORD='your-trading-password'
python3 scripts/trade.py --ticker US.AAPL --action buy --qty 10 --type market --env real --confirm
python3 scripts/trade.py --cancel --order-id 12345 --market US --env sim
python3 scripts/trade.py --modify --order-id 12345 --market US --price 155 --qty 10 --env sim
```

Useful extras:
- `--remark` adds an order remark.
- `--account-id` / `--account-index` let you target a specific trading account.

### Portfolio, orders, and deals

```bash
python3 scripts/portfolio.py --env sim
python3 scripts/portfolio.py --env sim --account
python3 scripts/portfolio.py --env sim --orders
python3 scripts/portfolio.py --env real --history-orders --start 2026-04-01 --end 2026-04-02
python3 scripts/portfolio.py --env real --deals
```

`--orders` shows open orders. `--history-orders` shows historical orders. `--deals` shows today's deals, or historical deals when paired with `--start` / `--end`.

### Price alerts

```bash
python3 scripts/watchlist.py --tickers US.AAPL,US.TSLA --above 200 --below 150
python3 scripts/watchlist.py --tickers US.NVDA --above 950 --quit-on-alert
python3 scripts/watchlist.py --tickers HK.00700 --below 320 --once
```

Alerts trigger once per threshold crossing by default. Use `--repeat-alerts` to spam every polling cycle instead.
