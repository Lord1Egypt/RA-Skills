---
name: pipeworx-iconify
description: Search 200,000+ open-source icons across 150+ collections — Material Design, Font Awesome, Heroicons, Lucide, and more
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🔣"
    homepage: https://pipeworx.io/packs/iconify
---

# Iconify

A unified API for 200,000+ open-source icons across 150+ collections including Material Design Icons, Font Awesome, Heroicons, Lucide, Tabler, and many more. Search by keyword, retrieve SVG data, or browse available collections.

## Tools

- **`search_icons`** — Search for icons by keyword across all collections (e.g., "home", "arrow", "user")
- **`get_icons`** — Retrieve SVG data for specific icons in a collection by prefix and name
- **`list_collections`** — Browse all available icon collections with metadata

## When to use

- "I need a settings gear icon" — search for "settings" and pick from multiple styles
- Fetching SVG icon data to embed directly in a web page or app
- Comparing icon styles across collections (Material vs. Heroicons vs. Lucide)
- Building an icon picker component

## Example: search for "download" icons

```bash
curl -s -X POST https://gateway.pipeworx.io/iconify/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_icons","arguments":{"query":"download","limit":5}}}'
```

Returns icon names with their collection prefix (e.g., "mdi:download", "heroicons:arrow-down-tray").

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-iconify": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/iconify/mcp"]
    }
  }
}
```
