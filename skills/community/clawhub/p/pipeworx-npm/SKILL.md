---
name: pipeworx-npm
description: npm MCP — wraps the npm Registry API (free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/npm
---

# pipeworx-npm

npm MCP — wraps the npm Registry API (free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `search_packages`
- `get_package`
- `get_downloads`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-npm": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/npm/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/npm](https://pipeworx.io/packs/npm)
