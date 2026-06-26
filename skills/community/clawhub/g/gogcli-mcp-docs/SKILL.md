---
name: gogcli-mcp-docs
description: Use when the user asks to read, write, edit, export, or comment on Google Docs. Triggers for requests involving document editing, inserting text, exporting as PDF/HTML/DOCX/RTF/ODT/EPUB, sed-like find-replace, managing document tabs, or working with comments and replies. Includes auth and Docs tools only.
---

# gogcli-mcp-docs

Extended Google Docs MCP server via [gogcli](https://github.com/openclaw/gogcli) — 30 tools: auth + 7 base Docs + 18 extra dedicated Docs tools.

- **Source:** [github.com/chrischall/gogcli-mcp](https://github.com/chrischall/gogcli-mcp)

## Requirements

- [gogcli](https://github.com/openclaw/gogcli) installed and authenticated
- Node.js 18 or later

## Setup

```json
{
  "mcpServers": {
    "gogcli-docs": {
      "command": "npx",
      "args": ["-y", "gogcli-mcp-docs"],
      "env": {
        "GOG_ACCOUNT": "you@gmail.com"
      }
    }
  }
}
```

## Extra Docs Tools

| Tool | What it does |
|------|-------------|
| `gog_docs_append` | Append text or markdown to the end of a doc |
| `gog_docs_copy` | Copy a document |
| `gog_docs_delete` | Delete content by character index range |
| `gog_docs_edit` | Find and replace with case-sensitivity |
| `gog_docs_export` | Export as PDF, TXT, HTML, DOCX, RTF, ODT, or EPUB |
| `gog_docs_format` | Apply character / paragraph formatting |
| `gog_docs_insert` | Insert text at a specific position |
| `gog_docs_list_tabs` | List all document tabs |
| `gog_docs_read` | Read doc as plain text or raw JSON |
| `gog_docs_sed` | Stream-edit with sed-like regex |
| `gog_docs_trash` | Move a doc to Drive trash |
| `gog_docs_update` | Update content at a specific position |
| `gog_docs_comments_list` | List comments (open or resolved) |
| `gog_docs_comments_get` | Get a comment with replies |
| `gog_docs_comments_add` | Add a comment with optional quoted text |
| `gog_docs_comments_reply` | Reply to a comment |
| `gog_docs_comments_resolve` | Resolve a comment |
| `gog_docs_comments_delete` | Delete a comment |

Plus 5 auth tools and 7 base Docs tools.

### `gog_docs_append` with `markdown: true` — known limitations

Three bugs in gogcli's upstream markdown→Docs converter to be aware of:

- **3+ tables in one call** reorders the trailing punctuation of the paragraph before the 3rd table — split into multiple calls with ≤2 tables each ([openclaw/gogcli#607](https://github.com/openclaw/gogcli/issues/607)).
- **Inline `**bold**` / `*italic*` / `` `code` `` inside table cells** renders as literal characters — insert plain cell text, then apply formatting via `gog_docs_format` ([openclaw/gogcli#608](https://github.com/openclaw/gogcli/issues/608)).
- **Empty-header tables** leak the last data row as literal pipe text — always supply a non-empty header row ([openclaw/gogcli#609](https://github.com/openclaw/gogcli/issues/609)).
