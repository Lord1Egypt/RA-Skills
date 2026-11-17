# Layouts

iA Presenter chooses a layout automatically from the slide's content. You steer it by
shaping cells; you can also force one with `Layout: Name`. Source: in-app Help
(`Layouts.html`, `Custom Themes.html`), the app's `layouts.json`, and live tests on
2.0.2.

## Cells

A **cell** ("element group") is a run of lines with no blank line inside it. Blank lines
split cells. The engine looks at:

1. the number of cells,
2. whether each cell contains a graphic,
3. the first heading level of each cell,
4. their order.

Rules of thumb (verified):

| Content | Result |
|---|---|
| `# Title` (+ TAB kicker/subtitle in the same cell) | cover-style big title |
| `## Title` alone | centered section title |
| `## Title` + blank + 2–3 cells (text or images) | title row + side-by-side columns |
| 2–3 cells, no leading title | split, side by side (stacks on narrow phones) |
| 4 or more cells | grid, in source order (`grid-items-4` …) |
| `## Title` + blank + one image | title + image |
| `#### Caption` then image / image then `#### Caption` | caption on top / at the bottom |
| image with `Background: true` + heading(s) | text over the full-bleed image |
| one lone image | full-bleed image |
| flush-left table | a real table (or chart with `Chart:`) |
| `## Title` + blank + table | title **beside** a narrow table (split) – keep the table in the same cell as the heading (no blank line) for a full-width table |

Keep a heading and its subtitle in the **same** cell (no blank line) when they belong
together; put a blank line between things that should be laid out separately.

## `Layout:` directive

First line of the slide (right after `---`), case-insensitive:

```
---
Layout: Title-and-Columns

## Title

### Left
⇥Left body

### Right
⇥Right body
```

Names from the app's `layouts.json` and what they do (2.0.2):

| Name | Container class | Content class | Behaviour | Verified |
|---|---|---|---|---|
| `Cover` | `.cover-container` | `.layout-cover` | content bottom-left, big | ✅ |
| `Title` | `.title-container` | `.layout-title` | content centered | (standard) |
| `Section` | `.section-container` | `.layout-section` | centered vertically, left aligned; dark appearance by default | ✅ |
| `Default` | `.default-container` | `.layout-default` | text layout, starts top-left, dynamic cells | (standard) |
| `Split` | `.v-split-container` | `.layout-v-split` | first two cells side by side | ✅ |
| `Grid` | `.grid-container` | `.layout-grid` + `grid-items-N` | every cell (incl. the heading) becomes a grid cell, up to 9 | ✅ (title becomes a cell) |
| `Columns` | `.columns-container` | `.layout-columns` + `columns-items-N` | **broken in 2.0.2**: cells stack with tiny text | ❌ avoid |
| `Title-and-Columns` | `.title-and-columns-container` | `.layout-title-and-columns` | first cell is the title row (`.title-part`), the rest are columns (`.column-part`) | ✅ |
| `Caption` | `.caption-container` | `.layout-caption` | image + caption band below | ✅ |
| `Caption-Top` | `.title-image-container` | `.layout-title-image` | caption band above image | ✅ |
| `Image` | `.full-image-container` | `.layout-full-image` | heading band + full-width image | ✅ |

The layout picker (`+` in the toolbar) inserts the same names, plus theme-provided
`LayoutExamples`. `Class: name` on the first line adds a CSS class to the slide instead.

## Slide DOM (for theme authors)

```
<section class="cover-container light|dark has-media …">   ← slide container
  <div class="header">…</div>
  <div class="layout-cover slide-contents">                  ← content class
    <div class="element-group">…cell…</div>                  ← one div per cell
  </div>
  <div class="footnotes">…</div>
  <div class="footer">…</div>
</section>
```

- Every slide also gets a **background div** with the same layout class inside
  `.backgrounds` (`.backgrounds .cover-container { … }` styles the cover background;
  `.slide-background` targets all).
- No footnotes → the footnotes div has zero height; no header/footer → content takes the
  whole slide.
- Extra state classes on the section: `has-media`, `has-media-first/middle/last`,
  `has-background-image`, `has-light-background`, `has-dark-background`, `has-header`,
  `has-footer`, `has-footnotes`, `has-logo`, `has-graph-background`, `light`, `dark`.
- Alignment inside a layout is set on the inner div:
  `.layout-cover > div { justify-content: flex-end; align-items: flex-start; }`
  (`justify-content` = vertical, `align-items` = horizontal), or via the engine variables
  `--text-horizontal-align-layout-cover`, `--text-vertical-align-layout-cover`, etc.

## Responsive

Layouts adapt to the screen (Settings → Presentation → Layout: Responsive, or fixed
4:3, 16:9, 9:16, 4:5, 1:1). Side-by-side cells may stack on phones. Theme CSS is
mobile-first; desktop rules go under `@media (min-width: 768px)`.
