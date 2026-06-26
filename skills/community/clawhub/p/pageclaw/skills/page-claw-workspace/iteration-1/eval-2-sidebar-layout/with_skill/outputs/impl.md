# 2026-03-15-ying-xiao-impl.md

Implementation plan for Ying Xiao's academic homepage.
Source: `skills/pageclaw-test/fixtures/page-story-test.md`
Design doc: `design.md` (Warm Paper aesthetic, single centered column, stacked cards)

---

## Task 1 — HTML scaffold and CSS foundation

### 1.1 Document shell

- DOCTYPE HTML5, `lang="en"`, charset UTF-8
- `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Title: `Ying Xiao — PhD Researcher`
- Google Fonts preconnect + link: `Lora:ital,wght@0,400;0,600;0,700;1,400` and `Source+Sans+3:wght@400;500;600`
- Inline `<style>` block (single-file deliverable, no external stylesheet)

### 1.2 CSS custom properties

Declare all design tokens at `:root`:

```css
:root {
  --color-bg: #faf7f2;
  --color-surface: #f5f0e8;
  --color-border: #e8ddd0;
  --color-text-primary: #2c2420;
  --color-text-secondary: #6b5c52;
  --color-accent: #8b4513;
  --color-accent-muted: #c4956a;
  --color-badge-bg: #ede6da;
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 32px;
  --space-xl: 64px;
  --space-2xl: 96px;
  --font-serif: 'Lora', Georgia, serif;
  --font-sans: 'Source Sans 3', system-ui, sans-serif;
  --column-width: 720px;
}
```

### 1.3 Global reset and base styles

- `*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }`
- `body`: `background: var(--color-bg); color: var(--color-text-primary); font-family: var(--font-serif); font-size: 1.05rem; line-height: 1.75;`
- `a`: `color: var(--color-text-primary); text-decoration: none;`
- `a:hover, a:focus-visible`: `color: var(--color-accent); text-decoration: underline; outline-offset: 2px;`
- `img`: `max-width: 100%; display: block;`

### 1.4 Layout: single centered column

```css
.column {
  max-width: var(--column-width);
  margin: 0 auto;
  padding: 0 var(--space-lg);
}
```

At ≤480px: `padding: 0 var(--space-md);`

### 1.5 Section card pattern

```css
.section-card {
  padding: var(--space-lg) 0;
  border-bottom: 1px solid var(--color-border);
}
.section-card:last-child {
  border-bottom: none;
}
.section-label {
  font-family: var(--font-sans);
  font-size: 0.75rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-md);
}
```

---

## Task 2 — Header section

Content source: page-story `##` (name heading — empty) and `## About Me` first paragraph.

- `<header>` inside `.column`
- `<h1>`: `Ying Xiao` — Lora 700, 2.4rem
- Subtitle line: `PhD Researcher · King's College London` — Source Sans 3, 0.9rem, `var(--color-text-secondary)`
- Thin ruled line below header: `border-bottom: 1px solid var(--color-border); padding-bottom: var(--space-lg);`

Name source: inferred from page-story filename and `About Me` section text. The empty `## ` heading in the page-story has no content; we display the name as `<h1>Ying Xiao</h1>`.

---

## Task 3 — About Me section

Content source: `## About Me` (avatar image + biographical paragraph + bold job-market statement)

### 3.1 Avatar

- `<img src="YING.jpg" alt="Portrait of Ying Xiao" width="120" height="120">`
- Style: `border-radius: 50%; width: 120px; height: 120px; object-fit: cover; margin-bottom: var(--space-md);`
- Float or block: block (single column, avatar sits above text paragraph)

### 3.2 Biographical paragraph

- Render as `<p>` with inline `<a>` links for all supervisor/institution hyperlinks
- All names that link to external URLs must be wrapped in `<a href="...">` matching page-story

### 3.3 Job-market callout

- The bold paragraph starting with "I am currently on the job market…" renders as a styled `<p class="callout">`
- Style: `border-left: 3px solid var(--color-accent-muted); padding-left: var(--space-md); font-style: italic; color: var(--color-text-secondary); margin-top: var(--space-md);`
- This is a visual treatment of the bold paragraph — it is not promoted into a hero element

---

## Task 4 — Links section (icon row)

Content source: `## Links` (Email, Google Scholar, GitHub, LinkedIn, rednote)

Render as an icon row using inline SVG from Simple Icons CDN. Do not render as text links.

```
https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<slug>.svg
```

Platform mapping:
| Platform | Slug | URL |
|----------|------|-----|
| Email | — (envelope SVG, generic) | `mailto:ying.1.xiao@kcl.ac.uk` |
| Google Scholar | `googlescholar` | the Scholar URL |
| GitHub | `github` | `https://github.com/xy-showing` |
| LinkedIn | `linkedin` | the LinkedIn URL |
| rednote | `xiaohongshu` | the rednote URL |

Icon implementation:
- Fetch each SVG via `<img src="https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<slug>.svg">` OR inline the SVG directly
- Preferred: inline SVG for reliability and color control
- Each icon: 24×24px, `fill: var(--color-text-secondary)`, hover: `fill: var(--color-accent)`
- Each icon wrapped in `<a href="..." aria-label="<Platform name>" target="_blank" rel="noopener">`
- Email link: `<a href="mailto:ying.1.xiao@kcl.ac.uk" aria-label="Email">`
- Row layout: `display: flex; gap: var(--space-md); align-items: center;`

