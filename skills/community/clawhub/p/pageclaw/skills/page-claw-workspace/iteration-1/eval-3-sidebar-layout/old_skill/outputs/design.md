# 2026-03-15-ying-xiao-design.md

## Design Context

### Users

Primary audience: hiring committees at research institutions and universities seeking candidates for postdoctoral positions in AI agents, AI alignment, SE4AI, and AI4Healthcare. Secondary audience: academic peers, conference attendees, and collaborators. Visitors arrive with task-oriented intent — they want to assess publication record, research focus, and institutional affiliations quickly. Context is typically desktop-first (CV review during a hiring process), with some mobile browsing from conference settings.

### Brand Personality

Three-word personality: **rigorous, trustworthy, precise**. Emotional goal: instill confidence in the depth of Ying Xiao's research output and the seriousness of her work on trustworthy AI. Tone is formal-academic but not cold — the job-market call-out signals urgency and directness. The page must not feel generic or template-like; it should feel authored.

### Aesthetic Direction

Visual direction: **High-contrast & typographic** — the design leans hard into text as structure. Type carries hierarchy. No decorative imagery. The page is a reading machine: dense information rendered with precision. Anti-reference: soft pastel academic pages, gradient hero sections, stock-photo backgrounds.

Aesthetic style: **Terminal Scholar** — monospace throughout, dark mode, command-line aesthetic. The unexpected direction for an academic page. Treats the page like a terminal session: fixed-width typeface, high-contrast white-on-dark, sparse color accents (only for structural cues), no rounded corners, no shadows. Publication entries read like log lines.

### Design Principles

1. **Typography is the layout** — hierarchy is established entirely through font size, weight, and letter-spacing. No decorative dividers or cards.
2. **Information density by design** — publications, news, and talks are presented at high density; every line earns its space.
3. **Signal over decoration** — venue badges (CCF-A, Core A*, Q1) are the only allowed color accents; they carry semantic weight.
4. **Structural honesty** — the page renders exactly the page-story content, in order, with no reinterpretation.
5. **Accessible contrast first** — dark background demands careful contrast validation; all text must meet WCAG AA minimum.

---

## Design System

### Pattern

Single-column reading layout with a narrow fixed header containing name + navigation anchors. Content flows top-to-bottom in document order matching the page-story. No sidebar, no multi-column grid. The terminal aesthetic means everything aligns to a monospace grid rhythm.

### Style

**Terminal Scholar**
- Dark mode only
- Monospace typeface throughout (heading and body)
- High-contrast white/near-white on very dark background
- No border-radius on any element
- No box-shadow
- Color used only for semantic badges and link hover states

### Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#0d1117` | Page background |
| `--surface` | `#161b22` | Section backgrounds, subtle separations |
| `--border` | `#30363d` | Horizontal rules, dividers |
| `--text-primary` | `#e6edf3` | Body text, paragraphs |
| `--text-secondary` | `#8b949e` | Author lists, secondary metadata |
| `--text-accent` | `#58a6ff` | Links, hovered states, anchor nav |
| `--badge-ccf` | `#1f6feb` | CCF-A / Core A* badge background |
| `--badge-ccf-text` | `#cae8ff` | Badge text |
| `--badge-q1` | `#388bfd` | JCR Q1 badge background |
| `--badge-q1-text` | `#cae8ff` | Badge text |
| `--news-bullet` | `#3fb950` | News bullet / timeline marker |

### Typography

**Typeface**: `JetBrains Mono`, fallback `'Courier New', monospace` — both heading and body.

| Level | Size | Weight | Letter-spacing |
|-------|------|--------|----------------|
| Name / H1 | `2rem` (32px) | `700` | `0.02em` |
| Section heading H2 | `1.125rem` (18px) | `700` | `0.1em` uppercase |
| Pub title | `0.9375rem` (15px) | `600` | `0` |
| Body / metadata | `0.875rem` (14px) | `400` | `0` |
| Badge label | `0.6875rem` (11px) | `700` | `0.05em` uppercase |

Line-height: `1.7` for body paragraphs; `1.4` for compact list items.

### Effects

- No shadows
- No blur
- No border-radius
- Hover on links: color shifts from `--text-primary` to `--text-accent`, no underline by default, underline on hover
- Focus-visible: `outline: 2px solid #58a6ff; outline-offset: 2px`
- Section entries use a subtle left border `3px solid #30363d` that turns `#58a6ff` on hover for publications/preprints

### Anti-patterns

- No gradient backgrounds
- No card elevation (box-shadow)
- No sans-serif typeface anywhere
- No hero section or avatar-in-circle framing
- No decorative icons or illustrations
- No animation beyond color transitions (150ms ease)

---

### Aesthetic Implementation

**Surface treatment**
```css
/* Sections: flat dark surfaces, no radius, no shadow */
section {
  background: #161b22;
  border-top: 1px solid #30363d;
  border-radius: 0;
  box-shadow: none;
}
/* Publication / preprint entries */
.entry {
  border-left: 3px solid #30363d;
  padding-left: 1rem;
  transition: border-color 150ms ease;
}
.entry:hover {
  border-color: #58a6ff;
}
```

**Typography expression**
```css
/* All text: monospace — heading and body share the same family */
* { font-family: 'JetBrains Mono', 'Courier New', monospace; }
h1 { font-size: 2rem; font-weight: 700; letter-spacing: 0.02em; }
h2 { font-size: 1.125rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }
/* Weight ratio: headings 700, body 400 — reinforced by uppercase treatment */
```

**Decorative rules**
- Permitted: horizontal rules (`border-top: 1px solid #30363d`), left-border accent on entries
- Forbidden: gradients, shadows, rounded corners, illustrations, decorative SVG patterns

**Spatial rhythm**
- Dense-but-breathable: compact publication lists, generous section padding
- Vertical section spacing: `padding: 2.5rem 0`
- Entry gap: `margin-bottom: 1.25rem`
- Max content width: `720px`, centered

**Signature CSS** (fingerprint of Terminal Scholar aesthetic)
```css
font-family: 'JetBrains Mono', 'Courier New', monospace;
background: #0d1117;
color: #e6edf3;
border-radius: 0;
box-shadow: none;
```
