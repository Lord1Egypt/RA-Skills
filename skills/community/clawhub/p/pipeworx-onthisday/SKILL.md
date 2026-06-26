---
name: pipeworx-onthisday
description: On This Day MCP — wraps byabbe.se/on-this-day (free, no auth)
version: 1.0.0
metadata:
  openclaw:
    homepage: https://pipeworx.io/packs/onthisday
---

# pipeworx-onthisday

On This Day MCP — wraps byabbe.se/on-this-day (free, no auth). Free, no API key. Part of [Pipeworx](https://pipeworx.io).

## Tools

- `get_events`
- `get_births`
- `get_deaths`

## Connect

```json
{
  "mcpServers": {
    "pipeworx-onthisday": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/onthisday/mcp"]
    }
  }
}
```

More at [pipeworx.io/packs/onthisday](https://pipeworx.io/packs/onthisday)
