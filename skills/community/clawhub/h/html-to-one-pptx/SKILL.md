---
name: html-to-one-pptx
description: >
  Convert any HTML file or design into a pixel-faithful PowerPoint (.pptx) slide.
  Trigger when the user uploads HTML file(s) and asks to "convert to PPT",
  "make a PowerPoint", "turn this into slides", or "一比一还原为 PPT".
  Handles single HTML or multiple HTML files (merged into one PPT).
  Always follow this skill — never improvise the workflow.
---

# HTML → PPTX Conversion Skill  (v4.4)

> **Read first**: `pptxgenjs.md` for the full API reference.

**Five principles:**
- **One HTML = one slide subfolder** — each HTML gets its own `tmp/slide_NN/` directory
- **Never batch-script** — write and run gen.js individually for each slide
- **Fit-to-page** — `SCALE = min(slide_w/html_w, slide_h/html_h)` guarantees 1-page output
- **Charts use native PPT** — detect chart data with detect_charts.py → addChart() (not images)
- **Color Master before gen.js** — always audit contrast and visibility before writing any code

---

## Workflow: Single HTML

```
PROJECT/
├── slide.html
└── tmp/
    ├── parsehtml.md          ← Claude writes this in Phase 1
    ├── colors.md             ← from Phase 2.5 Color Master
    ├── charts.json           ← from detect_charts.py (if charts found)
    ├── gen.js                ← write here
    └── output.pptx

① self-parse HTML   →  Claude reads HTML, writes tmp/parsehtml.md
② detect_charts.py  →  extracts chart data → tmp/charts.json  (skip if no charts)
③ Color Master      →  audit contrast + visibility → tmp/colors.md  (always run)
④ write gen.js      →  driven by parsehtml.md + charts.json + colors.md
⑤ node tmp/gen.js   →  tmp/output.pptx  ✅ done
```

---

## Workflow: Multiple HTML Files

```
PROJECT/
├── slide1.html
├── slide2.html
└── tmp/
    ├── slide_01/
    │   ├── parsehtml.md     ← Claude writes this first
    │   ├── colors.md        ← from Phase 2.5 Color Master
    │   ├── charts.json      ← if charts detected
    │   ├── gen.js
    │   └── output.pptx
    ├── slide_02/
    │   └── (same structure)
    └── final.pptx           ← merged result
```

### Multi-HTML step-by-step

**For EACH HTML file, one at a time (never batch):**

```bash
# Slide 1
SLIDE=./tmp/slide_01
mkdir -p $SLIDE
# ① Write tool → $SLIDE/parsehtml.md  (Phase 1 template)
python3 scripts/detect_charts.py slide1.html --out $SLIDE
# ③ Color Master → $SLIDE/colors.md   (Phase 2.5)
# → write $SLIDE/gen.js  (from parsehtml.md + charts.json + colors.md)
node $SLIDE/gen.js   # ✅ output.pptx generated

# Slide 2 — only after slide 1 is done
SLIDE=./tmp/slide_02
mkdir -p $SLIDE
# ① Write tool → $SLIDE/parsehtml.md
python3 scripts/detect_charts.py slide2.html --out $SLIDE
# ③ Color Master → $SLIDE/colors.md
# → write $SLIDE/gen.js
node $SLIDE/gen.js   # ✅ output.pptx generated

# Merge all slides
python3 scripts/merge_slides.py --slides-dir ./tmp
```

### CRITICAL anti-lazy rule

**NEVER batch-loop gen.js files** — write each one individually and run it before moving to the next.

---

## Phase 1 — Self-Parse HTML → write `tmp/parsehtml.md`

Read the HTML source completely, then **write `tmp/parsehtml.md`** (or `tmp/slide_NN/parsehtml.md`) with the following structure. This file is your single source of truth for gen.js — every shape, text, and chart must appear here before being coded.

````markdown
# parsehtml.md

## 1. Canvas
- size: {width}px × {height}px
- background: {color}
- font-family: {family}
- layout: {description of top-level structure with exact px values}
  Example: "header 72px / content 580px (left-panel 668px + right-panel 349px) / summary 48px / footer 20px"

