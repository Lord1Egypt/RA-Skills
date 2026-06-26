# Implementation Plan — Ying Xiao Academic Page

Source: `skills/pageclaw-test/fixtures/page-story-test.md`
Design: `outputs/design.md`
Aesthetic: Editorial Serif · Warm & editorial
Output: `outputs/index.html`

---

## Phase 1 — Document Shell

**Task 1.1** Create `index.html` with:
- `<!DOCTYPE html>`, `lang="en"`, `charset="UTF-8"`, viewport meta (`width=device-width, initial-scale=1`)
- `<title>Ying Xiao — PhD Researcher</title>`
- Google Fonts preconnect + stylesheet link:
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
  ```
- Inline `<style>` block (all CSS in-document, no external file)
- `<body>` with a single `<main>` container

**Task 1.2** Write CSS custom properties (`:root`) from design system palette and typography tokens.

**Task 1.3** Write base reset and layout CSS:
- `box-sizing: border-box` universal reset
- `body`: `background: var(--bg); color: var(--ink); font-family: 'Source Serif 4', Georgia, serif; font-size: 18px; line-height: 1.7`
- `main`: `max-width: 720px; margin: 0 auto; padding: 3rem 2rem`
- Responsive: `@media (max-width: 600px) { main { padding: 2rem 1.25rem } }`

---

## Phase 2 — Header / Name Section

**Task 2.1** Write `<header>` inside `<main>`:
- `<h1>` with name "Ying Xiao" — `font-family: 'Playfair Display'; font-size: clamp(2rem, 5vw, 3rem); font-weight: 700`
- Subtitle line: "PhD Researcher · AI Fairness & Reliability" — `font-size: 1rem; color: var(--ink-secondary); margin-top: 0.5rem`
- `<hr>` after header using `border: none; border-top: 1px solid var(--border); margin: 2rem 0`

---

## Phase 3 — About Me Section

**Task 3.1** Write `<section id="about">`:
- `<h2>About Me</h2>` with section heading styles
- Avatar image: `<img src="YING.jpg" alt="Ying Xiao" ...>` — positioned as inline float-left on desktop (`float: left; margin: 0 1.5rem 1rem 0; width: 140px; height: 140px; border-radius: 50%; object-fit: cover`), centered block on mobile
- Paragraph with bio text, preserving all hyperlinks to supervisors/institutions as `<a href="..." target="_blank" rel="noopener">Name</a>` — links styled `color: var(--accent); text-decoration: underline`
- Bold paragraph: "I am currently on the job market..." — wrapped in `<p><strong>...</strong></p>`, no visual promotion beyond bold weight
- Clearfix div after image+text

---

## Phase 4 — Links Section (Icon Links)

**Task 4.1** Write `<section id="links">`:
- `<h2>Links</h2>`
- Icon row rendered as `<nav aria-label="Social links">` containing `<ul>` of `<li><a>` items, styled as horizontal flex row with `gap: 1.25rem`
- Each icon: `width: 28px; height: 28px; display: inline-flex; align-items: center`
- Hover: `opacity: 0.7; transition: opacity 150ms ease`

**Task 4.2** Implement each icon using Simple Icons CDN fetch via `<img>` tag with CSS filter for color, or inline SVG masked with CSS `mask-image`:

Use `<img>` approach with CSS invert/sepia filter to tint icons to `var(--ink)`:
```css
.social-icon { width: 28px; height: 28px; filter: invert(13%) sepia(30%) saturate(600%) hue-rotate(10deg) brightness(60%); }
```

Icons to implement:
| Link | Platform | Simple Icons slug | aria-label |
|------|----------|-------------------|------------|
| `ying.1.xiao@kcl.ac.uk` | Email | N/A (envelope SVG) | "Email Ying Xiao" |
| Google Scholar URL | googlescholar | `googlescholar` | "Google Scholar profile" |
| GitHub URL | github | `github` | "GitHub profile" |
| LinkedIn URL | linkedin | `linkedin` | "LinkedIn profile" |
| Xiaohongshu URL | rednote | `xiaohongshu` | "rednote profile" |

Email link uses generic envelope SVG (inline, not from Simple Icons).

---

## Phase 5 — News Section

**Task 5.1** Write `<section id="news">`:
- `<h2>News</h2>`
- Render as structured timeline `<ul class="news-list">` — each item is a `<li>` with date extracted as `<time>` element styled in `var(--ink-secondary)` and bold, followed by news text
- Items:
  1. "Dec 17th [2025]" — ICSE 2026 paper acceptance
  2. "Nov 22nd [2025]" — Philosophical Transactions acceptance
  3. "April 15th, 2024" — FSE 2024 acceptance
- List style: no bullet. Each item: `border-left: 3px solid var(--accent-light); padding-left: 1rem; margin-bottom: 1.25rem`
- Date: `display: block; font-size: 0.85rem; color: var(--ink-secondary); font-weight: 600; margin-bottom: 0.25rem`

---

## Phase 6 — Selected Publications Section

**Task 6.1** Write `<section id="publications">`:
- `<h2>Selected Publications</h2>`
- Render as ordered list `<ol class="pub-list">` — sequence conveys ranking/date order
- Each `<li>`: title in `<strong>`, authors in regular weight, venue as small badge
- Venue badge: `<span class="venue-badge">ICSE 2026 · Core A* · CCF-A</span>` styled as:
  ```css
  .venue-badge { font-size: 0.8rem; color: var(--accent); border: 1px solid var(--accent-light); border-radius: 3px; padding: 0.1rem 0.4rem; margin-left: 0.5rem; white-space: nowrap; }
  ```
- Items separated by `margin-bottom: 1.5rem`
- The `<ol>` has `list-style: none; padding: 0`; each item has left border accent: `border-left: 3px solid var(--accent-light); padding-left: 1rem`

Publications to render (5 items, in given order):
1. Fairness Is Not Just Ethical... (ICSE 2026)
2. Mitigating Medical Bias... (Phil. Trans. Royal Society A, JCR Q1)
3. Software Fairness Dilemma... (FSE, CCF-A)
4. MirrorFair... (FSE 2024, CCF-A)
5. A Comprehensive Study of Real-World Bugs... (ICSE 2023, CCF-A)

---

## Phase 7 — Preprints Section

**Task 7.1** Write `<section id="preprints">`:
- `<h2>Preprints</h2>`
- Render as `<ul class="pub-list">` (unordered — preprints have no formal ordering)
- Same styling as publications list items (left border, venue badge as "Preprint")
- Three items from page-story in given order

---

## Phase 8 — Invited Talk Section

**Task 8.1** Write `<section id="talks">`:
- `<h2>Invited Talk</h2>`
- Render as structured list `<ul class="talk-list">`:
  - Each item: year as `<time>` in `var(--ink-secondary)` bold, followed by talk description
  - Same left-border accent styling as news list
- Two items: 2026 London; 2024 Porto de Galinhas

---

## Phase 9 — Footer

**Task 9.1** Write `<footer>` outside `<main>`:
- Simple centered line: "© Ying Xiao" in `var(--ink-secondary)`, `font-size: 0.875rem`, `padding: 2rem`
- Top border: `1px solid var(--border)`

---

## Phase 10 — CSS Polish

**Task 10.1** Section heading styles (`<h2>`):
```css
h2 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--ink);
  letter-spacing: 0.02em;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}
