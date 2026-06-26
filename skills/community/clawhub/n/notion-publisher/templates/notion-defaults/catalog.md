---
name: notion-publisher-notion-default-template-cache
description: Example cache registry for Notion database default templates.
---

# Cached Notion Default Templates

This file maps Notion databases or template IDs to local cached Markdown templates.

For public distribution, keep this file generic. Do not commit private database names, workspace URLs, database IDs, data source IDs, template IDs, or personal page URLs.

Example:

| Database | Database ID | Template | Template ID | Local file |
|---|---|---|---|---|
| Example Blog Database | `example-database-id` | Article Template | `example-template-id` | `templates/notion-defaults/example-article-template.md` |

Refresh policy:
- Prefer a local cached file for normal publishing.
- Fetch a Notion template only when the user asks to refresh/sync the cache, or when no matching local cache exists.
- If refreshed, overwrite the matching local file and update `cached_at`.
