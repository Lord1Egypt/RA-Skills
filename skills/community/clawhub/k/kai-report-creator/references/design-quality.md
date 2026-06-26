# Design Quality Baseline

This file defines the design quality rules for every generated report. Load alongside `rendering-rules.md` during `--generate` mode. These rules exist to prevent AI-slop patterns and enforce visual discipline.

## 1. The 90/8/2 Color Law

Every report must follow this color allocation:

| Share | Role | Variable | Usage |
|-------|------|----------|-------|
| **90%** | Neutral surface | `--bg`, `--surface`, `--text` | Background, body text, cards |
| **8%** | Structural color | `--primary` | Section borders, one accent block, h2 underlines |
| **2%** | Bullet point | `--accent-pop` (default = `--primary` at full opacity) | At most 1-2 precise hits: a single KPI value, one callout border, one chart series |

**Violations to avoid:**
- `var(--primary)` used on heading text, KPI values, chart bars, callout borders, TOC links, AND badges simultaneously → this is a primary-color flood
- Every KPI card a different accent color → accent system should feel like seasoning, not confetti
- Using more than 2 accent colors per page (chart series excluded)

## 2. Typography: 10:1 Scale Ratio

The largest text element on any page must be ≥ 10× the smallest readable element.

| Element | Min size | Max size |
|---------|----------|---------|
| Fine print, badges, meta | 11px | — |
| Body text | 15px | — |
| h3 | 17px | — |
| h2 | 20px | — |
| Report title | 2.6rem+ | — |

**Apply to report title:** Minimum `font-size: 2.8rem`. For strong content topics, push to `3.5–4rem` with `line-height: 1.05` and `letter-spacing: -0.03em`. The title should feel like an anchor, not a label.

**Apply to section headings:** `h2` gets a subtle left border or underline using `--primary` at 8% allocation — not a background color.

**Letter-spacing upper limit:** Body text and prose must never exceed `letter-spacing: 0.05em`. Wide letter-spacing on body text (>0.05em) breaks word shape recognition and slows reading. Negative letter-spacing is acceptable for titles (`-0.03em`) and headings (`-0.02em`).

## 3. KPI Grid Column Rules

Do not default all KPI grids to 3 columns. Match columns to KPI count for better proportion:

| KPI count | Grid columns | CSS |
|-----------|-------------|-----|
| 1–2 | 2 columns | `grid-template-columns: repeat(2, 1fr)` |
| 3 | 3 columns | `grid-template-columns: repeat(3, 1fr)` |
| 4 | 2×2 | `grid-template-columns: repeat(2, 1fr)` |
| 5–6 | 3 columns (last row 2) | `grid-template-columns: repeat(3, 1fr)` |
| 7+ | 3 columns with dividers between groups | `grid-template-columns: repeat(3, 1fr)` + `gap: 0.5rem 1rem` |

**Non-equal widths:** When one KPI is the "hero" metric, use `grid-template-columns: 2fr 1fr 1fr` or `1.5fr 1fr` to create visual hierarchy.

## 4. Forbidden Patterns (Anti-AI-Slop)

These patterns make a report look instantly AI-generated. Do not produce them:

