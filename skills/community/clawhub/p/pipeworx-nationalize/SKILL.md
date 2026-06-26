---
name: pipeworx-nationalize
description: Nationalize MCP — nationality prediction from first name (nationalize.io, free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/nationalize
---

# pipeworx-nationalize

Nationalize MCP — nationality prediction from first name (nationalize.io, free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `predict_nationality`
- `batch_predict`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-nationalize": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/nationalize/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/nationalize](https://pipeworx.io/packs/nationalize)
