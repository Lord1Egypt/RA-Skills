---
name: notion
description: Use Notion through mcporter-backed MCP tools. Use when working with Notion pages, databases, search, content updates, or workspace lookups via an MCP-integrated Notion server.
---

# notion

Use Notion through `mcporter`.

Quick checks:

- `mcporter list notion --schema`
- `mcporter call notion.<tool> --args '{"query":"project notes"}'`

Keep credentials out of prompts and committed files. Load the Notion token from the runtime environment, normally as `NOTION_TOKEN`.

Before writes, inspect the target page or database and keep changes narrow unless the user asks for a broader update.
