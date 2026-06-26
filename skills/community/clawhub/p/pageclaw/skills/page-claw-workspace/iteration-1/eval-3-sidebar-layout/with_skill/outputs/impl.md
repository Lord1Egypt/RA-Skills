# 2026-03-15-ying-xiao-impl.md

Implementation plan for Ying Xiao academic page.
Style: Brutalist Academic | Layout: asymmetric two-column sticky sidebar grid

---

## Task List

### Task 1 — HTML skeleton

Create `index.html` with:
- `<!DOCTYPE html>` + `<html lang="en">`
- `<head>`: charset, viewport meta, title ("Ying Xiao"), font preconnect + stylesheet links (Google Fonts: Space Grotesk, Inter; IBM Plex Mono CDN), inline `<style>` block
- `<body>`: two-column grid wrapper `<div class="page-grid">` containing:
  - `<aside class="sidebar">` — sticky left column
  - `<main class="content">` — scrollable right column

### Task 2 — CSS custom properties and reset

In `<style>`:
```css
:root {
  --color-ink: #0A0A0A;
  --color-ground: #FAFAFA;
  --color-muted: #555555;
  --color-accent: #0047FF;
  --color-border: #0A0A0A;
  --color-surface: #F0F0F0;
  --color-tag-bg: #0A0A0A;
  --color-tag-fg: #FAFAFA;
  --space-xs: 4px; --space-sm: 8px; --space-md: 16px;
  --space-lg: 24px; --space-xl: 48px; --space-2xl: 96px;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
/* Brutalist: zero border-radius, zero box-shadow */
* { border-radius: 0 !important; }
body { background: var(--color-ground); color: var(--color-ink);
       font-family: 'Inter', sans-serif; font-size: 0.9375rem; line-height: 1.65; }
a { color: var(--color-ink); text-decoration: none; }
a:hover { color: var(--color-accent); }
a:focus-visible { outline: 3px solid var(--color-accent); outline-offset: 2px; }
img { display: block; max-width: 100%; }
```

### Task 3 — Page layout (CSS Grid)

```css
.page-grid {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100vh;
}
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  background: var(--color-surface);
  border-right: 3px solid var(--color-border);
  padding: var(--space-xl) var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}
.content {
  padding: var(--space-xl) 48px;
  max-width: 800px; /* readable line length cap */
}
```

### Task 4 — Sidebar content

Inside `<aside class="sidebar">`:

1. **Name block:**
   ```html
   <div class="sidebar-name">
     <h1>Ying<br>Xiao</h1>
     <p class="sidebar-role">PhD Candidate</p>
     <p class="sidebar-inst">King's College London</p>
   </div>
   ```
   CSS: `h1` font-family Space Grotesk, 1.75rem, weight 800; role + inst in `--color-muted` at 0.8rem.

2. **Divider rule:** `<hr class="rule">` — `border: none; border-top: 3px solid var(--color-border)`

3. **Nav anchors** (matching each `<section>` id):
   ```html
   <nav class="sidebar-nav" aria-label="Page sections">
     <a href="#about">About</a>
     <a href="#links">Links</a>
     <a href="#news">News</a>
     <a href="#publications">Publications</a>
     <a href="#preprints">Preprints</a>
     <a href="#talks">Invited Talks</a>
   </nav>
   ```
   CSS: `display: flex; flex-direction: column; gap: var(--space-sm)` — each link uppercase, 0.75rem, letter-spacing 0.06em, font-weight 600. Active state: `border-left: 3px solid var(--color-accent); padding-left: 8px; color: var(--color-accent)`.

4. **Second divider rule.**

5. **Icon links** (from page-story `## Links`):
   Render five platform icons as inline SVG fetched from Simple Icons CDN + one mailto envelope. Wrap each in `<a href="..." aria-label="...">`. Display as `flex` row, `gap: 12px`, icon size `24px`.

   Platforms and slugs:
   - Email → envelope SVG (custom, not Simple Icons)
   - Google Scholar → `googlescholar`
   - GitHub → `github`
   - LinkedIn → `linkedin`
   - rednote → `xiaohongshu`

   CSS: `.icon-link svg { width: 24px; height: 24px; fill: var(--color-ink); transition: fill 80ms; }` `:hover svg { fill: var(--color-accent); }`

### Task 5 — Main content sections

Each section: `<section id="<id>" class="section">` with a `<h2>` heading.

CSS for all sections:
```css
.section { border-top: 3px solid var(--color-border); padding-top: var(--space-xl); margin-top: var(--space-xl); }
.section:first-of-type { border-top: none; margin-top: 0; padding-top: 0; }
h2 { font-family: 'Space Grotesk', sans-serif; font-size: 1.125rem; font-weight: 700;
     text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: var(--space-lg); }
```

#### Section: About Me (id="about")

- Avatar image: `<img src="YING.jpg" alt="Ying Xiao" class="avatar">` — CSS: `width: 80px; height: 80px; object-fit: cover; border: 3px solid var(--color-border);` (square, no border-radius)
- Bio paragraph: render verbatim from page-story, preserving `<a>` links to supervisors and institutions
- Job market bold paragraph: render as `<p class="job-market">` — CSS: `font-weight: 700; border-left: 4px solid var(--color-accent); padding-left: var(--space-md); margin-top: var(--space-lg);`

