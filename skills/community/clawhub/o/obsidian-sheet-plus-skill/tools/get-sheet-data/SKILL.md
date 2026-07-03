---
name: obsidian-sheet-plus-get-sheet-data
description: Use when reading cell values, ranges, or structured data from an Obsidian spreadsheet — for data analysis, reporting, export, or preparing to update cells
---

# get-sheet-data
Read cell data from a specified range in the worksheet. Suitable for data analysis, report generation, data export, or preparing data before updating cells.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | GET |
| Path | `/get_sheet_data` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Active worksheet | Target worksheet name |
| range | string | No | All data | Cell range, e.g. `A1:D10` |

## Response
```json
{"success":true,"data":[["Val1","Val2"]],"sheetName":"Sheet1"}
```

## Example
```bash
curl "http://127.0.0.1:3000/get_sheet_data?sheetName=Sheet1&range=A1:C5"
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| Sheet not found | The specified worksheet does not exist | Call get-sheet-list first to confirm the correct sheet name |
| Range is invalid | Range format is incorrect | Use A1 notation (e.g. `A1:C10`), row numbers start from 1 |
| No active workbook | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
