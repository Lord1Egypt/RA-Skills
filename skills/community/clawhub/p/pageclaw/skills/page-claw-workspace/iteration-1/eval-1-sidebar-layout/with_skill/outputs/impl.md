# 2026-03-15-ying-xiao-impl.md

Implementation plan for Ying Xiao's academic homepage. Source: `page-story-test.md`. Design spec: `design.md`. Style: Terminal Scholar (sticky sidebar + scrollable main, dark monospace).

---

## Task 1 — HTML scaffold and CSS custom properties

Create `index.html` with:

- `<!DOCTYPE html>` + `<html lang="en">`
- `<meta charset="UTF-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- `<title>Ying Xiao</title>`
- Google Fonts preconnect + `JetBrains Mono` stylesheet link (weights 400, 600)
- `<style>` block in `<head>` with all CSS (single-file deliverable)
- CSS custom properties on `:root`:
  ```css
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text-primary: #c9d1d9;
  --text-secondary: #8b949e;
  --text-accent: #58a6ff;
  --text-heading: #f0f6fc;
  --badge-bg: #1f2937;
  --badge-text: #79c0ff;
  ```
- Global reset: `*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }`
- `body` styles: `font-family`, `background: var(--bg)`, `color: var(--text-primary)`, `font-size: 0.875rem`, `line-height: 1.75`
- `::selection` background `#1f6feb`

## Task 2 — Two-column layout shell

`.layout` wrapper:
```css
.layout {
  display: flex;
  min-height: 100vh;
}
```

`.sidebar`:
```css
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  width: 240px;
  flex-shrink: 0;
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 1.5rem 1.25rem;
}
```

`.main-content`:
```css
.main-content {
  flex: 1;
  min-width: 0;
  padding: 2rem 2.5rem;
  max-width: 780px;
}
```

## Task 3 — Sidebar content

Inside `<aside class="sidebar">`:

1. **Avatar** — `<img src="YING.jpg" alt="Ying Xiao" class="avatar">`. CSS: `width: 72px; height: 72px; border-radius: 50%; object-fit: cover; display: block; margin-bottom: 1rem`. Include `onerror` fallback to hide if image missing.

2. **Name** — `<h1 class="sidebar-name">Ying Xiao</h1>`. CSS: `font-size: 1.1rem; font-weight: 600; color: var(--text-heading); margin-bottom: 0.25rem`.

3. **Title/affiliation line** — `<p class="sidebar-affiliation">PhD · King's College London</p>`. CSS: `font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 1.25rem`.

4. **Links section** (icon-based, per Rendering Conventions):
   - Render as `<ul class="sidebar-links">` with inline SVG icons from Simple Icons CDN
   - Email: envelope SVG (generic) — `mailto:ying.1.xiao@kcl.ac.uk`
   - Google Scholar: `googlescholar` slug
   - GitHub: `github` slug
   - LinkedIn: `linkedin` slug
   - rednote: `xiaohongshu` slug
   - Each `<li>` contains `<a href="..." aria-label="..." class="icon-link"><img src="https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<slug>.svg" ...></a>`
   - Icon size: `20px × 20px`, filtered to `--text-secondary` color via CSS filter, hover: `--text-accent`
   - Layout: `display: flex; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 1.5rem`
   - Email uses inline SVG envelope (not Simple Icons)

5. **Section navigation** — `<nav class="sidebar-nav" aria-label="Page sections">` with anchor links to each `<section>`:
   - About, News, Selected Publications, Preprints, Invited Talk
   - Each: `<a href="#about" class="nav-link">About</a>` etc.
   - CSS: `display: block; font-size: 0.75rem; color: var(--text-secondary); text-decoration: none; padding: 0.3rem 0; transition: color 150ms ease`
   - Hover: `color: var(--text-accent)`
   - Active (JS `IntersectionObserver`): `color: var(--text-accent); font-weight: 600`

## Task 4 — Main content: About Me section

`<section id="about" class="content-section">`:

- Section heading: `<h2 class="section-heading">About</h2>` (do not render the empty `##` from page-story line 3; render `## About Me` as "About")
- Body paragraph: render the full About Me text faithfully, with all hyperlinked supervisor names as `<a href="..." class="prose-link">Name</a>`
- Job market callout: the bold paragraph "I am currently on the job market..." renders as `<p class="callout">` with distinct treatment: `border-left: 2px solid var(--text-accent); padding-left: 0.75rem; color: var(--text-heading); margin-top: 1rem`
- Do NOT promote this to a hero or badge

## Task 5 — Main content: News section

`<section id="news" class="content-section">`:

- Section heading: `<h2 class="section-heading">News</h2>`
- Each `+` bullet renders as a timeline entry:
  ```html
  <ul class="news-list">
    <li class="news-item">
      <span class="news-date">Dec 2025</span>
      <span class="news-text">paper accepted...</span>
    </li>
  ```
