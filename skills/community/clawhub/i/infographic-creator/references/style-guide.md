# Modern operator-style infographic — design system

Reverse-engineered from a wide sample of high-engagement product/founder infographics on LinkedIn and Twitter. The look is clean, "operator-friendly," scannable on a phone in 3 seconds, dense with structure but never cluttered.

This guide is the source of truth for what makes an infographic feel intentional rather than AI-generated. Internalize the invariants, then pick the right layout.

---

## The 4 invariants

Every infographic produced with this system MUST have these four things. Skip any one and the brand identity collapses.

1. **Big bold black sans-serif title** + a **handwritten subtitle** in the user's accent color underneath.
2. **Two emojis flanking the title** (one top-left, one top-right). One literal, one emotional. 3D Apple-style — never flat.
3. **A single accent color carries the piece** — frame, accent words in the title, subtitle, hand-drawn arrows. Pick one and commit. The accent color is configured per-user in `style.json`; never hardcode.
4. **Author signature footer**: dark rounded pill at bottom-center with a small circular avatar + the user's handle. Anchors the post as theirs.

---

## Color tokens

The accent color is variable. The other tokens are fixed across the system.

| Token | Hex | Purpose |
|---|---|---|
| `bg.default` | `#FFFFFF` | Card background |
| `bg.dark` | `#0E0E0E` | Black pills, signature footer, emphasis tags |
| `ink.title` | `#0E0E0E` | Title + body text |
| `ink.handwritten` | *user-derived* | Handwritten subtitle, annotations — ~25% darker than the accent |
| `accent.primary` | *user-chosen* | Frame, accent words, primary pills (e.g. `#006EFF` blue, `#7C6BFF` purple, `#FF6B35` orange, `#16A34A` green) |
| `accent.alt` | `#F26B2A` | Optional secondary accent for skills/tools content |
| `state.good` | `#16A34A` | ✅ rows, "after" panels, positive verdict |
| `state.bad` | `#DC2626` | ❌ rows, "before" panels, negative verdict |
| `state.warn` | `#F59E0B` | ⚠ row labels, "tie" badges |
| `panel.lavender` | derived from accent | Soft fill behind grouped content (e.g. `#E5EFFF` for blue accent) |
| `panel.cream` | `#FFF7E6` | Definition / takeaway / "golden rule" callout boxes |
| `panel.mint` | `#E7F6EC` | "Why it works" / final-insight panels |
| `panel.coral` | `#FBE4E4` | Negative-example backgrounds |
| `border.thin` | `#E5E5EA` | 1px row dividers in tables |
| `border.frame` | *= accent.primary* | 2px outer frame on the whole canvas |

To derive `ink.handwritten` from the accent: drop lightness by ~25% (e.g. `#006EFF` → `#0050CC`, `#7C6BFF` → `#5B4FE9`).

To derive `panel.lavender` from the accent: lift lightness so it reads as a very pale wash (e.g. `#006EFF` → `#E5EFFF`).

---

## Typography

- **Title**: bold sans-serif (Inter Black / Manrope ExtraBold), ~64–80px, black. Max 6 words. Often broken across 2 lines. Sometimes one word in a black "code pill" — that pill uses a monospace or pixel font.
- **Subtitle**: handwritten script (Caveat / Patrick Hand / Kalam), ~28px, in the derived handwritten color. 1–2 lines, conversational.
- **Body**: clean sans (Inter / Manrope), 14–18px, black or dark gray.
- **Pills**: black rounded-full, white text, sans 14px bold. Used as column headers in tables, section dividers, brand series tags.
- **Numbered tags**: `01`, `02`… in light gray monospace, big — used as step markers.
- **Pixel/8-bit display font**: rare — only for "title-as-logo" series pieces.

---

## Recurring layout types

Tag every new piece with one of these. Each maps to a fill-in-the-blank prompt template in `prompt-templates.md`.

### L1 — Comparison table
**Use when**: comparing N approaches across M criteria.
- Columns are pills with the accent color (or black).
- Rows are criteria, alternating subtle background or just thin dividers.
- Each cell contains a screenshot/icon + 1-line caption.
- Optional: green ✅ verdict badge on the winning cell per row.

### L2 — Before/After (or Wrong/Right)
**Use when**: showing the wrong way vs. the right way.
- 2 columns: ❌ red header (left) / ✅ green header (right).
- Each example pair has a screenshot + a tiny dark "Why it works" callout on the right side.
- Bottom: a "rule of thumb" cream callout box.

### L3 — Stage flow (eras / journey)
**Use when**: showing progression through stages or eras.
- 4–5 colored cards in a grid, each card has emoji + title + bullets + tools row.
- Hand-drawn arrows between cards in reading order.
- Final stage gets a gradient or rainbow background to mark "the new way."

### L4 — Annotated screenshot
**Use when**: explaining one product or interface in depth.
- Centered hero screenshot with rounded corners + slight drop shadow.
- Lines/arrows pointing to labels around it (handwritten color text + black label).

