---
name: massive-data-feed
description: >
  Fetch real-time and historical market data from Massive (formerly Polygon.io)
  for use in OpenClaw's trading decisions. Use this skill whenever OpenClaw
  needs stock quotes, options chains, futures prices, crypto prices, OHLCV bars,
  trades, or any other market data. Triggers on any request for price data,
  market data, historical bars, real-time streaming, or backtesting data across
  stocks, options, futures, indices, forex, and crypto.
provider:
  name: "Massive (formerly Polygon.io)"
  website: "https://massive.com"
  github: "https://github.com/massive-com"
  docs: "https://massive.com/docs"
credentials:
  - name: MASSIVE_API_KEY
    description: Massive API key from https://massive.com/dashboard/keys. Existing Polygon.io keys work unchanged. Treat as sensitive.
    required: true
  - name: MASSIVE_S3_ACCESS_KEY
    description: S3 Access Key from https://massive.com/dashboard/keys. Only needed for Flat Files bulk downloads. Optional.
    required: false
  - name: MASSIVE_S3_SECRET_KEY
    description: S3 Secret Key from https://massive.com/dashboard/keys. Only needed for Flat Files. Optional.
    required: false
warnings:
  - Store credentials in a .env file or secret manager — never hardcode or log them.
  - Real-time WebSocket data requires a paid Massive subscription.
  - One concurrent WebSocket connection per asset class is allowed by default.
---

# Massive (formerly Polygon.io) — Data Feed Skill

Market data for OpenClaw. Does not execute trades — pair with `snaptrade-trading` for execution.

| Method | Best For |
|---|---|
| REST API | On-demand quotes, OHLCV bars, historical records |
| WebSocket | Real-time streaming — live trades, quotes, minute bars |
| Flat Files | Bulk historical CSVs — backtesting, ML datasets |

---

## Setup

```bash
bash scripts/setup.sh
source .venv-massive/bin/activate
```

API keys: https://massive.com/dashboard/keys

---

## SDK Initialization

```python
import os
from massive import Client

client = Client(api_key=os.environ["MASSIVE_API_KEY"])
```

---

## Raw HTTP (alternative)

```python
import requests

API_KEY = os.environ["MASSIVE_API_KEY"]
BASE_URL = "https://api.massive.com/v1"

resp = requests.get(f"{BASE_URL}/stocks/trades",
    params={"apiKey": API_KEY, "ticker": "AAPL"})
```

---

## Reference Files

| Task | Read |
|---|---|
| Stocks — quotes, trades, OHLCV, fundamentals | `references/stocks.md` |
| Options — chains, Greeks, trades, quotes | `references/options.md` |
| Futures — prices, historical bars | `references/futures.md` |
| Crypto — prices, trades, OHLCV | `references/crypto.md` |
| Real-time streaming | `references/websocket.md` |
| Bulk historical CSV downloads | `references/flat-files.md` |

---

## Response Format

```json
{ "status": "OK", "count": 10, "results": [ ... ] }
```

Always check `status == "OK"` before using `results`.

---

## Constraints

- Free plan: 15-min delayed data, 5 REST requests/min
- Real-time data requires a paid plan
- WebSocket: one connection per asset class by default
- Flat Files available ~11:00 AM ET the following trading day
