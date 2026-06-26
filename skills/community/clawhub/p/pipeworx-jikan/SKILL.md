---
name: pipeworx-jikan
description: Jikan MCP — wraps the Jikan v4 API (anime/manga data, free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/jikan
---

# pipeworx-jikan

Jikan MCP — wraps the Jikan v4 API (anime/manga data, free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `search_anime`
- `get_anime`
- `top_anime`
- `search_characters`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-jikan": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/jikan/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/jikan](https://pipeworx.io/packs/jikan)
