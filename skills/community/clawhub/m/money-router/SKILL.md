---
name: Money Router
slug: money-router
description: Find the cheapest way to send money between any two currencies. Compares 22+ crypto exchanges and 19 remittance providers in real-time. Free, open source, no affiliate fees.
author: Coinnect
version: 1.0.0
homepage: https://coinnect.bot
repository: https://github.com/coinnect-dev/coinnect
license: MIT
tags:
  - finance
  - remittance
  - crypto
  - money-transfer
  - exchange-rates
  - comparison
  - routing
  - mcp
---

# Money Router

Compare every way to send money across borders — fiat, crypto, and P2P — in one query.

## What it does

Given a source currency, destination currency, and amount, Money Router finds the cheapest route across 22+ crypto exchanges and 19 remittance providers. It returns ranked routes with step-by-step instructions, fees, exchange rates, and estimated delivery time.

Routes can be multi-hop: for example, USD → USDC (Coinbase) → MXN (Bitso) may be cheaper than USD → MXN (Wise) for certain amounts.

## Tools

### `coinnect_quote`

Find the cheapest routes to send money from one currency to another.

**Parameters:**
- `from` (string, required) — Source currency code (e.g., USD, EUR, BTC)
- `to` (string, required) — Destination currency code (e.g., MXN, NGN, PHP)
- `amount` (number, required) — Amount in source currency

**Example:**
```
GET https://coinnect.bot/v1/quote?from=USD&to=MXN&amount=500
```

**Returns:** Ranked routes with total cost %, recipient amount, provider path, and step-by-step instructions.

### `coinnect_corridors`

List the most active currency corridors with provider information.

```
GET https://coinnect.bot/v1/corridors
```

### `coinnect_verify`

Report a real rate you observed at a provider. Helps calibrate estimated rates toward real values. You earn quest rewards for verified reports.

**Parameters:**
- `from_currency` (string, required)
- `to_currency` (string, required)
- `provider` (string, required)
- `rate` (number, required) — The exchange rate you observed
- `fee_pct` (number, optional) — The fee percentage if known

```
POST https://coinnect.bot/v1/verify
```

### `coinnect_quests`

List open rate verification bounties. Complete quests by verifying rates at providers.

```
GET https://coinnect.bot/v1/quests
```

## MCP Server

Native MCP support for Claude and any MCP-compatible agent:

```bash
python -m coinnect.mcp_server
```

Tools: `coinnect_quote`, `coinnect_corridors`, `coinnect_explain_route`, `coinnect_verify`, `coinnect_quests`

## API Access

- **No auth required** for basic use (20 req/day)
- **Free API key** via `POST /v1/keys` (1,000 req/day, no signup)
- **Self-hosted** option: clone repo, run locally, unlimited

## What makes this different

- **Non-profit** — rankings are by cost, never by who pays us
- **Open source** (MIT) — audit the code, fork it, self-host it
- **Open data** (CC-BY 4.0) — historical rate snapshots as free CSV
- **Multi-hop routing** — finds paths through crypto intermediaries that single-provider tools miss
- **22+ live exchanges** — Binance, Kraken, Coinbase, OKX, Wise, and more
- **Community verification** — report real rates, earn quest rewards

## Links

- **Live:** [coinnect.bot](https://coinnect.bot)
- **API docs:** [coinnect.bot/docs](https://coinnect.bot/docs)
- **Whitepaper:** [coinnect.bot/whitepaper](https://coinnect.bot/whitepaper)
- **GitHub:** [coinnect-dev/coinnect](https://github.com/coinnect-dev/coinnect)
- **Telegram bot:** [@the_coinnect_bot](https://t.me/the_coinnect_bot)
