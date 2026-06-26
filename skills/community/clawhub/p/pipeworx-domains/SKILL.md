---
name: pipeworx-domains
description: Search registered domain names by keyword and TLD — find what's taken via Domainsdb.info
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🌐"
    homepage: https://pipeworx.io/packs/domains
---

# Domain Search

Search for registered domain names matching a keyword. Filter by TLD zone (.com, .net, .io, etc.) to see what's already taken. Useful for brand research, competitive analysis, and domain name brainstorming.

## Tools

- **`search_domains`** — Search registered domains by keyword, optionally filtered by TLD. Returns domain names, creation dates, and update timestamps.

## When to use

- Checking if variations of a brand name are registered
- Competitive research — see who owns domains around a keyword
- Domain squatting analysis for a particular term
- Brainstorming domain names by seeing what patterns are taken

## Example: search for "weather" domains in .io

```bash
curl -s -X POST https://gateway.pipeworx.io/domains/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_domains","arguments":{"query":"weather","zone":"io","limit":5}}}'
```

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-domains": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/domains/mcp"]
    }
  }
}
```