## 2. Layout Blocks
List every top-level structural section with page-level coordinates:

| id | x | y | w | h | bg | notes |
|----|---|---|---|---|----|-------|
| header | 0 | 0 | 1017 | 72 | #0f2460 | flex row, space-between, padding:0 28px |
| left-panel | 0 | 72 | 668 | 580 | #f0f5fd | padding:8 10 6 12, border-right:1px #bfdbfe |
| right-panel | 668 | 72 | 349 | 580 | #fff | padding:10 12 8 10 |
| summary | 0 | 652 | 1017 | 48 | #eef3fc | border-top:2px #2563eb |
| footer | 0 | 700 | 1017 | 20 | #0f2460 | flex space-between |

## 3. Nested Structure Analysis (CRITICAL)
For complex components (e.g., "house" container), document the FULL nested hierarchy:

```
house (x:12, y:80, w:646, h:497)
├── roof (h:44, y:82-126)
│   ├── bg:#0f2460, border-bottom:2px #2563eb at y=124
│   └── padding:0 44px (text starts at x=44)
├── floor-2col #1 (h:148, y:128-276)
│   ├── left: 应用安全 (w:322) + db-hd:24px + tile-grid:124px (2×4)
│   ├── col-sep: 1px at x=336
│   └── right: 网络安全 (w:322) + db-hd:24px + tile-grid:124px (2×4)
├── floor-div (h:1, y:276-277)
├── floor-2col #2 (h:116, y:278-394)
│   ├── left: 数据安全 (w:322) + db-hd:24px + tile-grid-3r:92px (2×3)
│   └── right: 内容安全 (w:322) + db-hd:24px + tile-grid-3r:92px (2×3)
├── floor-div (h:1, y:394-395)
├── model-floor (h:114, y:396-510) 全宽
│   ├── db-hd:24px + tile-grid-model:90px (3×3)
├── floor-div (h:1, y:510-511)
└── ops-floor (h:72, y:512-584) 全宽
    ├── ops-hd:24px + ops-tiles:48px (7 items horizontal)
```

## 4. Shapes
List every visual shape (div/span with background, border, border-radius, box-shadow):

| id | x | y | w | h | fill | border | radius | notes |
|----|---|---|---|---|------|--------|--------|-------|
| header-bg | 0 | 0 | 1017 | 72 | #0f2460 | bottom 3px #2563eb | 0 | |
| house | 12 | 80 | 646 | 497 | #f4f8ff | 2px #1e3a8a | 0 | container |
| roof | 14 | 82 | 642 | 44 | #0f2460 | bottom 2px #2563eb | 0 | trapezoid clip |
| db-hd-app | 14 | 128 | 322 | 24 | #3b82f6 | bottom 1px rgba(255,255,255,0.2) | 0 | |

## 5. Text Elements
List every visible text string with its style:

| id | text | x | y | w | h | size(px) | weight | color | align | wrap |
|----|------|---|---|---|---|----------|--------|-------|-------|------|
| h-title | "AI 安全管理框架" | 28 | 20 | 300 | 40 | 22 | bold | #ffffff | left | no |
| tag-1 | "GB/T 42118" | 560 | 20 | 80 | 28 | 11 | normal | #93c5fd | center | no |

## 6. Repeated Groups
For any element rendered N times (cards, tiles, table rows, tags):

### [group name] — N items, pattern: {forEach description}
- container: x={start_x}, y={start_y}, w={w}, h={h}, gap={g}, cols={c}
- cell calculation: cell_w=(container_w - padding_left - padding_right - (cols-1)*gap)/cols
- cell_h=(container_h - padding_top - padding_bottom - (rows-1)*gap)/rows
- shape_type: RECTANGLE | ROUNDED_RECTANGLE (from CSS border-radius)
- style: fill={color}, border={color:width}, text color={color}, font-size={px}
- data:
  1. "text content"
  2. "text content"
  ...

## 7. Charts
(If none, write "none")
- type: {radar/bar/line/pie/doughnut}
- x, y, w, h (page coords)
- data: {labels and values}
- colors: [...]

