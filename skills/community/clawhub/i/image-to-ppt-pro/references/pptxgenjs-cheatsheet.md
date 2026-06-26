# PptxGenJS API Quick Reference

## Basic Structure

```javascript
const pptxgen = require("pptxgenjs");
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9'; // 10" × 5.625"
let slide = pres.addSlide();
pres.writeFile({ fileName: "output.pptx" });
```

## Layout Dimensions

| Layout | Dimensions |
|------|------|
| LAYOUT_16x9 | 10" × 5.625" (default) |
| LAYOUT_16x10 | 10" × 6.25" |
| LAYOUT_4x3 | 10" × 7.5" |
| LAYOUT_WIDE | 13.3" × 7.5" |

---

## Text addText

```javascript
slide.addText("Text content", {
  x: 1, y: 1, w: 8, h: 1,
  fontSize: 14,           // Font size (pt)
  fontFace: "Microsoft YaHei", // Font (required for Chinese)
  color: "363636",        // ⚠️ No # prefix
  bold: true,
  italic: false,
  underline: { style: "sng" }, // Underline
  align: "center",        // left / center / right
  valign: "middle",       // top / middle / bottom
  margin: 0,              // Padding, set to 0 for precise alignment
  charSpacing: 2,         // Character spacing
});
```

### Rich Text (Mixed Styles)

```javascript
slide.addText([
  { text: "Normal text", options: { color: "333333" } },
  { text: "Blue link", options: { color: "1155CC", underline: { style: "sng" } } },
  { text: "After line break", options: { breakLine: true } },
  { text: "Second line", options: { fontSize: 10, color: "666666" } }
], { x: 1, y: 1, w: 6, h: 1, fontSize: 12, fontFace: "Microsoft YaHei" });
```

### Multi-line Text (breakLine)

```javascript
slide.addText([
  { text: "First line", options: { breakLine: true } },
  { text: "Second line" }
], { x: 0.5, y: 0.5, w: 8, h: 1 });
```

### Lists

```javascript
slide.addText([
  { text: "First item", options: { bullet: true, breakLine: true } },
  { text: "Second item", options: { bullet: true } }
], { x: 0.5, y: 1, w: 8, h: 2 });
// ⚠️ Don't use "•" unicode symbol, will become double bullet
```

---

## Shapes addShape

### Rectangle

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.65,
  fill: { color: "8B1A1A" },
  line: { color: "8B1A1A", width: 1 }
});
```

### Rounded Rectangle

```javascript
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1, y: 1, w: 3, h: 0.5,
  fill: { color: "D8EAF5" },
  line: { color: "A0C4E0", width: 1 },
  rectRadius: 0.05  // Corner radius (inches)
});
// ⚠️ Rounded rectangles not suitable for overlaying rectangular borders, use RECTANGLE instead
```

### Line (for connector arrows)

```javascript
// Vertical line
slide.addShape(pres.shapes.LINE, {
  x: 2.6, y: 1.37, w: 0, h: 0.25,
  line: { color: "888888", width: 1.5 }
});
// Horizontal line
slide.addShape(pres.shapes.LINE, {
  x: 1.0, y: 2.0, w: 3.0, h: 0,
  line: { color: "888888", width: 1.5 }
});
```

### Ellipse

```javascript
slide.addShape(pres.shapes.OVAL, {
  x: 4, y: 1, w: 2, h: 2,
  fill: { color: "0000FF" }
});
```

### Transparency

```javascript
fill: { color: "0088CC", transparency: 50 }  // 0-100
```

### Shadow

```javascript
// ⚠️ Must use opacity property, cannot encode transparency into color
shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15 }
// ⚠️ Reusing same shadow object multiple times causes corruption, use factory function:
const makeShadow = () => ({ type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15 });
```

---

## Images addImage

```javascript
// File path
slide.addImage({ path: "image.png", x: 1, y: 1, w: 5, h: 3 });
// URL
slide.addImage({ path: "https://example.com/img.jpg", x: 1, y: 1, w: 5, h: 3 });
// base64
slide.addImage({ data: "image/png;base64,iVBORw...", x: 1, y: 1, w: 5, h: 3 });
// Circular crop
slide.addImage({ path: "avatar.png", x: 1, y: 1, w: 1, h: 1, rounding: true });
```

---

## Background

```javascript
slide.background = { color: "FFFFFF" };                     // Solid color
slide.background = { path: "https://example.com/bg.jpg" }; // Image
```

---

## Tables addTable

```javascript
slide.addTable([
  [{ text: "Header", options: { bold: true, fill: { color: "4472C4" }, color: "FFFFFF" } }, "Column 2"],
  ["Data 1", "Data 2"]
], {
  x: 1, y: 1, w: 8, h: 2,
  border: { pt: 1, color: "999999" },
  fill: { color: "F1F1F1" }
});
```

---

## Common Color Reference

| Purpose | Color hex |
|------|---------|
| Dark red / Burgundy background | `8B1A1A`, `9B2335`, `7B1414` |
| White text | `FFFFFF` |
| Dark text | `333333`, `444444` |
| Light gray background | `F5F5F5`, `EEEEEE`, `D9D9D9` |
| Light purple (flow node) | `E8E0F0`, `EDE7F6`, `C0A8D8` (border) |
| Light blue (flow node) | `D8EAF5`, `DDEEFF`, `A0C4E0` (border) |
| Light green (flow node) | `D8EDD8`, `D0EDE0`, `90C8A8` (border) |
| Light pink (flow node) | `F5D8D8`, `FFEBEE`, `E0A8A8` (border) |
| Link blue | `1155CC`, `0070C0` |
| Description text gray | `666666`, `888888` |
| Border gray | `AAAAAA`, `CCCCCC`, `E0E0E0` |

---

## ⚠️ Must Avoid Errors

1. **No # before color**: `color: "FF0000"` ✅, `color: "#FF0000"` ❌
2. **Shadow color not 8-digit hex**: Use `opacity: 0.15` instead of `color: "00000026"` ❌
3. **Don't use unicode bullet**: Use `bullet: true` not `"• text"` ❌
4. **Don't reuse shadow objects**: Use `makeShadow()` factory function to generate new objects each call
5. **Chinese must specify font**: `fontFace: "Microsoft YaHei"` or `"SimHei"`
6. **ROUNDED_RECTANGLE don't overlay rectangular borders**: Use `RECTANGLE`

---

## Coordinate Calculation Tips

```javascript
// Horizontal center
const x = (10 - w) / 2;

// Node center x (for drawing connector lines)
const centerX = nodeX + nodeW / 2;
const centerY = nodeY + nodeH;  // Node bottom (arrow start point)

// Evenly spaced arrangement (n elements, total width W, start x0)
const gap = (W - n * itemW) / (n + 1);
const itemX = (i) => x0 + gap + i * (itemW + gap);
```