```

**Task 10.2** Anchor link states:
```css
a { color: var(--accent); text-decoration: underline; text-underline-offset: 3px; }
a:hover { color: var(--ink); }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 2px; }
```

**Task 10.3** Section spacing:
```css
section { margin-bottom: 4rem; }
```

**Task 10.4** Clearfix for About Me float:
```css
.clearfix::after { content: ''; display: table; clear: both; }
@media (max-width: 480px) { .avatar { float: none; display: block; margin: 0 auto 1.5rem; } }
```

**Task 10.5** Responsive image handling: avatar `max-width: 140px` on desktop, `max-width: 100px` on mobile.

---

## Verification Checklist

Before marking complete:
- [ ] All interactive elements have `:hover` and `:focus-visible` states
- [ ] Typography: at least 3 distinct size/weight levels (name 3rem/700, h2 1.75rem/700, body 1.125rem/400)
- [ ] Spacing follows consistent rhythm (4/8px base, section gaps 4rem)
- [ ] Responsive: no horizontal scroll at 375px or 1200px
- [ ] Links section renders as icon links with aria-labels, not bare text
- [ ] Aesthetic (Editorial Serif, warm palette) visible in CSS — not generic defaults
- [ ] All page-story content preserved verbatim and in order
- [ ] No content promoted to hero/header badge beyond the `<header>` name block
