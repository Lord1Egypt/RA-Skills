---
name: pipeworx-ukpolice
description: UK street-level crime data — reported crimes by location, police force directory, and case outcomes from data.police.uk
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🚔"
    homepage: https://pipeworx.io/packs/ukpolice
---

# UK Police Data

Street-level crime reports from every police force in England, Wales, and Northern Ireland. Query crimes near a location for a specific month, browse all police forces, and look up case outcomes.

## Tools

| Tool | Description |
|------|-------------|
| `get_crimes` | Street-level crimes near a lat/lng for a given month (YYYY-MM format) |
| `get_forces` | List all UK police forces |
| `get_outcomes` | Case outcomes (charged, cautioned, no further action, etc.) near a location |

## When to use

- Crime mapping and neighborhood safety analysis
- Journalism and public interest reporting on local crime trends
- Building location-based safety indicators for property or travel apps
- Research on policing outcomes and their geographic distribution

## Example: crimes near Westminster in January 2024

```bash
curl -s -X POST https://gateway.pipeworx.io/ukpolice/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_crimes","arguments":{"lat":51.5007,"lng":-0.1246,"month":"2024-01"}}}'
```

Returns crime category, location (street name and coordinates), outcome status, and unique ID.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-ukpolice": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/ukpolice/mcp"]
    }
  }
}
```
