# 2026-03-15-ying-xiao-design.md

## Design Context

### Users

Academic peers, hiring committees, postdoctoral search committees, potential collaborators, and conference attendees. They arrive with a specific intent: to assess Ying Xiao's research profile, publication record, and expertise. Usage context is desktop-primary (faculty offices, research labs), though mobile review during conference browsing is common. The job to be done is fast, credible assessment: "Is this person the right fit for our lab / position / collaboration?"

### Brand Personality

Precise, rigorous, quietly confident. Three words: **Trustworthy · Focused · Substantive**. The emotional goal is quiet authority — the page should communicate depth without self-promotion, and signal that the work speaks for itself.

### Aesthetic Direction

Q1 selection: **Cool & minimal**. The visual tone is restrained and scholarly — generous whitespace, cool neutrals, monospace or clean sans-serif type. No decorative flourishes. The aesthetic communicates rigor and precision rather than creativity or warmth.

Q2 selection: **Terminal Scholar** — Monospace throughout, dark mode, command-line aesthetic.
`CSS: font-family: 'JetBrains Mono', monospace; background: #0d1117; color: #c9d1d9 · layout: sticky sidebar left, scrollable main right`

This style aligns the "cool & minimal" direction with the subject's technical identity (AI/ML/SE researcher), gives the page a distinctive character, and keeps the reading experience focused. The sticky sidebar provides persistent navigation context while the main column handles dense publication content.

Q3: Reference skipped.

Anti-references: Marketing-style hero images, gradient backgrounds, card-heavy layouts that fragment the reading flow, anything that feels like a startup landing page.

### Design Principles

1. **Content supremacy** — every design decision must serve legibility and content hierarchy, never decoration.
2. **Persistent orientation** — the reader should always know where they are in the page; the sticky sidebar is the primary navigation anchor.
3. **Typographic hierarchy over visual ornament** — differentiate sections via weight, size, and spacing, not colors or borders.
4. **Monospace precision** — the terminal aesthetic is a semantic signal: this is a systems thinker. Maintain it consistently.
5. **Minimal hover surface** — interactive states are subtle; underlines and mild opacity shifts only.

---

## Design System

### Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#0d1117` | Page background |
| `--surface` | `#161b22` | Sidebar background |
| `--border` | `#30363d` | Dividers, section separators |
| `--text-primary` | `#c9d1d9` | Body text |
| `--text-secondary` | `#8b949e` | Metadata, dates, secondary labels |
| `--text-accent` | `#58a6ff` | Links, active nav items |
| `--text-heading` | `#f0f6fc` | Section headings, name |
| `--badge-bg` | `#1f2937` | Publication venue badges |
| `--badge-text` | `#79c0ff` | Badge labels (Core A*, CCF-A) |

All values sourced from GitHub's dark mode palette — a known-good monochrome dark system with proven contrast ratios.

### Typography

**Font stack:** `'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace`

Loaded via Google Fonts CDN: `JetBrains Mono` (weights 400, 600).

| Level | Size | Weight | Line-height | Usage |
|-------|------|--------|-------------|-------|
| Name / H1 | `1.5rem` | 600 | 1.2 | Subject name |
| Section heading | `0.75rem` | 600 | 1.4 | `## Section` labels, uppercased, letter-spacing 0.12em |
| Body | `0.875rem` | 400 | 1.75 | About, publication entries |
| Small / meta | `0.75rem` | 400 | 1.5 | Dates, venue labels, secondary info |
| Nav items | `0.75rem` | 400 | 1.4 | Sidebar navigation links |

Note: ui-ux-pro-max recommends 16px minimum body for mobile. On mobile, the sidebar collapses and body text scales to `0.9375rem` (15px) — acceptable for a desktop-primary academic audience. A `font-size: 100%` base is set on `html` to respect browser preferences.

### Style

**Terminal Scholar** — dark monospace academic. CSS world defined by:

