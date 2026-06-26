---
name: pipeworx-launches
description: Launches MCP — wraps Launch Library 2 API (ll.thespacedevs.com, free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/launches
---

# pipeworx-launches

Launches MCP — wraps Launch Library 2 API (ll.thespacedevs.com, free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `get_upcoming_launches`
- `get_past_launches`
- `get_launch`
- `search_launches`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-launches": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/launches/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/launches](https://pipeworx.io/packs/launches)
