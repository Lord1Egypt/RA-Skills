---
name: gogcli-mcp-sheets
description: Use when the user asks to read, write, format, or manage Google Sheets. Triggers for requests involving spreadsheet data, cell formatting, tab management, named ranges, merging cells, freezing rows/columns, exporting spreadsheets, or any Sheets operation. Includes auth and Sheets tools only.
---

# gogcli-mcp-sheets

Extended Google Sheets MCP server via [gogcli](https://github.com/openclaw/gogcli) — 35 tools: auth + 8 base Sheets + 22 extra dedicated Sheets tools.

- **Source:** [github.com/chrischall/gogcli-mcp](https://github.com/chrischall/gogcli-mcp)

## Requirements

- [gogcli](https://github.com/openclaw/gogcli) installed and authenticated
- Node.js 18 or later

## Setup

```json
{
  "mcpServers": {
    "gogcli-sheets": {
      "command": "npx",
      "args": ["-y", "gogcli-mcp-sheets"],
      "env": {
        "GOG_ACCOUNT": "you@gmail.com"
      }
    }
  }
}
```

## Extra Sheets Tools

| Tool | What it does |
|------|-------------|
| `gog_sheets_add_tab` | Add a new sheet tab |
| `gog_sheets_delete_tab` | Delete a sheet tab |
| `gog_sheets_rename_tab` | Rename a sheet tab |
| `gog_sheets_copy` | Copy a sheet to another spreadsheet |
| `gog_sheets_export` | Export as CSV, TSV, XLSX, PDF |
| `gog_sheets_freeze` | Freeze rows and/or columns |
| `gog_sheets_insert` | Insert rows or columns |
| `gog_sheets_merge` | Merge cells |
| `gog_sheets_unmerge` | Unmerge cells |
| `gog_sheets_format` | Apply cell formatting |
| `gog_sheets_number_format` | Set number format |
| `gog_sheets_read_format` | Read cell formatting |
| `gog_sheets_resize_columns` | Resize column widths |
| `gog_sheets_resize_rows` | Resize row heights |
| `gog_sheets_notes` | Read cell notes |
| `gog_sheets_update_note` | Add or update cell notes |
| `gog_sheets_links` | List hyperlinks in a range |
| `gog_sheets_set_links` | Set =HYPERLINK() cells in one call (batch) |
| `gog_sheets_snapshot` | Back up a whole spreadsheet before a risky edit |
| `gog_sheets_named_ranges_list` | List named ranges |
| `gog_sheets_named_ranges_get` | Get a named range |
| `gog_sheets_named_ranges_add` | Create a named range |
| `gog_sheets_named_ranges_update` | Update a named range |
| `gog_sheets_named_ranges_delete` | Delete a named range |

Plus 5 auth tools and 8 base Sheets tools.
