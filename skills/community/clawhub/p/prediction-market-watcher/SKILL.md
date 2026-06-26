---
name: prediction-market-watcher
description: Monitor, analyze, and trade on Kalshi and Polymarket prediction markets. Use when the user wants to check open positions, scan for value bets, place bets, check settlement status, or get a portfolio summary on Kalshi or Polymarket. Also use proactively when a bet is approaching settlement time.
---

# Prediction Market Watcher

Connects to Kalshi (and Polymarket) to track positions, scan markets, and place bets.

## Setup

**Kalshi** (live trading, US):
- API key + RSA private key required
- Config lives at `kalshi-agent/config.json` in the workspace
- Key file: `kalshi-agent/kalshi.key`
- Scripts use `kalshi_client.py` with RSA-PSS signed requests

**Polymarket** (coming soon — read-only via public API for now)

## Common Tasks

### Check portfolio / open positions
```bash
cd ~/workspace/kalshi-agent && python3 kalshi_agent.py --status
cd ~/workspace/kalshi-agent && python3 kalshi_agent.py --positions
```

### Check a specific market
```python
from kalshi_client import KalshiClient
import json
c = KalshiClient('KEY_ID', 'kalshi.key')
market = c.get('/trade-api/v2/markets/TICKER_HERE')
print(json.dumps(market, indent=2))
```
Key fields: `yes_bid_dollars`, `yes_ask_dollars`, `floor_strike`, `cap_strike`, `close_time`, `rules_primary`

### Check BTC/crypto price vs bet range
- Fetch live price via web search or Brave API
- Compare against `floor_strike` / `cap_strike` from market data
- Settlement uses CF Benchmarks RTI (60s avg before close) — not Coinbase/Google price

### Scan for opportunities
```bash
cd ~/workspace/kalshi-agent && python3 kalshi_agent.py --scan
```

### Place a bet (manual)
```python
order = c.create_order(ticker="TICKER", side="yes", action="buy", count=N, limit_price=CENTS)
```
- `limit_price` is in cents (e.g. 8 = $0.08)
- `count` = number of $1 contracts
- Always check `risk_state.json` limits before placing

### Settlement reminders
- Use a cron job scheduled ~15 min before `close_time`
- Message Katie on Telegram with: current price, range, whether we're in/out, time remaining

## Risk Rules (from risk.py)
- Max $20/day budget
- Max 5 open positions
- Max single bet: $5 (high confidence), $3 (medium), $1 (low)
- Check `can_bet()` before any auto-place

## API Base URL
`https://api.elections.kalshi.com/trade-api/v2/`

Key endpoints:
- `GET /portfolio/positions` → open positions (use `/trade-api/v2/portfolio/positions`)
- `GET /markets/{ticker}` → single market detail
- `GET /markets?status=open&limit=100` → scan markets
- `GET /portfolio/balance` → balance + portfolio value
- `POST /portfolio/orders` → place order

See `references/kalshi-api.md` for full endpoint reference.

## Polymarket (read-only)
Public REST API — no auth needed for reads:
```
GET https://gamma-api.polymarket.com/markets?active=true&limit=20
```
See `references/polymarket-api.md` for details.
