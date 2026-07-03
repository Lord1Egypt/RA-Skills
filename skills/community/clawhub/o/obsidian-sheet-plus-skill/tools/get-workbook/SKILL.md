---
name: obsidian-sheet-plus-get-workbook
description: Use when exporting or backing up entire workbook data including all sheets, styles, and formulas — for full data migration or snapshot creation
---

# get-workbook
Export complete data of the entire workbook, including all worksheets, styles, and formulas. Suitable for full data migration or creating backup snapshots.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | GET |
| Path | `/get_workbook` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |

## Parameters
None.

## Response
```json
{"success":true,"data":{...complete workbook JSON, including all sheet data, styles, formulas, etc...}}
```

## Example
```bash
curl http://127.0.0.1:3000/get_workbook
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| No active workbook | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
| Connection refused | Obsidian is not running or the plugin is not enabled | Call check-status first to confirm API availability |
