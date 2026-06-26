---
name: kalshi-trading
description: Read-only Kalshi OpenAPI scouting skill for market discovery, liquidity checks, and market validation. Use for scanning and ranking Kalshi opportunities. Pair with a separate paper-trading skill if you want open/close execution.
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["node"] }
      }
  }
---

# Kalshi Trading (OpenAPI, Read-Only)

Use this skill for Kalshi scouting and market validation only.

## Rules

- Use OpenAPI read endpoints for market discovery and validation.
- This skill does not place, amend, or cancel orders.
- This skill does not include paper ledger execution scripts.

## Primary Commands

Exchange status:

```bash
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs status --pretty
```

Broad market scan:

```bash
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs markets --status open --limit 1000 --pretty
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs events --limit 100 --pretty
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs series --limit 400 --pretty
```

Focused validation:

```bash
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs market --ticker <TICKER> --pretty
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs trades --ticker <TICKER> --limit 200 --pretty
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs orderbook --ticker <TICKER> --pretty
```

## Optional Integration: Paper Ledger Skill Required

If you want paper open/close workflows, install and use a separate paper-trading skill that provides the execution script.
This Kalshi skill can supply candidate/market data to that separate skill.

```bash
node --experimental-strip-types skills/paper-trading/scripts/paper_trading.ts status --account kalshi --format json --pretty
```

## Environment

Optional override (defaults to Kalshi production API):

```bash
export KALSHI_BASE_URL="https://api.elections.kalshi.com/trade-api/v2"
```

## Tests

Run the Kalshi reader smoke tests:

```bash
node --test skills/kalshi-trading/tests/kalshi_openapi_reader.test.mjs
```
