---
name: pipeworx-mhw
description: MHW MCP — Monster Hunter World data (mhw-db.com, free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/mhw
---

# pipeworx-mhw

MHW MCP — Monster Hunter World data (mhw-db.com, free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `get_monsters`
- `get_weapons`
- `get_armor`
- `get_skills`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-mhw": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/mhw/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/mhw](https://pipeworx.io/packs/mhw)