## 8. Z-order (draw sequence)
1. {bottom-most shape} - e.g., "header-bg"
2. {next level} - e.g., "left-panel-bg"
3. ...
N. {top-most element} - e.g., "footer text"

## 9. Scale & Offsets
- SLIDE_W = 10, SLIDE_H = 7.5  (LAYOUT_4x3)
- HTML_W = {w}, HTML_H = {h}
- SCALE = min(10/{w}, 7.5/{h}) = {value}
- X_OFF = (10 - HTML_W * SCALE) / 2 = {value}
- Y_OFF = (7.5 - HTML_H * SCALE) / 2 = {value}
````

**Golden Rules:**
1. **Cumulative Y verification**: After documenting nested structures, verify:
   - Each floor's end_y = start_y + height
   - Divider positions match floor endings
   - Total height = sum of all sections (roof + floors + dividers)

2. **Grid cell calculation**: For tile grids:
   - Available width = container_w - padding_left - padding_right
   - Available height = container_h - padding_top - padding_bottom
   - cell_w = (available_w - (cols-1) * gap) / cols
   - cell_h = (available_h - (rows-1) * gap) / rows

3. **Every row in §4 Shapes** becomes one `addShape()` call in gen.js
4. **Every row in §5 Text** becomes one `addText()` call in gen.js
5. **Every §6 group** becomes one `forEach()` loop in gen.js
6. **§9 values** are copied verbatim into the gen.js boilerplate
7. **If a shape has `border-radius`** → use `pres.shapes.ROUNDED_RECTANGLE`
8. **If a shape uses `clip-path` / `conic-gradient` / `polygon`** → note it and use the closest PPT shape

### Fit-to-Page Scale

```javascript
const SCALE = Math.min(SLIDE_W / HTML_W, SLIDE_H / HTML_H);
const X_OFF = (SLIDE_W - HTML_W * SCALE) / 2;
const Y_OFF = (SLIDE_H - HTML_H * SCALE) / 2;
```

Layout reference:
```
LAYOUT_WIDE  →  13.3 × 7.5 inches
LAYOUT_16x9  →  10   × 5.625 inches
LAYOUT_4x3   →  10   × 7.5 inches   ← default
```

---

## Phase 2 — Detect Charts

Run **only if HTML contains charts** (`<canvas>`, Chart.js, ECharts, conic-gradient):

```bash
python3 scripts/detect_charts.py input.html
# Multi-HTML:
python3 scripts/detect_charts.py slide1.html --out ./tmp/slide_01
```

Detects:
| Source | Pattern |
|--------|---------|
| Chart.js | `new Chart(ctx, { type, data: { labels, datasets } })` |
| ECharts | `setOption({ xAxis, series })` |
| CSS | `conic-gradient(...)` → pie approximation |
| SVG | `<polygon>` → radar approximation |

**Output: ready-to-paste gen.js snippet**

```javascript
// Chart 1: radar
slide.addChart(pres.ChartType.radar, [
  { name:"2024 年", labels:["技术能力","市场份额","客户满意度","创新指数","团队实力"],
    values:[85,70,90,75,80] },
  { name:"2023 年", labels:["技术能力","市场份额","客户满意度","创新指数","团队实力"],
    values:[70,65,80,60,75] }
], {
  x:0.5, y:0.5, w:5.5, h:3.8,
  chartColors: ['0891b2','22c55e'],
  showLegend: true, legendPos: 'b',
  radarStyle: 'filled',
});
```

Adjust `x`, `y`, `w`, `h` to match the chart's position from **parsehtml.md §7**.

If `datasets=0` (data not extracted) — fill in the data manually in **parsehtml.md §7**, then build addChart() by hand.

### Supported chart types

```javascript
pres.ChartType.radar      // spider/radar
pres.ChartType.line       // trend line
pres.ChartType.area       // filled trend area
pres.ChartType.bar        // bar/column (barDir: 'col' or 'bar')
pres.ChartType.pie        // pie
pres.ChartType.doughnut   // doughnut (holeSize: 50)
pres.ChartType.scatter
pres.ChartType.bubble
```

### addChart() full reference