| ❌ Forbidden | ✅ Instead |
|---|---|
| Every section starts with a one-sentence definition: "X is a..." | Start sections in the middle of the idea, with data or a claim |
| 3-equal-column KPI grid when you have 4 KPIs | Use 2×2 grid |
| All h2 headings are 3–4 words ("Overview", "Key Findings", "Next Steps") | Allow longer, specific headings that reflect actual content |
| `border-radius: 12px` on every card and button | Mix radii: sharp (2px) for data elements, soft (8px) for prose cards |
| Callout boxes for every key insight | Use `.highlight-sentence` for inline highlights; reserve callout for truly exceptional notes |
| Same font size for every paragraph | Vary prose density: lead paragraphs slightly larger (16px), supporting detail smaller (14px) |
| Symmetrical two-column layouts everywhere | Use `2fr 1fr` or `3fr 1fr` — asymmetry implies hierarchy |
| Inter as body font | Use system-ui / -apple-system stack (already in themes) |
| `:::kpi` block with placeholder values (`[INSERT VALUE]` / `[数据待填写]`) in any report | Use `:::callout`, `:::timeline`, or `:::table` as the visual anchor instead |
| `:::kpi` value is status-only or contains a full sentence/descriptive paragraph (e.g. "通过" or "支持CSV/Excel等表格文件的统计汇总、趋势分析、数据可视化") | KPI value = short real number only. Status goes in badges; explanations go in prose, callout, or table cell |
| `:::chart` with all-placeholder data in a text-heavy (narrative/mixed) section | Use `:::diagram` (flowchart/mindmap) or a `highlight-sentence` paragraph |
| Nested cards (card inside a card) | Flatten hierarchy — use indentation, sub-lists, or adjacent blocks instead |
| Default text alignment centered everywhere | Left-align body text; center only the title and hero metrics |
| Glassmorphism (blur/backdrop-filter) as decoration | Solid or subtly tinted backgrounds; blur signals no information |
| `text-align: justify` on body text | Left-align — justified text creates rivers of whitespace |
| Using monospace fonts to signal "technical/developer" vibes | System sans-serif for all prose; reserve monospace for actual code blocks only |
| Icon tile (small rounded-square icon container) stacked above section heading | Inline icon in heading or skip entirely — decorative icon squares add no information |
| `text-transform: uppercase` on body text (all-caps paragraphs) | Normal case for body; all-caps only for small labels or chips |

## 5. Content-Tone Color Calibration

When generating `theme_overrides` in `--plan` mode, suggest a tone-appropriate primary color based on content keywords:

| Content tone | Trigger keywords | Suggested `primary_color` override | Feel |
|---|---|---|---|
| **Contemplative / Research** | 认知、思维、本质、意义、哲学、研究、白皮书、学术 / philosophy, cognition, research, academic | `#7C6853` (warm brown) | Grounded, editorial |
| **Technical / Engineering** | 架构、系统、API、性能、部署、代码、工程 / architecture, system, API, performance, engineering | `#3D5A80` (navy blue) | Precise, authoritative |
| **Business / Data** | 销售、营收、KPI、增长、季报、业绩 / sales, revenue, KPI, growth, quarterly | `#1F6F50` (pine green) | Restrained, commercial, premium |
| **Narrative / Annual** | 故事、增长、复盘、年度 / story, growth, retrospective, annual | `#B45309` (amber) | Warm, momentum |
| **Editorial / News** | 新闻、行业、趋势、观察 / news, industry, trend | `#1C1C1E` (near-black) | Authoritative, print |

No override needed if the default theme color already matches the tone.

## 6. Semantic Highlight Extraction

When rendering prose sections, identify **key-insight sentences** and apply `.highlight-sentence`:

A sentence qualifies if it meets ALL of:
- Stands alone as its own paragraph
- ≤ 45 characters (Chinese) or ≤ 80 characters (English)
- Declarative/conclusive tone (states a fact, principle, or finding)
- Not already inside a `:::callout` or `:::kpi` block

```html
<p class="highlight-sentence">真正的增长来自产品本身，而非渠道。</p>
```

CSS for `.highlight-sentence` (add to shared.css section in html-shell-template.md):
```css
.highlight-sentence {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--primary);
  border-left: 3px solid var(--primary);
  padding-left: 1rem;
  margin: 1.5rem 0;
  line-height: 1.5;
}
```

### Narrative Cadence Blocks

For `narrative` and `mixed` reports, do not stop at "shorter paragraphs". The better rhythm is:

`claim -> explanation -> scan anchor`

Use these render-time prose upgrades when the section supports them:

- `lead-block` — for a decisive opening sentence that frames the section before detail.
- `section-quote` — for a short judgment or implication that should read like a pull-quote.
- `action-grid` — for 2-5 concrete moves, contrasts, or recommendations that scan better as cards than as one long list.

