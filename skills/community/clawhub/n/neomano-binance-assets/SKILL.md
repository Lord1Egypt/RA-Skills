---
name: neomano-binance-assets
description: Safe, read-only Binance balance viewer (Spot wallet) using Binance API keys with READ-ONLY permissions. Use when the user wants to check holdings/balances/assets without trading.
metadata: {"clawdbot":{"emoji":"🏦","requires":{"bins":["python3"],"env":["BINANCE_API_KEY","BINANCE_API_SECRET"]},"primaryEnv":"BINANCE_API_KEY"}}
---

## Safety (mandatory)

This skill is designed to be a **safe way to query balances**.

- **READ-ONLY keys only**: In Binance, create an API key with **Read-only / Enable Reading** permissions.
- Do **not** enable trading, margin, futures, transfers, or withdrawals.
- (Recommended) Restrict the API key by **IP allowlist**.
- Never print or send `BINANCE_API_SECRET`.

## Credentials

Set these environment variables (recommended: `~/.openclaw/.env` on the gateway machine):

- `BINANCE_API_KEY`
- `BINANCE_API_SECRET`

## What it does

- Fetch Spot account balances via Binance signed endpoint:
  - `GET https://api.binance.com/api/v3/account`
- By default, it filters to **non-zero** assets.

## Run

```bash
python3 {baseDir}/scripts/assets.py
python3 {baseDir}/scripts/assets.py --all
python3 {baseDir}/scripts/assets.py --min 0.0001
```
