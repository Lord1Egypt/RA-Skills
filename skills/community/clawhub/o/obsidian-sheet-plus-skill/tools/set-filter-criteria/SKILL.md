---
name: obsidian-sheet-plus-set-filter-criteria
description: Use when configuring filter conditions on a specific column — for showing/hiding rows based on values, conditions, or colors
---

# set-filter-criteria
Sets filter conditions on a column that already has a filter. Supports filtering by value, by condition (equals, greater than, contains, etc.), and by color.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`
- Target range already has a filter added via add-filter

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/set_filter_criteria` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |
| range | string | Yes | - | Range with an existing filter, e.g. `A1:D10` |
| criteria | object | Yes | - | Filter criteria object |
| criteria.column | string | Yes | - | Column letter, e.g. `"A"`, `"C"` |
| criteria.type | string | Yes | - | Filter type: `"equals"` / `"contains"` / `"greaterThan"` / `"lessThan"` / `"between"` / `"notBlank"` / `"blank"` |
| criteria.values | array | depends on type | - | Filter values. For `equals`: `["value"]`; for `between`: `["min","max"]` |

## Response
```json
{
  "success": true,
  "data": {
    "range": "A1:D10",
    "column": "C",
    "type": "equals",
    "values": ["已完成", "进行中"]
  }
}
```

## Example

### Filter by value (show specific statuses)
```bash
curl -X POST http://127.0.0.1:3000/set_filter_criteria \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:D10",
    "criteria": {
      "column": "C",
      "type": "equals",
      "values": ["已完成", "进行中"]
    }
  }'
```

### Numeric condition filter
```bash
curl -X POST http://127.0.0.1:3000/set_filter_criteria \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:D10",
    "criteria": {
      "column": "B",
      "type": "greaterThan",
      "values": ["100"]
    }
  }'
```

### Text contains filter
```bash
curl -X POST http://127.0.0.1:3000/set_filter_criteria \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:D10",
    "criteria": {
      "column": "A",
      "type": "contains",
      "values": ["项目"]
    }
  }'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Filter not found` | No filter exists on the range | Use add-filter first to add a filter to the range |
| `Range is invalid` | Invalid range format | Use A1 notation (e.g. `A1:D10`) |
| Filter criteria not applied | Column value is outside the range | Ensure the column letter is within the range's column scope |
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the sheet name |

## Related Tools
- **add-filter**: Add a filter first
- **remove-filter**: Remove the filter
