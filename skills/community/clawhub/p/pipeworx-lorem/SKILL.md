---
name: pipeworx-lorem
description: Lorem MCP — wraps loripsum.net (free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/lorem
---

# pipeworx-lorem

Lorem MCP — wraps loripsum.net (free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `generate_paragraphs`
- `generate_with_options`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-lorem": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/lorem/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/lorem](https://pipeworx.io/packs/lorem)
