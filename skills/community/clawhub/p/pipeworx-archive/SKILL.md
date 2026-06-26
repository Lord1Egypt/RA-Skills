---
name: pipeworx-archive
description: Archive MCP — wraps the Internet Archive APIs (free, no auth)
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "⚡"
    homepage: https://pipeworx.io/packs/archive
---

# Pipeworx archive

Archive MCP — wraps the Internet Archive APIs (free, no auth)

Free, no API key required. Part of the [Pipeworx](https://pipeworx.io) open MCP gateway.

## When to Use

Use this skill when the user asks about archive data or needs to query archive information.

## Available Tools


## How to Call

The Pipeworx gateway speaks JSON-RPC 2.0 over HTTP POST.

### List available tools
```bash
curl -s -X POST https://gateway.pipeworx.io/archive/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

### Call a tool
```bash
curl -s -X POST https://gateway.pipeworx.io/archive/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"TOOL_NAME","arguments":{"param":"value"}}}'
```

### MCP Client Config
```json
{
  "mcpServers": {
    "pipeworx-archive": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/archive/mcp"]
    }
  }
}
```

## Notes

- No authentication required
- Free for all users
- Rate limited for anonymous users (sign up at pipeworx.io for higher limits)
- Returns JSON-RPC 2.0 responses
