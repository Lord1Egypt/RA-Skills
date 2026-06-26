# Style: Stripe

> Source: <https://getdesign.md/>
> Clean white · weight-300 elegance · blue-tinted shadows · fintech luxury.
> Best for fintech, payment platforms, premium B2B SaaS.

## Identity (1-line)

White canvas + deep navy headings (`#061b31`) + saturated brand purple (`#533afd`). Signature is **sohne-var weight 300 at display sizes** with `"ss01"` stylistic set globally — lightness as luxury. Shadows are blue-tinted (`rgba(50,50,93,0.25)`), giving elevation a brand atmosphere. Border-radius stays conservative (4–8 px).

## Token Table

| Token | Value | Notes |
|-------|-------|-------|
| Background | `#ffffff` | Pure white |
| Heading | `#061b31` | Deep navy — not black |
| Label | `#273951` | Form labels / secondary heading |
| Body | `#64748d` | Slate gray |
| Brand Purple | `#533afd` | CTA / link / interactive |
| Purple Hover | `#4434d4` | |
| Purple Light | `#b9b9f9` | Outlined button border |
| Brand Dark | `#1c1e54` | Dark immersive sections |
| Border default | `#e5edf5` | Card / divider |
| Success | `#15be53` (bg α0.2) / `#108c3d` (text) | |
| Decorative Ruby | `#ea2261` | Gradient only |
| Decorative Magenta | `#f96bee` | Gradient only |

## Typography

- Family: `sohne-var` (fallback `Inter`). Enable `font-feature-settings: "ss01"` on all text.
- Mono: `SourceCodePro`.
- Two-weight simplicity: **300 (default headings + body) / 400 (UI / buttons)**. No bold.
- Letter-spacing scale:

| Size | Spacing |
|------|---------|
| 56 px | -1.4 px |
| 48 px | -0.96 px |
| 32 px | -0.64 px |
| 26 px | -0.26 px |
| 22 px | -0.22 px |
| ≤ 16 px | normal |

- Use `"tnum"` for numeric data (financial tables/charts).

## Radius & Shadow

- Radius: standard 4 · card 5–6 · featured 8. **Never** pill (9999) on primary buttons.
- Signature shadow stack (blue-tinted multi-layer):
  ```
  rgba(50,50,93,0.25) 0 30px 45px -30px,
  rgba(0,0,0,0.1)     0 18px 36px -18px
  ```
- Ambient shadow: `rgba(23,23,23,0.08) 0 15px 35px 0`.

## Pencil `variables` block (copy-ready)

```json
"variables": {
  "--background":         { "type": "color", "value": "#ffffff" },
  "--card":               { "type": "color", "value": "#ffffff" },
  "--foreground":         { "type": "color", "value": "#061b31" },
  "--muted-foreground":   { "type": "color", "value": "#64748d" },
  "--label":              { "type": "color", "value": "#273951" },
  "--primary":            { "type": "color", "value": "#533afd" },
  "--primary-foreground": { "type": "color", "value": "#ffffff" },
  "--primary-hover":      { "type": "color", "value": "#4434d4" },
  "--secondary":          { "type": "color", "value": "#b9b9f9" },
  "--brand-dark":         { "type": "color", "value": "#1c1e54" },
  "--border":             { "type": "color", "value": "#e5edf5" },
  "--success":            { "type": "color", "value": "#15be53" },
  "--success-foreground": { "type": "color", "value": "#108c3d" },
  "--radius-sm":          { "type": "number", "value": 4 },
  "--radius-md":          { "type": "number", "value": 6 },
  "--radius-lg":          { "type": "number", "value": 8 },
  "--font-primary":       { "type": "string", "value": "Inter" }
}
```

## Component Recipes

**Primary button**: `#533afd` fill, white text, 4 px radius, padding `[8,16]`, 16 px sohne-var 400.

**Outlined button**: transparent fill, `1px solid #b9b9f9`, `#533afd` text, 4 px radius.

**Card**: white fill, `1px solid #e5edf5`, 6 px radius, blue-tinted shadow stack above.

**Hero heading**: 48 px sohne-var weight **300**, line-height 1.15, letter-spacing -0.96 px, `#061b31`.

**Dark section**: `#1c1e54` bg, white text, 32 px weight 300 heading.

## Do / Don't

✓ Weight 300 for everything except UI · `"ss01"` on every sohne-var text · blue-tinted shadows · `#061b31` not `#000` · radius 4–8 only · `"tnum"` for tabular numbers.

✗ No weight 600/700 in headings · no pill shapes on buttons/cards · no neutral gray shadows (always tint blue) · no positive letter-spacing at display · no Ruby/Magenta on buttons (decorative only).