These are **prose/HTML patterns, not IR tags**. Narrative cadence blocks are optional upgrades, not a quota. The renderer should promote qualifying prose into these blocks instead of leaving every narrative section as paragraph + list.

- Never use them just to break up a page visually.
- Do not stack multiple cadence blocks in one section unless the source clearly contains multiple distinct beats.
- If uncertain, keep plain prose plus one stronger scan anchor instead of forcing a cadence block.

```html
<div class="lead-block">先抓主线：这部分讨论的不是聊天入口，而是委托边界。</div>
<div class="section-quote">真正决定信任的，不是入口，而是编排层。</div>
<div class="action-grid">
  <div class="action-card"><strong>先做</strong><p>先把意图和边界收清楚。</p></div>
  <div class="action-card"><strong>再做</strong><p>再把行动回执和恢复路径补上。</p></div>
</div>
```

### Summary Card Hierarchy

Summary cards should read like posters, not metadata panels.

- Prefer `poster_title` + `poster_subtitle` only when the report's core judgment is stronger than the document title.
- The poster title should dominate the card visually.
- After fixing wrap quality, do not leave the poster title undersized; it should still feel like the dominant visual mass on the left panel.
- Keep subtitle below the poster title, not merged into one dense headline.
- On the left panel, keep only the title hierarchy and one short closing sentence near the bottom.
- Leave visible breathing room around the title; do not let the left panel turn into a paragraph block.
- Do not artificially squeeze the subtitle or closing sentence into a narrow column that wastes available width.
- Do not duplicate audience, author/date byline, or explanatory filler inside the summary card.
- Remove chips, bottom notes, and metadata filler if they weaken the poster read.

## 7. Pre-Output Self-Check

Before writing the final HTML, answer each question. Fix any "no":

- [ ] Does the report title feel like an anchor, or just a label? (target: anchor — at least 2.8rem)
- [ ] Is `var(--primary)` used in more than 4 distinct element types? If yes → reduce
- [ ] Are any KPI grids 3 columns when the count is 4 or 7+? If yes → fix column rule
- [ ] Are there 3+ consecutive all-prose sections with no component? If yes → insert visual anchor
- [ ] Do all section headings feel like AI-generated template phrases? If yes → make them content-specific
- [ ] Is every card's `border-radius` identical? If yes → vary radii between data elements and prose cards
- [ ] Does any `:::kpi` or `:::chart` block contain placeholder values (`[INSERT VALUE]` / `[数据待填写]`)? If yes → replace with `:::callout`, `:::timeline`, `:::table`, or `:::diagram`
- [ ] Does any `.kpi-value` lack a real number, or contain a sentence/paragraph longer than 8 Chinese chars / 3 English words? If yes → move status/explanation to badges, prose, callout, or table; keep KPI value quantitative
- [ ] Does the report use `.badge` elements in at least 2 locations (section headers, KPI cards, table cells, timeline items)? If no → add badges at appropriate locations
- [ ] **If you told someone "an AI wrote this", would they immediately believe it?** If yes → find the most generic-looking part and redesign it
- [ ] Is any prose line wider than ~75 characters (Chinese: ~50 chars)? If yes → constrain with `max-width` or `max-inline-size` in CSS
- [ ] Is any `text-align: justify` applied to body text? If yes → change to left-align
- [ ] Is any background `#000000` or `#000`? If yes → use `#111` or `#181818` instead — pure black is harsh and unnatural
- [ ] Is any gray text (`#888`, `#999`, `var(--text-muted)`) placed on a colored background? If yes → darken text or lighten background for WCAG AA contrast
- [ ] Is any body text `letter-spacing` greater than `0.05em`? If yes → reduce or remove
- [ ] Are there nested cards (a `.kpi-card`, `.callout`, or `.table-wrapper` inside another card)? If yes → flatten hierarchy
- [ ] Is any card or container padding less than `0.75rem` (data elements) or `0.9rem` (prose)? If yes → increase — cramped padding makes reports feel cheap

