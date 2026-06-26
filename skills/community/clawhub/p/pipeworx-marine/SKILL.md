---
name: pipeworx-marine
description: Marine MCP — wraps marine-api.open-meteo.com (free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/marine
---

# pipeworx-marine

Marine MCP — wraps marine-api.open-meteo.com (free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `get_wave_forecast`
- `get_current_waves`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-marine": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/marine/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/marine](https://pipeworx.io/packs/marine)
