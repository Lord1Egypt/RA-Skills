---
name: pipeworx-poetry
description: Poetry MCP — PoetryDB API (free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/poetry
---

# pipeworx-poetry

Poetry MCP — PoetryDB API (free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `search_poems`
- `poems_by_author`
- `random_poems`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-poetry": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/poetry/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/poetry](https://pipeworx.io/packs/poetry)