### L5 — Ranked list
**Use when**: top N skills/tasks/tools.
- Numbered circles `① ② ③ …` on the left.
- Row label + delta arrow (↑ green / ↓ red) + horizontal accent-color bar + 3 small avatars or company logos on the right.
- Top 3 rows highlighted with the lavender panel fill.

### L6 — Hero chart with annotations
**Use when**: there's one number/curve that tells the story.
- Big bold title + handwritten subtitle.
- Single line/bar chart taking ~60% of canvas.
- Colored callout boxes pinned to specific points on the curve.
- Emojis as data point markers.

### L7 — Framework grid (2x2 / metaphor)
**Use when**: a framework with 4 quadrants or a strong visual metaphor.
- 4 cards arranged 2x2.
- Same metaphorical icon repeated with one variable changing (e.g. a scale tipping differently).
- Hand-drawn arrow connectors with handwritten labels between cards.

### L8 — Cheat sheet
**Use when**: dense reference for one topic; "everything you need to know about X". The most repeated format in the source archive.
- Top-right "Cheat sheet" pill in the accent color.
- Top-right cream box: "🥇 Golden rule" + 1-sentence rule.
- Body split into 4–6 colored panels (each with its own header pill — accent / orange / green / yellow).
- Each panel: section title pill + bullet list / table / mini-chart.
- Often combines DOs ✅ / DON'Ts ❌ side by side.
- Optional logo strip or book-cover row at the bottom.

### L9 — Commitment ladder
**Use when**: showing escalating user behaviors / a funnel.
- Vertical stack of rounded accent-fill rows.
- Green ↓ arrows between rows (1, 2, 3 arrows growing in count to show increasing commitment).
- Side rail labeled "less commitment" → "more commitment".
- Right column has parallel detail (e.g. tools used at that step).

### L10 — Myth vs. Truth
**Use when**: debunking 3 common assumptions with data.
- 2 columns: "What people think" (left, in quotes) → "The truth" (right, with screenshot/chart/number).
- Black arrow between columns.
- 3 rows stacked vertically.

### L11 — Process numbered grid
**Use when**: a 4-step playbook where each step has its own visual.
- 2x2 grid of cards with colored header pills (yellow / orange / accent / green).
- Each card: "1. [step name]" + 1-paragraph description + small visual/screenshot + ✅ rules.
- Variant: 5 steps as a vertical stack with arrows between, when sequence matters more than parity.

### L12 — Visual metaphor diagram
**Use when**: one strong shape carries the whole concept.
- Single dominant shape (T, train, scale, ladder, mountain) drawn or constructed from UI elements.
- Handwritten annotations pinned to the shape.
- Minimal body text — the metaphor does the work.

---

## Series branding

If the user is producing a recurring series, give it a brand pill that appears on every entry. Examples from the source archive:

- **"Cheat sheet"** (accent-colored pill, top-right) — dense single-page reference. Always paired with a "🥇 Golden rule" cream-box callout.
- **"Product hack"** (orange pill) — single-tactic teardown, often "inspired by [company]" in handwritten subtitle.
- **"Product tips"** (green pill) — short tactical post, usually one diagram/metaphor + handwritten arrow.
- **Sub-series tag** (handwritten, no pill) — small underlined tag under the main title (e.g. "pt.1", "vol.2", "pre-PMF").

Each series has its own visual rhythm. Adopting one gives the user's feed instant recognizability.

---

## Recurring visual motifs

These small details make the difference between "AI infographic" and "intentional brand."

- **Hand-drawn arrows** in the accent color, slightly wobbly, with handwritten labels.
- **3D Apple-style emoji** (not flat) used as decorative anchors.
- **Yellow `new` badge** for highlighted rows.
- **Pointing finger emoji** ☝ to mark callouts.
- **Black rounded pill** as the row-header for "Why it works?" callouts (white handwritten text inside).
- **Screenshots are real product UIs** with rounded corners and slight drop shadow — not abstract icons. Real screenshots build credibility.
- **Tools row**: small colorful logos in a horizontal strip.

---

## Frame & canvas

- Default canvas: portrait 4:5 ratio (`1024×1536` native at gpt-image-2). Other formats: 1:1 (`1024×1024`) and 16:9 (`1536×1024`).
- 2px solid accent-colored outer border at the absolute edge.
- ~32px inner padding.
- Title block sits in the top ~20% with breathing room.
- Footer signature pill sits in the bottom ~5%.

---

## Tone of writing

- **Title**: ≤6 words, declarative, often a metaphor or a contrast ("Efficiency Ratio", "Product Train", "Tidy interface", "11-star experience").
- **Subtitle**: explains the title in a single sentence, conversational, often a question or "How to ___."
- **Body**: lowercase fragments, no full sentences in cells when possible. ✅/❌ as visual scannables.
- **Closing line**: a one-sentence takeaway in the bottom panel — a rule, a verdict, or a punchline.

---

## What makes the look intentional

- Mixing **clean grid systems** with **hand-drawn accent annotations** — corporate clarity + personal voice.
- Using **real product screenshots**, not abstract icons.
- Always ending with a **rule** or **takeaway box**, not just data.
- The **accent-color frame + handwritten subtitle** combo is the strongest signature element. If you skip nothing else, keep these two.
