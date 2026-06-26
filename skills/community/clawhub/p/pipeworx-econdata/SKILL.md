---
name: pipeworx-econdata
description: US economic indicators from the Bureau of Labor Statistics — unemployment, CPI, and employment by industry
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📊"
    homepage: https://pipeworx.io/packs/econdata
---

# US Economic Data (BLS)

Access official US economic statistics from the Bureau of Labor Statistics. Pull unemployment rates, Consumer Price Index (CPI), and employment figures by industry. Query any BLS time series directly or use the convenience tools.

## Tools

| Tool | Description |
|------|-------------|
| `get_series` | Fetch any BLS time series by ID (e.g., "CUUR0000SA0" for CPI) |
| `get_unemployment` | Civilian unemployment rate (seasonally adjusted) |
| `get_cpi` | Consumer Price Index for all urban consumers |
| `get_employment_by_industry` | Total nonfarm employment by industry sector |

## Scenarios

- "What's the current US unemployment rate?" — call `get_unemployment`
- Tracking inflation trends via CPI over a specific year range
- Comparing employment growth across industries (healthcare, tech, manufacturing)
- Building economic dashboards with official government data

## Example: CPI for 2022-2024

```bash
curl -s -X POST https://gateway.pipeworx.io/econdata/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_cpi","arguments":{"start_year":"2022","end_year":"2024"}}}'
```

Returns monthly CPI values with period name, year, and value.

## Setup

```json
{
  "mcpServers": {
    "pipeworx-econdata": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/econdata/mcp"]
    }
  }
}
```