---

## Task 5 — News section

Content source: `## News` (3 bullet items with dates and paper titles)

### 5.1 Structure

- Section label: `NEWS`
- List: `<ul class="news-list">` — no bullets (list-style: none)
- Each item: `<li class="news-item">` containing:
  - Date badge: `<span class="news-date">Dec 17th</span>` — Source Sans 3, 0.8rem, color: var(--color-text-secondary)
  - Body text with paper title in `<em>` and author list as plain text

### 5.2 Styles

```css
.news-list { list-style: none; display: flex; flex-direction: column; gap: var(--space-md); }
.news-item { display: grid; grid-template-columns: 80px 1fr; gap: var(--space-sm); align-items: start; }
.news-date { font-family: var(--font-sans); font-size: 0.8rem; color: var(--color-text-secondary); padding-top: 0.3rem; }
```

---

## Task 6 — Selected Publications section

Content source: `## Selected Publications` (5 bullet items)

### 6.1 Structure

- Section label: `SELECTED PUBLICATIONS`
- List: `<ol class="pub-list">` ordered (or `<ul>` — match page-story which uses `+` bullets, so `<ul>`)
- Each item: `<li class="pub-item">`
  - Paper title in `<strong>` (first element, visually prominent)
  - Author list in `<span class="pub-authors">` — Source Sans 3, 0.85rem, secondary color
  - Venue badge: `<span class="venue-badge">ICSE 2026</span>` — extract venue from each entry

### 6.2 Venue badge styles

```css
.venue-badge {
  display: inline-block;
  background: var(--color-badge-bg);
  border: 1px solid var(--color-border);
  border-radius: 3px;
  padding: 2px 7px;
  font-family: var(--font-sans);
  font-size: 0.78rem;
  color: var(--color-text-secondary);
  margin-left: var(--space-xs);
}
```

### 6.3 Publication item spacing

```css
.pub-list { list-style: none; display: flex; flex-direction: column; gap: var(--space-md); }
.pub-item { border-left: 2px solid var(--color-border); padding-left: var(--space-md); }
```

---

## Task 7 — Preprints section

Content source: `## Preprints` (3 bullet items)

- Section label: `PREPRINTS`
- Same list structure as publications, without venue badges (preprints have no venue)
- Author list rendered as Source Sans 3, 0.85rem, secondary color
- No badge — instead, a subtle `[Preprint]` label in Source Sans 3 small-caps

---

## Task 8 — Invited Talk section

Content source: `## Invited Talk` (2 bullet items)

### 8.1 Render as timeline

Two entries are a sequence in time — render as a minimal vertical timeline:

```css
.talk-item {
  display: grid;
  grid-template-columns: 52px 1fr;
  gap: var(--space-sm);
  align-items: start;
  position: relative;
}
.talk-year {
  font-family: var(--font-sans);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-text-secondary);
}
```

Timeline connector: `::before` pseudo-element left border line connecting items.

---

## Task 9 — Footer

- Simple centered footer: `<footer>`
- Text: `© 2026 Ying Xiao` — Source Sans 3, 0.8rem, `var(--color-text-secondary)`
- `padding: var(--space-lg) 0;`

---

## Task 10 — Responsive pass

- Single column layout is inherently mobile-friendly
- At ≤480px: reduce `<h1>` to 1.8rem; reduce section padding to `var(--space-md)`
- News item grid: at ≤480px, collapse to single-column `grid-template-columns: 1fr`
- Avatar width: 96px at mobile
- Verify no horizontal scroll at 375px

```css
@media (max-width: 480px) {
  h1 { font-size: 1.8rem; }
  .column { padding: 0 var(--space-md); }
  .section-card { padding: var(--space-md) 0; }
  .news-item { grid-template-columns: 1fr; }
  .news-date { padding-top: 0; }
}
```

---

## Task 11 — Interactive states and accessibility

- All `<a>` elements: `:hover` and `:focus-visible` states defined
- Icon links: `aria-label` on every `<a>`
- Avatar image: descriptive `alt` text
- Skip link: `<a class="skip-link" href="#main">Skip to content</a>` — visually hidden until focused
- Heading hierarchy: `h1` (name) → `h2` (section headers) — no level skipping
- Callout paragraph: `role` is implicit `<p>`, no ARIA role needed
- `prefers-reduced-motion`: wrap any transitions in `@media (prefers-reduced-motion: no-preference)`

---

## Task 12 — Quality pass checklist

Before marking complete:

- [ ] All interactive elements have `:hover` and `:focus-visible`
- [ ] Typography hierarchy: h1 (2.4rem/700) → h2 (1.4rem/600) → body (1.05rem/400) — 3 distinct levels
- [ ] Spacing follows 8pt rhythm throughout
- [ ] No horizontal scroll at 375px or 1200px
- [ ] Links section rendered as icon SVGs, not text
- [ ] Warm Paper aesthetic reflected: paper bg, Lora serif, ruled lines, no shadows
- [ ] All supervisor/institution links in About Me are functional hrefs
- [ ] Venue badges appear on publication items
- [ ] Timeline pattern used for Invited Talk section
