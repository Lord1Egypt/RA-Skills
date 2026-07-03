---
name: obsidian-sheet-plus-delete-rows
description: Use when removing rows from a sheet — for cleaning up empty rows or removing unwanted data sections
---

# delete-rows
Deletes rows at a specified position. Subsequent rows shift up.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/delete_rows` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |
| rowIndex | number | Yes | - | Start row index (0-based), delete starting from this row |
| numberOfRows | number | Yes | - | Number of rows to delete |

> **Note**: Deletion is irreversible. Ensure data is backed up or no longer needed.

## Response
```json
{
  "success": true,
  "data": {
    "rowIndex": 2,
    "numberOfRows": 3,
    "sheetName": "Sheet1"
  }
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/delete_rows \
  -H "Content-Type: application/json" \
  -d '{"sheetName":"Sheet1","rowIndex":2,"numberOfRows":3}'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the correct sheet name |
| `No active workbook` | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
| `rowIndex` out of range | Row index is outside the valid range | Ensure the start row is within the valid range |
