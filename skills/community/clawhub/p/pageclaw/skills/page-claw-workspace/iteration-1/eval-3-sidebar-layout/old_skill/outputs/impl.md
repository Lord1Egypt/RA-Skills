# 2026-03-15-ying-xiao-impl.md

## Implementation Plan — Ying Xiao Academic Page

Source: `skills/pageclaw-test/fixtures/page-story-test.md`
Design spec: `design.md` (Terminal Scholar — dark monospace, high-contrast)
Target: `index.html` (single file, no external dependencies except Google Fonts + Simple Icons CDN)

---

## Task List

### T1 — HTML Scaffold

- Create `index.html` with `<!DOCTYPE html>` and `<html lang="en">`
- Set `<meta charset="UTF-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- Set `<title>Ying Xiao — PhD Researcher</title>`
- Preload JetBrains Mono from Google Fonts: `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap`
- Embed all CSS in a single `<style>` block in `<head>`
- All content in `<main>` inside `<body>`

### T2 — CSS Reset and Design Tokens

Apply the Terminal Scholar signature:

```css
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --text-accent: #58a6ff;
  --badge-ccf-bg: #1f6feb;
  --badge-ccf-text: #cae8ff;
  --badge-q1-bg: #388bfd;
  --badge-q1-text: #cae8ff;
  --news-bullet: #3fb950;
  --max-width: 720px;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; }
body {
  font-family: 'JetBrains Mono', 'Courier New', monospace;
  background: var(--bg);
  color: var(--text-primary);
  line-height: 1.7;
  padding: 0 1rem;
}
a {
  color: var(--text-accent);
  text-decoration: none;
}
a:hover { text-decoration: underline; }
a:focus-visible {
  outline: 2px solid var(--text-accent);
  outline-offset: 2px;
}
```

### T3 — Skip Link (Accessibility)

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
  top: auto;
}
.skip-link:focus {
  position: static;
  left: auto;
}
```

### T4 — Header / Name Block

Render the top section from page-story:
- `<header>` contains `<h1>Ying Xiao</h1>` and a subtitle line: `PhD Researcher · King's College London`
- Below name, render inline nav anchors (About, Links, News, Publications, Preprints, Invited Talk)

```css
header {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 3rem 0 2rem;
  border-bottom: 1px solid var(--border);
}
h1 {
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: var(--text-primary);
}
.subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}
nav.page-nav {
  margin-top: 1.25rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}
nav.page-nav a {
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--text-secondary);
}
nav.page-nav a:hover { color: var(--text-accent); }
```

### T5 — Main Content Wrapper

```html
<main id="main-content">
  <!-- sections go here -->
</main>
```

```css
main {
  max-width: var(--max-width);
  margin: 0 auto;
}
section {
  padding: 2.5rem 0;
  border-top: 1px solid var(--border);
}
h2 {
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-primary);
  margin-bottom: 1.25rem;
}
```

### T6 — About Me Section

- `<section id="about">` with `<h2>About Me</h2>`
- The avatar image (`YING.jpg`) is referenced in the page-story; render it as `<img src="YING.jpg" alt="Portrait of Ying Xiao" ...>` with fixed dimensions to prevent layout shift
- Paragraph text from page-story rendered as `<p>` with inline links preserved
- Job-market bold statement rendered as `<p class="job-market">` with distinct treatment

```css
.about-avatar {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 0;
  border: 1px solid var(--border);
  margin-bottom: 1.25rem;
  display: block;
}
.job-market {
  margin-top: 1rem;
  color: var(--text-accent);
  font-weight: 600;
}
```

### T7 — Links Section (Icon-based)

Render as icon links using Simple Icons CDN per Rendering Conventions:

| Link | Platform | Slug |
|------|----------|------|
| Email | envelope (custom SVG) | — |
| Google Scholar | googlescholar | `googlescholar` |
| GitHub | github | `github` |
| LinkedIn | linkedin | `linkedin` |
| rednote | xiaohongshu | `xiaohongshu` |

```html
<section id="links">
  <h2>Links</h2>
  <div class="icon-links">
    <!-- each: <a href="..." aria-label="..."><img src="CDN_URL" ...></a> -->
  </div>
</section>
```

