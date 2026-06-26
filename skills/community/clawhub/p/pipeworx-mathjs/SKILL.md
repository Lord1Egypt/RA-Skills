---
name: pipeworx-mathjs
description: Math.js MCP — wraps the mathjs.org API (free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/mathjs
---

# pipeworx-mathjs

Math.js MCP — wraps the mathjs.org API (free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `evaluate`
- `convert_units`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-mathjs": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/mathjs/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/mathjs](https://pipeworx.io/packs/mathjs)
