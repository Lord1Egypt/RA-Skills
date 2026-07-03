---
name: obsidian-sheet-plus-get-filter
description: Use when inspecting existing filter settings on a sheet — to understand current filter state before modifying or clearing filters
---

# get-filter
Inspect existing filter settings on a worksheet. Use to understand the current filter state before modifying or clearing filters.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | GET |
| Path | `/get_filter` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Active worksheet | Target worksheet name |
| range | string | No | Entire range | Filter range, e.g. `A1:D10` |

## Response
```json
{"success":true,"data":{"hasFilter":true,"filterInfo":{"range":"A1:D10","filteredOutRows":[]}}}
```

## Example
```bash
curl "http://127.0.0.1:3000/get_filter?sheetName=Sheet1&range=A1:D10"
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| Sheet not found | The specified worksheet does not exist | Call get-sheet-list first to confirm the correct sheet name |
| No active workbook | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
