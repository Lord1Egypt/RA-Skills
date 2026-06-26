---
name: olaxbt-nexus-data
description: "Access OlaXBT Nexus cryptocurrency data APIs — market data, news, KOL tracking, technical indicators, and trading insights. Uses a wallet-linked JWT; no private key in the skill."
metadata: {"clawdbot": {"requires": {"env": ["NEXUS_JWT"]}}}
---

# OlaXBT Nexus Data Skill

This skill provides access to OlaXBT Nexus cryptocurrency data APIs via a Python client. The skill uses a **JWT** only; it does not request or handle private keys. Obtain the JWT by following the spec (POST /auth/message → sign with your wallet → POST /auth/wallet → use the returned `token`).

## Required environment variable

| Variable | Purpose |
|----------|---------|
| `NEXUS_JWT` | Bearer token for the Nexus data API. Obtain it via the auth flow (POST /auth/message, sign with wallet, POST /auth/wallet). |

Optional: `NEXUS_AUTH_URL`, `NEXUS_DATA_URL` to override API base URLs.

## When to use this skill
- When you need real-time cryptocurrency market data
- When you want to analyze crypto news and sentiment
- When tracking key opinion leaders (KOLs) in crypto
- When analyzing technical indicators for trading
- When monitoring smart money flows

## Features
- 14 comprehensive API endpoints
- JWT-based auth (obtain token outside the skill; no private key here)
- Real-time market data
- KOL and sentiment tracking
- Technical indicators analysis

## Installation
```bash
pip install olaxbt-nexus-data
```

## Quick Start

1. Obtain a JWT using the [Nexus auth flow](https://github.com/olaxbt/olaxbt-skills-hub/blob/main/skills/nexus/SKILL.md): POST `/auth/message` with your wallet address, sign the returned message with your wallet (e.g. via OpenClaw or a one-time sign-in), then POST `/auth/wallet` to get the token.
2. Set the token and use the client:

```bash
export NEXUS_JWT="<your-jwt-token>"
```

```python
from olaxbt_nexus_data import NexusClient

client = NexusClient()  # uses NEXUS_JWT from env
client.authenticate()
news = client.news.get_latest(limit=10)
```

## Same API via HTTP (curl-style)

The underlying API is HTTP. You can call it with any client (curl, fetch, etc.) using the [Nexus Skills API spec](https://github.com/olaxbt/olaxbt-skills-hub/blob/main/skills/nexus/SKILL.md). This Python package is a wrapper that uses your existing JWT.

## Security
- The skill only reads `NEXUS_JWT` (and optional `NEXUS_*` URLs). It does not request or store private keys.
- All API calls use HTTPS; rate limiting is implemented.

## Repository
https://github.com/olaxbt/olaxbt-nexus-data
