# 2026-03-15-ying-xiao-design.md

## Pipeline Context

**Source:** `skills/pageclaw-test/fixtures/page-story-test.md`
**Subject:** Ying Xiao — PhD researcher, King's College London
**Date:** 2026-03-15

---

## User Choices (Simulated)

### Q1 — Visual Direction

Options presented:
1. **Clean & Academic** — Warm whitespace, serif body, restrained academic tone
2. **Cool & Minimal** — Refined sans-serif, generous margins, pure white ground
3. **Bold & Expressive** — High-contrast, strong typographic punch, personality-forward ← **Selected**
4. **Warm & Editorial** — Magazine-editorial feel, warm tones, curated reading experience

**Choice:** Bold & Expressive — most bold/unexpected direction for an academic page.

---

### Q2 — Aesthetic Style (generated for academic researcher + Bold & Expressive direction)

1. **Brutalist Academic** — Raw grid, stark black-on-white contrast, reading-machine feel with intentional friction.
   `CSS: border: 3px solid currentColor; border-radius: 0; box-shadow: none · layout: asymmetric two-column grid, sticky sidebar left, content bleed right`

2. **Glassmorphism Scholar** — Frosted-glass panels, layered translucency, cool blue tones evoking precision instruments.
   `CSS: backdrop-filter: blur(12px); background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.3) · layout: stacked frosted cards, single centered column`

3. **Terminal Scholar** — Monospace throughout, dark mode, command-line aesthetic that signals systems-thinking.
   `CSS: font-family: 'JetBrains Mono', monospace; background: #0d1117; color: #c9d1d9 · layout: sticky sidebar left, scrollable main right`

4. **Museum Whitespace** — Extreme negative space, caption-driven, artifact-display feel — each publication rendered as an exhibit.
   `CSS: padding: 5rem 6rem; max-width: 640px; font-size: 0.85rem · layout: narrow single column, wide margins, content as artifact`

**Choice:** **Brutalist Academic** — most unexpected for an academic page; asymmetric two-column grid breaks the single-column academic norm most radically.

---

### Q3 — Reference Design

**Response:** Skip
No reference URL provided. No reference signals extracted.

---

## Design Context

### Users

**Primary audience:** Academic hiring committees, postdoc search committees, faculty members, and research collaborators scanning the page to evaluate Ying Xiao as a postdoctoral candidate.
**Secondary audience:** Peer researchers in AI fairness, SE4AI, and AI4Healthcare who want to quickly survey publications.
**Context of use:** Desktop browser, typically during a search session; the user has likely arrived from a paper citation, a LinkedIn link, or a CV link. They need to quickly assess credibility, recency of work, and research focus.
**Job to be done:** Confirm that the researcher is credible, active, and relevant — then find a way to reach them.

### Brand Personality

**Three words:** Rigorous · Unconventional · Precise
**Voice:** Confident but evidence-grounded. The page does not need to sell — it needs to substantiate.
**Emotional goal:** Readers should feel the researcher is serious without being stiff — someone at the intersection of technical depth and ethical urgency.
**Anti-references:** Generic WordPress academic templates; pastel-washed portfolio sites; anything that visually implies "I filled in a form."

### Aesthetic Direction

**Visual tone:** High-contrast, typographic authority. Black and white ground with a single punchy accent. The brutalist direction signals that the researcher is not beholden to convention — appropriate for work in AI ethics and bias mitigation.
**Style choice:** Brutalist Academic
**Layout:** Asymmetric two-column grid — a fixed-width sticky sidebar (left) holds identity + links + navigation anchors; a wider scrollable main column (right) holds all content sections.
**Anti-references:** Rounded cards with drop shadows, gradient hero sections, pastel color schemes, centered single-column layouts.
**Theme:** Light mode, black/white ground, one accent color (a sharp electric blue or signal red).

### Design Principles

1. **Structure is the aesthetic.** Decoration is absent. The grid itself, the border rules, and the typography scale carry all visual weight.
2. **Hierarchy through contrast, not color.** Section heads are bold and large; publication titles are medium; author lists and venues are small and muted. Color is used only for interactive states and the accent element.
3. **Sidebar as navigation scaffold.** The sticky left column allows fast scanning without scrolling — the reader can orient at a glance.
4. **Content fidelity above all.** Every word from the page-story is rendered as-is. No paraphrasing, no reordering, no promotion of elements out of their original section.
5. **Accessible brutalism.** Raw aesthetics do not mean inaccessible ones. All contrast ratios meet WCAG AA (4.5:1 minimum). Focus states are visible and explicit.

---

## Design System

### Color Palette

| Token | Value | Use |
|-------|-------|-----|
| `--color-ink` | `#0A0A0A` | Primary text, borders |
| `--color-ground` | `#FAFAFA` | Page background |
| `--color-muted` | `#555555` | Secondary text (venues, dates, co-authors) |
| `--color-accent` | `#0047FF` | Interactive links, hover states, active anchor |
| `--color-border` | `#0A0A0A` | All structural borders (3px solid) |
| `--color-surface` | `#F0F0F0` | Sidebar background |
| `--color-tag-bg` | `#0A0A0A` | Badge/tag background |
| `--color-tag-fg` | `#FAFAFA` | Badge/tag text |

### Typography

**Font pairing:** `Space Grotesk` (headings) + `IBM Plex Mono` (name/code elements) + `Inter` (body)
— All loaded from Google Fonts / CDN.