- Extract date from start of each entry; render as `<span class="news-date">` in `--text-accent` color, monospace, `font-size: 0.75rem`, `min-width: 80px`, `flex-shrink: 0`
- Layout: `display: flex; gap: 0.75rem; align-items: baseline` per item
- Paper titles in news items: `<em>` (italic in monospace produces distinguishable slant)
- Venue labels (ICSE 2026, Philosophical Transactions, FSE 2024): render as badge chips `<span class="badge">ICSE 2026</span>`

## Task 6 — Main content: Selected Publications section

`<section id="publications" class="content-section">`:

- Section heading: `<h2 class="section-heading">Selected Publications</h2>`
- Each `+` entry renders as a flat list item (no cards):
  ```html
  <ol class="pub-list">
    <li class="pub-entry">
      <p class="pub-title">Fairness Is Not Just Ethical...</p>
      <p class="pub-meta">Ying Xiao, Shangwen Wang, ... · <span class="badge">ICSE 2026</span> <span class="badge badge-tier">Core A* · CCF-A</span></p>
    </li>
  ```
- `pub-title`: `font-weight: 600; color: var(--text-heading); font-size: 0.875rem`
- `pub-meta`: `font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.25rem`
- Badges: `background: var(--badge-bg); color: var(--badge-text); border-radius: 3px; padding: 1px 6px; font-size: 0.7rem; font-weight: 600`
- Between entries: `margin-bottom: 1.25rem`
- Author names: render as plain text (no links unless page-story provides URLs — it does not)
- First author "Ying Xiao" in entries where she is first: `font-weight: 600; color: var(--text-primary)` (slightly elevated vs. `--text-secondary`)

## Task 7 — Main content: Preprints section

`<section id="preprints" class="content-section">`:

- Same rendering pattern as Selected Publications
- Section heading: `<h2 class="section-heading">Preprints</h2>`
- No venue badges (preprints have no venue); omit badge column
- Three entries rendered as flat list

## Task 8 — Main content: Invited Talk section

`<section id="invited-talk" class="content-section">`:

- Section heading: `<h2 class="section-heading">Invited Talk</h2>`
- Two entries; each is a year + talk title + location:
  ```html
  <ul class="talk-list">
    <li class="talk-entry">
      <span class="talk-year">2026</span>
      <div>
        <p class="talk-title">Mitigating machine learning software bias via correlation tuning</p>
        <p class="talk-location">London, United Kingdom</p>
      </div>
    </li>
  ```
- `talk-year`: `font-size: 0.75rem; color: var(--text-accent); font-weight: 600; min-width: 48px; flex-shrink: 0`
- Layout: `display: flex; gap: 0.75rem; align-items: flex-start`

## Task 9 — Section separators and spacing

Between each `<section>`: `margin-bottom: 2.5rem`. Section heading `margin-bottom: 1rem`. Section heading preceded by `border-top: 1px solid var(--border); padding-top: 1.5rem` (except the first section, About, which has no top border).

## Task 10 — Responsive: mobile collapse

At `max-width: 768px`:
- `.layout`: `flex-direction: column`
- `.sidebar`: `position: static; height: auto; width: 100%; border-right: none; border-bottom: 1px solid var(--border)`
- `.sidebar-nav`: `display: none` (hide nav anchors on mobile — page is linear scroll)
- `.main-content`: `padding: 1.5rem 1rem`
- Avatar: `width: 56px; height: 56px`

## Task 11 — Hover and focus states

All interactive elements:
- `<a>`: `transition: color 150ms ease, opacity 150ms ease`
- `.prose-link`: `color: var(--text-accent); text-decoration: underline`; hover: `opacity: 0.8`
- `.nav-link`: no underline; hover: `color: var(--text-accent)`
- `.icon-link`: hover filter shifts icon to accent color
- All `<a>` elements: `:focus-visible { outline: 2px solid var(--text-accent); outline-offset: 2px; border-radius: 2px }`

## Task 12 — Active nav highlighting (JS)

Small inline `<script>` at bottom of body using `IntersectionObserver`:
- Observe all `<section>` elements
- On intersection, find corresponding `.nav-link[href="#<id>"]` and add `.is-active` class
- `.is-active`: `color: var(--text-accent); font-weight: 600`

## Task 13 — Accessibility and final checks

- `<html lang="en">`
- All SVG icons: `aria-hidden="true"` on `<img>` (label is on parent `<a aria-label="...">`)
- `<main>` element wrapping `.main-content` for landmark
- `<aside>` element for sidebar
- Skip link: `<a href="#about" class="skip-link">Skip to content</a>` at top of body, visually hidden until focused
- Verify no horizontal scroll at 375px
- Verify contrast: `--text-primary` (#c9d1d9) on `--bg` (#0d1117) > 7:1 ✓

## Checklist before done

- [ ] Sticky sidebar stays fixed while main content scrolls (desktop)
- [ ] All supervisor links in About Me are clickable
- [ ] Job market callout has left-border accent treatment
- [ ] News items show date as colored prefix
- [ ] Publication badges render for venue and tier
- [ ] Links section uses SVG icons (not text)
- [ ] Mobile: sidebar collapses, no horizontal scroll
- [ ] All hover + focus states implemented
- [ ] Active nav highlighting works on scroll
