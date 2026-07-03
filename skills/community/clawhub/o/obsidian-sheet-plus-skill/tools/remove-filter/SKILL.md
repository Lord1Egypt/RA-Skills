---
name: obsidian-sheet-plus-remove-filter
description: Use when removing filter from a range or entire sheet — for restoring unfiltered data view
---

# remove-filter
Removes the filter from a specified range or the entire sheet. All data is shown again after removal.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/remove_filter` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |
| range | string | No | All | Range to remove filter from. If omitted, removes all filters in the sheet |

## Response
```json
{
  "success": true,
  "data": {
    "sheetName": "Sheet1"
  }
}
```

## Example

### Remove filter from a specific range
```bash
curl -X POST http://127.0.0.1:3000/remove_filter \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:D10"
  }'
```

### Remove all filters from the sheet
```bash
curl -X POST http://127.0.0.1:3000/remove_filter \
  -H "Content-Type: application/json" \
  -d '{"sheetName": "Sheet1"}'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Range is invalid` | Invalid range format | Use A1 notation (e.g. `A1:D10`) |
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the sheet name |

## Related Tools
- **add-filter**: Add a filter
- **set-filter-criteria**: Set filter criteria
- **get-filter**: View current filter state
