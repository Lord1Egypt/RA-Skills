# PptxGenJS — Create Presentations from Scratch

Use `pptxgenjs` (Node.js) to programmatically generate `.pptx` files
when no template is available.

---

## Setup

```bash
# Install globally using managed Node.js
C:\Users\Administrator\.workbuddy\binaries\node\versions\node-v20.18.0-win-x64\npm.cmd install -g pptxgenjs
```

Verify:
```bash
C:\Users\Administrator\.workbuddy\binaries\node\versions\node-v20.18.0-win-x64\node.exe -e "const p=require('pptxgenjs'); console.log(p.version);"
```

---

## Basic Usage

```javascript
const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';   // 10" × 5.625" (default)
pres.author = 'Your Name';
pres.title = 'Presentation Title';

let slide = pres.addSlide();
slide.addText("Hello World!", { x: 0.5, y: 0.5, fontSize: 36, color: "363636" });

pres.writeFile({ fileName: "output.pptx" });
```

### Slide Sizes

| Layout | Size |
|--------|------|
| `LAYOUT_16x9` | 10" × 5.625" (default) |
| `LAYOUT_16x10` | 10" × 6.25" |
| `LAYOUT_4x3` | 10" × 7.5" |
| `LAYOUT_WIDE` | 13.3" × 7.5" |

---

## Text & Formatting

```javascript
// Basic text
slide.addText("Text", {
  x: 1, y: 1, w: 8, h: 2,
  fontSize: 24, fontFace: "Arial", color: "363636",
  bold: true, align: "center", valign: "middle"
});

// Character spacing (use charSpacing — letterSpacing is ignored)
slide.addText("SPACED", { x: 1, y: 1, w: 8, h: 1, charSpacing: 6 });

// Rich text array
slide.addText([
  { text: "Bold ", options: { bold: true } },
  { text: "Italic ", options: { italic: true } }
], { x: 1, y: 3, w: 8, h: 1 });

// Multi-line text (breakLine: true)
slide.addText([
  { text: "Line 1", options: { breakLine: true } },
  { text: "Line 2", options: { breakLine: true } },
  { text: "Line 3" }
], { x: 0.5, y: 0.5, w: 8, h: 2 });

// Text box margin (set to 0 when aligning with shapes/icons)
slide.addText("Title", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  margin: 0
});
```

> **Tip**: Text boxes have default internal padding. Set `margin: 0` when
> aligning with shapes, lines, or icons.

---

## Lists & Bullets

```javascript
// ✅ CORRECT: multiple bullet items
slide.addText([
  { text: "First item", options: { bullet: true, breakLine: true } },
  { text: "Second item", options: { bullet: true, breakLine: true } },
  { text: "Third item", options: { bullet: true } }
], { x: 0.5, y: 0.5, w: 8, h: 3 });

// ❌ WRONG: never use unicode bullet character
slide.addText("• First item", { ... });  // creates double bullets

// Sub-items and numbered lists
// indented sub-item:
{ text: "Sub-item", options: { bullet: true, indentLevel: 1 } }
// numbered list:
{ text: "First", options: { bullet: { type: "number" }, breakLine: true } }
```

---

## Shapes

```javascript
// Rectangle
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.8, w: 1.5, h: 3.0,
  fill: { color: "FF0000" },
  line: { color: "000000", width: 2 }
});

// Oval
slide.addShape(pres.shapes.OVAL, { x: 4, y: 1, w: 2, h: 2, fill: { color: "0000FF" } });

// Line
slide.addShape(pres.shapes.LINE, {
  x: 1, y: 3, w: 5, h: 0,
  line: { color: "FF0000", width: 3, dashType: "dash" }
});

// Transparency
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "0088CC", transparency: 50 }
});

// Rounded rectangle (use rectRadius only with ROUNDED_RECTANGLE)
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "FFFFFF" }, rectRadius: 0.1
});

// Shadow
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "FFFFFF" },
  shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15 }
});
```

### Shadow Options

| Property | Type | Range | Notes |
|----------|------|-------|-------|
| `type` | string | `"outer"`, `"inner"` | |
| `color` | string | 6-char hex (e.g. `"000000"`) | No `#` prefix; no 8-char hex |
| `blur` | number | 0–100 pt | |
| `offset` | number | 0–200 pt | **Must be non-negative** — negative values corrupt the file |
| `angle` | number | 0–359 degrees | 135 = bottom-right, 270 = up |
| `opacity` | number | 0.0–1.0 | Use this to control transparency |

