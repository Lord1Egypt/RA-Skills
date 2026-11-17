# Rendering engine: classes and CSS variables

Extracted from `.Engine/main.css`, `core.css`, `style.css` and `layouts.json` of iA
Presenter 2.0.2. Use these when writing theme CSS. Engine files are regenerated on every
launch – never edit them; override from your theme CSS instead.

## Document structure

```
body.responsive
└── .reveal > .slides
    └── section.<layout>-container.light|dark[.has-…]      one per slide
        ├── .header
        ├── .<layout-class>.slide-contents[.grid-items-N|.columns-items-N]
        │   └── .element-group (one per cell; .title-part / .column-part in Title-and-Columns)
        ├── .footnotes
        └── .footer
.backgrounds > .<layout>-container.slide-background        matching background layer
```

Root/presentation classes come from the theme's `CssClasses`
(`variable-size-headings`, `fixed-size-headings`, `has-graph-background`) plus state
such as `night-mode`, `print-pdf`, `context-pdf-export`, `web-sharing`.

## Layout classes

| Layout | container | content |
|---|---|---|
| Cover | `.cover-container` | `.layout-cover` |
| Title | `.title-container` | `.layout-title` |
| Section | `.section-container` | `.layout-section` |
| Default | `.default-container` | `.layout-default` |
| Split | `.v-split-container` | `.layout-v-split` (also `.layout-split`) |
| Grid | `.grid-container` | `.layout-grid` + `.grid-items-1…10` |
| Columns | `.columns-container` | `.layout-columns` + `.columns-items-2/3` |
| Title-and-Columns | `.title-and-columns-container` | `.layout-title-and-columns`, `.title-part`, `.column-part` |
| Caption | `.caption-container` | `.layout-caption` |
| Caption-Top | `.title-image-container` | `.layout-title-image` |
| Image | `.full-image-container` | `.layout-full-image` |
| (notes) | – | `.layout-notes` |

## State classes on `section`

`light`, `dark`, `has-media`, `has-media-first`, `has-media-middle`, `has-media-last`,
`has-background-image`, `has-light-background`, `has-dark-background`,
`has-parallax-background`, `has-graph-background`, `has-header`, `has-footer`,
`has-footnotes`, `has-logo`, `has-highlights`, `has-N-series` (charts),
`has-positive-and-negative-values`, `single-image`, `image-grid`, `media-grid`,
`two-rows`, `fitted`, `present`, `past`, `future`, `current-visible`.

## Media classes

- Figures: `figure.default-image` (placeholder), `.single-image-wrapper`, `.videoWrapper`,
  `.html-videoWrapper`, `.embedded`.
- Size: `.size-cover`, `.size-contain`.
- Position: `.position-{left|center|right}-{top|center|bottom}`.
- Filters: `.image-filter-{lighten|darken|grayscale|sepia|blur}`,
  `.background-filter-{…}`.
- Opacity: `.image-opacity-10…100`, `.background-opacity-10…100` (steps of 10).
- Kicker: `.kicker`. Highlight: `mark` with `.highlight-*`, `.yellow`/`.blue`/… marks.
- Tasks: `.task-list-item`, `.task-list-item-checkbox`.
- Code: `.hljs` and `.hljs-*` token classes (highlight.js).
- Charts: `.graph-container`, `.graph-bar`, `.graph-line`, `.graph-pie`, `.graph-caption`,
  `.html-legend`, `.html-x-axis-label`, `.html-y-axis-label`, `.is-stacked`,
  `.is-rotated`, `.is-step`, `.colorset-sequential`, `.colorset-differential`, `.bb-*`
  (billboard.js).
- Fragments/animation (reveal.js): `.fragment`, `.fade-in`, `.fade-up`, `.grow`,
  `.highlight-red`, `.current-visible`… (not exposed by Markdown; for HTML export tweaks).

## CSS variables you can set

Set on `:root`, `section`, `section.light` / `section.dark`, or a layout container.

