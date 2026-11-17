---
name: pollen
description: Draft a launch page for a product or business as standalone HTML, using Pollen's remote MCP server. Use when someone wants a first draft of a product or business site they can save, open and host anywhere.
version: 1.0.1
metadata:
  openclaw:
    homepage: https://pollensites.com
    emoji: "🌼"
---

# Pollen

Pollen makes a draft launch page as standalone HTML. You give it a business name and a
short description, and it returns a page in one of three styles. Nothing is published.

## Connect

Pollen is a remote MCP server over Streamable HTTP at `https://pollensites.com/mcp`.
It needs no account or API key. For clients that take JSON configuration:

```json
{
  "mcpServers": {
    "pollen": {
      "type": "http",
      "url": "https://pollensites.com/mcp"
    }
  }
}
```

## Make a draft

1. Initialize the MCP session and call `tools/list`. The returned schemas govern the calls.
2. Call `start_draft` with public business copy:
   - `name`: the business or product name, 1–120 characters.
   - `brief`: what it does, 1–2000 characters.
   - `headline`: optional, up to 160 characters.
   - `style`: `editorial` (portfolio), `studio` (SaaS) or `bold` (consumer).
3. `start_draft` returns a draft id. Call `check_draft` once with that id. It returns a
   filename and the standalone HTML right away.
4. Give the person the HTML to save and open.

## What the page includes

The HTML has semantic sections, a page title, a description, and JSON-LD with WebPage and
Organization facts from the draft. These help software read the page. They don't guarantee
discovery, search rankings or citations.

## Limits

- Use public business copy only, never secrets or private contact details. Anyone holding a
  draft's id can read it.
- Each caller can start up to 60 drafts at once, refilling at one a second.
- Each layout includes its own artwork. Pollen doesn't generate custom images.
- Pollen doesn't publish, host, take payments or send messages. The exported page has no MCP
  server or llms.txt file of its own.

## More

- Agent instructions: https://pollensites.com/connect.md
- Privacy: https://pollensites.com/legal/privacy
- Terms: https://pollensites.com/legal/terms
- Support: auto-units@auto-units.com
