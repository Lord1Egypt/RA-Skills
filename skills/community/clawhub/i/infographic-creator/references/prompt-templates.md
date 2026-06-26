# Prompt templates for gpt-image-2

One template per layout. Fill the `{{...}}` placeholders, then concatenate `PREAMBLE` + the template body to form the final prompt sent to `images.edit`.

The `{{ACCENT_NAME}}` placeholder must be the actual color word (e.g. "blue", "purple", "orange") — NOT just the hex. Models weight words higher than hex codes, so always include both.

---

## Universal preamble (prepend to every prompt)

```
Style: clean modern social-media infographic. Portrait/square/landscape canvas (matches requested size), white background, 2px solid {{ACCENT_NAME}} ({{ACCENT_HEX}}) outer frame with ~32px inner padding.
Title: bold black sans-serif (Inter Black weight) ~72px, max 6 words, broken across 2 lines, centered top.
Subtitle directly under title: handwritten {{ACCENT_NAME}} ({{HANDWRITTEN_HEX}}) script font (Caveat-style) ~28px, conversational tone.
Two 3D-style emojis flanking the title — one top-left, one top-right.
Body text Inter 16px black. Hand-drawn {{ACCENT_NAME}} wobbly arrows where flow is implied.
Footer: black rounded pill at bottom-center reading "{{HANDLE}}" with the provided avatar photo (reference image: avatar) as a small circle to the left of the text.
Crisp typography, dense but readable on a phone.
```

---

## L1 — Comparison table

```
{{PREAMBLE}}

Layout: comparison table. Head-to-head comparison across multiple criteria.

Reference images attached:
{{REFERENCE_IMAGES_DESCRIPTION}}

Title (bold black sans-serif, two lines):
  Line 1: "{{TITLE_LINE_1}}"
  Line 2: "{{TITLE_LINE_2}}" — the word "{{ACCENT_WORD}}" in {{ACCENT_NAME}} ({{ACCENT_HEX}})
Subtitle (handwritten {{ACCENT_NAME}}): "{{SUBTITLE}}"
Title emojis: {{LEFT_EMOJI}} (top-left), {{RIGHT_EMOJI}} (top-right).

Optional "Core difference" callout strip near top — two side-by-side rounded cards with brief framing for each side.

Comparison table with N columns:
  Column header pills (black rounded, white text): {{COLUMN_HEADERS}}
  Rows (thin gray dividers between):
{{ROWS_FORMATTED}}

Optional bottom takeaway box (cream #FFF7E6, rounded, with 🔥 emoji on left):
  Bold line: "{{TAKEAWAY_HEADLINE}}"
  Below: "{{TAKEAWAY_DETAIL}}"

Footer: black pill with avatar + "{{HANDLE}}".
```

---

## L2 — Before/After

```
{{PREAMBLE}}

Layout: before/after comparison. Shows wrong way vs right way across N examples.

Title: "{{TITLE}}"
Subtitle (handwritten {{ACCENT_NAME}}): "{{SUBTITLE}}"
Title emojis: {{LEFT_EMOJI}} and {{RIGHT_EMOJI}}.

For each of {{N}} sections:
  Section header: "{{SECTION_TITLE}}"
  Left column header: ❌ "{{BAD_LABEL}}: '{{BAD_QUOTE}}'" with screenshot/mock placeholder
  Right column header: ✅ "{{GOOD_LABEL}}: '{{GOOD_QUOTE}}'" with screenshot/mock placeholder
  Right side of each row: black rounded pill "Why it works?" with handwritten white text inside: "{{WHY}}"

Bottom: cream-background rounded box with one-sentence rule of thumb: "{{TAKEAWAY}}"
```

---

## L3 — Stage flow

```
{{PREAMBLE}}

Layout: 4-stage progression grid (2x2) showing evolution across stages or eras.

Title: "{{TITLE}}"
Subtitle (handwritten {{ACCENT_NAME}}): "{{SUBTITLE}}"

Stage 1 card (pastel yellow #FFF7E6 bg): emoji {{E1}} + name "{{S1_NAME}}" + 1-line description + small visual + Constraint: "{{S1_CONSTRAINT}}" + Tools: 3 logos + ✅ pro / ❌ con.
Stage 2 card (pastel coral #FBE4E4 bg): same structure with stage 2 data.
Stage 3 card (pastel mint #E7F6EC bg): same structure with stage 3 data.
Stage 4 card (gradient/rainbow bg, full-width at bottom): emoji {{E4}} + "{{S4_NAME}}" + description + larger visual + multiple ✅ pros / ❌ cons in two columns.

Hand-drawn {{ACCENT_NAME}} arrows connecting cards in reading order.
```

---

## L4 — Annotated screenshot

