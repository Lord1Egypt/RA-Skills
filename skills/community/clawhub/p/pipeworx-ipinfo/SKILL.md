---
name: pipeworx-ipinfo
description: IPInfo MCP — wraps ipinfo.io (free tier, no auth required for basic usage)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/ipinfo
---

# pipeworx-ipinfo

IPInfo MCP — wraps ipinfo.io (free tier, no auth required for basic usage). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `lookup_ip`
- `get_my_ip`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-ipinfo": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/ipinfo/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/ipinfo](https://pipeworx.io/packs/ipinfo)