| Scale | Element | Size | Weight | Transform |
|-------|---------|------|--------|-----------|
| `--text-display` | Name h1 | `2.5rem` | `800` | none |
| `--text-heading` | Section h2 | `1.25rem` | `700` | uppercase, letter-spacing 0.08em |
| `--text-subhead` | Paper titles | `1rem` | `600` | none |
| `--text-body` | About me, news items | `0.9375rem` (15px) | `400` | none |
| `--text-meta` | Authors, venues, dates | `0.8125rem` (13px) | `400` | none |
| Line height (body) | — | — | — | `1.65` |

### Spacing Scale (4px base)

`4px · 8px · 12px · 16px · 24px · 32px · 48px · 64px · 96px`

| Token | Value |
|-------|-------|
| `--space-xs` | `4px` |
| `--space-sm` | `8px` |
| `--space-md` | `16px` |
| `--space-lg` | `24px` |
| `--space-xl` | `48px` |
| `--space-2xl` | `96px` |

### Layout Structure

**Layout pattern:** Asymmetric two-column grid (CSS Grid)

```
+------------------+-----------------------------------------------+
|  SIDEBAR (240px) |  MAIN CONTENT (flex: 1, max readable width)   |
|  position: sticky|                                               |
|  top: 0          |  ## About Me                                  |
|  height: 100vh   |  ## News                                      |
|                  |  ## Selected Publications                     |
|  [Name]          |  ## Preprints                                 |
|  [Position]      |  ## Invited Talk                              |
|  [Institution]   |                                               |
|  ────────────    |                                               |
|  [Nav anchors]   |                                               |
|  ────────────    |                                               |
|  [Icon links]    |                                               |
+------------------+-----------------------------------------------+
```

- Sidebar width: `240px` fixed, `background: var(--color-surface)`, `border-right: 3px solid var(--color-border)`
- Main column: `min-width: 0`, padded `40px 48px`
- Page wrapper: `display: grid; grid-template-columns: 240px 1fr; min-height: 100vh`
- On mobile (≤768px): sidebar collapses to top header strip; main fills full width

### Surface Treatment

```css
/* Brutalist: no border-radius, no box-shadow, no gradient */
border-radius: 0;
box-shadow: none;
border: 3px solid var(--color-border);
background: transparent;
```

Sections are separated by a full-width `3px solid` rule, not cards or shadows.

Publication entries use a left `4px solid var(--color-accent)` border on hover only — the only decorative touch.

### Decorative Rules

**Present:**
- Full-width `border-bottom: 3px solid` between every major section
- `3px solid` right border on sidebar
- Section `h2` in uppercase with letter-spacing
- A single `--color-accent` used only for interactive states (link hover, active nav anchor, publication left-border hover)

**Forbidden:**
- Border-radius (anywhere)
- Box-shadow
- Gradient backgrounds
- Decorative imagery or illustrations
- Rounded chips or pill badges

### Spatial Rhythm

**Density disposition:** Dense-readable. Content is compact but not cramped. Section gaps are `48px`; internal publication gaps are `24px`. Sidebar has tighter internal rhythm at `16px`. The overall feel is a printed journal layout — not airy, but not suffocating.

### Aesthetic Implementation

This section translates the **Brutalist Academic** Q2 choice into concrete CSS patterns for the build step.

**Layout structure:** The HTML skeleton is a two-column CSS Grid: `grid-template-columns: 240px 1fr`. The left column (sidebar `<aside>`) is `position: sticky; top: 0; height: 100vh; overflow-y: auto`. The right column (`<main>`) scrolls normally. This is the defining structural gesture of this aesthetic.

**Surface treatment:**
```css
/* Global reset for brutalist aesthetic */
*, *::before, *::after { border-radius: 0 !important; box-shadow: none !important; }
body { background: var(--color-ground); color: var(--color-ink); }
aside { background: var(--color-surface); border-right: 3px solid var(--color-border); }
section { border-top: 3px solid var(--color-border); padding-top: var(--space-xl); margin-top: var(--space-xl); }
```

**Typography expression:**
```css
h1 { font-family: 'Space Grotesk', sans-serif; font-size: 2.5rem; font-weight: 800; line-height: 1.1; }
h2 { font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 700;
     text-transform: uppercase; letter-spacing: 0.08em; }
body { font-family: 'Inter', sans-serif; font-size: 0.9375rem; line-height: 1.65; }
.meta { font-size: 0.8125rem; color: var(--color-muted); }
```

**Decorative rules:** Only `3px solid` borders and a single accent color. No shadows. No gradients. No rounded corners.

**Spatial rhythm:** `section + section` gap `48px`; publication item gap `24px`; sidebar internal gap `16px`; body padding `40px 48px`.

**Signature CSS (fingerprint of Brutalist Academic):**
```css
border-radius: 0;
border: 3px solid currentColor;
box-shadow: none;
font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; /* section headings */
transition: none; /* or border-color 0.1s for hover only */
```

### Effects and Animation

**Minimal, intentional:**
- Link hover: `color: var(--color-accent)` only, no underline animation. `transition: color 80ms`
- Nav anchor active: `border-left: 3px solid var(--color-accent); background: rgba(0,71,255,0.06)`
- Publication hover: `border-left: 4px solid var(--color-accent)` — a single decorative reveal
- No scroll animations, no entrance animations, no parallax

### Anti-Patterns to Avoid

- Rounded corners anywhere
- Drop shadows or box-shadows
- Gradient backgrounds
- More than one accent color
- Large hero banner or hero image section
- Animated background patterns
- Centered single-column layout (defeats the purpose of the asymmetric grid)
