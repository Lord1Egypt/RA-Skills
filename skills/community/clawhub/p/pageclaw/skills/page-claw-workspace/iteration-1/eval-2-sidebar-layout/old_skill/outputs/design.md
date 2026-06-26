## Design Context

### Users

Academic peers (researchers, hiring committees, conference attendees) and potential postdoctoral employers. They arrive to quickly assess Ying Xiao's research profile, publication record, and fit for AI/ML research roles. Context: desktop-first but must work on mobile. Primary job: find publication list, assess seniority, locate contact info.

### Brand Personality

Scholarly, trustworthy, approachable. Three words: **Rigorous · Human · Warm**. The page should feel like a well-edited journal — serious enough for peer review committees, warm enough to convey the person behind the research. Emotional goal: confidence in competence, invitation to connect.

### Aesthetic Direction

**Q1 — Visual direction chosen: Warm & editorial**

Warm amber-adjacent neutrals, serif typography for headings, generous whitespace. The page reads like a high-quality academic journal or a personal essay. No cold blue-grey startup aesthetics. No dark mode (academic hiring committees expect light, readable pages).

**Q2 — Aesthetic style chosen: Editorial Serif**

> **Editorial Serif** — Long-form reading experience, large serif headings, ink-on-paper warmth; feels like a well-typeset academic monograph.
> `CSS signature: font-family: 'Playfair Display', serif; color: #2C1A0E; background: #FDFAF6`

Rationale: This aesthetic pairs with "Warm & editorial" most authentically. It is a full-width, vertically-stacked reading layout — not a sidebar design. The warmth comes from off-white parchment background and dark brown ink tone.

**Anti-references:** Cold tech portfolios, neon-on-dark developer pages, sidebar-heavy academic templates (e.g., standard Jekyll/Hugo academic themes).

**Reference design:** Skipped.

### Design Principles

1. **Content fidelity** — Render the page-story faithfully; do not add, remove, or reorder sections. The About Me, News, Publications, Preprints, Invited Talk sections appear in their given sequence.
2. **Typography as hierarchy** — Three distinct levels: large serif display headings (name/section heads), medium serif subheadings, and readable 18px body text. No reliance on color alone for hierarchy.
3. **Warmth through restraint** — Amber/parchment palette; decoration is only a thin rule or warm accent color. No illustrations, no gradient fills, no shadows beyond hairline.
4. **Links as icons** — The Links section renders as icon-based social links (inline SVG from Simple Icons CDN), not bare text URLs.
5. **Responsive without compromise** — Single-column vertical flow makes the page work perfectly at 375px and 1440px without layout gymnastics.

---

## Design System

### Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#FDFAF6` | Page background (warm parchment) |
| `--surface` | `#F7F2EB` | Card/section backgrounds |
| `--ink` | `#2C1A0E` | Primary text (dark warm brown) |
| `--ink-secondary` | `#6B4F3A` | Secondary text, metadata |
| `--accent` | `#B5470B` | Links, accent rules, badge borders |
| `--accent-light` | `#EDD9C8` | Subtle highlight backgrounds |
| `--border` | `#D9CCBE` | Hairline dividers |
| `--white` | `#FFFFFF` | Icon fill, inverted text |

### Typography

**Heading font:** Playfair Display (Google Fonts) — serif, high contrast strokes, classic editorial
**Body font:** Source Serif 4 (Google Fonts) — readable at small sizes, warm texture

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| Name / Page Title | 3rem / 48px | 700 | `<h1>` |
| Section Headings | 1.75rem / 28px | 700 | `<h2>` |
| Subheadings | 1.125rem / 18px | 600 | `<h3>`, publication year |
| Body | 1.125rem / 18px | 400 | Prose paragraphs |
| Caption / Meta | 0.875rem / 14px | 400 | Dates, venue labels |

Line-height: 1.7 for body, 1.2 for headings. Max-width: 720px centered.

### Aesthetic Implementation

**Aesthetic: Editorial Serif**

- **Surface treatment** — No card borders or shadows. Section separation via a `1px solid var(--border)` horizontal rule and `3rem` vertical spacing. Publication items use a thin left border: `border-left: 3px solid var(--accent-light); padding-left: 1rem`.
- **Typography expression** — Heading weight contrast is strong: 700 serif headings vs 400 serif body. Scale ratio ≈ 1.56× between levels. Letter-spacing on `<h2>`: `0.04em`. Body letter-spacing: default (0).
- **Decorative rules** — Thin `1px` horizontal rules (`<hr>`) between major sections. Section heading has a short `3px` warm accent underline via `::after` pseudo-element (width: 2rem). No drop shadows, no gradients, no rounded corners on containers.
- **Spatial rhythm** — Airy: `5rem` between sections, `2rem` between list items, `1.5rem` internal paragraph spacing. Page padding: `2rem` on mobile, `4rem` on desktop.
- **Signature CSS:**
  ```css
  font-family: 'Playfair Display', Georgia, serif;       /* headings */
  font-family: 'Source Serif 4', 'Georgia', serif;       /* body */
  background: #FDFAF6;
  color: #2C1A0E;
  max-width: 720px;
  margin: 0 auto;
  ```

### Effects

- Hover on links: `color: var(--accent)` transition `150ms ease`.
- Hover on icon links: `opacity: 0.75` transition `150ms ease`.
- Focus-visible: `outline: 2px solid var(--accent); outline-offset: 3px`.
- No box-shadow, no blur, no animation beyond hover/focus transitions.

### Anti-patterns for this aesthetic

- No grid or flex column layouts that divide the page into sidebar + content
- No rounded cards with shadows
- No dark mode toggle
- No hero image header
- No background gradients
- No emoji icons