```
{{PREAMBLE}}

Layout: single hero screenshot with surrounding annotations.

Title: "{{TITLE}}"
Subtitle (handwritten {{ACCENT_NAME}}): "{{SUBTITLE}}"

Center: realistic screenshot of {{INTERFACE_DESC}} with rounded corners and shadow. Use the attached reference image as the screenshot source.

Annotations radiating around the screenshot, each with a thin {{ACCENT_NAME}} line pointing to a UI element:
  - Top left: "{{LABEL_1}}" + 2-line description
  - Top right: "{{LABEL_2}}" + description
  - Mid left: "{{LABEL_3}}" + description
  - Mid right: "{{LABEL_4}}" + description
  - Bottom left: "{{LABEL_5}}" + description
  - Bottom right: "{{LABEL_6}}" + description

Labels in handwritten {{ACCENT_NAME}} ({{HANDWRITTEN_HEX}}). Lines slightly hand-drawn.
```

---

## L5 — Ranked list

```
{{PREAMBLE}}

Layout: top-{{N}} ranked list.

Title: "{{TITLE}}"
Subtitle (handwritten {{ACCENT_NAME}}): "{{SUBTITLE}}"
Title emojis: {{LEFT_EMOJI}} and {{RIGHT_EMOJI}}.

Top 3 rows have a soft lavender (derived from {{ACCENT_HEX}}) rounded-pill background. Other rows have thin gray dividers.

Each row contains, left to right:
  - A numbered circle: ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩
  - The item label in bold black 18px
  - A short description in gray 14px on the line below
  - A delta arrow ↑ (green) or ↓ (red) with percentage "{{PCT}}%"
  - A horizontal {{ACCENT_NAME}} progress bar (length proportional to value)
  - 3 small avatar/logo circles on the far right

Items in order:
{{ITEMS_FORMATTED}}

Bottom: cream rounded box with one-sentence takeaway: "{{TAKEAWAY}}"
```

---

## L6 — Hero chart

```
{{PREAMBLE}}

Layout: single hero {{CHART_TYPE}} chart with annotations.

Title: "{{TITLE}}"
Subtitle (handwritten {{ACCENT_NAME}}): "{{SUBTITLE}}"
Title emojis: {{LEFT_EMOJI}} and {{RIGHT_EMOJI}}.

Center: large {{CHART_TYPE}} taking ~60% of canvas.
Y-axis: {{Y_LABEL}}, X-axis: {{X_LABEL}}.
Plot: {{PLOT_DESCRIPTION}}

Pin colored callout boxes at key data points:
  - At {{POINT_1}}: rounded rectangle filled {{POINT_1_COLOR}}, white text "{{CALLOUT_1}}", with {{POINT_1_EMOJI}} nearby
  - At {{POINT_2}}: rounded rectangle filled {{POINT_2_COLOR}}, white text "{{CALLOUT_2}}", with {{POINT_2_EMOJI}} nearby
  {{ADDITIONAL_CALLOUTS}}

Use emojis as data point markers where it tells the story.
```

---

## L7 — Framework grid (2x2 metaphor)

```
{{PREAMBLE}}

Layout: 2x2 metaphor framework.

Title: "{{TITLE}}" with the word "{{ACCENT_WORD}}" in {{ACCENT_NAME}}.
Subtitle (handwritten {{ACCENT_NAME}}): "{{SUBTITLE}}"
Title emojis: {{LEFT_EMOJI}} and {{RIGHT_EMOJI}}.

Quadrant 1 (top-left): metaphor visual showing {{METAPHOR_VARIANT_1}} + label box "{{Q1_TITLE}}" + 2-line description + 3 example logos.
Quadrant 2 (top-right): same structure with metaphor variant 2.
Quadrant 3 (bottom-left): variant 3.
Quadrant 4 (bottom-right, highlighted with rainbow border): variant 4 + handwritten "aim for this!" arrow.

Handwritten {{ACCENT_NAME}} arrows between quadrants with labels like "miss this and you'll hit X".
```

---

## L8 — Cheat sheet

```
{{PREAMBLE}}

Layout: dense "Cheat sheet" reference page.

Top-left: title in bold black sans-serif "{{TITLE_PART_1}}" on line one, "{{TITLE_PART_2}}" on line two with the word "Cheat sheet" wrapped in a {{ACCENT_NAME}} ({{ACCENT_HEX}}) rounded pill with white text.
Below the title: a small handwritten {{ACCENT_NAME}} ({{HANDWRITTEN_HEX}}) underlined tag reading "{{SUB_SERIES_TAG}}" (e.g. "pt.1")
Top-right: a cream (#FFF7E6) rounded box titled "🥇 Golden rule" in bold, with subtitle text: "{{GOLDEN_RULE}}"
Title emojis: {{LEFT_EMOJI}} (top-left, above title) and {{RIGHT_EMOJI}} (top-right, above golden rule).

Body: 4-6 colored panels in a grid, each with a header pill at the top:

Panel 1 (background {{P1_BG}}, header pill "{{P1_TITLE}}"):
  {{P1_BULLETS}}

Panel 2 (background {{P2_BG}}, header pill "{{P2_TITLE}}"):
  {{P2_BULLETS}}

Panel 3 (background {{P3_BG}}, header pill "{{P3_TITLE}}"):
  {{P3_BULLETS}}

Panel 4 (background {{P4_BG}}, header pill "{{P4_TITLE}}"):
  {{P4_BULLETS}}

Bottom: thin gray divider, then a single-line takeaway in handwritten {{ACCENT_NAME}}: "{{TAKEAWAY}}"
```

