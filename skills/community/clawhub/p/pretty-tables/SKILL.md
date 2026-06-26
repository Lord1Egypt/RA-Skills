---
name: pretty-tables
version: 2.0.0
description: Create beautiful, full-width tables in Word documents using the docx npm library. Tables are properly sized, centered, and styled. Use when you need to create DOCX files with professional-looking tables like itineraries, schedules, data tables, or reports.
author: Jimmy
tags:
  - docx
  - tables
  - word
  - document
  - formatting
---

# pretty-tables

Create beautiful tables in Word documents that work consistently across Word and Google Docs.

## ⚠️ THE 5 CRITICAL RULES

After extensive testing, these are the essential patterns for tables that render correctly everywhere:

### 1. Dual-Width Sizing (MOST CRITICAL)

Every table needs widths set in **TWO places** — on the table itself AND on each individual cell:

```javascript
// Table level
new Table({
  width: { size: 9360, type: WidthType.DXA },  // Total width
  columnWidths: [1872, 7488],                   // Per-column widths
  rows: [...]
})

// Cell level - EVERY cell needs this!
new TableCell({
  width: { size: 1872, type: WidthType.DXA },   // This cell's width
  children: [...]
})
```

**If either is missing, the table renders incorrectly on some platforms.**

### 2. Use DXA Only, Never Percentages

Percentages break in Google Docs. Always use DXA (twips):

- 1 inch = 1440 DXA
- US Letter (8.5") with 1" margins = 9360 DXA content width

```javascript
// ❌ WRONG - breaks in Google Docs
width: { size: 100, type: WidthType.PERCENTAGE }

// ✅ CORRECT
width: { size: 9360, type: WidthType.DXA }
```

### 3. Use ShadingType.CLEAR, Not SOLID

This is a subtle but critical gotcha:

```javascript
const { ShadingType } = require('docx');

// ❌ WRONG - produces BLACK background
shading: { type: ShadingType.SOLID, fill: "E0F2F1" }

// ✅ CORRECT - applies the fill color
shading: { type: ShadingType.CLEAR, fill: "E0F2F1" }
```

### 4. Add Cell Padding (Margins)

Keep text from crowding the borders:

```javascript
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

new TableCell({
  children: [...],
  margins: cellMargins
})
```

### 5. Column Widths Must Sum Exactly

For US Letter with 1" margins: **9360 DXA**

```javascript
// 2 columns: 20% + 80%
columnWidths: [1872, 7488]  // = 9360 ✓

// 3 columns: equal
columnWidths: [3120, 3120, 3120]  // = 9360 ✓

// 3 columns: 25% + 25% + 50%
columnWidths: [2340, 2340, 4680]  // = 9360 ✓
```

## Complete Working Example

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
         WidthType, AlignmentType, BorderStyle, TableLayoutType, ShadingType } = require('docx');
const fs = require('fs');

// Constants
const TOTAL_WIDTH = 9360;  // US Letter with 1" margins
const TIME_COL = 1872;     // 20%
const CONTENT_COL = 7488;  // 80%

// Light gray borders
const cellBorders = {
  top: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
  bottom: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
  left: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
  right: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" }
};

// Cell padding
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

