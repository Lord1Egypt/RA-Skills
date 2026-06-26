---
name: pipeworx-iplookup
description: IP Lookup MCP — ip-api.com (free, no auth for basic usage)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/iplookup
---

# pipeworx-iplookup

IP Lookup MCP — ip-api.com (free, no auth for basic usage). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `geolocate_ip`
- `batch_geolocate`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-iplookup": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/iplookup/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/iplookup](https://pipeworx.io/packs/iplookup)
