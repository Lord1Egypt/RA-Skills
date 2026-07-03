---
name: obsidian-sheet-plus-get-max-rows
description: Use when determining sheet capacity before inserting data — to check available row count for bulk data operations
---

# get-max-rows
Get the maximum number of rows for the specified worksheet. Use to confirm worksheet capacity before bulk data insertion.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | GET |
| Path | `/get_max_rows` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Active worksheet | Target worksheet name |

## Response
```json
{"success":true,"data":{"maxRows":1000,"sheetName":"Sheet1"}}
```

## Example
```bash
curl "http://127.0.0.1:3000/get_max_rows?sheetName=Sheet1"
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| Sheet not found | The specified worksheet does not exist | Call get-sheet-list first to confirm the correct sheet name |
| No active workbook | No spreadsheet file is currently open and sheetName is not specified | Open a .sheet file in Obsidian or specify the sheetName parameter |