---

## L9 — Commitment ladder

```
{{PREAMBLE}}

Layout: vertical commitment ladder showing escalating user behaviors.

Title: "{{TITLE}}"
Subtitle (handwritten {{ACCENT_NAME}}): "{{SUBTITLE}}"

Side rail on the left: vertical arrow labeled "less commitment" at top, "more commitment" at bottom, in {{ACCENT_NAME}}.

Vertical stack of {{N}} rounded {{ACCENT_NAME}}-tinted rows, each containing a behavior label.
Between consecutive rows: green ↓ arrows — each tier has one MORE arrow than the previous (1, 2, 3, 4...) to show increasing commitment.

Right side, parallel detail column: tools, examples, or status linked to each row.

Bottom: cream rounded takeaway box: "{{TAKEAWAY}}"
```

---

## L10 — Myth vs. Truth

```
{{PREAMBLE}}

Layout: 3-row myth-vs-truth comparison.

Title: "{{TITLE}}"
Subtitle (handwritten {{ACCENT_NAME}}): "{{SUBTITLE}}"
Title emojis: {{LEFT_EMOJI}} and {{RIGHT_EMOJI}}.

Two columns: "What people think" (left, in handwritten {{ACCENT_NAME}}) → "The truth" (right, in bold black).

3 rows stacked vertically, each row:
  Left cell: quoted myth in italic gray
  Black arrow → middle
  Right cell: real data — screenshot, stat, or chart proving the truth
```

---

## L11 — Process numbered grid (4-step or 5-step vertical variant)

```
{{PREAMBLE}}

Layout (4-step variant): 2x2 grid of step cards.
Layout (5-step variant): vertical stack of 5 full-width step cards with hand-drawn down-arrows between them.

Title: "{{TITLE}}"
Subtitle (handwritten {{ACCENT_NAME}}): "{{SUBTITLE}}"
Title emojis: {{LEFT_EMOJI}} and {{RIGHT_EMOJI}}.

For each step card:
  - Solid-color number circle on the far left (60px) with the step number in bold white
  - Step title in bold black 22px
  - One-line description in gray 14px below
  - 1-2 small logo squares on the far right (from reference images)

Step 1 (background #FFF7E6 cream, number circle yellow #F59E0B):
  Title: "{{S1_TITLE}}"
  Description: "{{S1_DESC}}"
  Logos: {{S1_LOGOS}}

Step 2 (background #FBE4E4 coral, number circle orange #F26B2A):
  Title: "{{S2_TITLE}}"
  Description: "{{S2_DESC}}"
  Logos: {{S2_LOGOS}}

Step 3 (background #E7F6EC mint, number circle green #16A34A):
  Title: "{{S3_TITLE}}"
  Description: "{{S3_DESC}}"
  Logos: {{S3_LOGOS}}

Step 4 (background lavender, number circle {{ACCENT_HEX}}):
  Title: "{{S4_TITLE}}"
  Description: "{{S4_DESC}}"
  Logos: {{S4_LOGOS}}

(For 5-step variant, add Step 5 with darker {{HANDWRITTEN_HEX}} number circle.)

Between each card pair: small hand-drawn wobbly {{HANDWRITTEN_HEX}} down-arrow.

Bottom: cream takeaway box with 🔥 emoji + bold text: "{{TAKEAWAY}}"
```

---

## L12 — Visual metaphor diagram

```
{{PREAMBLE}}

Layout: single dominant visual metaphor carrying the entire concept.

Title: "{{TITLE}}"
Subtitle (handwritten {{ACCENT_NAME}}): "{{SUBTITLE}}"

Center: large {{METAPHOR_SHAPE}} (e.g. T-shape, train, scale, ladder, mountain) drawn or constructed from icons/UI elements representing the concept.

Handwritten {{ACCENT_NAME}} annotations pinned to specific parts of the shape — short labels with arrows.

Minimal body text. The metaphor does the work.

Bottom: optional cream takeaway box: "{{TAKEAWAY}}"
```

---

## Tips for image generation

- **Generate the frame and title first** mentally — make sure those are crisp before piling on body text. Image-2 handles ~10–12 distinct text strings per image well; beyond that, text starts garbling.
- **Real screenshots are unreliable to invent** — always pass them as reference images via `images.edit`. Generated screenshots usually look fake.
- **Hand-drawn arrows** are the hardest to get right purely from prompt — include "wobbly hand-drawn marker stroke" explicitly.
- **For pixel/8-bit titles** (rare): say "pixel font Press Start 2P style, [color] brick texture".
- **Iterate by region**, not from scratch — if one label comes out garbled, regenerate with `images.edit` using the previous output + a focused fix-this-region prompt.
- **Always include the hex AND the color word** for the accent. The model can drift to a similar but wrong color if only one is given.
