---
name: obsidian-sheet-plus-add-conditional-formatting
description: Use when applying automatic cell formatting based on cell values — for highlighting outliers, data bars, color scales, or icon sets
---

# add-conditional-formatting
Adds conditional formatting rules that automatically apply styles based on cell content. Supports numeric, text, date, cell status, average, color scale, data bar, and icon set rule types.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/add_conditional_formatting` |
| Auth | None by default. When enabled, requires `X-API-KEY` header |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active sheet | Target sheet name |
| range | string | Yes | - | Target range, e.g. `B1:B10` |
| ruleType | string | Yes | - | Rule type (see enum below) |
| condition | object | Yes | - | Condition settings (varies by ruleType) |
| format | object | No | - | Format settings: `{backgroundColor, fontColor, bold, italic, underline}` |

### ruleType Enum

| Value | Description | condition Structure |
|------|------|------|
| `number` | Numeric condition | `{operator: "greaterThan"/"lessThan"/..., value1: number, value2?: number}` |
| `text` | Text condition | `{textOperator: "contains"/"notContains"/"beginsWith"/"endsWith", text: string}` |
| `date` | Date condition | `{dateOperator: "today"/"yesterday"/"tomorrow"/"last7Days"/"thisMonth"/...}` |
| `cell` | Cell status | `{cellType: "empty"/"notEmpty"/"error"/"noError"}` |
| `average` | Average comparison | `{averageOperator: "above"/"below"/"equalOrAbove"/"equalOrBelow"/"aboveOrBelow"}` |
| `colorScale` | Color scale | `{colorScale: [{index, color, value:{type, value}}, ...]}` |
| `dataBar` | Data bar | `{min, max, positiveColor, nativeColor, isGradient, isShowValue}` |
| `iconSet` | Icon set | `{iconConfigs: [{iconType, iconId, operator, value:{type, value}}], isShowValue}` |

> **iconType values**: `3Arrows`, `3ArrowsGray`, `4Arrows`, `4ArrowsGray`, `5Arrows`, `5ArrowsGray`, `3Triangles`, `3TrafficLights1`, `3Signs`, `3TrafficLights2`, `4RedToBlack`, `4TrafficLights`, `3Symbols`, `3Symbols2`, `3Flags`, `4Rating`, `5Rating`, `5Quarters`, `5Felling`, `5Boxes`, `3Stars`

## Response
```json
{
  "success": true,
  "data": {
    "range": "B1:B10",
    "ruleType": "number"
  }
}
```

## Example

### Numeric highlight (mark red if greater than 100)
```bash
curl -X POST http://127.0.0.1:3000/add_conditional_formatting \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "B1:B10",
    "ruleType": "number",
    "condition": {
      "operator": "greaterThan",
      "value1": 100
    },
    "format": {
      "backgroundColor": "#FF0000",
      "fontColor": "#FFFFFF"
    }
  }'
```

### Text contains specific keyword
```bash
curl -X POST http://127.0.0.1:3000/add_conditional_formatting \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:A10",
    "ruleType": "text",
    "condition": {
      "textOperator": "contains",
      "text": "紧急"
    },
    "format": {
      "backgroundColor": "#FFC000",
      "bold": true
    }
  }'
```

### Data bar
```bash
curl -X POST http://127.0.0.1:3000/add_conditional_formatting \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "C1:C10",
    "ruleType": "dataBar",
    "condition": {
      "min": {"type": "min", "value": 0},
      "max": {"type": "max", "value": 100},
      "positiveColor": "#4472C4",
      "isGradient": true,
      "isShowValue": true
    }
  }'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Range is invalid` | Invalid range format | Use A1 notation (e.g. `A1:C10`) |
| Conditional formatting not applied | ruleType does not match the condition structure | Ensure condition fields match the requirements of the corresponding ruleType |
| `Sheet not found` | Sheet name does not exist | Call get-sheet-list first to confirm the sheet name |

## Related Tools
- **remove-conditional-formatting**: Remove conditional formatting from a specific range
- **clear-all-conditional-formatting**: Clear all conditional formatting from the sheet