> **Note**: Gradients are not natively supported. Use a gradient image as a background instead.

---

## Images

### Image Sources

```javascript
// From file path
slide.addImage({ path: "images/chart.png", x: 1, y: 1, w: 5, h: 3 });

// From URL
slide.addImage({ path: "https://example.com/img.jpg", x: 1, y: 1, w: 5, h: 3 });

// From base64 (faster — no file I/O)
slide.addImage({ data: "image/png;base64,iVBORw0KGgo...", x: 1, y: 1, w: 5, h: 3 });
```

### Image Options

```javascript
slide.addImage({
  path: "image.png",
  x: 1, y: 1, w: 5, h: 3,
  rotate: 45,               // 0–359 degrees
  rounding: true,           // circular crop
  transparency: 50,         // 0–100
  flipH: true,              // horizontal flip
  flipV: false,             // vertical flip
  altText: "Description",   // accessibility
  hyperlink: { url: "https://example.com" }
});
```

### Image Sizing Modes

```javascript
// Contain — fit inside, preserve aspect ratio
{ sizing: { type: 'contain', w: 4, h: 3 } }

// Cover — fill area, preserve aspect ratio (may crop)
{ sizing: { type: 'cover', w: 4, h: 3 } }

// Crop — crop to specific region
{ sizing: { type: 'crop', x: 0.5, y: 0.5, w: 2, h: 2 } }
```

### Calculate Dimensions (preserve aspect ratio)

```javascript
const origWidth = 1978, origHeight = 923, maxHeight = 3.0;
const calcWidth = maxHeight * (origWidth / origHeight);
const centerX = (10 - calcWidth) / 2;

slide.addImage({ path: "image.png", x: centerX, y: 1.2, w: calcWidth, h: maxHeight });
```

### Supported Formats

- **Standard**: PNG, JPG, GIF (animated GIF works in Microsoft 365)
- **SVG**: Available in modern PowerPoint / Microsoft 365

---

## Icons

Use `react-icons` to generate SVG icons, then rasterize to PNG for universal compatibility.

### Setup

```bash
npm install -g react react-dom sharp react-icons
```

### Usage

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaCheckCircle, FaChartLine } = require("react-icons/fa");

function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}
```

### Add Icon to Slide

```javascript
const iconData = await iconToBase64Png(FaCheckCircle, "#4472C4", 256);

slide.addImage({
  data: iconData,
  x: 1, y: 1, w: 0.5, h: 0.5   // size in inches
});
```

> **Note**: Use 256 or higher for crisp icons. The `size` param controls
> rasterization resolution, not display size (controlled by `w`/`h`).

### Popular Icon Sets (react-icons)

- `react-icons/fa` — Font Awesome
- `react-icons/md` — Material Design
- `react-icons/hi` — Heroicons
- `react-icons/bi` — Bootstrap Icons

---

## Slide Background

```javascript
// Solid color
slide.background = { color: "F1F1F1" };

// Color with transparency
slide.background = { color: "FF3399", transparency: 50 };

// Image from URL
slide.background = { path: "https://example.com/bg.jpg" };

// Image from base64
slide.background = { data: "image/png;base64,iVBORw0KGgo..." };
```

---

## Tables

```javascript
// Basic table
slide.addTable([
  ["Header 1", "Header 2"],
  ["Cell 1", "Cell 2"]
], {
  x: 1, y: 1, w: 8, h: 2,
  border: { pt: 1, color: "999999" },
  fill: { color: "F1F1F1" }
});

// Merged cells
let tableData = [
  [{ text: "Header", options: { fill: { color: "6699CC" }, color: "FFFFFF", bold: true } }, "Cell"],
  [{ text: "Merged", options: { colspan: 2 } }]
];
slide.addTable(tableData, { x: 1, y: 3.5, w: 8, colW: [4, 4] });
```

---

## Charts

```javascript
// Bar chart
slide.addChart(pres.charts.BAR, [{
  name: "Sales", labels: ["Q1", "Q2", "Q3", "Q4"],
  values: [4500, 5500, 6200, 7100]
}], {
  x: 0.5, y: 0.6, w: 6, h: 3, barDir: 'col',
  showTitle: true, title: 'Quarterly Sales'
});

// Line chart
slide.addChart(pres.charts.LINE, [{
  name: "Temp", labels: ["Jan", "Feb", "Mar"], values: [32, 35, 42]
}], { x: 0.5, y: 4, w: 6, h: 3, lineSize: 3, lineSmooth: true });

