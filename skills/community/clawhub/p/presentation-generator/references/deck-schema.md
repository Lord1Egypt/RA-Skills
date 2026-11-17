# Deck JSON schema (quick reference)

A deck is `{ "type": "deck", "meta": {...}, "slides": [...] }`. Full JSON Schema:
`@presentation-md/core/deck-schema` (`deck.schema.json`).

**Craft knobs Studio exposes** (set them in JSON so HTML + PPTX stay aligned):
`two-column.ratio` / `reverse`, `comparison.emphasis`, `feature-grid` `columns: "bento"`,
`ranked-list`, `logo-wall`, `streak-grid`, `metric-ring`, closing `actions[]`, per-slide `tone`,
`code.filename` / `language`, and optional `notes` on any slide (Studio present-mode drawer + PPTX notes pane; not drawn on the HTML slide face).

**Authoring craft (required when the layout supports it):**
- `comparison`: always set `emphasis` to `"left"` or `"right"`.
- `two-column`: prefer a non-`1-1` `ratio` unless weight is truly equal; use `reverse` when media should lead.
- `feature-grid` with 5 cards: set `columns: "bento"`.
- Include at least one `image-hero` when the brief implies a visual product, place, or atmosphere.
- Add brief `notes` on 2–4 key slides for the presenter.

## meta
| field | notes |
|-------|-------|
| `title` | document title (browser tab) |
| `company` | brand/project name |
| `description` | meta description |
| `theme` | theme name (default: `default-tech`) |

## slide layouts

Every slide needs `layout`. Fields are per-layout; unused fields are ignored.

### title / closing
`{ "layout": "title", "eyebrow"?, "heading", "lead"? }`
`closing` takes `actions[]` (solid + outline share pills) or legacy `cta: { "label", "href" }` (`cta` ≡ `actions[0]`).

### section
`{ "layout": "section", "number"?, "heading", "lead"? }`

### two-column
`{ "layout": "two-column", "eyebrow"?, "heading", "body"?, "image"?, "imageAlt"?,
   "aside"?, "ratio"?: "1-1"|"2-1"|"1-2"|"3-2"|"2-3", "reverse"? }`
Use `aside` for a pull-quote panel when there is no image. `ratio` / `reverse` unlock asymmetric craft.

### image-hero
`{ "layout": "image-hero", "eyebrow"?, "heading", "lead"?, "image", "imageAlt"? }`

### comparison
`{ "layout": "comparison", "eyebrow"?, "heading"?, "leftLabel"?, "left", "rightLabel"?, "right",
   "emphasis"?: "left"|"right" }`

### feature-grid
`{ "layout": "feature-grid", "eyebrow"?, "heading"?, "columns": 2|3|4|"bento",
   "cards": [ { "icon"?: "fa-solid fa-bolt", "title", "body"? } ] }`
`"bento"` = asymmetric hero card + four supporting cards.

### quote
`{ "layout": "quote", "quote", "by"? }`

### stat-row
`{ "layout": "stat-row", "eyebrow"?, "heading"?, "lead"?, "variant"?: "default"|"hero",
   "stats": [ { "value", "label" } ] }`
`"hero"` = mega-number wrap beat (first stat dominates; rest become secondary chips).

### ranked-list
`{ "layout": "ranked-list", "eyebrow"?, "heading"?, "lead"?,
   "items": [ { "rank"?, "label", "value"?, "widthPct"? } ] }`
Ordered progress / ranking bars — prefer this over `custom-html` for Pulse-style stacks.
PPTX maps natively (no crude text blob).

### logo-wall
`{ "layout": "logo-wall", "eyebrow"?, "heading"?, "lead"?, "columns"?: 2|3|4|5|6,
   "cards": [ { "title", "image"?, "imageAlt"?, "icon"?, "body"? } ] }`
Customer / partner / team marks. Prefer `image` (URL or data URI); falls back to icon or title text.
PPTX embeds images when prefetchable.

