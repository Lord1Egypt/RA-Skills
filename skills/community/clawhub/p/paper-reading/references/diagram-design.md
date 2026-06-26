# Diagram design system

Load this file before building any architecture diagram with `--draw-structure`. It defines every visual primitive you need: colors, typography, spacing, arrows, component patterns. Treat these as the defaults — only deviate with a reason.

## Theme selection

The `--bg-theme` flag controls the diagram palette:

- `--bg-theme dark` (default): technical slate canvas, luminous strokes, white component titles.
- `--bg-theme light`: paper-white canvas, darker text, softer tinted fills, and lower-contrast grid/strokes. Do **not** reuse dark fills on a light canvas; they become muddy and too heavy.

Implement themes with CSS variables in HTML where possible. For standalone SVG, inline the chosen literal colors.

## Canvas

- **Dark background:** `#020617` (slate-950).
- **Light background:** `#f8fafc` (slate-50) for the page, with `#ffffff` or `#f8fafc` for the SVG canvas.
- **Grid overlay:** subtle 40px grid for spatial reference. Use `#1e293b` at `0.5` stroke on dark; use `#dbe4ee` at `0.6` stroke on light.
  ```svg
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="GRID_COLOR" stroke-width="0.5"/>
  </pattern>
  <rect width="100%" height="100%" fill="url(#grid)"/>
  ```
- **ViewBox:** start with `1200 × 800`. Expand height as needed — don't cram content to fit.

## Color semantics

Every box's color tells the reader what *kind* of thing it is. Use these mappings consistently within a diagram.

### Dark theme palette

| Role in a paper diagram | Fill | Stroke | Hex stroke |
|---|---|---|---|
| **Core contribution / novel method** | `rgba(6, 78, 59, 0.4)` | emerald | `#34d399` |
| **Input / data / rollouts** | `rgba(8, 51, 68, 0.4)` | cyan | `#22d3ee` |
| **Storage / memory / dataset** | `rgba(76, 29, 149, 0.4)` | violet | `#a78bfa` |
| **External / baseline / generic** | `rgba(30, 41, 59, 0.5)` | slate | `#94a3b8` |
| **Prior work's failure / warning** | `rgba(136, 19, 55, 0.4)` | rose | `#fb7185` |
| **Reward / signal / intermediate flow** | `rgba(251, 146, 60, 0.3)` | orange | `#fb923c` |
| **Region / cluster boundary** | `rgba(251, 191, 36, 0.05)` | amber | `#fbbf24` |
| **Priority / weighting / auxiliary** | `rgba(76, 29, 149, 0.4)` | violet | `#a78bfa` |

Supporting dark tokens:

| Token | Value |
|---|---|
| `page-bg` | `#020617` |
| `panel-bg` | `rgba(15, 23, 42, 0.5)` |
| `box-mask` | `#0f172a` |
| `text-main` | `#ffffff` |
| `text-muted` | `#94a3b8` |
| `text-faint` | `#475569` |
| `grid` | `#1e293b` |
| `arrow` | `#64748b` |

### Light theme palette

Use the same semantic hues, but shift to deeper strokes and pale fills so the diagram reads cleanly on white.

| Role in a paper diagram | Fill | Stroke | Hex stroke |
|---|---|---|---|
| **Core contribution / novel method** | `rgba(16, 185, 129, 0.13)` | emerald | `#047857` |
| **Input / data / rollouts** | `rgba(14, 165, 233, 0.12)` | cyan/sky | `#0284c7` |
| **Storage / memory / dataset** | `rgba(124, 58, 237, 0.11)` | violet | `#7c3aed` |
| **External / baseline / generic** | `rgba(100, 116, 139, 0.10)` | slate | `#64748b` |
| **Prior work's failure / warning** | `rgba(244, 63, 94, 0.12)` | rose | `#e11d48` |
| **Reward / signal / intermediate flow** | `rgba(249, 115, 22, 0.13)` | orange | `#ea580c` |
| **Region / cluster boundary** | `rgba(16, 185, 129, 0.06)` | emerald | `#059669` |
| **Priority / weighting / auxiliary** | `rgba(139, 92, 246, 0.12)` | violet | `#7c3aed` |

Supporting light tokens:

| Token | Value |
|---|---|
| `page-bg` | `#f8fafc` |
| `panel-bg` | `#ffffff` |
| `box-mask` | `#ffffff` |
| `text-main` | `#0f172a` |
| `text-muted` | `#475569` |
| `text-faint` | `#64748b` |
| `grid` | `#dbe4ee` |
| `arrow` | `#94a3b8` |
| `panel-border` | `#d8e0ea` |

