---
name: pipeworx-pokemon
description: Pokemon MCP — wraps PokéAPI (free, no auth required)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/pokemon
---

# pipeworx-pokemon

Pokemon MCP — wraps PokéAPI (free, no auth required). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `get_pokemon`
- `get_type`
- `get_ability`
- `get_evolution_chain`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-pokemon": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/pokemon/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/pokemon](https://pipeworx.io/packs/pokemon)
