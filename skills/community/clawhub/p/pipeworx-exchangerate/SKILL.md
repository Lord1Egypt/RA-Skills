---
name: pipeworx-exchangerate
description: Simple currency exchange rates — all rates for a base currency or a direct pair lookup via open.er-api.com
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "💵"
    homepage: https://pipeworx.io/packs/exchangerate
---

# ExchangeRate API

A lightweight exchange rate service. Get all rates for a base currency in one call, or fetch a specific currency pair. Uses data from open.er-api.com with rates updated daily.

## Tools

- **`get_rates`** — All exchange rates relative to a base currency (e.g., "USD" returns rates for EUR, GBP, JPY, and 150+ others)
- **`get_pair`** — Direct exchange rate between two specific currencies

## Differs from the `exchange` pack

This pack is simpler — no historical rates or amount conversion, just current rates. Use this when you need a quick rate check or a full rate table. Use the `exchange` pack when you need conversion math or historical data.

## Example: USD rates

```bash
curl -s -X POST https://gateway.pipeworx.io/exchangerate/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_rates","arguments":{"base":"USD"}}}'
```

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-exchangerate": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/exchangerate/mcp"]
    }
  }
}
```
