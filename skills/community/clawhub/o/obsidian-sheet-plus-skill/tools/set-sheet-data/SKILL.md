---
name: obsidian-sheet-plus-set-sheet-data
description: Use when writing or updating cell values in an Obsidian spreadsheet — for data entry, bulk updates, or populating template sheets
---

# set-sheet-data
Write/update cell data in a worksheet. Supports single-cell and batch range writes, and can update multiple non-contiguous areas simultaneously.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/set_sheet_data` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active worksheet | Target worksheet name |
| range | string | Yes | - | Data range, e.g. `A1:B2` |
| values | array[array] | Yes | - | 2D array, each row corresponds to a row in the range |

> **Note**: The dimensions of `values` must match the `range`. For example, `range: "A1:B2"` requires a 2×2 array: `[["A1_value","B1_value"],["A2_value","B2_value"]]`.

## Response
```json
{
  "success": true,
  "message": "Sheet data updated successfully"
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/set_sheet_data \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:B2",
    "values": [["Name", "Age"], ["Zhang San", 25]]
  }'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Sheet not found` | Worksheet name does not exist | Call get-sheet-list first to confirm the correct sheet name |
| `Range is invalid` | Range format is incorrect | Use A1 notation (e.g. `A1:C10`), row numbers start from 1 |
| Data not written | values dimensions do not match range | Ensure the 2D array has the same number of rows and columns as the range |
| `No active workbook` | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
