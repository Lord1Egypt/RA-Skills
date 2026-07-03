---
name: obsidian-sheet-plus-get-max-columns
description: Use when determining sheet width before inserting columns — to check available column count for wide data structures
---

# get-max-columns
Get the maximum number of columns for the specified worksheet. Use to confirm column capacity before inserting columns or designing wide table structures.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | GET |
| Path | `/get_max_columns` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Active worksheet | Target worksheet name |

## Response
```json
{"success":true,"data":{"maxColumns":26,"sheetName":"Sheet1"}}
```

## Example
```bash
curl "http://127.0.0.1:3000/get_max_columns?sheetName=Sheet1"
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| Sheet not found | The specified worksheet does not exist | Call get-sheet-list first to confirm the correct sheet name |
| No active workbook | No spreadsheet file is currently open and sheetName is not specified | Open a .sheet file in Obsidian or specify the sheetName parameter |