**Typography scale** – `--scale-factor-h1` … `--scale-factor-h6`,
`--scale-factor-blockquote`, `--scale-factor-td`, `--scale-factor-th`,
`--font-size-scale`, `--scale-multiplier`, `--min-font-size`, `--max-font-size`,
`--p-base-size`, `--p-mobile-base-size`, `--single-column-max-width`,
`--text-scale-intensity`, `--max-text-scale-intensity`.

**Per element (h1…h6, p, header-footer)** – `--font-weight-h1`, `--line-height-h1`,
`--letter-spacing-h1`, `--margin-h1`, `--case-h1` (`uppercase`/`none`),
`--font-variation-settings-h1`, `--h1-offset`, `--h1-mobile-offset`; same for h2…h6,
`--font-weight-p`, `--line-height-p`, `--letter-spacing-p`, `--margin-p`, `--case-p`,
`--font-weight-header-and-footer`, `--font-size-header-footer`,
`--paragraph-spacing`, `--paragraph-indentation`, `--blockquote-offset`,
`--first-list-margin-top`, `--nested-list-margin`, `--list-counter-style`.

**Fonts / colors (set by presets, overridable)** – `--titlefont`, `--bodyfont`,
`--font-family-head`, `--font-family-body`, `--font-family-mono`, `--text-color`,
`--darkbackgroundcolor`, `--lightbackgroundcolor`, `--darkbodytextcolor`,
`--lightbodytextcolor`, `--darktitletextcolor`, `--lighttitletextcolor`.

**Alignment per layout** – `--text-horizontal-align-layout-{cover|title|section|default|caption}`
(`left|center|right`), `--text-vertical-align-layout-{cover|title|section|default|split|3-column}`
(`top|center|bottom`).

**Spacing** – `--padding`, `--padding-top/right/bottom/left`, `--min-padding`,
`--max-padding`, `--slide-margin`, `--top-space`, `--bottom-space`,
`--extra-padding-top/…`, `--CONTENT_PADDING_X`, `--CONTENT_PADDING_Y`,
`--vertical-padding-size-header-footer-footnotes`, `--multi-column-minimum-item-size`.

**Logo / header** – `--logo-size`, `--min-logo-height`, `--max-logo-height`.

**Code blocks** – `--code-background`, `--code-border`, `--code-text`, `--code-comment`,
`--code-type`, `--code-include`, `--code-string`, `--code-class-name`, `--code-numbers`,
`--code-variables`, `--code-functions`, `--code-literal`, and the `--dark-code-*` twins.

**Highlights** – `--mark-background-color`, `--mark-background-alpha`,
`--mark-text-color`, `--mark-underline-color`, `--mark-underline-thickness`.

**Tables** – `--border-table-color`, `--border-table-width`, `--border-row-color`,
`--border-row-width`, `--dark-border-table-color`, `--dark-border-row-color`,
`--td`, `--th`, `--checkbox-size`.

**Charts** – `--graph-data-0` … `--graph-data-7`, `--sequential-color`,
`--sequential-shade-1…13`, `--differential-color-positive`,
`--differential-color-negative`, `--differential-shade-1…15`, `--positive-color`,
`--negative-color`, `--graph-font-family`, `--graph-font-size`, `--graph-background`,
`--graph-grid-line`, `--graph-stroke-width`, `--graph-axis-tick-font-size`,
`--legend-text`, `--label-text`, `--tooltip-text`.

**Media** – `--embed-aspect-ratio`.

## Worked examples

```css
/* Uppercase, tight, heavy titles */
:root { --case-h1: uppercase; --letter-spacing-h1: -0.02em; --font-weight-h1: 800; --scale-factor-h1: 1.15; }

/* Bigger body text on slides, narrower measure */
:root { --p-base-size: 1.15; --single-column-max-width: 34em; }

/* Center everything on cover and section */
:root { --text-horizontal-align-layout-cover: center; --text-vertical-align-layout-cover: center;
        --text-horizontal-align-layout-section: center; }

/* Brand chart palette */
section { --graph-data-0: #0a84ff; --graph-data-1: #ff9f0a; --graph-data-2: #30d158; }
```
