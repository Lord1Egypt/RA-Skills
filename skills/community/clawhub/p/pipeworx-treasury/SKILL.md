---
name: pipeworx-treasury
description: US fiscal data — national debt, Treasury interest rates, and federal spending breakdowns from the Treasury Fiscal Data API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🇺🇸"
    homepage: https://pipeworx.io/packs/treasury
---

# US Treasury Fiscal Data

Official US government fiscal data. Check the current national debt (down to the penny), browse Treasury average interest rates by security type, and analyze federal spending by category and fiscal year.

## Tools

| Tool | Description |
|------|-------------|
| `get_national_debt` | Current US national debt — total public debt outstanding |
| `get_treasury_rates` | Average interest rates on Treasury securities by type and date |
| `get_federal_spending` | Federal spending breakdown by budget function and fiscal year |

## Scenarios

- "What is the current US national debt?" — a single call gives you the answer
- Tracking how Treasury bond rates have changed
- Analyzing where federal dollars are going by spending category
- Building economic research tools with authoritative government data

## Example: current national debt

```bash
curl -s -X POST https://gateway.pipeworx.io/treasury/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_national_debt","arguments":{}}}'
```

Returns the total public debt outstanding with the record date.

## Setup

```json
{
  "mcpServers": {
    "pipeworx-treasury": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/treasury/mcp"]
    }
  }
}
```
