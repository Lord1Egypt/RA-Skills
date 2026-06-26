---
name: pipeworx-exchange
description: Currency exchange rates and conversion — current, historical, and all supported pairs via the Frankfurter API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "💱"
    homepage: https://pipeworx.io/packs/exchange
---

# Frankfurter Currency Exchange

Convert between 30+ currencies using the European Central Bank's reference rates via the Frankfurter API. Get current rates, convert amounts, look up historical rates back to 1999, and list all supported currencies.

## Tools

| Tool | Purpose |
|------|---------|
| `get_rate` | Current exchange rate between two currencies (e.g., USD to EUR) |
| `convert` | Convert a specific amount at today's rate |
| `get_historical_rate` | Exchange rate on a specific date (YYYY-MM-DD format, back to 1999-01-04) |
| `get_currencies` | List all supported currencies with full names |

## When to use

- "How much is 500 USD in Japanese Yen?" — `convert` with from=USD, to=JPY, amount=500
- Travel planning — check current rates before a trip
- Historical analysis — track how GBP/EUR changed over the past year
- E-commerce apps that need to display prices in local currencies

## Example: convert 1000 EUR to GBP

```bash
curl -s -X POST https://gateway.pipeworx.io/exchange/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"convert","arguments":{"from":"EUR","to":"GBP","amount":1000}}}'
```

```json
{
  "from": "EUR",
  "to": "GBP",
  "amount": 1000,
  "result": 858.42,
  "rate": 0.85842,
  "date": "2024-03-15"
}
```

## MCP client config

```json
{
  "mcpServers": {
    "pipeworx-exchange": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/exchange/mcp"]
    }
  }
}
```
