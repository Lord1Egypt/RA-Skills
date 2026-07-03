---
name: obsidian-sheet-plus-auto-resize-columns
description: Use when adjusting column widths to fit cell content — for making all column data visible without manual resizing
---

# auto-resize-columns
Automatically adjusts column widths to fit cell content, ensuring all data is visible without manual resizing.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/auto_resize_columns` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |
| startColumn | number | Yes | - | Start column index (0-based) |
| numberOfColumns | number | Yes | - | Number of columns to resize |

## Response
```json
{
  "success": true,
  "data": {
    "startColumn": 0,
    "numberOfColumns": 5,
    "sheetName": "Sheet1"
  }
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/auto_resize_columns \
  -H "Content-Type: application/json" \
  -d '{"sheetName":"Sheet1","startColumn":0,"numberOfColumns":5}'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the correct sheet name |
| `No active workbook` | No spreadsheet file is currently open | Open a .sheet file in Obsidian |
| `startColumn` out of range | Start column index is outside the valid range | Call get-max-columns first to check the maximum column count |