### streak-grid
`{ "layout": "streak-grid", "eyebrow"?, "heading"?, "lead"?, "filled", "total"?, "cols"?, "body"? }`
Day-streak / habit cells (Pulse gallery parity). Cap `total` at 120. Prefer over `custom-html` squares.

### metric-ring
`{ "layout": "metric-ring", "eyebrow"?, "heading"?, "value", "label"?, "pct"?, "lead"?, "body"? }`
Circular KPI badge. Omit/`pct: 100` = full ring; `1–99` = arc progress. Prefer over plain stats for percentile flex.

### closing
`{ "layout": "closing", "eyebrow"?, "heading", "lead"?,
   "actions"?: [ { "label", "href"?, "style"?: "solid"|"outline"|"ghost", "icon"? } ],
   "cta"?: { "label"?, "href"? } }`
Prefer `actions[]` for dual share pills (solid + outline). `cta` is alias for `actions[0]`.
Icon every pill (`icon`) so HTML + PPTX stays scannable — FA brands for social, rocket/download/calendar for CTAs.

### timeline
`{ "layout": "timeline", "eyebrow"?, "heading"?, "orientation"?: "horizontal"|"vertical",
   "steps": [ { "title", "body"? } ] }`
Default rail is horizontal (matches HTML). Set `orientation: "vertical"` for a process stack.

### data-table
`{ "layout": "data-table", "eyebrow"?, "heading"?, "columns": ["A","B"],
   "rows": [ ["a1","b1"], ["a2","b2"] ] }`

### code
`{ "layout": "code", "eyebrow"?, "heading"?, "lead"?, "code", "language"?, "filename"? }`
Plain-text snippet in window chrome. HTML is escaped on render — no markup inside `code`.

### chart
`{ "layout": "chart", "eyebrow"?, "heading"?, "lead"?,
   "chartType"?: "bar"|"horizontal-bar"|"line"|"area"|"pie"|"donut",
   "categories"?: string[],
   "series": [ { "name"?, "values": number[] } ],
   "showLegend"?: boolean, "showValues"?: boolean, "stacked"?: boolean }`
Theme-colored SVG in HTML; native editable charts in PPTX. Prefer `bar`/`line` for trends,
`pie`/`donut` for composition (single series). Set `showValues` sparingly — labels are craft, not default noise.

### custom-html
`{ "layout": "custom-html", "eyebrow"?, "heading"?, "lead"?, "html" }`
Schema-preserving escape hatch for one-off art (frontend-slides energy without abandoning Deck JSON).
Scripts, event handlers, and dangerous URLs are stripped on render. Prefer `ranked-list` / `streak-grid` / `metric-ring` /
`stat-row` hero / `chart` when the art fits those shapes. PPTX approximates bars/panels/text —
keep HTML export when the art matters. Copy-paste craft: `references/custom-html-recipes.md`
(split panels, big-number+rule, poster stamps, typographic explosion).

### tone (any slide)
Optional `tone`: `"default"|"lime"|"magenta"|"cyan"|"orange"|"violet"` — per-slide hue beat for
`kinetic-wrapped` / Pulse multi-hue craft. Omit to use surface auto-cycle accents.

## Example
```json
{
  "type": "deck",
  "meta": { "title": "Acme", "company": "Acme", "theme": "corporate" },
  "slides": [
    { "layout": "title", "eyebrow": "Acme", "heading": "We make X faster.", "lead": "One line." },
    { "layout": "feature-grid", "heading": "Why Acme", "columns": 3,
      "cards": [
        { "icon": "fa-solid fa-bolt", "title": "Fast", "body": "Sub-second." },
        { "icon": "fa-solid fa-shield", "title": "Trusted", "body": "SOC2." },
        { "icon": "fa-solid fa-chart-line", "title": "Proven", "body": "200 teams." }
      ] },
    { "layout": "closing", "heading": "Let's talk.", "cta": { "label": "hello@acme.com", "href": "#" } }
  ]
}
```