// Pie chart
slide.addChart(pres.charts.PIE, [{
  name: "Share", labels: ["A", "B", "Other"], values: [35, 45, 20]
}], { x: 7, y: 1, w: 5, h: 4, showPercent: true });
```

### Better-Looking Chart Styles

Default chart styles look dated. Apply the following options for a modern clean look:

```javascript
slide.addChart(pres.charts.BAR, chartData, {
  x: 0.5, y: 1, w: 9, h: 4, barDir: "col",

  // Custom colors (match presentation palette)
  chartColors: ["0D9488", "14B8A6", "5EEAD4"],

  // Clean background
  chartArea: { fill: { color: "FFFFFF" }, roundedCorners: true },

  // Subtle axis labels
  catAxisLabelColor: "64748B",
  valAxisLabelColor: "64748B",

  // Faint gridlines (value axis only)
  valGridLine: { color: "E2E8F0", size: 0.5 },
  catGridLine: { style: "none" },

  // Data labels on bars
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelColor: "1E293B",

  // Hide legend for single series
  showLegend: false,
});
```

**Key Style Options:**
- `chartColors: [...]` — hex colors for series/segments
- `chartArea: { fill, border, roundedCorners }` — chart background
- `catGridLine/valGridLine: { color, style, size }` — gridlines (`style: "none"` hides)
- `lineSmooth: true` — smooth curves (line charts)
- `legendPos: "r"` — legend position: `"b"`, `"t"`, `"l"`, `"r"`, `"tr"`

---

## Slide Masters

```javascript
pres.defineSlideMaster({
  title: 'TITLE_SLIDE',
  background: { color: '283A5E' },
  objects: [{
    placeholder: { options: { name: 'title', type: 'title', x: 1, y: 2, w: 8, h: 2 } }
  }]
});

let titleSlide = pres.addSlide({ masterName: "TITLE_SLIDE" });
titleSlide.addText("My Title", { placeholder: "title" });
```

---

## ⚠️ Common Pitfalls

1. **Never use `#` in hex colors** — corrupts the file
   ```javascript
   color: "FF0000"      // ✅ correct
   color: "#FF0000"     // ❌ wrong
   ```

2. **Never encode transparency in hex color strings** — 8-char colors (e.g. `"00000020"`) corrupt the file. Use `opacity` instead.
   ```javascript
   shadow: { type: "outer", blur: 6, offset: 2, color: "00000020" }          // ❌ corrupts
   shadow: { type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.12 }  // ✅ correct
   ```

3. **Use `bullet: true`** — don't use unicode `•` (creates double bullets)

4. **Use `breakLine: true`** between array items

5. **Avoid `lineSpacing` with bullets** — causes excessive spacing; use `paraSpaceAfter` instead

6. **New instance per presentation** — don't reuse `pptxgen()` object

7. **Never reuse options objects across calls** — PptxGenJS modifies objects in-place.
   ```javascript
   // ❌ WRONG — second shape gets converted values
   const shadow = { type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 };
   slide.addShape(pres.shapes.RECTANGLE, { shadow, ... });
   slide.addShape(pres.shapes.RECTANGLE, { shadow, ... });

   // ✅ CORRECT — create a new object each time
   const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 });
   slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
   slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
   ```

8. **Don't use `ROUNDED_RECTANGLE` with accent bars** — the rectangle overlay won't cover the rounded corners. Use `RECTANGLE` instead.
   ```javascript
   // ❌ WRONG: accent bar won't cover rounded corners
   slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 1, y: 1, w: 3, h: 1.5, fill: { color: "FFFFFF" } });
   slide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 1, w: 0.08, h: 1.5, fill: { color: "0891B2" } });

   // ✅ CORRECT: use RECTANGLE for both
   slide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 1, w: 3, h: 1.5, fill: { color: "FFFFFF" } });
   slide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 1, w: 0.08, h: 1.5, fill: { color: "0891B2" } });
   ```

---

## Quick Reference

| Category | Available Options |
|----------|-------------------|
| **Shapes** | RECTANGLE, OVAL, LINE, ROUNDED_RECTANGLE |
| **Charts** | BAR, LINE, PIE, DOUGHNUT, SCATTER, BUBBLE, RADAR |
| **Layouts** | LAYOUT_16x9, LAYOUT_16x10, LAYOUT_4x3, LAYOUT_WIDE |
| **Alignment** | `"left"`, `"center"`, `"right"` |
| **Chart data label pos** | `"outEnd"`, `"inEnd"`, `"center"` |
