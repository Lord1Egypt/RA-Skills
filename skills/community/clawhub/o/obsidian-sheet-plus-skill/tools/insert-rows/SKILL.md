---
name: obsidian-sheet-plus-insert-rows
description: Use when adding empty rows at a specific position — for expanding a sheet to accommodate new data without overwriting existing rows
---

# insert-rows
Inserts new rows at a specified position. Existing rows shift down.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/insert_rows` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |
| rowIndex | number | Yes | - | Row index for insertion (0-based), new rows are inserted before this position |
| numberOfRows | number | Yes | - | Number of rows to insert |

> **Note**: After insertion, existing rows starting from `rowIndex` will shift down.

## Response
```json
{
  "success": true,
  "data": {
    "rowIndex": 2,
    "numberOfRows": 3,
    "sheetName": "Sheet1"
  },
  "message": "3 row(s) inserted successfully at row 2"
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/insert_rows \
  -H "Content-Type: application/json" \
  -d '{"sheetName":"Sheet1","rowIndex":2,"numberOfRows":3}'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the correct sheet name |
| `No active workbook` | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
| `rowIndex` out of range | Row index exceeds the current maximum row count | Ensure the target position is within the valid range |