- Zero decorative borders except functional separators (`1px solid var(--border)`)
- No box shadows, no border-radius beyond `3px` on badges
- All whitespace from padding/margin only — no pseudo-element decorations
- Hover states: `color` shift to `--text-accent`, `opacity: 0.8` on secondary items

### Effects

- No blur, no gradients, no glassmorphism
- `transition: color 150ms ease, opacity 150ms ease` on interactive elements only
- `text-decoration: underline` on links within body prose; no underline on nav items (color differentiates)
- `::selection` background `#1f6feb` (GitHub blue selection)

### Anti-patterns

- No `border-radius > 4px` (softness contradicts the aesthetic)
- No warm colors in any context
- No hero section, no banner image
- No card-based layout (flat list rendering for publications)
- No decorative icons (only functional SVG icons in the Links section)

---

### Aesthetic Implementation

**Style chosen:** Terminal Scholar
**Q2 CSS signature:** `font-family: 'JetBrains Mono', monospace; background: #0d1117; color: #c9d1d9 · layout: sticky sidebar left, scrollable main right`

#### Layout structure

Two-column layout: sticky sidebar (left, fixed width) + scrollable main content (right, fills remaining space).

HTML skeleton:
```
<body>
  <div class="layout">
    <aside class="sidebar">        <!-- position: sticky; top: 0; height: 100vh; overflow-y: auto -->
      <nav class="sidebar-nav">   <!-- name, avatar, links, section anchors -->
    </aside>
    <main class="main-content">   <!-- flex: 1; overflow-y: auto; padding -->
      <!-- all page-story sections rendered sequentially -->
    </main>
  </div>
</body>
```

`body` is `display: flex` (or the `.layout` wrapper is). The sidebar is `position: sticky; top: 0; align-self: flex-start; height: 100vh; overflow-y: auto`. Main content scrolls independently.

On mobile (`max-width: 768px`): sidebar collapses — avatar, name, and links move inline above main content; nav anchors are hidden.

#### Surface treatment

- Sidebar: `background: var(--surface)` (`#161b22`), `border-right: 1px solid var(--border)`
- Main: `background: var(--bg)` (`#0d1117`)
- Publication venue badges: `background: var(--badge-bg); color: var(--badge-text); border-radius: 3px; padding: 1px 6px; font-size: 0.7rem`
- Section dividers: `border-top: 1px solid var(--border); margin: 2rem 0`
- No cards, no shadows

#### Typography expression

- Headings use `font-weight: 600`, uppercased (`text-transform: uppercase`), `letter-spacing: 0.12em`, `font-size: 0.75rem` — they read as labels, not loud titles
- Body text: `font-weight: 400`, `font-size: 0.875rem`, `line-height: 1.75`
- Name: `font-size: 1.5rem`, `font-weight: 600`, `color: var(--text-heading)`
- Ratio: heading label is quiet (0.75rem/600/uppercase) vs. body is readable (0.875rem/400/normal) — hierarchy through contrast of treatment, not size

#### Decorative rules

Present: monospace font universally, `--border` hairline separators between sections, colored badge chips for venue labels (Core A*, CCF-A, JCR Q1).

Forbidden: gradients, shadows, border-radius > 4px, warm tones, decorative pseudo-elements, icons as decoration.

#### Spatial rhythm

Compact-to-moderate. The terminal aesthetic is dense — content is the substance, whitespace is editorial restraint, not luxury. Section padding: `2rem 2.5rem` on main. Between publication entries: `1.25rem` gap. Between sections: `2.5rem`. Sidebar padding: `1.5rem 1.25rem`.

#### Signature CSS

```css
body {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  background: #0d1117;
  color: #c9d1d9;
}

.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  width: 240px;
  flex-shrink: 0;
  background: #161b22;
  border-right: 1px solid #30363d;
}

.main-content {
  flex: 1;
  min-width: 0;
  padding: 2rem 2.5rem;
}

.section-heading {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #8b949e;
  margin-bottom: 1rem;
}
```