```javascript
slide.addChart(pres.ChartType.radar, [
  { name: "Series", labels: ["A","B","C","D","E"], values: [85,70,90,75,80] }
], {
  x: 1.0, y: 0.5, w: 5.5, h: 4.0,
  chartColors: ["0891b2", "22c55e", "7c3aed"],  // NO # prefix
  showLegend: true,  legendPos: "b",  legendFontSize: 9,
  showValue: true,   showPercent: true,
  dataLabelFontSize: 9,  dataLabelColor: "374151",
  catAxisLabelFontSize: 9,  valAxisLabelFontSize: 8,  valAxisMajorUnit: 25,
  radarStyle: "filled",          // "standard" | "filled" | "marker"
  barDir: "col",                 // "col" | "bar"
  barGrouping: "clustered",      // "clustered" | "stacked" | "percentStacked"
  barGapWidthPct: 50,
  lineDataSymbol: "circle",      // "circle" | "dash" | "diamond" | "none" | "square" | "triangle"
  lineSmooth: false,
  holeSize: 50,                  // doughnut only (10–90%)
  showTitle: true,  title: "Chart Title",  titleFontSize: 11,
});
```

---

## Phase 2.5 — Color Master (调色大师)

**Always run this phase** after parsehtml.md is complete and before writing gen.js.
Perform a full color audit every time — write `colors.md` even if no issues are found.

### What to check

1. Any text element with contrast ratio < 4.5:1 against its parent background
2. Overlapping or adjacent shapes with visually indistinguishable fills (ΔL < 10 in HSL)
3. Repeated group cards sharing the same fill as their container (invisible cards)
4. User's explicit color requirements (e.g. "换成蓝色系", "颜色深一点", "高对比度")

---

### Step 1 — Build the contrast map

From parsehtml.md §4 Shapes + §5 Text, construct a parent-child color table:

| text-id | text-color | parent-shape | parent-fill | contrast | pass? |
|---------|-----------|--------------|-------------|----------|-------|
| h-title | #ffffff | header-bg | #0f2460 | 12.4:1 | ✅ |
| tag-1 | #93c5fd | header-bg | #0f2460 | 5.8:1 | ✅ |
| tile-label | #6b7280 | tile-bg | #f0f9ff | 3.1:1 | ❌ small text |

**WCAG contrast ratio calculation (simplified):**
```
L = 0.2126·R + 0.7152·G + 0.0722·B  (linearized)
contrast = (L_lighter + 0.05) / (L_darker + 0.05)
```

**Minimum thresholds:**
- Normal text (< 18px or < 14px bold): contrast ≥ **4.5:1**
- Large text (≥ 18px or ≥ 14px bold): contrast ≥ **3:1**
- UI components / borders vs adjacent bg: contrast ≥ **3:1**

---

### Step 2 — Detect invisible / near-invisible elements

For overlapping shape pairs (child on top of parent), flag if:
- Both fills are light (L > 85%) with ΔL < 10
- Both fills are dark (L < 20%) with ΔL < 10
- Card fill ≈ container fill AND border is absent or thin (< 1px)

| issue | element | fill | parent-fill | ΔL | fix-strategy |
|-------|---------|------|-------------|-----|-------------|
| invisible card | tile-3 | #f0f9ff | #f0f5fd | 2 | darken fill or add border |
| low-contrast text | sub-label | #9ca3af | #f9fafb | — | darken text |

---

### Step 3 — Apply user requirements (if any)

If the user specified colors:
- Honor the user's hue as the primary change
- Adjust surrounding text/borders for contrast compliance
- Never change the dominant brand color unless the user explicitly targets it

---

### Step 4 — Write `tmp/colors.md`

````markdown
# colors.md — Color Overrides (Phase 2.5 output)

