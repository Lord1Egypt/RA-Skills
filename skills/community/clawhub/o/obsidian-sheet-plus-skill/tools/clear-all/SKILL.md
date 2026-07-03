---
name: obsidian-sheet-plus-clear-all
description: Use when removing both cell content and formatting — for fully resetting a range to its default empty state
---

# clear-all
Clears both cell content and formatting (background color, font, borders, alignment, etc.) from a specified range, restoring it to default empty state.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/clear_all` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | Yes | - | Target sheet name |
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
curl -X POST http://127.0.0.1:3000/clear_all \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:B10"
  }'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Range is invalid` | Invalid range format | Use A1 notation (e.g. `A1:C10`) |
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the sheet name |

## Related Tools
- **clear-contents**: Clear only content, keep formatting
- **clear-format**: Clear only formatting, keep content
