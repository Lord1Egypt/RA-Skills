---
name: obsidian-sheet-plus-auto-resize-rows
description: Use when adjusting row heights to fit cell content — for making all row data visible without manual resizing
---

# auto-resize-rows
Automatically adjusts row heights to fit cell content, ensuring all data is visible without manual resizing.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/auto_resize_rows` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |
| startRow | number | Yes | - | Start row index (0-based) |
| numberOfRows | number | Yes | - | Number of rows to resize |

## Response
```json
{
  "success": true,
  "data": {
    "startRow": 0,
    "numberOfRows": 10,
    "sheetName": "Sheet1"
  }
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/auto_resize_rows \
  -H "Content-Type: application/json" \
  -d '{"sheetName":"Sheet1","startRow":0,"numberOfRows":10}'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the correct sheet name |
| `No active workbook` | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
| `startRow` out of range | Start row index is outside the valid range | Call get-max-rows first to check the maximum row count |
