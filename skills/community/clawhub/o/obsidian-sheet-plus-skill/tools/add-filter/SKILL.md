---
name: obsidian-sheet-plus-add-filter
description: Use when adding dropdown filter arrows to a header row — for enabling data filtering and sorting on columns
---

# add-filter
Adds filter dropdown arrows to a specified range. The first row is automatically treated as the header row. Users can filter or sort column data via dropdowns.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/add_filter` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |
| range | string | Yes | - | Filter range, e.g. `A1:D10`, first row is the header row |

## Response
```json
{
  "success": true,
  "data": {
    "range": "A1:D10"
  }
}
```

## Example
```bash
curl -X POST http://127.0.0.1:3000/add_filter \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:D10"
  }'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Range is invalid` | Invalid range format | Use A1 notation (e.g. `A1:D10`) |
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the sheet name |
| Filter not appearing | Range must include at least header row + 1 data row | Ensure the range includes at least 2 rows |

## Related Tools
- **set-filter-criteria**: Set specific filter conditions on an existing filter
- **remove-filter**: Remove the filter
- **get-filter**: View current filter state
