---
name: obsidian-sheet-plus-delete-columns
description: Use when removing columns from a sheet — for cleaning up empty columns or removing unwanted data fields
---

# delete-columns
Deletes columns at a specified position. Subsequent columns shift left.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/delete_columns` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |
| columnIndex | number | Yes | - | Start column index (0-based), delete starting from this column |
| numberOfColumns | number | Yes | - | Number of columns to delete |

> **Note**: Deletion is irreversible. Ensure data is backed up or no longer needed.

## Response
```json
{
  "success": true,
  "data": {
    "columnIndex": 1,
    "numberOfColumns": 2,
    "sheetName": "Sheet1"
  }
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/delete_columns \
  -H "Content-Type: application/json" \
  -d '{"sheetName":"Sheet1","columnIndex":1,"numberOfColumns":2}'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the correct sheet name |
| `No active workbook` | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
| `columnIndex` out of range | Column index is outside the valid range | Ensure the start column is within the valid range |
