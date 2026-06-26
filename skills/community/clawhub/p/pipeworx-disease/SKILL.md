---
name: pipeworx-disease
description: COVID-19 statistics — global totals, per-country breakdowns, historical trends, and vaccination data from disease.sh
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🦠"
    homepage: https://pipeworx.io/packs/disease
---

# COVID-19 Statistics

Real-time and historical COVID-19 data from disease.sh. Pull global totals, per-country stats, time-series trends, and vaccination numbers. Data is aggregated from Johns Hopkins, Worldometers, and government sources.

## Tools

| Tool | Description |
|------|-------------|
| `get_global_stats` | Current global totals: cases, deaths, recovered, active, tests |
| `get_country_stats` | Stats for a specific country by name or ISO code (e.g., "USA", "germany", "gb") |
| `get_historical` | Time-series data for cases, deaths, and recovered over N days |
| `get_vaccine_stats` | Vaccination totals — global or per country |

## Use cases

- Answering questions about COVID-19 statistics for a specific country
- Charting pandemic trends over time
- Comparing vaccination rates across countries
- Historical research on pandemic impact

## Example: Germany's COVID stats

```bash
curl -s -X POST https://gateway.pipeworx.io/disease/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_country_stats","arguments":{"country":"germany"}}}'
```

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-disease": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/disease/mcp"]
    }
  }
}
```