#### Section: Links (id="links") — SKIP as standalone section

The links are rendered in the sidebar (Task 4, step 5). The `## Links` section from page-story is fulfilled by the sidebar icon links. Do not duplicate as a content section in main.

#### Section: News (id="news")

Render as a timeline list: `<ul class="news-list">`, each item `<li class="news-item">`.

Each news item structure:
```html
<li class="news-item">
  <span class="news-date">Dec 17th</span>
  <p class="news-text">our paper "..." is accepted by ...</p>
</li>
```
CSS: `news-list { list-style: none; display: flex; flex-direction: column; gap: var(--space-lg); }` — `news-item { display: grid; grid-template-columns: 80px 1fr; gap: var(--space-md); align-items: start; }` — `news-date { font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; font-weight: 600; color: var(--color-accent); padding-top: 3px; }` — Paper title in quotes: `font-style: italic`.

#### Section: Selected Publications (id="publications")

Render as an ordered list `<ol class="pub-list">`. Each `<li class="pub-item">` contains:
```html
<li class="pub-item">
  <p class="pub-title">Fairness Is Not Just Ethical: ...</p>
  <p class="pub-meta">Ying Xiao, Shangwen Wang, ... · ICSE 2026 · <span class="pub-badge">Core A* · CCF-A</span></p>
</li>
```
CSS:
```css
.pub-list { list-style: none; display: flex; flex-direction: column; gap: var(--space-lg); counter-reset: pub-counter; }
.pub-item { padding-left: var(--space-md); border-left: 3px solid transparent; transition: border-color 80ms; counter-increment: pub-counter; }
.pub-item:hover { border-left-color: var(--color-accent); }
.pub-title { font-weight: 600; margin-bottom: var(--space-xs); }
.pub-meta { font-size: 0.8125rem; color: var(--color-muted); }
.pub-badge { display: inline-block; background: var(--color-tag-bg); color: var(--color-tag-fg);
             font-size: 0.6875rem; font-weight: 700; padding: 2px 6px; letter-spacing: 0.04em;
             text-transform: uppercase; margin-left: var(--space-sm); }
```

Ying Xiao's name in author lists: `<strong class="author-self">Ying Xiao</strong>` — CSS: `font-weight: 700; text-decoration: underline;`

#### Section: Preprints (id="preprints")

Same structure as publications but with `<ul>` (unordered) and no venue badge (prepints have no conference venue). Each item shows title, authors. No badge.

#### Section: Invited Talk (id="talks")

Timeline: `<ul class="talk-list">`, each item:
```html
<li class="talk-item">
  <span class="talk-year">2026</span>
  <p class="talk-desc">Mitigating machine learning software bias via correlation tuning, London, United Kingdom.</p>
</li>
```
CSS: `talk-item { display: grid; grid-template-columns: 60px 1fr; gap: var(--space-md); }` — `talk-year { font-family: 'IBM Plex Mono', monospace; font-weight: 700; font-size: 0.875rem; color: var(--color-accent); }`

### Task 6 — Responsive behavior

```css
@media (max-width: 768px) {
  .page-grid {
    grid-template-columns: 1fr;
  }
  .sidebar {
    position: static;
    height: auto;
    border-right: none;
    border-bottom: 3px solid var(--color-border);
    flex-direction: row;
    flex-wrap: wrap;
    padding: var(--space-md);
    gap: var(--space-sm);
  }
  .sidebar-name h1 { font-size: 1.25rem; }
  .sidebar-nav { flex-direction: row; flex-wrap: wrap; }
  .content { padding: var(--space-xl) var(--space-md); }
}
```

### Task 7 — Accessibility and quality checks

- [ ] `<html lang="en">` present
- [ ] All icon links have `aria-label`
- [ ] Avatar `<img>` has descriptive `alt`
- [ ] Skip link: `<a href="#about" class="skip-link">Skip to content</a>` before `<body>` content — CSS: visually hidden until focused
- [ ] Color contrast: ink on ground = #0A0A0A on #FAFAFA ≈ 19:1 ✓ | muted #555 on #FAFAFA ≈ 7.5:1 ✓ | accent #0047FF on white ≈ 8.6:1 ✓
- [ ] All `<a>` have `:focus-visible` outline
- [ ] `viewport-meta`: `<meta name="viewport" content="width=device-width, initial-scale=1">`
- [ ] `font-display: swap` or Google Fonts `display=swap` param
- [ ] No horizontal scroll at 375px or 1200px
- [ ] `@media (prefers-reduced-motion: reduce)` — disable transition on links

### Task 8 — Quality pass

After build:
1. **Polish:** Verify alignment, spacing rhythm consistency, hover/focus states on all interactive elements
2. **Audit:** Confirm accessibility (contrast, keyboard nav, ARIA), no horizontal scroll, icon SVG fallbacks
3. **Quieter:** Assess if accent color (#0047FF) usage is excessive — keep to interactive states only
