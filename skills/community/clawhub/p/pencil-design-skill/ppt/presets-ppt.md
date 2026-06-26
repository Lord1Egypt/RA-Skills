# PPT / Slide Deck Preset

Default style for presentations / slide decks when the user does not specify a color scheme.

> **Before designing any slide, also read [`layout-integrity.md`](../references/layout-integrity.md).**
> PPT slides are fixed-size canvases (1280×720) with zero scroll — overflow and misalignment are immediately visible and must be prevented by construction, not fixed afterward.

## Slide Setup

- **Size**: `1280 × 720` px
- **Stacking**: **horizontal by default** (x 递增, 100 px gap, y = 0). Switch to vertical (y 递增, x = 0, 100 px gap) only when the user picks it. Follow the multi-artboard ask in [`SKILL.md`](../SKILL.md) Critical Rule 7.
- **Font**: `Inter` for all text (not PingFang SC)

## Color Tokens

```json
"variables": {
  "--bg-page":       { "type": "color", "value": "#FFFFFF" },
  "--bg-card":       { "type": "color", "value": "#F0F7FF" },
  "--bg-footer":     { "type": "color", "value": "#E8F4FD" },
  "--border-card":   { "type": "color", "value": "#C5D9F2" },
  "--text-heading":  { "type": "color", "value": "#0D1B8E" },
  "--text-body":     { "type": "color", "value": "#1565C0" },
  "--accent-sky":    { "type": "color", "value": "#29B6F6" },
  "--white":         { "type": "color", "value": "#FFFFFF" }
}
```

## Header Bar (content slides)

```json
{
  "type": "frame", "id": "hdr1",
  "width": "fill_container", "height": 64,
  "fill": {
    "type": "gradient", "gradientType": "linear", "rotation": 270,
    "colors": [
      { "color": "#0D1B8E", "position": 0 },
      { "color": "#29B6F6", "position": 1 }
    ]
  }
}
```

## Cover / Closing Slide (full-bleed gradient)

```json
"fill": {
  "type": "gradient", "gradientType": "linear", "rotation": 45,
  "colors": [
    { "color": "#29B6F6", "position": 0 },
    { "color": "#1565C0", "position": 0.5 },
    { "color": "#0D1B8E", "position": 1 }
  ]
}
```
Deep color (`#0D1B8E`) lands top-left, sky blue bottom-right.

## Default Slide Sequence (when building a complete deck)

1. **Cover** — full diagonal gradient · large title · subtitle · presenter info
2. **Table of Contents** — left gradient sidebar (180 px) + right card list
3. **Content (3-column)** — header bar + white body + 3 icon cards
4. **Data Dashboard** — header bar + 4 KPI cards + bar chart
5. **Gantt Chart** — header bar + month axis + task rows with `#29B6F6` bars + status badges
6. **Thank You** — full diagonal gradient · centered large text · decorative circles

## Component Recipes

**Card / panel**: `fill: "$--bg-card"`, `stroke: { thickness: 1, fill: "$--border-card" }`, `cornerRadius: 8`, `padding: [16, 20]`.

**Footer bar**: full-width, `fill: "$--bg-footer"`, `text: "$--text-body"`, height `40`.

**Heading text**: `fontFamily: "Inter"`, `fontWeight: "700"`, `fill: "$--text-heading"`.

**Body text**: `fontFamily: "Inter"`, `fontWeight: "400"`, `fill: "$--text-body"`, `fontSize: 14–16`.

**Data callout / progress bar / Gantt bar**: `fill: "$--accent-sky"`.