**The one rule to never break:** the paper's core contribution gets emerald. Everything else is context.

Light theme design notes:

- Prefer white panels over gray panels; use border and shadow for structure.
- Use deeper accent strokes (`#047857`, `#0284c7`, `#e11d48`) rather than neon colors.
- Text inside boxes should be `#0f172a`; sublabels should be `#475569`.
- Avoid large saturated backgrounds. Keep fills around 10–14% opacity.
- Use a soft shadow on the main diagram container only, not on every box.

## Typography

Primary font: **JetBrains Mono** (monospace gives the technical aesthetic; consistent character widths help grid-align elements).

```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

For Chinese labels (`--showcase-language cn`), extend the stack:

```css
font-family: 'JetBrains Mono', 'Noto Sans SC', 'Courier New', monospace;
```

And include `Noto+Sans+SC` in the Google Fonts URL.

Size hierarchy:

| Purpose | Size | Weight | Color |
|---|---|---|---|
| Section headers (▸ GDPO PIPELINE) | 11 | 700 | accent (match section) |
| Component name (box title) | 11 | 600 | `text-main` |
| Component sublabel | 9 | 400 | `text-muted` |
| Small annotations / arrow labels | 8 | 400 | `text-muted` |
| Tiny legend labels | 8 | 400 | `text-muted` |
| Math / formulas inside boxes | 10–11 | italic | accent |

## Component patterns

### Standard component box

```svg
<rect x="X" y="Y" width="W" height="H" rx="6"
      fill="FILL_COLOR" stroke="STROKE_COLOR" stroke-width="1.5"/>
<text x="CENTER_X" y="Y+20" fill="TEXT_MAIN" font-size="11"
      font-weight="600" text-anchor="middle">LABEL</text>
<text x="CENTER_X" y="Y+36" fill="TEXT_MUTED" font-size="9"
      text-anchor="middle">sublabel</text>
```

Standard heights: 60px for simple services, 70–80px for labeled boxes, 100–120px for multi-line content.

### Region / cluster boundary

Dashed amber rectangle enclosing a logical group (e.g., "GDPO CORE"):

```svg
<rect x="X" y="Y" width="W" height="H" rx="12"
      fill="REGION_FILL" stroke="CORE_STROKE"
      stroke-width="1.5" stroke-dasharray="8,4"/>
<text x="X+20" y="Y+25" fill="CORE_STROKE" font-size="11"
      font-weight="700" letter-spacing="1">◆ REGION LABEL</text>
```

The `◆` (or `▸`, `⚠`, `◇`) glyph serves as a visual section marker — use consistently.

### Security-group style (transparent dashed box)

For sub-groupings within a region:

```svg
<rect x="X" y="Y" width="W" height="H" rx="8"
      fill="transparent" stroke="WARNING_STROKE"
      stroke-width="1" stroke-dasharray="4,4"/>
```

## Arrows

### Definitions

```svg
<defs>
  <marker id="arrowhead" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="ARROW_COLOR"/>
  </marker>
  <marker id="arrowhead-emerald" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="CORE_STROKE"/>
  </marker>
  <!-- One per accent color you use -->
</defs>
```

### Arrow types

| Purpose | Style |
|---|---|
| Standard data flow | solid 1.5px, `arrow`, `marker-end="url(#arrowhead)"` |
| Core method flow | solid 2px, core stroke, core arrowhead |
| Training loop / feedback | dashed 1.5px `stroke-dasharray="5,5"`, data stroke |
| Auth / priority / guarded flow | dashed 1.5px, warning stroke |
| Contrast marker (GRPO → GDPO) | solid, larger, slate |

### Z-order

SVG elements paint in document order. Draw arrows **early** (right after the grid) so they sit behind boxes. Then draw boxes on top.

### Masking arrows behind semi-transparent fills

Component boxes use translucent fills, so arrows behind them show through as washed-out lines. If you need a clean mask, lay an opaque base rect first. Use `#0f172a` in dark mode and `#ffffff` in light mode:

```svg
<!-- Opaque background mask -->
<rect x="X" y="Y" width="W" height="H" rx="6" fill="BOX_MASK"/>
<!-- Styled component on top -->
<rect x="X" y="Y" width="W" height="H" rx="6"
      fill="CORE_FILL" stroke="CORE_STROKE" stroke-width="1.5"/>
```

## Spacing discipline

