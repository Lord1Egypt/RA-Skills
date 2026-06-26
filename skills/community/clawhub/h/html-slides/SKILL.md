---
name: corporate-slides
description: Create interactive, self-contained HTML slide decks with sidebar navigation, comment panel, zoom controls, inline editing, and present mode. Default brand is Shopee/Sea but supports custom brand presets. Use when the user says "做slides"、"create slides"、"创建幻灯片"、"做PPT"、"做汇报"、"bi-weekly"、"biweekly"、"双周汇报"、"quarterly review"、"product review"、"roadmap presentation"、"strategy deck"、"post-mortem slides", or any request to create a presentation deck.
---

# Corporate Slides

Create zero-dependency, interactive HTML presentations that run in any browser. Every output is a single self-contained HTML file with built-in navigation, commenting, editing, and presentation capabilities.

## Core Principles

1. **Zero Dependencies** — Single HTML file with inline CSS/JS. No npm, no build tools.
2. **Interactive Chrome** — Left sidebar navigation (bilingual-aware), right comment panel, zoom controls, inline text editing, present mode, EN/CN language switch — all built in by default.
3. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides.
4. **Brand-Configurable** — Default brand is Shopee/Sea. User can select a different brand preset or define custom colors/fonts. The design token system makes this a single-point swap.
5. **Content-Driven** — Slides are built around data, comparisons, timelines, and action items — not filler graphics.
6. **Bilingual by Default** — Unless user specifies a single language, generate **both EN and CN** content for every text element with an EN/CN toggle in the toolbar. If user explicitly requests a single language, skip the toggle and generate monolingual content.

---

## Phase 0: Detect Mode

- **Mode A: New Presentation** — Create from scratch. Go to Phase 1.
- **Mode B: Enhancement** — Modify an existing HTML slide deck. Read it first, understand its brand/style, then modify. When adding content, check density limits; split slides if overflow would occur.

---

## Phase 1: Content Discovery

**Ask ALL questions in a single call:**

**Question 1 — Purpose** (header: "Purpose"):
What is this presentation for? Options:
- Bi-weekly / periodic update
- Product review / feature walkthrough
- Roadmap / strategy deck
- Post-mortem / retrospective
- Quarterly business review
- Training / onboarding
- Other (describe)