## User requirements
{none | copy user's exact color words here}

## Contrast issues found
| element-id | text-color | bg-color | contrast | status |
|------------|-----------|---------|---------|--------|
| tile-label | 6b7280 | f0f9ff | 3.1:1 | ❌ fix needed |

## Visibility issues found
| element-id | fill | parent-fill | ΔL | status |
|------------|------|------------|-----|--------|
| tile-3 | f0f9ff | f0f5fd | 2 | ❌ invisible |

## Color override table
| element-id | property | original | optimized | reason |
|------------|----------|----------|-----------|--------|
| tile-label | color | 6b7280 | 374151 | contrast 3.1→7.2:1 |
| tile-3 | fill | f0f9ff | ffffff | card invisible on f0f5fd |
| tile-3 | border-color | bfdbfe | 93c5fd | add visible separation |

## Final palette (verbatim copy into gen.js const C block)
```javascript
const C = {
  tileLabel:  "374151",   // was 6b7280 — contrast fix
  tileFill:   "ffffff",   // was f0f9ff — visibility fix
  tileBorder: "93c5fd",   // was bfdbfe — visibility fix
};
```
````

**If no issues found**, still write `colors.md` with:
```markdown
# colors.md
## No issues found — using parsehtml.md colors as-is
const C = {};  // no overrides needed
```

---

### Step 5 — Inject `C` overrides into gen.js

In gen.js, add the `const C` block immediately after the boilerplate dimensions, and use `C.prop` anywhere the color was flagged:

```javascript
// ── color overrides (from tmp/colors.md) ─────────────────────────────────────
const C = {
  tileLabel:  "374151",
  tileFill:   "ffffff",
  tileBorder: "93c5fd",
};

// Then in addShape / addText calls:
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  fill: { color: C.tileFill },
  line: { color: C.tileBorder, width: 1 },
  ...
});
slide.addText(label, {
  color: C.tileLabel,
  ...
});
```

---

### Contrast quick-reference card

```
White #fff on:
  #0f2460 → 12.4:1 ✅   #1e3a8a → 10.2:1 ✅   #2563eb → 5.9:1 ✅
  #3b82f6 → 3.9:1 ❌txt   #60a5fa → 2.5:1 ❌    #93c5fd → 1.8:1 ❌

Dark #1f2937 on:
  #f9fafb → 15.8:1 ✅   #f0f9ff → 14.7:1 ✅   #e0f2fe → 12.3:1 ✅

Fixes for common gray-on-white fails:
  #9ca3af → use #6b7280 (4.6:1) ✅
  #d1d5db → use #9ca3af is still bad → use #6b7280 ✅
  #6b7280 → use #4b5563 (7.4:1) for small text ✅
```

---

## Phase 3 — Write gen.js

### Boilerplate

```javascript
"use strict";
const path = require("path");

let pptxgen;
try { pptxgen = require("pptxgenjs"); }
catch(e) { pptxgen = require(path.join(__dirname, "node_modules", "pptxgenjs")); }

// ── dimensions (from parsehtml.md §9) ────────────────────────────────────────
const SLIDE_W = 10, SLIDE_H = 7.5;   // LAYOUT_4x3 — change if needed
const HTML_W  = 1017, HTML_H  = 720; // ← copy from parsehtml.md §9
const SCALE = Math.min(SLIDE_W / HTML_W, SLIDE_H / HTML_H);
const X_OFF = (SLIDE_W - HTML_W * SCALE) / 2;
const Y_OFF = (SLIDE_H - HTML_H * SCALE) / 2;

// Conversion functions (NO rounding - keep precision)
const px = (v) => v * SCALE;
const x  = (v) => v * SCALE + X_OFF;
const y  = (v) => v * SCALE + Y_OFF;

const pres = new pptxgen();
pres.defineLayout({ name:"LAYOUT_4x3", width: SLIDE_W, height: SLIDE_H });
pres.layout = "LAYOUT_4x3";

const slide = pres.addSlide();

// ── shapes + charts ───────────────────────────────────────────────────────────
// Source: tmp/parsehtml.md §4 Shapes  → addShape() calls
// Source: tmp/parsehtml.md §6 Groups  → forEach() loops
// Source: tmp/parsehtml.md §5 Text    → addText() calls
// Source: tmp/charts.json             → addChart() calls
// Source: tmp/colors.md  const C{}    → color overrides (supersede §4/§5/§6 colors)

pres.writeFile({ fileName: path.join(__dirname, "output.pptx") })
    .then(() => console.log("✅ Written:", path.join(__dirname, "output.pptx")))
    .catch(err => { console.error("❌", err); process.exit(1); });
```

### String safety

```javascript
// ✅ Unicode escapes — always safe
slide.addText("\u6570\u636E\u5B89\u5168", { ... });

// ✅ Raw Chinese safe inside Write tool (UTF-8)
slide.addText("数据安全", { ... });
```

### ⚠️ Unicode escape validation — CRITICAL

Every `\uXXXX` escape **must** use exactly 4 hexadecimal digits (0–9, a–f, A–F).
Non-hex characters cause a `SyntaxError: Invalid Unicode escape sequence` that aborts the entire slide.

**Common failure patterns found in practice:**

| Bad | Why broken | Fix |
|-----|-----------|-----|
| `"\u8诗"` | `诗` is not a hex digit | Find correct codepoint: `"\u8BC7"` |
| `"\u26Q1"` | `Q` is not hex | Use literal or correct escape: `"26Q1"` |
| `"\uD83C\uDFCX"` | `X` invalid | Look up the actual emoji codepoint |

**Before writing gen.js, grep every `\u` sequence:**
```bash
# Any \u followed by non-hex char → fix immediately
grep -oP '\\u[0-9a-fA-F]{0,3}[^0-9a-fA-F"\\]' gen.js
```

**Safe alternative** — use the literal character in the Write tool (UTF-8):
```javascript
slide.addText("史诗风格", { ... });   // raw UTF-8, always valid
```

### ⚠️ Text properties — CRITICAL

| Property | Wrong | Correct | Reason |
|----------|-------|---------|--------|
| `fontSize` | `12` (px) | `12 * 0.75 = 9` (pt) | PPT uses points, not pixels |
| `wrap` | omit | `false` (single-line) / `true` (multi-line) | Control text wrapping |
| `margin` | omit / `5` | `0` | PPT default adds 0.05" per side |
| `valign` | omit | `middle` / `top` / `bottom` | Vertical alignment |

```javascript
// ✅ CORRECT single-line text
slide.addText("\u6570\u636E\u5B89\u5168", {
  x: x(24), y: y(100), w: px(280), h: px(32),
  fontSize: 12 * 0.75,          // CSS px → pt
  fontFace: "Microsoft YaHei",
  color:    "1a1a2e",           // no #
  wrap:      false,             // REQUIRED for single-line
  margin:    0,                 // REQUIRED
  valign:   "middle",
});

// ✅ Multi-line text (word-wrap elements only)
slide.addText("long text...", {
  x: x(24), y: y(200), w: px(320), h: px(64),
  fontSize: 12, fontFace: "Microsoft YaHei",
  wrap: true, margin: 0, valign: "top",
});
```

**CSS px → pt conversion:**
```
 8px→6pt   10px→7.5pt   12px→9pt   14px→10.5pt   16px→12pt   18px→13.5pt   24px→18pt
```

### Font mapping

```javascript
"PingFang SC"    →  "Microsoft YaHei"
"system-ui"      →  "Segoe UI"
"Helvetica Neue" →  "Arial"
"Inter"          →  "Calibri"
"KaiTi", "楷体"   →  "Microsoft YaHei"  // KaiTi not always available
```

### Draw order follows parsehtml.md §8 Z-order

### Layout Master Checklist

Before writing gen.js, verify:

1. **Background layers first**: header-bg → panel-bg → container-bg
2. **Borders as separate shapes**: bottom borders, divider lines, column separators
3. **Domain headers before tiles**: Each domain's header bar drawn before its tiles
4. **Tiles use loop**: forEach for repeated tiles, not individual calls
5. **Text on top**: All text elements after shapes
6. **Coordinates match parsehtml.md §4**: Every x/y/w/h value traces back to the table — layering is intentional, gaps are not

---

## Phase 4 — Run gen.js

```bash
node ./tmp/gen.js                 # single HTML
node ./tmp/slide_01/gen.js        # per-slide (multi-HTML)
```

---

## Phase 5 — Merge Slides (multi-HTML or user request)

**Trigger**: run this phase if ANY of these apply:
- More than one HTML was converted (multiple `tmp/slide_NN/output.pptx` exist)
- User asks to "合并", "merge", "combine into one file", or "生成最终 PPT"

### Pre-merge checklist

Run the script's built-in inspector first — it validates every slide before merging:

```bash
# The script auto-rejects empty slides; review its output before proceeding
python3 scripts/merge_slides.py --slides-dir ./tmp
```

### Run merge

```bash
# Auto-detect all tmp/slide_*/output.pptx → ./final.pptx
python3 scripts/merge_slides.py

# Explicit slides dir
python3 scripts/merge_slides.py --slides-dir ./tmp

# Custom output path
python3 scripts/merge_slides.py --out ./my-report.pptx

# Explicit file list (custom order)
python3 scripts/merge_slides.py tmp/slide_01/output.pptx tmp/slide_03/output.pptx tmp/slide_02/output.pptx

# Skip empty-slide rejection (not recommended)
python3 scripts/merge_slides.py --no-strict
```

### What the script does

```
For each source PPTX (after the first), using ZIP-level manipulation:
  1. Read source slide XML verbatim
  2. Parse slide rels — find chart, media, notes relationships
  3. Chart handling (KEY FIX — pptxgenjs uses ABSOLUTE chart paths):
       - pptxgenjs writes Target="/ppt/charts/chart1.xml" (absolute)
       - Every source PPTX has its own chart1.xml → name collision without renaming
       - Script renames: src chart1.xml → dest chartN.xml (next available index)
       - Updates chart refs in slide rels to new absolute path
       - Copies chart rels (.rels) with updated embedding refs
       - Copies embedding .xlsx files renamed to next available index
  4. Media handling: renames image1.png → imageN.png to avoid collision
  5. Removes notesSlide rels (notes not merged)
  6. Writes slide{N}.xml + updated rels into dest zip
  7. Patches presentation.xml sldIdLst with new slide id + rId
  8. Patches ppt/_rels/presentation.xml.rels with new Relationship entry
  9. Patches [Content_Types].xml with Override entries for new slide + charts
Pre-merge:  inspects each PPTX for shapes > 0
Post-merge: re-inspects final.pptx, prints slide/shape counts
```

> **Why NOT python-pptx `relate_to()` API**: that API copies part *references*
> across presentations and produces duplicate zip entries (`Duplicate name: ppt/charts/chart1.xml`)
> causing chart data corruption. Always use ZIP-level manipulation for merging.

### Output structure

```
PROJECT/
└── tmp/
    ├── slide_01/output.pptx   ✅ 42KB, 8 shapes
    ├── slide_02/output.pptx   ✅ 38KB, 6 shapes
    └── ...
final.pptx                     ✅ merged result
```

### Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `[ERROR] No slide files found` | Wrong working dir | `cd` to project root first |
| Slide appears blank in final.pptx | gen.js had a runtime error | Re-run `node gen.js` — check for errors before merging |
| **Charts show wrong data after merge** | **pptxgenjs uses absolute chart paths (`/ppt/charts/chart1.xml`); multiple slides share the same name → first slide's chart overwrites the rest** | **Use zip-level merge script (v4.3+) which renames chart files to unique indices** |
| **Charts display as empty grey box** | Chart XML copied but embedding .xlsx not copied, or Content_Types missing chart override | Ensure merge script copies both `ppt/charts/chartN.xml` AND `ppt/charts/_rels/chartN.xml.rels` AND `ppt/embeddings/*.xlsx` |
| `SyntaxError: Invalid Unicode escape sequence` | `\uXXXX` in gen.js contains non-hex character (e.g. `\u8诗`, `\u26Q1`) | Find correct 4-hex codepoint or use raw UTF-8 string literal |
| `Duplicate name: ppt/charts/chart1.xml` warning | Using python-pptx `relate_to()` API to merge — wrong approach | Switch to zip-level merge script; never use `add_slide()` + `relate_to()` for merging |
| `ModuleNotFoundError: pptx` | python-pptx not installed | `pip install python-pptx lxml` |
| `ModuleNotFoundError: lxml` | lxml not installed | `pip install lxml` |

---

## CSS → PPT Reference

### Colors
```javascript
"#0891b2"              → color: "0891b2"   // strip #
"rgba(8,145,178,0.18)" → color: "0891b2"   // rgb→hex, use dominant
"linear-gradient(…)"   → color: "ecfeff"   // dominant color as flat fill
```

### Border as accent bar
```javascript
// border-left: 3px solid #0891b2
slide.addShape(pres.shapes.RECTANGLE, {
  x: x(cardX), y: y(cardY), w: px(3), h: px(cardH),
  fill: { color: "0891b2" }, line: { width: 0 },
});
```

### Box shadow
```javascript
shadow: { type:"outer", color:"000000", opacity:0.1, blur:8, offset:2, angle:270 }
```

### Repeated elements — always forEach
```javascript
const rows = [
  { name:"采集", desc:"分类分级" },
  { name:"传输", desc:"TLS/国密" },
];
rows.forEach((row, i) => {
  const ry = y(380 + i * 63);
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x:x(760), y:ry, w:px(320), h:px(58),
    fill:{color:"f0fdf4"}, line:{color:"86efac",width:1},
  });
  slide.addText(row.name, {
    x:x(790), y:ry, w:px(80), h:px(58),
    valign:"middle", fontSize:7, fontFace:"Microsoft YaHei", color:"166534",
    wrap:false, margin:0,
  });
});
```

---

## Critical Don'ts

| ❌ Don't | ✅ Do |
|---------|-------|
| Skip writing parsehtml.md | Complete all 9 sections of parsehtml.md before touching gen.js |
| Write gen.js without parsehtml.md | Every addShape/addText must trace back to parsehtml.md |
| Skip Color Master (Phase 2.5) | Always write colors.md — even if no issues found, write `const C = {}` |
| Ignore invisible cards / low-contrast text | Run full contrast map; darken text or lighten/darken fills to meet thresholds |
| Batch-loop all gen.js | Write each gen.js individually, run it, then move to next |
| Draw charts as shapes/polygons | Use addChart() — PPT native charts |
| Skip detect_charts.py when `<canvas>` present | Always run it for Chart.js / ECharts / canvas |
| Use scale = sw/html_w only | Use min(sw/html_w, sh/html_h) — from parsehtml.md §9 |
| Forget X_OFF / Y_OFF | x_in = css_px × SCALE + X_OFF — from parsehtml.md §9 |
| color: "#0891b2" | color: "0891b2" |
| fontFace: "PingFang SC" | fontFace: "Microsoft YaHei" |
| fontSize in CSS px | fontSize × 0.75 for pt |
| Omit wrap/margin on text | wrap:false, margin:0 on every single-line text |
| Copy-paste repeated elements | Use forEach loop (shape_type from parsehtml.md §6) |
| Round coordinates in conversion | Use `v * SCALE` directly, no Math.round |
| Skip cumulative Y verification | Verify: end_y = start_y + height for each section |
| Misplace draw order | Follow z-order: backgrounds → shapes → text |
| Use px() for positions | Use x()/y() for positions, px() for dimensions |
| **Write `\uXXXX` without verifying all 4 chars are hex** | **Validate every Unicode escape: digits 0–9 and letters a–f/A–F only. Invalid digit (e.g. `\u8诗`, `\u26Q1`) = SyntaxError. Use raw UTF-8 literal when unsure.** |
| **Merge PPTX with python-pptx `add_slide()` + `relate_to()`** | **Use ZIP-level merge script — pptxgenjs absolute chart paths cause duplicate zip entries and wrong chart data with the python-pptx API** |

---

## Debugging Checklist

If output has misaligned elements:

1. **Verify SCALE calculation**: `console.log(SCALE, X_OFF, Y_OFF)`
2. **Check cumulative Y**: Each section's end_y must match next section's start_y
3. **Verify grid calculations**: cell_w/cell_h formulas account for all gaps
4. **Confirm z-order**: Backgrounds drawn before foreground elements
5. **Check border positions**: Separate shape for borders (not included in main rect)
6. **Validate padding**: Container padding subtracted from cell calculations

If colors look wrong or elements are invisible:

7. **Re-read colors.md**: Verify `const C` block was copied into gen.js correctly
8. **Check contrast map**: Re-run Phase 2.5 audit for the affected element
9. **Verify parent bg**: Confirm which shape is the visual parent — may differ from DOM parent
