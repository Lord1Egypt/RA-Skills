---
name: obsidian-sheet-plus
version: 1.0.0
description: Use when working with Obsidian spreadsheet data — reading, writing, formatting, filtering, creating formulas, setting data validation, conditional formatting, merging cells, or managing sheets via the Sheet Plus plugin REST API. Triggers on tasks involving Excel-like operations in Obsidian, spreadsheet automation, data analysis, or bulk data manipulation.
tags:
  - obsidian
  - spreadsheet
  - excel
  - data-analysis
  - automation
  - productivity
  - formatting
  - sheet-plus
---

# Obsidian Sheet Plus Skill

Operate spreadsheet data through the Obsidian Sheet Plus plugin REST API. Supports reading, writing, formatting, filtering, formulas, data validation, conditional formatting, row/column operations, and cell merging.

## Prerequisites

1. **Obsidian is running** and the **Sheet Plus** plugin is enabled
2. The REST API service is started within the plugin (default `http://127.0.0.1:3000`)

## Base Configuration

| Field | Value |
|------|-----|
| Base URL | `http://127.0.0.1:3000` |
| Authentication | No auth by default (`requireApiKey: false`). If enabled, use Header `X-API-KEY: <key>` |
| Content-Type | `application/json` |

Base URL can be overridden via environment variable: `OBSIDIAN_SHEET_PLUS_BASE_URL=http://127.0.0.1:3000`

## Three-Step Safety Mode

Perform these checks in order before every operation:

```
1. GET / → Verify REST API is available
2. GET /get_sheet_list → Confirm the target sheet exists
3. Execute the specific operation
```

### Step 1 Failure Reference

| Error | Meaning | User Guidance |
|------|------|---------|
| Connection refused | Obsidian not running or plugin not enabled | "Please confirm Obsidian is running and Sheet Plus plugin is enabled" |
| Invalid API key (401) | API Key required | "Please obtain the API Key from Obsidian plugin settings and configure it" |
| Other errors | Port or configuration issue | "Please check REST API service status, default port 3000" |

## Tool Index

### Status Check
| Tool | Path | Description |
|------|------|------|
| [check-status](tools/check-status/SKILL.md) | `GET /` | Check API status and version |

### Read Data
| Tool | Path | Description |
|------|------|------|
| [get-sheet-list](tools/get-sheet-list/SKILL.md) | `GET /get_sheet_list` | Get all worksheet names |
| [get-sheet-data](tools/get-sheet-data/SKILL.md) | `GET /get_sheet_data` | Read cell data |
| [get-workbook](tools/get-workbook/SKILL.md) | `GET /get_workbook` | Get full workbook data |
| [get-max-rows](tools/get-max-rows/SKILL.md) | `GET /get_max_rows` | Get max row count |
| [get-max-columns](tools/get-max-columns/SKILL.md) | `GET /get_max_columns` | Get max column count |
| [get-filter](tools/get-filter/SKILL.md) | `GET /get_filter` | Get filter information |

### Write Data
| Tool | Path | Description |
|------|------|------|
| [set-sheet-data](tools/set-sheet-data/SKILL.md) | `POST /set_sheet_data` | Write/update cell data |
| [create-sheet](tools/create-sheet/SKILL.md) | `POST /create_sheet` | Create a new worksheet |

### Formulas & Styles
| Tool | Path | Description |
|------|------|------|
| [set-formula](tools/set-formula/SKILL.md) | `POST /set_formula` | Set cell formulas |
| [set-range-style](tools/set-range-style/SKILL.md) | `POST /set_range_style` | Set range style (font, color, borders, etc.) |

### Data Validation
| Tool | Path | Description |
|------|------|------|
| [set-data-validation](tools/set-data-validation/SKILL.md) | `POST /set_data_validation` | Set data validation rules |
| [clear-data-validation](tools/clear-data-validation/SKILL.md) | `POST /clear_data_validation` | Clear data validation rules |

### Clear Data
| Tool | Path | Description |
|------|------|------|
| [clear-contents](tools/clear-contents/SKILL.md) | `POST /clear_contents` | Clear cell contents |
| [clear-format](tools/clear-format/SKILL.md) | `POST /clear_format` | Clear cell formatting |
| [clear-all](tools/clear-all/SKILL.md) | `POST /clear_all` | Clear both contents and formatting |

### Filters
| Tool | Path | Description |
|------|------|------|
| [add-filter](tools/add-filter/SKILL.md) | `POST /add_filter` | Add a filter |
| [remove-filter](tools/remove-filter/SKILL.md) | `POST /remove_filter` | Remove a filter |
| [set-filter-criteria](tools/set-filter-criteria/SKILL.md) | `POST /set_filter_criteria` | Set filter criteria |

### Conditional Formatting
| Tool | Path | Description |
|------|------|------|
| [add-conditional-formatting](tools/add-conditional-formatting/SKILL.md) | `POST /add_conditional_formatting` | Add conditional formatting rules |
| [remove-conditional-formatting](tools/remove-conditional-formatting/SKILL.md) | `POST /remove_conditional_formatting` | Remove conditional formatting rules |
| [clear-all-conditional-formatting](tools/clear-all-conditional-formatting/SKILL.md) | `POST /clear_all_conditional_formatting` | Clear all conditional formatting |

### Row & Column Operations
| Tool | Path | Description |
|------|------|------|
| [insert-rows](tools/insert-rows/SKILL.md) | `POST /insert_rows` | Insert rows |
| [delete-rows](tools/delete-rows/SKILL.md) | `POST /delete_rows` | Delete rows |
| [insert-columns](tools/insert-columns/SKILL.md) | `POST /insert_columns` | Insert columns |
| [delete-columns](tools/delete-columns/SKILL.md) | `POST /delete_columns` | Delete columns |
| [auto-resize-rows](tools/auto-resize-rows/SKILL.md) | `POST /auto_resize_rows` | Auto-resize row height |
| [auto-resize-columns](tools/auto-resize-columns/SKILL.md) | `POST /auto_resize_columns` | Auto-resize column width |

### Cell Operations
| Tool | Path | Description |
|------|------|------|
| [merge-cells](tools/merge-cells/SKILL.md) | `POST /merge_cells` | Merge cells |
| [unmerge-cells](tools/unmerge-cells/SKILL.md) | `POST /unmerge_cells` | Unmerge cells |

## Common Errors

| Error | Cause | Solution |
|------|------|------|
| `Connection refused` | Obsidian not running or plugin not enabled | Start Obsidian and confirm Sheet Plus plugin is enabled |
| `Sheet not found` | Worksheet name does not exist | Call get-sheet-list first to confirm the correct sheet name |
| `Range is invalid` | Invalid range format | Use A1 notation (e.g., `A1:C10`), row numbers start at 1 |
| `No active workbook` | No spreadsheet file currently open | Open a .sheet file in Obsidian |