**Question 2 — Brand** (header: "Brand"):
Which brand preset? Options:
- Shopee / Sea (default — orange + navy)
- Custom (I'll provide colors/fonts)
- Neutral / Minimal (dark charcoal + blue accent, no logos)

**Question 3 — Content** (header: "Content"):
Do you have content ready? Options:
- All content ready (paste text, metrics, etc.)
- Rough notes / bullet points
- Topic only — help me structure it

**Question 4 — Length** (header: "Length"):
Approximately how many slides? Options: Short 5-8 / Medium 8-14 / Long 14+

**Question 5 — Interactive Features** (header: "Features"):
Which interactive features to include? Options:
- Full (sidebar + comments + zoom + edit + present + language toggle) — recommended
- Light (sidebar + present only)
- Minimal (no chrome, static slides)

**Language handling (NO question needed — apply automatically):**
- If user has NOT specified a single language → generate bilingual (EN + CN) with language toggle. This is the default.
- If user explicitly says "English only", "只要中文", or similar → generate monolingual, no toggle.
- The language toggle is part of the toolbar chrome, not a separate question.

If user selected **Custom brand**, follow up with:
- Primary accent color (hex)
- Secondary / heading color (hex)
- Display font preference (or "your choice")
- Logo image file (or "no logo")

If user has content, ask them to share it. Then proceed to Phase 2.

---

## Phase 2: Plan Slide Structure

Based on user content, plan the slide deck using available slide types and components.

### Available Slide Types

| Type | When to Use |
|------|-------------|
| **Cover** | First slide — title, date, team, optional logos |
| **Section Divider** | Transition between major topics — colored background, section number |
| **Content** | Main information slides — header bar + body components |
| **Closing** | Last slide — thank you, contact, next steps |

### Available Components (for Content Slides)

Read [components.md](references/components.md) for full HTML templates.

| Component | Best For |
|-----------|----------|
| **Metrics Grid** | KPI cards (3-column) with values and change indicators |
| **Bi-weekly Table** | Period-over-period comparison with insight cards |
| **Feature Table** | Feature comparisons, scope definitions, matrices |
| **Two-Column Grid** | Findings vs Actions, Pros vs Cons, Before vs After |
| **Action List** | Action items, scope items, decisions with owners |
| **Timeline** | Roadmap milestones, project phases |
| **Status Badge** | Inline status indicators (on-track, at-risk, done) |
| **Screenshot Slot** | Replaceable image placeholder for operational screenshots (dashed border when empty, auto-shows image when `src` set) |

### Content Density Limits Per Slide

| Slide Type | Maximum Content |
|------------|-----------------|
| Cover | Title + subtitle + meta |
| Section Divider | Title + subtitle + section number |
| Content (text) | 1 heading + 1 paragraph + 1 component |
| Content (table) | 1 heading + 1 table (up to 12 rows) |
| Content (mixed) | 1 heading + 2 smaller components |
| Closing | Title + subtitle + meta |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

Present the slide plan to the user for confirmation before generating.

---

## Phase 3: Generate Presentation

### Brand Resolution

1. If **Shopee/Sea** (default): use the Shopee/Sea preset from [design-tokens.md](references/design-tokens.md). MUST include BOTH base64-embedded Shopee and SeaMoney logos on cover, section dividers, content headers, and closing slides.
2. If **Custom**: swap `--accent-primary`, `--accent-secondary`, `--color-navy`, fonts, and logo. Keep all other structural tokens unchanged.
3. If **Neutral**: use the Neutral preset from design-tokens.md. No logos — use a text-only header.

### HTML Architecture

```
<!DOCTYPE html>
<html lang="zh">
<head>
    <!-- Google Fonts (based on brand preset) -->
    <style>
        /* 1. CSS Custom Properties (from design-tokens.md — brand-resolved) */
        /* 2. Reset & Base Typography */
        /* 3. Viewport Fitting (MANDATORY — from viewport-chrome.md) */
        /* 4. Language Toggle (bilingual only — from viewport-chrome.md) */
        /* 5. Sidebar Navigation */
        /* 6. Progress Bar */
        /* 7. Comment Panel */
        /* 8. Zoom Controls */
        /* 9. Slide Type Styles (cover, section, content, closing) */
        /* 10. Component Styles */
        /* 11. Edit Mode */
        /* 12. Present Mode */
        /* 13. Responsive Breakpoints */
        /* 14. Embedded Logos (if applicable) */
    </style>
</head>
<body class="lang-cn">
    <!-- Chrome: sidebar + toggle (left), progress bar (top, slide area only), horizontal toolbar (top-right: lang→present→zoom→edit→comment), comment panel (right) -->
    <!-- SLIDES (each is a <section class="slide">) with lang-en/lang-cn spans -->
    <!-- JS: SlidePresentation class -->
</body>
</html>
```

**Before generating, read ALL reference files:**

- [design-tokens.md](references/design-tokens.md) — CSS custom properties, brand presets, typography
- [slide-types.md](references/slide-types.md) — HTML templates for each slide type
- [components.md](references/components.md) — Reusable component HTML/CSS
- [viewport-chrome.md](references/viewport-chrome.md) — Interactive chrome + viewport rules
- [js-controller.md](references/js-controller.md) — SlidePresentation JS class

### Bilingual Content Rules (when generating EN + CN)

Every user-visible text element must contain **both language spans**:

```html
<h2>
    <span class="lang-en">Architecture Overview</span>
    <span class="lang-cn">架构概览</span>
</h2>
<p>
    <span class="lang-en">Smart acts as a Package Registry.</span>
    <span class="lang-cn">Smart 作为 Package Registry。</span>
</p>
```

**Rules:**
1. Wrap each translatable text node in `<span class="lang-en">` and `<span class="lang-cn">`
2. Technical terms, product names, and code snippets stay unchanged across both languages (e.g. "SKILL.md", "SuperAgent", "CLI", variable names)
3. `data-title` (CN) and `data-title-en` (EN) attributes on slides; `data-group` (CN) and `data-group-en` (EN) on group headers. Sidebar switches language along with body class.
4. The `<html lang>` attribute should be set to `"zh"` (CN is the default display language)
5. Body starts with class `lang-cn` — CN is shown first, user toggles to EN
6. For list items, wrap the text content inside each `<li>`, not the `<li>` itself
7. For table cells, wrap content inside each `<td>`/`<th>`, not the cell itself

**CSS (included in viewport-chrome.md):**
```css
body.lang-en .lang-cn { display: none; }
body.lang-cn .lang-en { display: none; }
```

**When monolingual:** Skip all `lang-en`/`lang-cn` spans, write plain text, omit the language toggle button from the toolbar, and omit the language CSS/JS.

### Key Requirements

1. **Single self-contained HTML file** — all CSS/JS inline
2. **Every slide** must have `data-title` (CN), `data-title-en` (EN), `data-group` (CN), and `data-group-en` (EN) attributes for bilingual sidebar. Monolingual slides only need `data-title` and `data-group`.
3. **Every slide** must include a footer with page numbers (populated by JS)
4. **All sizes** must use `clamp(min, preferred, max)` — never fixed px/rem
5. **Logos**: Shopee/Sea — BOTH `.shopee` and `.seamoney` logos MUST appear, embedded via CSS `content: url(data:...)`. Custom brand — embed user-provided logo(s). Neutral — no logos, text-only headers.
6. Include `prefers-reduced-motion` support
7. Clear `/* === SECTION NAME === */` comment blocks throughout CSS
8. **Bilingual presentations** must include the EN/CN language switch in the toolbar and all lang-en/lang-cn CSS (see viewport-chrome.md). Sidebar nav must also be bilingual-aware.

---

## Phase 4: Delivery

1. **Save** to `work/slides/` with a descriptive filename
2. **Open** using `open [filename].html` to launch in browser
3. **Summarize** — Tell the user:
   - File location, slide count, brand preset used
   - Navigation: Arrow keys, Space, scroll/swipe, sidebar click
   - Top-right toolbar (horizontal, left to right): Language switch → Present → Zoom → Edit → Comment
   - Language: Click "EN" or "CN" segment in the switch to change language; sidebar nav follows. Press `L` to toggle.
   - Present: Press `F5` or click ▶ — fullscreen, hides all chrome
   - Zoom: +/- buttons (70%–150%)
   - Edit: Press `E` — click any text to edit, undo/redo in toolbar
   - Comment panel: Press `C` — per-slide notes saved to localStorage, Copy All exports as Markdown
   - Sidebar: Click ☰ at sidebar right edge to collapse/expand

---

## Supporting Files

| File | Purpose | When to Read |
|------|---------|-------------|
| [design-tokens.md](references/design-tokens.md) | Brand presets, CSS variables, colors, typography, spacing | Phase 3 (always) |
| [slide-types.md](references/slide-types.md) | HTML templates for cover, section, content, closing | Phase 3 (always) |
| [components.md](references/components.md) | Reusable component HTML: metrics, tables, timelines, etc. | Phase 3 (always) |
| [viewport-chrome.md](references/viewport-chrome.md) | Viewport fitting CSS + interactive chrome HTML/CSS | Phase 3 (always) |
| [js-controller.md](references/js-controller.md) | SlidePresentation JS class with all interactive features | Phase 3 (always) |
