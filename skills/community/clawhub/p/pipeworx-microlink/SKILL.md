---
name: pipeworx-microlink
description: Microlink MCP — wraps Microlink API (free tier, no auth required)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/microlink
---

# pipeworx-microlink

Microlink MCP — wraps Microlink API (free tier, no auth required). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `get_metadata`
- `take_screenshot`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-microlink": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/microlink/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/microlink](https://pipeworx.io/packs/microlink)
