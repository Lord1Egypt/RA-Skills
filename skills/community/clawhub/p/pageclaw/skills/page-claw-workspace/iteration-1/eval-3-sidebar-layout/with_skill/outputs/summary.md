# Pipeline Run Summary

**Source:** `skills/pageclaw-test/fixtures/page-story-test.md`
**Subject:** Ying Xiao — PhD Candidate, King's College London
**Date:** 2026-03-15

---

## 1. Which Q2 option was chosen and what layout descriptor it had

**Option chosen:** Brutalist Academic

**Layout descriptor (from Q2 CSS signature):**
`layout: asymmetric two-column grid, sticky sidebar left, content bleed right`

The four Q2 options generated for an academic researcher page + Bold & Expressive Q1 direction were:
1. Brutalist Academic — `asymmetric two-column grid, sticky sidebar left` ← **chosen**
2. Glassmorphism Scholar — `stacked frosted cards, single centered column`
3. Terminal Scholar — `sticky sidebar left, scrollable main right, dark mode`
4. Museum Whitespace — `narrow single column, wide margins, content as artifact`

Brutalist Academic was selected as the most unexpected/bold direction for an academic page — it applies the structural vocabulary of counter-culture web design (no border-radius, no shadows, stark 3px borders, uppercase section headings) to a scholarly CV, which conventionally renders as a single-column minimalist page.

---

## 2. Does the HTML actually reflect the bold/asymmetric layout?

Yes — the HTML directly implements the asymmetric two-column grid specified in the Q2 layout descriptor.

Specific structural evidence in `index.html`:

- `div.page-grid` uses `display: grid; grid-template-columns: 240px 1fr` — a fixed 240px sidebar column and a fluid main column.
- `aside.sidebar` is `position: sticky; top: 0; height: 100vh` — the sidebar locks in place while the main content scrolls.
- The sidebar has `border-right: 3px solid var(--color-border)` — the primary structural divider.
- `border-radius: 0 !important` and `box-shadow: none !important` applied globally in reset — no softening anywhere.
- Section headings are `text-transform: uppercase; letter-spacing: 0.08em` — raw typographic authority.
- Publication entries use `border-left: 3px solid transparent` that reveals `var(--color-accent)` on hover — the only decorative element, and only on interaction.
- News and talk sections use a two-column `grid-template-columns: 90px 1fr` inner grid — monospace date/year badges in accent color on the left, content on the right. This is a deliberate structural pattern, not prose.
- IBM Plex Mono used for date badges and year labels — reinforces the reading-machine aesthetic.

The layout does not default to single-column anywhere on desktop. The asymmetry is structural, not decorative.

---

## 3. How visually distinct is this from a typical single-column academic page?

Substantially different on every dimension that defines conventional academic pages:

| Dimension | Typical academic page | This page |
|-----------|----------------------|-----------|
| Layout | Single centered column, max-width ~700px | Asymmetric two-column grid (240px sidebar + fluid main) |
| Sidebar | None | Sticky left sidebar with name, nav anchors, icon links |
| Typography | Serif body, neutral headings | Space Grotesk display, uppercase section headings, IBM Plex Mono for data labels |
| Borders | None or thin decorative | 3px solid structural borders everywhere — sidebar divider, section separators |
| Border radius | Rounded profile image, rounded cards | Zero border-radius globally |
| Shadows | Subtle card shadows | No shadows anywhere |
| Color | Grey/beige academic palette, blue links | Black/white ground with single electric blue accent (#0047FF), only on interactive states |
| Publication items | Plain paragraph or list items | Left-border reveal on hover, monospace venue badges, author self-emphasis with underline |
| Links section | Bare text links | Icon-based SVG links in sidebar |
| News section | Bulleted list | Timeline grid layout with monospace date badges |
| Avatar | Circular, soft shadow | Square, 3px solid border — matches the aesthetic vocabulary |

A visitor arriving from a standard academic homepage (e.g., a typical university faculty page) would immediately register this as structurally and aesthetically different — the sticky sidebar alone creates a navigation behavior absent from single-column pages, and the brutalist visual language signals intent rather than convention.
