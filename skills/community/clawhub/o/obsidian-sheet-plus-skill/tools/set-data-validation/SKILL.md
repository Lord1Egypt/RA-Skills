---
name: obsidian-sheet-plus-set-data-validation
description: Use when restricting cell input to specific values, ranges, or types — for dropdown lists, number limits, date constraints, or preventing invalid data entry
---

# set-data-validation
Set data validation rules to restrict cell input. Supports multiple validation types including dropdown lists, numeric ranges, date constraints, text length limits, and more, effectively preventing data entry errors.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/set_data_validation` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active worksheet | Target worksheet name |
| range | string | Yes | - | Cell range, e.g. `A1:A10` |
| type | string | Yes | - | Validation type (see enum below) |
| formula1 | string | Yes | - | First formula or value. For list/listMultiple types: comma-separated options. For checkbox: `TRUE` |
| formula2 | string | No | - | Second formula or value. For checkbox: `FALSE`. Required for other types when operator is not equal/notEqual |
| operator | string | No | - | Operator (see enum below), default `equal` |
| allowBlank | boolean | No | `false` | Whether to allow blank values |
| showErrorMessage | boolean | No | `false` | Whether to show error message |
| errorMessage | string | No | - | Custom error message content |

### type Enum
| Value | Description |
|------|------|
| `whole` | Integer |
| `decimal` | Decimal |
| `list` | Dropdown list (single select) |
| `listMultiple` | Dropdown list (multi-select) |
| `date` | Date |
| `time` | Time |
| `textLength` | Text length |
| `custom` | Custom formula |
| `checkbox` | Checkbox |
| `any` | Any value (equivalent to removing validation) |

### operator Enum
| Value | Description |
|------|------|
| `between` | Between |
| `notBetween` | Not between |
| `equal` | Equal to |
| `notEqual` | Not equal to |
| `greaterThan` | Greater than |
| `lessThan` | Less than |
| `greaterThanOrEqual` | Greater than or equal to |
| `lessThanOrEqual` | Less than or equal to |

## Response
```json
{
  "success": true,
  "data": {
    "range": "A1:A10",
    "type": "list"
  }
}
```

## Example

### Dropdown List
```bash
curl -X POST http://127.0.0.1:3000/set_data_validation \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:A10",
    "type": "list",
    "formula1": "Todo,In Progress,Done"
  }'
```

### Numeric Range Limit
```bash
curl -X POST http://127.0.0.1:3000/set_data_validation \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "B1:B10",
    "type": "whole",
    "formula1": "0",
    "formula2": "100",
    "operator": "between",
    "showErrorMessage": true,
    "errorMessage": "Please enter an integer between 0-100"
  }'
```

### Date Constraint
```bash
curl -X POST http://127.0.0.1:3000/set_data_validation \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "C1:C10",
    "type": "date",
    "formula1": "2024-01-01",
    "formula2": "2024-12-31",
    "operator": "between"
  }'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Range is invalid` | Range format is incorrect | Use A1 notation (e.g. `A1:C10`) |
| Dropdown list has no options | formula1 is empty or format is incorrect | Ensure formula1 is a comma-separated option string |
| `Sheet not found` | Worksheet name does not exist | Call get-sheet-list first to confirm the sheet name |
