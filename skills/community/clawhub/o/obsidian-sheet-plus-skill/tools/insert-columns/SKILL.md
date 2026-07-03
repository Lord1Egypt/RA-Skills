---
name: obsidian-sheet-plus-insert-columns
description: Use when adding empty columns at a specific position — for expanding column structure without overwriting existing data
---

# insert-columns
Inserts new columns at a specified position. Existing columns shift right.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/insert_columns` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |
| columnIndex | number | Yes | - | Column index for insertion (0-based), new columns are inserted before this position |
| numberOfColumns | number | Yes | - | Number of columns to insert |

> **Note**: After insertion, existing columns starting from `columnIndex` will shift right.

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
curl -X POST http://127.0.0.1:3000/insert_columns \
  -H "Content-Type: application/json" \
  -d '{"sheetName":"Sheet1","columnIndex":1,"numberOfColumns":2}'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the correct sheet name |
| `No active workbook` | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
| `columnIndex` out of range | Column index exceeds the current maximum column count | Ensure the target position is within the valid range |
