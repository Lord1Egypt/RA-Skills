---
name: obsidian-sheet-plus-set-range-style
description: Use when formatting cells with fonts, colors, borders, alignment, or text wrapping — for creating visually organized and professional-looking spreadsheets
---

# set-range-style
Set range styles including font, color, background, borders, alignment, text rotation, and wrapping. Multiple style properties can be set in a single call.

## Prerequisites
- Obsidian is running, Sheet Plus plugin is enabled
- Verified API availability via `GET /`

## REST API
| Field | Value |
|------|-----|
| Method | POST |
| Path | `/set_range_style` |
| Auth | None by default. Requires `X-API-KEY` header when enabled |
| Content-Type | `application/json` |

## Parameters
| Parameter | Type | Required | Default | Description |
|------|------|------|--------|------|
| sheetName | string | No | Current active worksheet | Target worksheet name |
| range | string | Yes | - | Cell range, e.g. `A1:D10` |
| style | object | Yes | - | Style object (see detailed description below) |

### style Object Properties

| Property | Type | Description | Example Value |
|------|------|------|--------|
| backgroundColor | string | Background color (hex) | `"#4472C4"` |
| fontColor | string | Font color (hex) | `"#FFFFFF"` |
| fontSize | number | Font size (pt) | `12` |
| fontFamily | string | Font family | `"Arial"` |
| fontWeight | string | Font weight | `"normal"` / `"bold"` |
| fontStyle | string | Font style | `"normal"` / `"italic"` |
| fontLine | string | Font line style | `"none"` / `"single"` / `"double"` |
| textDecoration | string | Text decoration | `"none"` / `"underline"` / `"line-through"` |
| horizontalAlignment | string | Horizontal alignment | `"left"` / `"center"` / `"right"` |
| verticalAlignment | string | Vertical alignment | `"top"` / `"middle"` / `"bottom"` |
| textRotation | number | Text rotation angle | `0` ~ `360` |
| wrap | boolean | Text wrapping | `true` / `false` |
| border | object | Border style | See border description below |

### border Object Properties

| Property | Type | Description | Allowed Values |
|------|------|------|--------|
| type | string | Border type | `top` / `bottom` / `left` / `right` / `all` / `outside` / `inside` / `horizontal` / `vertical` / `tlbr` / `tlbc_tlmr` / `tlbr_tlbc_tlmr` / `bl_tr` / `mltr_bctr` |
| style | string/number | Border style | `"NONE"`(0) / `"THIN"`(1) / `"HAIR"`(2) / `"DOTTED"`(3) / `"DASHED"`(4) / `"DASH_DOT"`(5) / `"DASH_DOT_DOT"`(6) / `"DOUBLE"`(7) / `"MEDIUM"`(8) / `"MEDIUM_DASHED"`(9) / `"MEDIUM_DASH_DOT"`(10) / `"MEDIUM_DASH_DOT_DOT"`(11) / `"SLANT_DASH_DOT"`(12) / `"THICK"`(13) |
| color | string | Border color | Hex format, e.g. `"#000000"` |

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

### Set Header Style
```bash
curl -X POST http://127.0.0.1:3000/set_range_style \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:D1",
    "style": {
      "backgroundColor": "#4472C4",
      "fontColor": "#FFFFFF",
      "fontWeight": "bold",
      "horizontalAlignment": "center"
    }
  }'
```

### Set Full Border
```bash
curl -X POST http://127.0.0.1:3000/set_range_style \
  -H "Content-Type: application/json" \
  -d '{
    "sheetName": "Sheet1",
    "range": "A1:D10",
    "style": {
      "border": {
        "type": "all",
        "style": "THIN",
        "color": "#000000"
      }
    }
  }'
```

## Common Errors
| Error | Cause | Solution |
|------|------|------|
| `Range is invalid` | Range format is incorrect | Use A1 notation (e.g. `A1:C10`) |
| Style not applied | style object format is incorrect | Check property name spelling and confirm values are within allowed ranges |
| `Sheet not found` | Worksheet name does not exist | Call get-sheet-list first to confirm the sheet name |
