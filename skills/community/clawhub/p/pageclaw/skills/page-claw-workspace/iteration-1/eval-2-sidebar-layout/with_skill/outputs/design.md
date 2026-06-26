# 2026-03-15-ying-xiao-design.md

## User Selections

- **Q1 (Visual direction):** Warm & editorial
- **Q2 (Aesthetic style):** Warm Paper — *see full descriptor below*
- **Q3 (Reference design):** Skip

### Q2 Choice Detail

**Warm Paper** — Aged paper warmth, generous whitespace, serif body text, editorial typographic hierarchy; feels like a curated print journal brought online.
`CSS: background: #faf7f2; font-family: 'Lora', Georgia, serif; border-bottom: 1px solid #e8ddd0 · layout: single centered column, stacked content cards, wide comfortable margins`

---

## Design Context

### Users

Academic peers, potential postdoctoral supervisors, hiring committees at universities and research labs, and conference collaborators. They arrive with a professional intent: to quickly evaluate Ying Xiao's research profile, publication record, and whether she is a fit for an open postdoc position. Context is typically desktop or laptop, during focused research or hiring evaluation. They expect credibility signals (venue names, co-authors, institutional affiliations) to be immediately scannable.

### Brand Personality

Rigorous, warm, trustworthy. Three words: **precise · approachable · credible**. The emotional goal is quiet confidence — a researcher who is serious about her work but accessible as a collaborator. The page should feel like a well-edited academic CV turned into a living profile, not a flashy portfolio.

### Aesthetic Direction

Warm & editorial. Think: the warmth of aged paper, the clarity of a well-typeset journal article, generous whitespace, and a serif-forward typographic system. No decorative flourishes beyond subtle ruled lines. The palette is cream/off-white with warm brown-gray accents. Anti-references: cold blue-white tech portfolios, neon accents, heavy card shadows, sidebar navigation grids.

### Design Principles

1. **Content legibility first** — Typography choices and spacing must serve long-form reading, not visual spectacle.
2. **Credibility through restraint** — Venue names (ICSE, FSE, Royal Society) are the strongest visual elements; do not compete with them.
3. **Warm but professional** — The color temperature tilts warm, but the overall register remains formal.
4. **Faithful to the page-story** — No content reordering, no section promotion. Hero is not a separate zone.
5. **Progressive disclosure** — News items and publications are scannable lists; the reader decides depth.

---

## Design System

### Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--color-bg` | `#faf7f2` | Page background (warm off-white / aged paper) |
| `--color-surface` | `#f5f0e8` | Card / section surface |
| `--color-border` | `#e8ddd0` | Horizontal rules, card borders |
| `--color-text-primary` | `#2c2420` | Body text, headings |
| `--color-text-secondary` | `#6b5c52` | Captions, metadata, secondary labels |
| `--color-accent` | `#8b4513` | Links on hover, section anchors, badge borders |
| `--color-accent-muted` | `#c4956a` | Subtle inline accents, icon fills |
| `--color-badge-bg` | `#ede6da` | Badge / tag background |

### Typography

| Element | Font | Size | Weight | Line-height |
|---------|------|------|--------|-------------|
| Display / Name | Lora (serif) | 2.4rem | 700 | 1.15 |
| Section headings (h2) | Lora (serif) | 1.4rem | 600 | 1.3 |
| Body text | Lora (serif) | 1.05rem | 400 | 1.75 |
| Metadata / labels | Source Sans 3 (sans) | 0.85rem | 500 | 1.4 |
| Links / nav | Source Sans 3 (sans) | 0.9rem | 500 | — |

Font pairing rationale: Lora for warmth and editorial credibility in prose; Source Sans 3 for metadata clarity without coldness.

Google Fonts import:
```
Lora:ital,wght@0,400;0,600;0,700;1,400&Source+Sans+3:wght@400;500;600
```

### Spacing Scale (8pt base)

| Token | Value |
|-------|-------|
| `--space-xs` | 4px |
| `--space-sm` | 8px |
| `--space-md` | 16px |
| `--space-lg` | 32px |
| `--space-xl` | 64px |
| `--space-2xl` | 96px |

### Aesthetic Implementation

#### Layout structure

Single centered column, stacked content cards. The HTML skeleton is:

```
<body>                                     ← bg: #faf7f2
  <header>                                 ← name + tagline, full-width top
  <main class="column">                    ← max-width: 720px, margin: 0 auto, padding: 0 2rem
    <section class="about-card">           ← stacked card, border-bottom separator
    <section class="links-card">           ← icon row
    <section class="news-card">            ← stacked list items
    <section class="publications-card">    ← stacked list items
    <section class="preprints-card">       ← stacked list items
    <section class="talks-card">           ← stacked list items
  </main>
  <footer>                                 ← minimal, centered
```

No sidebar. No two-column grid. All sections stack vertically in a single reading lane. Cards are separated by `border-bottom: 1px solid var(--color-border)` rather than box-shadow elevation.

#### Surface treatment

```css
.section-card {
  background: transparent;           /* cards inherit page bg, no panel lift */
  border-bottom: 1px solid var(--color-border);
  border-radius: 0;
  box-shadow: none;
  padding: var(--space-lg) 0;
}
```

No shadow-based elevation. Sections are delimited by thin warm ruled lines, consistent with the editorial print metaphor.

#### Typography expression

- **Headings vs body contrast**: Lora Bold (700) at 2.4rem for name; Lora SemiBold (600) at 1.4rem for section headers; Lora Regular (400) at 1.05rem for all prose
- **Section header style**: all-caps tracking with Source Sans 3, `font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--color-text-secondary)`
- **Weight ratio**: 700 : 400 — clear separation; no medium weight overuse

#### Decorative rules

Present:
- Thin horizontal ruled lines (`border-bottom: 1px solid var(--color-border)`) as section dividers
- Section labels in small-caps uppercase Source Sans 3
- Warm accent color on link hover (`color: var(--color-accent)`)
- Publication venue badges: `background: var(--color-badge-bg); border: 1px solid var(--color-border); border-radius: 3px; padding: 2px 7px; font-size: 0.78rem`

Forbidden:
- Box shadows on cards
- Border-radius > 4px on any element
- Gradients
- Bold color blocks or hero backgrounds
- Decorative illustrations or background textures
- Sidebar or multi-column layout

#### Spatial rhythm

Airy. Section padding: `var(--space-lg)` (32px) top and bottom. Between list items within a section: `var(--space-md)` (16px). The single column with `max-width: 720px` and generous side margins produces a reading experience comparable to a typeset academic journal page.

#### Signature CSS

```css
/* 1. Warm paper background — the unmistakable ground */
body {
  background: #faf7f2;
  color: #2c2420;
}

/* 2. Serif editorial body — the unmistakable type texture */
body, p, li {
  font-family: 'Lora', Georgia, serif;
  font-size: 1.05rem;
  line-height: 1.75;
}

/* 3. Thin ruled section dividers — print metaphor */
.section-card {
  border-bottom: 1px solid #e8ddd0;
}

/* 4. Small-caps section labels — editorial categorization */
.section-label {
  font-family: 'Source Sans 3', sans-serif;
  font-size: 0.75rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #6b5c52;
}

/* 5. Warm link hover — the only color moment */
a:hover {
  color: #8b4513;
  text-decoration: underline;
}
```

### Anti-patterns to avoid

- No sidebar layout (would conflict with chosen aesthetic)
- No CSS grid with asymmetric columns
- No glassmorphism, frosted panels, or backdrop-filter
- No dark mode (single warm light mode)
- No emoji — use inline SVG icons only
- No `box-shadow` on content cards
- No color backgrounds on sections
