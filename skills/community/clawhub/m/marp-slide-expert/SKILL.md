---
name: marp-slide-expert
description: Convert or create Marp slide decks from Markdown sources. Use when working with .marp.md / .md files meant for marp CLI rendering, designing page-level slide layouts (cover, divider, text, tables, multi-column / split layouts), drawing infographics and relation diagrams as inline SVG (staircase, arrow chain, 2x2 matrix, value tree, sankey, funnel, swimlanes, bento grid, icon-rail, card-row, wave-timeline, argument map, pie / radar / balance-wheel charts), splitting long content into slides (15-line per-slide cap), writing speaker notes as invisible HTML comments, preparing image assets, or troubleshooting marp syntax errors and content overflow. Applies to marp / marpit slide format.
---

# Marp Expert

Convert content into Marp slide decks that render cleanly via `marp --pdf --allow-local-files`. The constraints below are non-obvious pitfalls confirmed against [marpit.marp.app](https://marpit.marp.app/) — read once, apply always.

## Hard rules

These break rendering silently if violated:

- **Only `![bg ...](...)` for images.** Marp does NOT support `![w:60% center]`, `![width:200px]`, or any inline image sizing. If you need an image, it must be a background.
- **Wrap paths containing spaces in `<...>`**: `![bg](<path with spaces.png>)`. Without the brackets, marp silently treats the space as URL terminator.
- **Inline SVG requires `--html`.** Marp escapes HTML by default, so a `<svg>` diagram renders as a page of visible source code. Any deck containing inline SVG must be rendered with `marp deck.marp.md --html --pdf --allow-local-files`. See "Smart drawing" below.
- **Slides overflow when content is too dense.** Marp has no auto-shrink. Split proactively.
- **Max 15 visible lines per slide.** Count every rendered line — paragraph lines, bullet items, table rows (including the header row), code block lines, quote/callout-box lines. Over 15 and the bottom of the slide gets cut off in the PDF. See "15-line hard cap" below.

## 先分清：页级版式 vs 图级版式

这是两种完全不同的东西，**用错工具是最常见的返工原因**：

| | 页级版式（slide layout） | 图级版式（diagram） |
|---|---|---|
| **排的是** | 一页的**内容块**——文字、表格、图 | 一张图**内部**的节点和连线 |
| **手段** | CSS grid + `<div>` / marp 语法 | 内联 `<svg>` |
| **要不要 `--html`** | **不需要** | **需要** |
| **文件** | [references/layout-patterns.md](references/layout-patterns.md) | [references/infographics-svg/](references/infographics-svg/INDEX.md) |
| **例子** | 三栏对比、双栏各带表、上下分区 | 阶梯、箭头串、2×2、桑基、泳道、便当格 |

**判断：这一页要表达「内容之间的结构关系」吗？**
- 是（要看谁依赖谁、怎么演进、卡在哪）→ **画图**
- 否（只是内容多，并排放不下）→ **排版式**

## Layout patterns (cheat sheet)

| Scenario | Pattern |
|---|---|
| Cover | `<!-- _class: cover -->` + `# Title` + `## Subtitle` |
| Major section break | `<!-- _class: divider -->` + `# Section Name` |
| Text only / text + table | Plain markdown, default content slide |
| **Two columns** | `<div class="cols cols-2">` — 并列论点、两套方案 |
| **Three columns** | `<div class="cols cols-3">` — 演进/挑战/对策，**每栏 ≤ 5 行** |
| **Main + side** | `<div class="cols cols-main">` (2:1) — 左要点右佐证，最常用 |
| **Top / bottom split** | `<div class="split-h">` — 上结论下证据 |
| Single image + text | `![bg left contain opacity:.9](<path>)` — image left, text right |
| Multi-image, no text | `![bg](<a>)` `![bg](<b>)` — horizontal row by default |
| Text + 2 images | `![bg right vertical](<a>)` + `![bg](<b>)` — img(a) right column, img(b) fills left, content overlays left |
| Portrait multi-image | Add `vertical` to each: `![bg vertical](<a>)` etc. |
| Infographic / 关系图 | `<!-- _class: diagram -->` + inline `<svg>` — see below |

**15-line cap is per slide, not per column** — a 3-column slide gives each column only ~5 lines. Splitting into three pages usually reads better than cramming one.

For full syntax and orientation logic, read [references/image-syntax.md](references/image-syntax.md). For column layout details and the CSS block, read [references/layout-patterns.md](references/layout-patterns.md).

## Infographics & relation diagrams — 内联 SVG

Infographics and relation diagrams (staircase, arrow chain, 2×2 matrix, value tree, sankey, funnel, swimlanes, bento grid, argument map, pie, radar, balance wheel) are drawn as **inline SVG written directly in the `.md`** — not as images. A PNG has to be redrawn to change one number; SVG travels with the file, keeps its text searchable, stays vector in the PDF, and recolours with one hex value.

```bash
# 含内联 SVG 的 deck 必须带 --html，否则 SVG 被转义成一整页源码
marp deck.marp.md --html --pdf --allow-local-files
```

**The diagram module is a four-layer pipeline.** Work through them in order — each answers exactly one question:

| Layer | Question | File |
|---|---|---|
| ① structures 选题 | 这份内容能画哪几张图？ | [structures.md](references/infographics-svg/structures.md) |
| ② skeletons 体裁 | 用什么图形承载这个关系？ | [skeletons/INDEX.md](references/infographics-svg/skeletons/INDEX.md) |
| ③ metaphors 语气 | 在同一副骨架上换什么叙事外壳？ | [metaphors.md](references/infographics-svg/metaphors.md) |
| ④ styles 配色 | 什么颜色、什么字阶？ | [styles/INDEX.md](references/infographics-svg/styles/INDEX.md) |
| craft 笔法 | 画布多大？线怎么连？字怎么排？ | [craft/](references/infographics-svg/craft/canvas.md) |

**Pick the skeleton in two steps: relationship first, then metaphors.** Relationship families (hierarchy / sequence / cycle / comparison / matrix / framework / strategy / mapping / growth / composition / profile / balance) route to a skeleton. The narrative layer — staircase, pyramid, flywheel, iceberg, funnel, bridge, mountain — swaps the *shell* on that same skeleton without changing the routing. That separation is what lets the skeleton library grow without the metaphors table ever changing.

| Relationship | Answers | Skeleton |
|---|---|---|
| Sequence | what happens first, then next | Arrow chain |
| Hierarchy (depth 3+) | where value comes from | Value tree |
| Matrix (2 independent dimensions) | who gets the money, who doesn't | 2×2 quadrant |
| Growth / evolution | where we are, what's next | Staircase |
| Flow with magnitude | where does the volume go | Sankey |
| Parallel tracks | who did what, when | Swimlanes |
| Argument | what backs this claim | Toulmin map |
| Composition | part-to-whole shares, 1–3 pies | Pie / donut |
| Profile | multi-dimension score shape | Radar |
| Balance | one object, current vs target | Balance wheel |

**Non-negotiables when writing SVG into markdown:**

- **No blank lines inside the SVG block** — markdown cuts the HTML block at the first blank line and the diagram vanishes without an error.
- **Unique `marker` / `clipPath` ids per diagram** (`a1`, `a2`, …) — in a merged single-HTML export every SVG shares one DOM, so duplicate ids make all arrowheads resolve to the first definition.
- **No `---` inside the SVG** — it is still parsed as a page break.
- **Font sizes come from CSS classes, never a `font-size` attribute** — the deck's `style:` block already defines `svg .t / .tb / .sm / .qt / .lbl` (see [references/style-bootstrap.md](references/style-bootstrap.md)), so one edit re-sizes every diagram.
- **Add `<!-- _class: diagram -->`** when diagram content reaches the bottom of the viewBox (axis titles, legends, footnotes) — the CSS hides the footer on those slides so they don't collide.
- **Keep nodes ≤ 7 per diagram.** Past that, split the page or fall back to a table.
- **One colour family + one accent.** Three or more hues turn muddy under projection.
- **Geometry must not contradict the data.** A funnel drawn layer-by-layer with drifting slopes reads as a stack of plates, and casual band widths imply proportions the numbers don't support. Draw one generatrix through all bands, add rim + spout, and label the diagram "band width is schematic" — exact proportions belong in a sankey. See [flow-cycle](references/infographics-svg/skeletons/flow-cycle.md).

**Before shipping, run both gates** — the first catches what is *certainly* wrong, the second catches what merely *looks* wrong:

```bash
node scripts/svg-lint.mjs deck.marp.md                 # 6 deterministic checks
marp deck.marp.md --html --images png -o check          # render and actually look
```

Trust the **rendered PNG**, never the SVG source.

Full templates with coordinate formulas, connector-semantics table, visual-hierarchy rules, and QA checklist: **[references/infographics-svg/](references/infographics-svg/INDEX.md)**. Every skeleton, metaphors and style, one per slide: **[examples/infographic-gallery.marp.md](examples/infographic-gallery.marp.md)**.

## Content density — the 15-line hard cap

**Every slide renders at most 15 lines of content. Count them before shipping. HTML comments are excluded.**

Count each of these as one line:

| Element | How to count |
|---|---|
| Paragraph | One visual line as wrapped, ≈ 38 CJK chars or ≈ 75 Latin chars per line at default font. A 4-sentence paragraph ≈ 3 lines. |
| Bullet / numbered item | 1 line per item, plus 1 more if it wraps |
| Table | 1 line per row, **including the header row**. A 4-column × 4-row table = 5 lines. |
| Code block | 1 line per code line — no exceptions, no partial credit |
| Quote / tip / warn box (`>`) | Every wrapped line inside the box |
| Heading | Count it — `##` costs 1 line before the body starts |
| Speaker note / any HTML comment `<!-- -->` | **0 lines** — comments never render, so they never count |

A slide is a **budget of 15 total**, not 15 per element. `##` title (1) + table 6 rows (6) + 2 bullets (2) + closing paragraph (2 lines) = 11 → fine. Add a 5-line code block and you're at 16 → split.

**Speaker notes and other HTML comments do not count** — they never render. So an overflowing slide can often be fixed by moving detail into a note rather than cutting it.

Corollary limits that follow from the 15-line cap:

- **Title + 1 image** → ≤ 8 body lines. Images eat vertical space even though they don't count as lines.
- **Text only** → up to 15 lines, but aim for 10–12; long lines are hard to read from the back row.
- **Code blocks** → ≤ 10 lines per slide. More than that, split at logical boundaries (function def, between classes) or move to an appendix slide.
- **Tables** → ≤ 8 rows incl. header, ≤ 4 columns. Over 4 columns, the table overflows horizontally instead of vertically.
- **Bulleted lists** → ≤ 10 items. Past that, split around a logical midpoint or convert to a table.
- **Never split a bullet or a table row** across slides — a bullet cut in half, or a table with a dangling header, reads as broken.

Counting rule of thumb: **CJK ≈ 1 line per 38 characters; Latin ≈ 1 line per 75 characters.** A 600-character Chinese paragraph is already ~16 lines on its own.

For splitting heuristics, read [references/slide-density.md](references/slide-density.md).

## Image asset prep

When converting external image URLs (HTML course content, scraped diagrams):

1. Download all unique images to a local `assests/` (or `assets/`) directory.
2. Compress each to ≤ 100 KB using Pillow + sips. Convert complex diagrams with many colors to JPEG q=82; keep simple line art as PNG with `optimize=True`.
3. **Rename with a chapter prefix** so paths are stable across slides: `L1_1.1-01_section-overview.png` instead of raw URL slugs.
4. Build a URL → local-name mapping before generating slides so replacements are deterministic.

For full prep workflow, read [references/asset-prep.md](references/asset-prep.md).

## CSS bootstrap

**All UPerform / openclaw marp decks share one palette** (red + deep navy-black theme). The complete style block lives in [references/style-bootstrap.md](references/style-bootstrap.md). The palette is calibrated against `openclaw_lesson01.md` and the `fde_lesson*.marp.md` family.

It includes:
- CJK font stack (PingFang SC / Microsoft YaHei / Noto Sans CJK SC)
- Cover gradient (deep navy-black `#1a1a2e` → red `#c0392b`, white text)
- Divider slides (deep blue-grey `#2c3e50` background + red `#e74c3c` heading)
- Tables (red `#c0392b` header + `#f5f5f5` alternating rows) — plus the `display: table !important` fix, without which marp's default theme makes every table half-width
- H1/H2/H3 color scale (red / deep blue-grey / bright red)
- Code blocks (dark `#1a1a2e` background + green `#2ecc71` text)
- SVG helpers: `svg` sizing, CJK font for `svg text`, the `.t / .tb / .sm / .qt / .lbl` type scale, and `section.cover/divider/diagram footer { display: none }`
- Page-level column layouts: `.cols-2` / `.cols-3` / `.cols-main` / `.split-h` grids, plus in-column `h3`/`p`/`ul`/`table` scaling

Copy the `style: |-` block verbatim into a new deck's frontmatter.


## Speaker notes (HTML comments — invisible in the PDF)

Different audiences need different things. **Anything only the speaker needs — background, transitions, backup numbers, Q&A prep — goes in an HTML comment `<!-- ... -->`:**

```markdown
## Three deployment modes

- Public cloud: fastest to launch
- On-premise: compliance first
- Hybrid: best cost

<!--
Speaker notes:
- "Hybrid" is the newest option; long-time customers ask about it most.
- Case: a bank went on-premise, 8M contract.
- If asked about pricing, jump to the table on the next slide.
-->
```

Rules:

- Notes are **never rendered**: absent from the generated HTML, PDF, and PPTX. They exist only in the `.md` source, which is where the speaker reads them.
- Notes **do not count toward the 15-line cap** — they cost zero lines and can be as long as needed.
- One note block per slide, placed after that slide's content and before the `---` separator.
- **Never write `---` inside a note** — it is still parsed as a page break and will split the slide.
- Also useful for draft markers that must not ship: `<!-- TODO: add real pricing data -->`.
- Marpit directives (`<!-- _class: ... -->`, `<!-- _paginate: -->`) also use `<!-- -->` but start with `_` and stay active. Speaker notes must not start with `_`.
- **First fix for an over-15-line slide:** ask "is this for the audience or for me?" If it's for you, move the whole thing into a comment — it costs no lines. Only content the audience genuinely needs to read is worth a new slide.

## Workflow

1. Read source markdown; identify cover, dividers (H1/H2), and content sections (H3+).
2. Prep image assets (see asset-prep above).
3. Generate slides with these defaults:
   - One `## section` → divider slide.
   - One `### topic` → content slide titled `## Topic`.
   - Split so **no slide exceeds 15 rendered lines** (see the count table above). When a section is long, decide per-paragraph: audience-facing content splits onto a new slide; speaker-only context moves into a `<!-- -->` note.
   - Never split mid-sentence, mid-bullet, or mid-table-row. Cut at paragraph boundaries.
   - Image placement per the cheat sheet above.
   - For column layouts, use the `cols-*` / `split-h` classes in [references/layout-patterns.md](references/layout-patterns.md) — remember the 15-line cap is per slide, so a 3-column slide gets ~5 lines per column.
   - For relationship diagrams, route by relationship type → pick the skeleton in [references/infographics-svg/skeletons/INDEX.md](references/infographics-svg/skeletons/INDEX.md) → optionally swap the shell via [metaphors.md](references/infographics-svg/metaphors.md) → mark the slide `<!-- _class: diagram -->`.
4. Count lines on every generated slide before rendering. Any slide > 15 → fix now.
5. Lint and render: `node scripts/svg-lint.mjs deck.marp.md`, then `marp deck.marp.md --pdf --allow-local-files` (add `--html` if the deck contains inline SVG) and visually check first 5 pages plus a sample from middle/end. For a deck with diagrams, render **every** page to PNG (`--images png`) — SVG geometry is not verifiable from the source.
6. Iterate on overflow / awkward layout.

## Quick troubleshooting

| Symptom | Likely cause |
|---|---|
| Image shows as markdown text instead of background | Path has unescaped spaces — wrap in `<...>` |
| Two images stack weirdly | Missing `vertical` keyword for portrait images |
| Content cut off at bottom | Slide has > 15 rendered lines — split, or move speaker-only detail into a `<!-- -->` note |
| Table rows truncated horizontally | Table too wide — keep ≤ 4 columns or shrink font in CSS |
| Table renders at half width | marp's default theme sets `table { display: block }` — the block box stretches but the inner anonymous table shrink-wraps. Fix with `display: table !important` (already in style-bootstrap) |
| Whole slide shows SVG source code | Missing `--html` at render time (columns do **not** need it — only inline SVG) |
| Table inside a column is half width | The `display: table !important` fix was dropped from the `style:` block |
| **All styling gone** — default theme, colours lost, columns collapsed | An HTML comment `<!-- -->` was placed **inside the YAML frontmatter**, breaking the YAML parse so the whole `style:` block is silently dropped. Comments go **after** the closing `---` |
| Table inside a column overflows sideways | Column count too high for the narrower column — cut columns or add `font-size: 0.66em` |
| Column bottoms look ragged | Missing `align-items: start` on the grid |
| 3-column slide is an unreadable wall of text | The 15-line cap is per slide; a 3-column slide gets ~5 lines per column — split into separate pages |
| SVG fine in Obsidian reading mode but exports as source in PDF | Obsidian's built-in exporter flattens inline HTML/SVG — export with Marp CLI `--html --pdf`, or use the Enhanced PDF Export plugin. The deck is not at fault; see [references/infographics-svg/craft/marp-compat.md](references/infographics-svg/craft/marp-compat.md) §4 |
| Obsidian's Marp plugin exports SVG as source | Its export command omits `--html`; patch `main.js` (2 sites in the `il()` function) — see [references/infographics-svg/craft/marp-compat.md](references/infographics-svg/craft/marp-compat.md) §4.1 |
| SVG diagram disappeared entirely | A blank line inside the SVG block split the HTML block — remove it |
| One slide split into two | A `---` inside the SVG or inside an HTML comment |
| All diagrams' arrowheads look identical | Duplicate `marker` id across SVGs in one merged HTML export — suffix per diagram |
| White text invisible on an arrow shape | Drawn as a hollow chevron — use a 5-point path (rectangle + right tip) and centre text on the rectangle |
| Chinese label overflows its node | SVG `<text>` does not wrap — shorten the label or split it across `<tspan>` lines |
| Funnel doesn't look like a funnel | Bands were drawn layer-by-layer with drifting slopes, or the rim/spout is missing — use the single-generatrix template (s=0.9, no gaps) in [flow-cycle](references/infographics-svg/skeletons/flow-cycle.md) |
| SVG text ignores the deck's CSS classes | A `font-size` attribute was hardcoded, or the class was declared in an SVG-internal `<style>` instead of the frontmatter `style:` block |
| Axis title / legend overlaps the footer | Add `<!-- _class: diagram -->` to that slide |
| Slide split awkwardly | Cut mid-bullet or mid-table-row — re-split at paragraph boundaries |
| Speaker note text visible in the PDF | It's not inside an HTML comment — wrap it in `<!-- ... -->` |
| One slide became two / empty slide appeared | A `---` inside an HTML comment is still a page break — remove it |
| Cover slide has wrong background | Missing `<!-- _class: cover -->` directive |
| PDF render fails silently on images | Path doesn't resolve from .md file location — invoke marp from a directory where the relative path is valid |

For deeper marpit syntax reference, consult [https://marpit.marp.app/](https://marpit.marp.app/) — particularly the image-syntax and slide-layouts pages.
