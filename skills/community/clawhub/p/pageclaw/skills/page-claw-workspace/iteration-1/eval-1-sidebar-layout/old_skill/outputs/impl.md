# Implementation Plan — Ying Xiao Academic Homepage

**Design doc:** `outputs/design.md`
**Target:** `outputs/index.html`
**Generated:** 2026-03-15

---

## Overview

Build a single-file static HTML page for Ying Xiao's academic homepage using the Structured Sidebar Scholar aesthetic. The page uses a two-column CSS Grid layout: a sticky left sidebar (260px) for identity and navigation, and a scrollable right main column for all content sections.

---

## Task List

### T1 — HTML Skeleton

1. Create `<!DOCTYPE html>` with `lang="en"`
2. `<head>`: charset, viewport, title ("Ying Xiao"), Inter font import from Google Fonts
3. Inline all CSS in a single `<style>` block (no external CSS file)
4. Body: `display: grid; grid-template-columns: 260px 1fr; min-height: 100vh`
5. Two top-level children: `<aside class="sidebar">` and `<main class="main">`

### T2 — CSS Reset and Base

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Inter', sans-serif; font-size: 0.9375rem; color: #111827; background: #ffffff; }
a { color: #2563eb; text-decoration: none; font-weight: 500; }
a:hover { color: #1d4ed8; text-decoration: underline; }
a:focus-visible { outline: 2px solid #2563eb; outline-offset: 2px; border-radius: 2px; }
```

### T3 — Sidebar Structure

Build `<aside class="sidebar">` with:

1. **CSS:**
   ```css
   .sidebar {
     position: sticky;
     top: 0;
     height: 100vh;
     overflow-y: auto;
     background: #f8f9fa;
     border-right: 1px solid #e5e7eb;
     padding: 32px 24px;
     display: flex;
     flex-direction: column;
     gap: 24px;
   }
   ```

2. **Avatar block:**
   - `<img src="YING.jpg" alt="Ying Xiao" class="avatar">` — `width: 96px; height: 96px; border-radius: 50%; object-fit: cover`

3. **Name and affiliation:**
   - `<h1 class="name">Ying Xiao</h1>` — `font-weight: 700; font-size: 1.5rem; letter-spacing: -0.02em; line-height: 1.2`
   - `<p class="affiliation">PhD Student · King's College London</p>` — `font-size: 0.8125rem; color: #6b7280; line-height: 1.5`

4. **Job-market status badge:**
   - `<div class="status-badge">Open to Postdoc Positions</div>`
   - CSS: `background: #eff6ff; color: #1e40af; font-size: 0.75rem; font-weight: 600; padding: 6px 10px; border-radius: 4px; line-height: 1.4`

5. **Icon links (from ## Links section):**
   - Rendered as icon-only links using inline SVG from Simple Icons CDN
   - Layout: `display: flex; flex-wrap: wrap; gap: 12px; align-items: center`
   - Platforms and slugs:
     - Email → envelope SVG (custom, not Simple Icons)
     - Google Scholar → `googlescholar`
     - GitHub → `github`
     - LinkedIn → `linkedin`
     - rednote → `xiaohongshu`
   - Each icon: `width: 20px; height: 20px; fill: #6b7280`
   - Hover: `fill: #2563eb`
   - Each wrapped in `<a href="..." aria-label="[Platform]" class="icon-link">`

### T4 — Main Content Column

Build `<main class="main">` with:

```css
.main {
  padding: 48px 56px;
  max-width: 800px;
}
.section { margin-bottom: 48px; }
h2.section-label {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 20px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}
```

### T5 — About Me Section

- Render the About Me prose as `<p>` elements inside `<section class="section">`
- Section heading: `<h2 class="section-label">About Me</h2>`
- Avatar is in sidebar, NOT repeated here
- The bold job-market sentence (`**I am currently on the job market…**`) is rendered as `<p><strong>…</strong></p>` within the About Me section — do NOT promote it to a separate component outside this section
- Supervisor links rendered as `<a href="...">Prof. Name</a>`

### T6 — Links Section (icon rendering)

- The `## Links` section content is rendered in the sidebar as icon links (T3 step 5)
- No separate `## Links` section appears in the main content column
- (The Links section from the page-story maps entirely to the sidebar icon block)

### T7 — News Section

- Section heading: `<h2 class="section-label">News</h2>`
- Each news item rendered as a list item with a subtle left-border treatment:
  ```css
  .news-list { list-style: none; display: flex; flex-direction: column; gap: 16px; }
  .news-item { border-left: 3px solid #e5e7eb; padding-left: 16px; line-height: 1.65; }
  .news-item:hover { border-left-color: #2563eb; }
  ```
- Paper titles wrapped in `<em>` for emphasis; venue names in plain text
- No date-prefix stripping — render dates as they appear in the page-story

### T8 — Selected Publications Section

- Section heading: `<h2 class="section-label">Selected Publications</h2>`
- Each publication as a `.pub-entry` list item:
  ```css
  .pub-list { list-style: none; display: flex; flex-direction: column; gap: 20px; }
  .pub-entry { border-left: 3px solid #e5e7eb; padding-left: 16px; }
  .pub-entry:hover { border-left-color: #2563eb; }
  .pub-title { font-weight: 600; color: #111827; line-height: 1.4; margin-bottom: 4px; }
  .pub-authors { font-size: 0.8125rem; color: #6b7280; line-height: 1.5; margin-bottom: 4px; }
  .pub-venue { font-size: 0.8125rem; color: #6b7280; }
  .pub-badge { display: inline-block; font-size: 0.6875rem; font-weight: 600; background: #eff6ff; color: #1e40af; padding: 2px 6px; border-radius: 3px; margin-left: 6px; vertical-align: middle; }
  ```
- Venue badges: `Core A*` and `CCF-A` and `JCR Q1` rendered as `.pub-badge` inline tags after venue text
- Ying Xiao's name bolded within author lists: `<strong>Ying Xiao</strong>`

### T9 — Preprints Section

- Section heading: `<h2 class="section-label">Preprints</h2>`
- Same `.pub-entry` treatment as publications
- No venue badges (preprints have no venue ranking)

### T10 — Invited Talk Section

- Section heading: `<h2 class="section-label">Invited Talk</h2>`
- Each talk as a list item with year prefix:
  ```css
  .talk-list { list-style: none; display: flex; flex-direction: column; gap: 12px; }
  .talk-item { display: grid; grid-template-columns: 48px 1fr; gap: 8px; align-items: baseline; }
  .talk-year { font-weight: 600; color: #2563eb; font-size: 0.8125rem; }
  .talk-desc { color: #111827; line-height: 1.65; }
  ```

### T11 — Responsive Breakpoint

```css
@media (max-width: 768px) {
  body { grid-template-columns: 1fr; }
  .sidebar { position: static; height: auto; border-right: none; border-bottom: 1px solid #e5e7eb; }
  .main { padding: 32px 24px; }
}
```

### T12 — Icon Link Implementation

For each social link, fetch SVG from Simple Icons CDN and inline it, or use `<img>` with the CDN URL:

```html
<a href="https://github.com/xy-showing" aria-label="GitHub" class="icon-link">
  <img src="https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/github.svg"
       alt="" width="20" height="20" class="social-icon">
</a>
```

```css
.icon-link { display: inline-flex; align-items: center; justify-content: center;
             width: 32px; height: 32px; border-radius: 6px; transition: background 0.15s; }
.icon-link:hover { background: #e5e7eb; }
.social-icon { width: 20px; height: 20px; opacity: 0.6; transition: opacity 0.15s; }
.icon-link:hover .social-icon { opacity: 1; }
.icon-link:focus-visible { outline: 2px solid #2563eb; outline-offset: 2px; }
```

Envelope SVG for email (custom inline):
```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
     stroke-width="2" width="20" height="20" aria-hidden="true">
  <rect x="2" y="4" width="20" height="16" rx="2"/>
  <polyline points="2,4 12,13 22,4"/>
</svg>
```

### T13 — Quality Checklist (pre-completion)

- [ ] Sidebar is sticky: `position: sticky; top: 0; height: 100vh`
- [ ] No horizontal scroll at 375px
- [ ] No horizontal scroll at 1200px
- [ ] All links have `:hover` and `:focus-visible` states
- [ ] Icon links have `aria-label` attributes
- [ ] Typography hierarchy: H1 (700, 1.5rem) > H2 (600, 0.875rem) > body (400, 0.9375rem) > meta (400, 0.8125rem)
- [ ] Status badge visible in sidebar
- [ ] Job-market sentence in About Me section (not promoted outside)
- [ ] Venue badges on publications
- [ ] Author name "Ying Xiao" bolded in publication entries

---

## Build Order

1. T1 HTML skeleton → T2 CSS reset
2. T3 Sidebar (identity, avatar, links)
3. T4 Main column structure
4. T5 About Me → T6 Links (sidebar) → T7 News → T8 Publications → T9 Preprints → T10 Invited Talk
5. T11 Responsive
6. T12 Icon links
7. T13 Quality checklist