// Table helper
function table(columnWidths, rows) {
  return new Table({
    layout: TableLayoutType.FIXED,
    width: { size: columnWidths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: columnWidths,
    rows: rows
  });
}

// Header row
function headerRow(text, color) {
  return new TableRow({
    children: [
      new TableCell({
        children: [new Paragraph({ 
          children: [new TextRun({ text, bold: true, size: 32, color: "FFFFFF" })],
          alignment: AlignmentType.CENTER
        })],
        width: { size: TIME_COL + CONTENT_COL, type: WidthType.DXA },
        columnSpan: 2,
        shading: { type: ShadingType.CLEAR, fill: color },
        borders: cellBorders,
        margins: cellMargins
      })
    ]
  });
}

// Data row
function dataRow(time, activity, color) {
  return new TableRow({
    children: [
      new TableCell({
        children: [new Paragraph({ 
          children: [new TextRun({ text: time, bold: true, size: 26, color })],
          alignment: AlignmentType.CENTER
        })],
        width: { size: TIME_COL, type: WidthType.DXA },
        borders: cellBorders,
        margins: cellMargins
      }),
      new TableCell({
        children: [new Paragraph({ 
          children: [new TextRun({ text: activity, size: 26 })]
        })],
        width: { size: CONTENT_COL, type: WidthType.DXA },
        borders: cellBorders,
        margins: cellMargins
      })
    ]
  });
}

// Build document
const doc = new Document({
  sections: [{
    properties: { 
      page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    children: [
      table([TIME_COL, CONTENT_COL], [
        headerRow("SCHEDULE", "1565C0"),
        dataRow("9:00 AM", "Arrive at destination", "1565C0"),
        dataRow("10:00 AM", "Morning activity", "1565C0"),
        dataRow("12:00 PM", "Lunch break", "1565C0"),
      ])
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('output.docx', buffer);
});
```

## Column Width Cheat Sheet

For **US Letter (8.5") with 1" margins = 9360 DXA**:

| Layout | Column Widths | Sum |
|--------|--------------|-----|
| 2 cols (20/80) | `[1872, 7488]` | 9360 |
| 2 cols (25/75) | `[2340, 7020]` | 9360 |
| 2 cols (30/70) | `[2808, 6552]` | 9360 |
| 2 cols (equal) | `[4680, 4680]` | 9360 |
| 3 cols (equal) | `[3120, 3120, 3120]` | 9360 |
| 3 cols (25/25/50) | `[2340, 2340, 4680]` | 9360 |
| 3 cols (20/30/50) | `[1872, 2808, 4680]` | 9360 |
| 4 cols (equal) | `[2340, 2340, 2340, 2340]` | 9360 |

## Common Mistakes

❌ **Missing cell widths:**
```javascript
new TableCell({ children: [...] })  // No width!
```

❌ **Using percentages:**
```javascript
width: { size: 100, type: WidthType.PERCENTAGE }  // Breaks in Google Docs
```

❌ **Wrong shading type:**
```javascript
shading: { type: ShadingType.SOLID, fill: "E0F2F1" }  // BLACK background!
```

❌ **Columns don't sum:**
```javascript
columnWidths: [2000, 7000]  // = 9000, not 9360
```

✅ **Correct:**
```javascript
new TableCell({
  width: { size: 1872, type: WidthType.DXA },
  shading: { type: ShadingType.CLEAR, fill: "E0F2F1" },
  margins: { top: 80, bottom: 80, left: 120, right: 120 },
  borders: cellBorders,
  children: [...]
})
```

## Color Palette

**Header colors:**
| Color | Hex | Use |
|-------|-----|-----|
| Blue | `1565C0` | Default headers |
| Red | `C62828` | Important |
| Green | `2E7D32` | Success |
| Orange | `EF6C00` | Warning |
| Purple | `6A1B9A` | Special |
| Teal | `00695C` | Info |

**Light backgrounds:**
| Color | Hex | Use |
|-------|-----|-----|
| Light Blue | `BBDEFB` | Highlight |
| Light Green | `C8E6C9` | Success |
| Light Yellow | `FFF9C4` | Note |
| Light Gray | `F5F5F5` | Alternating |

## Why This Works

The combination of:
1. **Exact DXA sizing** on both table and cells
2. **ShadingType.CLEAR** for correct colors
3. **Consistent padding** for readability
4. **Precise column sums** for layout

...produces tables that render correctly in Microsoft Word, Google Docs, and other DOCX viewers.

## Troubleshooting

**Q: Table is narrow in Google Docs**
- Make sure you're using `WidthType.DXA`, not PERCENTAGE
- Check that every TableCell has a `width` property

**Q: Cell backgrounds are black**
- Change `ShadingType.SOLID` to `ShadingType.CLEAR`

**Q: Text touches the borders**
- Add `margins: { top: 80, bottom: 80, left: 120, right: 120 }` to each cell

**Q: Columns are uneven**
- Verify column widths sum exactly to table width (9360 for 1" margins)