Icon CDN pattern: `https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<slug>.svg`

Email uses inline envelope SVG (not Simple Icons).

Icons styled: `width: 24px; height: 24px; filter: invert(1)` (to appear white on dark bg).

```css
.icon-links {
  display: flex;
  gap: 1.25rem;
  align-items: center;
  flex-wrap: wrap;
}
.icon-links a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border: 1px solid var(--border);
  transition: border-color 150ms ease;
}
.icon-links a:hover {
  border-color: var(--text-accent);
}
.icon-links img {
  width: 20px;
  height: 20px;
  filter: invert(90%) sepia(10%) saturate(200%) hue-rotate(180deg);
}
```

### T8 — News Section

Render as a list with timeline treatment. Each news item is a `<li>` with a date marker and text.

```css
.news-list {
  list-style: none;
}
.news-list li {
  position: relative;
  padding-left: 1.25rem;
  margin-bottom: 0.875rem;
  font-size: 0.875rem;
  color: var(--text-primary);
}
.news-list li::before {
  content: '+';
  position: absolute;
  left: 0;
  color: var(--news-bullet);
  font-weight: 700;
}
```

### T9 — Selected Publications Section

Each publication entry rendered as a structured block:
- Paper title (linked if URL available — no URLs in page-story, so plain text)
- Author list (comma-separated, Ying Xiao in `<strong>`)
- Venue + year
- Venue rank badges (CCF-A, Core A*, JCR Q1) as inline `<span class="badge">`

```css
.pub-list { list-style: none; }
.entry {
  border-left: 3px solid var(--border);
  padding-left: 1rem;
  margin-bottom: 1.5rem;
  transition: border-color 150ms ease;
}
.entry:hover { border-color: var(--text-accent); }
.entry-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.5;
}
.entry-authors {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}
.entry-venue {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  margin-top: 0.125rem;
}
.badge {
  display: inline-block;
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 0.1em 0.4em;
  border-radius: 0;
  margin-left: 0.375rem;
  vertical-align: middle;
}
.badge-ccf { background: var(--badge-ccf-bg); color: var(--badge-ccf-text); }
.badge-q1 { background: var(--badge-q1-bg); color: var(--badge-q1-text); }
```

### T10 — Preprints Section

Same entry structure as publications, without venue badges (preprints have no venue rank). Rendered as `<section id="preprints">`.

### T11 — Invited Talk Section

Render as a list. Each item: year + talk title + location.

```css
.talk-list { list-style: none; }
.talk-list li {
  padding-left: 1.25rem;
  position: relative;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
}
.talk-list li::before {
  content: '+';
  position: absolute;
  left: 0;
  color: var(--text-accent);
  font-weight: 700;
}
```

### T12 — Footer

Minimal footer: no content in page-story footer, so render only a closing rule.

```css
footer {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 2rem 0;
  border-top: 1px solid var(--border);
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-align: right;
}
```

### T13 — Responsive

- Mobile-first: single column at all widths (max-width 720px centered)
- At 375px: reduce `padding: 0 0.75rem` on body; nav wraps naturally
- No horizontal scroll at any breakpoint
- Avatar image max-width: 100%

```css
@media (max-width: 480px) {
  h1 { font-size: 1.5rem; }
  body { padding: 0 0.75rem; }
}
```

### T14 — Build Verification Checklist

Before marking complete:
- [ ] All interactive elements have `:hover` and `:focus-visible`
- [ ] Typography: H1 (32px/700) > H2 (18px/700 uppercase) > body (14px/400) = 3 distinct levels
- [ ] Spacing follows 8px rhythm throughout
- [ ] No horizontal scroll at 375px
- [ ] Links section uses inline SVG icons
- [ ] Terminal Scholar CSS fingerprint present: monospace, `#0d1117` bg, `#e6edf3` text, `border-radius: 0`, `box-shadow: none`

### T15 — Quality Pass

After build:
1. Run `polish` skill — alignment, states, edge cases
2. Run `audit` skill — accessibility, performance, anti-pattern check
3. If visually aggressive: run `quieter`
4. If quality concerns remain: run `critique`