This is where most diagrams go wrong. The rules:

- **Minimum vertical gap between stacked boxes:** 40px.
- **Inline connectors (small message buses, labels):** place *in* the gap, not overlapping the boxes.
- **Arrow length:** at least 30px of visible shaft. If two boxes are too close, move them apart.
- **Text-to-edge padding inside boxes:** 10px minimum on all sides.
- **Legend placement:** outside all boundary boxes. Compute the lowest boundary bottom, add ≥20px, place legend below that. Extend the SVG viewBox height if needed.

### Worked spacing example

```
Box A: y=70,   height=60   → bottom at y=130
Gap:   y=130 to y=170      → 40px gap
         (message bus at y=140, 20px tall → sits in middle)
Box B: y=170,  height=60   → bottom at y=230
```

**Wrong:** Box B at y=160 when Box A ends at y=130 (only 30px gap — too tight).
**Right:** Box B at y=170 (40px gap) with an optional inline element at y=140.

## Layout for paper diagrams

A paper diagram has three typical sections, stacked vertically:

1. **Main pipeline** (top): the left-to-right or top-to-bottom flow of the method. Most important part — give it the most real estate.
2. **Contrast panel** (middle, optional): the "why this beats prior work" comparison. Two side-by-side boxes — rose-colored for prior work, emerald for this paper. Include concrete numbers if the paper provides them (like GDPO's advantage values).
3. **Auxiliary detail** (bottom, optional): priority handling, loss decomposition, hyperparameter table — anything secondary the reader might care about.

Each section gets its own header line: `▸ SECTION NAME` in the accent color for that section.

## Summary cards (HTML output only)

Below the SVG, use a CSS grid of 3–6 cards capturing the paper's key points. One card per theme:

```html
<div class="card">
  <div class="card-header">
    <div class="card-dot COLOR"></div>
    <h3>Card title</h3>
  </div>
  <ul>
    <li>• Bullet one (one specific fact)</li>
    <li>• Bullet two</li>
  </ul>
</div>
```

Theme card styling:

- Dark: card `background: rgba(15, 23, 42, 0.5)`, border `#1e293b`, title `#ffffff`, body `#94a3b8`.
- Light: card `background: #ffffff`, border `#d8e0ea`, title `#0f172a`, body `#475569`, optional subtle `box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08)`.

Suggested cards for a method paper:

1. **The Problem** (rose dot) — what failure mode the paper identifies
2. **The Fix** (emerald dot) — the method in 3–4 bullets
3. **Empirical Validation** (amber dot) — headline numbers with concrete deltas
4. **Secondary Insights** (violet dot) — priority handling, conditioning, etc.
5. **Design Choices to Note** (cyan dot) — reproduction gotchas
6. **Open Questions** (orange dot) — what the paper leaves unresolved

Bullet content should be specific. "Improves accuracy" is useless; "+6.3% pass@1 on AIME with DS-R1-1.5B" is useful.

## Checklist before committing the diagram

Walk through these before you declare done:

- [ ] Core contribution is emerald and visually dominant
- [ ] The selected `--bg-theme` palette is applied consistently to page, SVG canvas, cards, legend, arrows, masks, and text
- [ ] Light theme uses dark readable text and pale fills, not dark-theme colors pasted onto white
- [ ] Every box has a purpose — no decorative placeholders
- [ ] Every arrow has a clear source and target; no dangling lines
- [ ] Every region boundary contains what it labels; nothing spills out
- [ ] Legend is outside all boundaries
- [ ] ViewBox height accommodates the legend
- [ ] Key equations are inline in the flow, not buried in a separate panel
- [ ] The diagram would be comprehensible without the paper open alongside
- [ ] The contrast panel (if included) uses concrete numbers, not hand-waves
- [ ] No text overlaps another text; no text overlaps a stroke line
- [ ] Chinese labels (if applicable) have `Noto Sans SC` in the font stack
- [ ] File saved under `/mnt/user-data/outputs/` with a descriptive filename
- [ ] `present_files` called with the output path

## Rendering notes

**For PNG output via Playwright:** use `device_scale_factor=2` and `wait_for_timeout(1500)` after `networkidle` to let Google Fonts finish loading. Without the wait, fonts fall back to generic monospace.

**For SVG standalone:** the `<style>` block must use CDATA. Otherwise the `&` in the Google Fonts URL breaks XML parsing:

```svg
<style><![CDATA[
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');
  text { font-family: 'JetBrains Mono', monospace; }
]]></style>
```
