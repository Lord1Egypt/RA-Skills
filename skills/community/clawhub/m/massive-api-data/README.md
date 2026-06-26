# Massive Data Feed Skill — Setup Guide

This skill provides OpenClaw with real-time and historical market data via the
[Massive API](https://massive.com), covering stocks, options, futures, crypto,
forex, and indices.

---

## Step 1 — Create a Massive Account

1. Go to https://massive.com/dashboard/signup and create an account
2. Verify your email
3. Go to https://massive.com/dashboard/keys to find your credentials

You will see:
- **API Key** → `MASSIVE_API_KEY` (used for REST + WebSocket)
- **S3 Access Key** → `MASSIVE_S3_ACCESS_KEY` (only needed for Flat Files)
- **S3 Secret Key** → `MASSIVE_S3_SECRET_KEY` (only needed for Flat Files)

> ⚠️ Keep your API key secure. Do not share it or commit it to git.

---

## Step 2 — Set Your Credentials

Add to a `.env` file in your OpenClaw working directory:

```
MASSIVE_API_KEY=your_api_key_here

# Only needed for bulk historical CSV downloads (Flat Files):
MASSIVE_S3_ACCESS_KEY=your_s3_access_key
MASSIVE_S3_SECRET_KEY=your_s3_secret_key
```

Or export in your shell:

```bash
export MASSIVE_API_KEY=your_api_key_here
```

> ⚠️ Add `.env` to your `.gitignore` — never commit credentials.

---

## Step 3 — Run Setup

```bash
bash scripts/setup.sh
source .venv-massive/bin/activate
```

---

## Data Access Methods

| Method | Use Case |
|---|---|
| REST API | On-demand queries — quotes, OHLCV, historical records |
| WebSocket | Real-time streaming — live trades, quotes, minute bars |
| Flat Files | Bulk historical CSVs — backtesting, ML model training |

**Free plan:** 15-minute delayed data, 5 REST requests/minute
**Paid plan:** Real-time data, higher rate limits, Flat Files access

See https://massive.com/pricing for plan details.

---

## Supported Asset Classes

- Stocks (NYSE, NASDAQ, all US exchanges)
- Options (US equity options)
- Futures (CME, CBOT, NYMEX, COMEX)
- Crypto (BTC, ETH, SOL, and more)
- Forex
- Indices

---

## Useful Links

- Dashboard & API Keys: https://massive.com/dashboard/keys
- REST API Docs: https://massive.com/docs/rest/quickstart
- WebSocket Docs: https://massive.com/docs/websocket/quickstart
- Flat Files Docs: https://massive.com/docs/flat-files/quickstart
- Pricing: https://massive.com/pricing
- Support: https://massive.com/contact
