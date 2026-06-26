---
name: gogcli-mcp-slides
description: Use when the user asks to create, edit, read, or export Google Slides presentations. Triggers for requests involving slides, decks, presentations, speaker notes, slide images, markdown-to-slides, presentation templates with placeholder replacement, or exporting to pdf/pptx. Includes auth and Slides tools only.
---

# gogcli-mcp-slides

Extended Google Slides MCP server via [gogcli](https://github.com/openclaw/gogcli) — 18 tools: auth + 12 Slides + 1 run escape hatch.

- **Source:** [github.com/chrischall/gogcli-mcp](https://github.com/chrischall/gogcli-mcp)

## Requirements

- [gogcli](https://github.com/openclaw/gogcli) installed and authenticated
- Node.js 18 or later

## Setup

```json
{
  "mcpServers": {
    "gogcli-slides": {
      "command": "npx",
      "args": ["-y", "gogcli-mcp-slides"],
      "env": {
        "GOG_ACCOUNT": "you@gmail.com"
      }
    }
  }
}
```

## Slides Tools

| Tool | What it does |
|------|-------------|
| `gog_slides_export` | Export a presentation to pdf or pptx |
| `gog_slides_info` | Get presentation metadata |
| `gog_slides_create` | Create a new presentation (optionally from a template) |
| `gog_slides_create_from_markdown` | Create a new presentation from markdown |
| `gog_slides_create_from_template` | Create from a template with placeholder replacements |
| `gog_slides_copy` | Copy a presentation |
| `gog_slides_add_slide` | Add a slide from a local image |
| `gog_slides_list_slides` | List slides in a presentation |
| `gog_slides_delete_slide` | Delete a slide |
| `gog_slides_read_slide` | Read the content of a slide |
| `gog_slides_update_notes` | Update speaker notes |
| `gog_slides_replace_slide` | Replace the image on an existing slide |

Plus 5 auth tools and `gog_slides_run` for anything not covered.