## 8. L2 HTML Shell Structure (MANDATORY)

These checks verify the HTML shell was built according to `references/html-shell-template.md`. **This is NOT about content quality — it's about the container itself.**

**Root cause:** BUG-001 (2026-04-13). AI skipped template structure, generated obsolete TOC implementation and lost summary card + export buttons. Prevention: check the shell before writing.

### 8.1 Required Elements

Every generated report HTML **MUST** contain these elements. If any are missing, reconstruct from `html-shell-template.md`:

| Element | Required ID/class | Purpose |
|---------|------------------|---------|
| TOC toggle button | `id="toc-toggle-btn"` + class `toc-toggle` | Visible `☰` button, top-left corner |
| TOC sidebar nav | `id="toc-sidebar"` + class `toc-sidebar` | Sliding sidebar with section links |
| Summary card button | `id="card-mode-btn"` + class `card-mode-btn` | `⊞ 摘要卡` button next to h1 title |
| Summary card overlay | `id="sc-overlay"` + class `sc-overlay` | Modal overlay for summary card |
| Summary card | `id="sc-card"` + class `sc-card` | Two-panel summary card (injected by JS) |
| Export button | `id="export-btn"` + class `export-btn` | `↓ 导出` button, bottom-right |
| Export menu | `id="export-menu"` + class `export-menu` | Dropdown with Print/PNG/IM options |
| Export item: print | `id="export-print"` | `打印 / PDF` entry |
| Export item: desktop | `id="export-png-desktop"` | `桌面截图` entry |
| Export item: mobile | `id="export-png-mobile"` | `手机长图` entry |
| Export item: IM | `id="export-im-share"` | `IM 长图` entry |
| JSON summary block | `type="application/json" id="report-summary"` | Machine-readable report metadata |
| Report mode attribute | `data-report-mode="[default\|comparison]"` on `<body>` | Semantic mode flag |

**Important:** `id="export-menu"` by itself is not enough. The menu is incomplete unless all four export items above exist. If any one is missing, rebuild the entire export block from `html-shell-template.md` rather than leaving a partial menu.

### 8.2 TOC JavaScript Contract

The TOC JS logic **MUST** include:

- `scheduleClose` function with **≥100ms delay** (prevents instant-close bug)
- Both `tocBtn` and `tocSidebar` must have `mouseenter` / `mouseleave` handlers
- `locked` state with click-to-lock toggle on `tocBtn`

### 8.3 Edit Mode (always present)

- `id="edit-hotzone"` — bottom-left corner hotzone
- `id="edit-toggle"` — edit toggle button

### 8.4 CSS Assembly Verification

Before writing, verify CSS includes:

- `.toc-toggle` and `.toc-sidebar` styles (from html-shell-template.md §163-198)
- `.sc-card`, `.sc-left`, `.sc-right`, `.sc-overlay` styles (summary card)
- `.export-btn`, `.export-menu`, `.export-item` styles
- `.edit-hotzone`, `.edit-toggle` styles
- `@media print` rules hiding UI chrome
- Export JS bindings for all four entries: `export-print`, `export-png-desktop`, `export-png-mobile`, `export-im-share`

## L1 Content Review

For content, structure, and reading-flow checks, see [review-checklist.md](review-checklist.md).

**L0 (Visual)**: This file — color, typography, layout, anti-slop presentation rules.
**L1 (Content)**: `review-checklist.md` — BLUF opening, heading logic, prose walls, takeaways, scan anchors.
**L2 (Shell Structure)**: This file §8 — HTML shell element existence, TOC JS contract, edit mode, CSS assembly.

**When to apply:**

- `--generate`: run a **silent final review pass** using the L1 checklist before writing HTML, then run L2 shell structure checks before writing
- `--review`: run the same one-pass automatic refinement explicitly against an existing report
