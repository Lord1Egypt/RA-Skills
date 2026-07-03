---
name: obsidian-sheet-plus-get-sheet-list
description: Use when needing to discover available worksheets in the Obsidian workbook — for confirming sheet names before reading or writing data
---

# get-sheet-list
Retrieve a list of all worksheets in the current workbook. Use to confirm worksheet names before reading or writing data.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | GET |
| Path | `/get_sheet_list` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |

## Parameters
None.

## Response
```json
{"success":true,"data":[{"id":"sheet-001","name":"Sheet1","index":0}]}
```

## Example
```bash
curl http://127.0.0.1:3000/get_sheet_list
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| No active workbook | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
| Connection refused | Obsidian is not running or the plugin is not enabled | Call check-status first to confirm API availability |
