---
name: binance-earn
description: |
  Query Binance Simple Earn product lists, subscribe to and redeem earn products,
  and check earn account positions. Use when fetching flexible or locked earn products,
  subscribing to earn products, redeeming earn products, or querying earn holdings.
metadata: '{"openclaw":{"requires":{"env":["BINANCE_API_KEY","BINANCE_API_SECRET"]}}}'
---

# Binance Earn Skill

All Binance Earn API operations are encapsulated in `{baseDir}/../bin/earn-api.ts`. Do NOT construct curl commands manually — always use the CLI below.

Before any write operation (subscribe / redeem), run authorization check first via `{baseDir}/../bin/auth-check.ts`.

## CLI Reference

```bash
# List products
node {baseDir}/../bin/earn-api.ts list-flexible [--asset BNB] [--size 10]
node {baseDir}/../bin/earn-api.ts list-locked   [--asset USDT] [--size 10]

# Subscribe
node {baseDir}/../bin/earn-api.ts subscribe-flexible --productId BNB001 --amount 100
node {baseDir}/../bin/earn-api.ts subscribe-locked   --projectId USDT30D --amount 500

# Redeem
node {baseDir}/../bin/earn-api.ts redeem-flexible --productId BNB001 --amount 100
node {baseDir}/../bin/earn-api.ts redeem-flexible --productId BNB001 --all
node {baseDir}/../bin/earn-api.ts redeem-locked   --positionId 12345

# Query positions & earn account
node {baseDir}/../bin/earn-api.ts positions --type flexible [--asset BNB]
node {baseDir}/../bin/earn-api.ts positions --type locked   [--asset USDT]
node {baseDir}/../bin/earn-api.ts account

# For spot balance breakdown: node {baseDir}/../bin/earn-api.ts balance
# For price queries: use the Binance Spot skill
```

All commands output JSON to stdout. On error, exit code is non-zero and error JSON is written to stderr.

## Error Codes

The script handles Binance API errors. When an error occurs, interpret the response:

| Code | Meaning | What to tell the user |
|------|---------|----------------------|
| -6003, -6004 | Product unavailable | Product is not available or not in purchase status |
| -6005 | Below minimum | Amount is below the minimum purchase limit |
| -6011, -6014 | Quota exceeded | Product quota is full, suggest alternatives |
| -6012, -6018 | Insufficient balance | Show available balance |
| -6006, -6007, -6008 | Redeem error | Explain the specific redemption issue |
| Other | API error | Show error message, do not auto-retry |
