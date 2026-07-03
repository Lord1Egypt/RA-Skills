---
name: obsidian-sheet-plus-clear-contents
description: Use when removing cell values while preserving formatting — for resetting data without losing styles
---

# clear-contents
Clear cell contents in the specified range while preserving formatting (fonts, colors, borders, alignment, etc.). Suitable for scenarios requiring data reset while retaining the table's appearance.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/clear_contents` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | Yes | - | Target worksheet name |
| range | string | Yes | - | Cell range, e.g. `A1:B10` |

## Response
```json
{
  "success": true,
  "data": {
    "range": "A1:B10"
  }
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/clear_contents \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:B10"
  }'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Range is invalid` | Range format is incorrect | Use A1 notation (e.g. `A1:C10`) |
| `Sheet not found` | Worksheet name does not exist | Call get-sheet-list first to confirm the sheet name |
