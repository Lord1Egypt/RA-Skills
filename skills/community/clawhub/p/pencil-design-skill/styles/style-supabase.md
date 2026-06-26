# Style: Supabase

> Source: <https://getdesign.md/>
> Dark developer-native · emerald accent · **no shadows** · border-hierarchy depth · terminal aesthetic.
> Best for backend-as-a-service, developer portals, open-source project sites.

## Identity (1-line)

Dark canvas (`#171717` page, `#0f0f0f` buttons) with depth expressed entirely through a **border color hierarchy** (`#242424` → `#2e2e2e` → `#363636`) — Supabase deliberately avoids shadows. Circular at weight 400 baseline with **1.00 line-height** at hero size (terminal density). Emerald green (`#3ecf8e` / `#00c573`) is an identity marker — used only for logo, links, and accent borders.

## Token Table

| Token | Value | Notes |
|-------|-------|-------|
| Background | `#171717` | Page bg — NEVER lighten above this |
| Button bg | `#0f0f0f` | Deeper than page |
| Border subtle | `#242424` | Horizontal rules |
| Border default | `#2e2e2e` | Cards |
| Border prominent | `#363636` | Buttons / interactive |
| Border heavier | `#393939` | Dividers |
| Border (charcoal) | `#434343` | Tertiary |
| Primary text | `#fafafa` | |
| Secondary text | `#b4b4b4` | |
| Muted text | `#898989` | Links default |
| Disabled | `#6a6b6c` | |
| Brand green | `#3ecf8e` | Logo / accent borders |
| Link green | `#00c573` | Interactive |
| Green border accent | `rgba(62,207,142,0.3)` | Brand-highlighted elements |

## Typography

- Family: `Circular` (fallback `Inter`).
- Mono: `Source Code Pro` — used in **uppercase with letter-spacing 1.2 px** for technical labels.
- **Two weights only**: 400 (everything) / 500 (nav links, button labels). No bold.

| Role | Size | Weight | Line height | Spacing |
|------|------|--------|-------------|---------|
| Hero | 72 | 400 | **1.00** | normal |
| Section | 36 | 400 | 1.25 | normal |
| Card title | 24 | 400 | 1.33 | -0.16 px |
| Sub-heading | 18 | 400 | 1.56 | normal |
| Body | 16 | 400 | 1.50 | normal |
| Nav / Button | 14 | 500 | 1.14-1.43 | normal |
| Code label | 12 (mono) | 400 | 1.33 | +1.2 px UPPERCASE |

## Radius & Depth

- Radius: ghost 6 · cards 8-16 · primary CTA **9999 (full pill)**.
- **No box-shadows** in dark theme. Depth = border color hierarchy:
  - Default: `1px solid #2e2e2e`
  - Hover: `1px solid #363636` or `#393939`
  - Brand-elevated: `1px solid rgba(62,207,142,0.3)` (green border = "elevated")
  - Focus only: `rgba(0,0,0,0.1) 0 4px 12px`

## Pencil `variables` block (copy-ready)

```json
"variables": {
  "--background":         { "type": "color", "value": "#171717" },
  "--card":               { "type": "color", "value": "#171717" },
  "--popover":            { "type": "color", "value": "#0f0f0f" },
  "--foreground":         { "type": "color", "value": "#fafafa" },
  "--muted-foreground":   { "type": "color", "value": "#898989" },
  "--secondary-foreground": { "type": "color", "value": "#b4b4b4" },
  "--primary":            { "type": "color", "value": "#0f0f0f" },
  "--primary-foreground": { "type": "color", "value": "#fafafa" },
  "--accent":             { "type": "color", "value": "#3ecf8e" },
  "--accent-link":        { "type": "color", "value": "#00c573" },
  "--border":             { "type": "color", "value": "#2e2e2e" },
  "--border-strong":      { "type": "color", "value": "#363636" },
  "--border-subtle":      { "type": "color", "value": "#242424" },
  "--ring":               { "type": "color", "value": "#3ecf8e" },
  "--radius-sm":          { "type": "number", "value": 6 },
  "--radius-md":          { "type": "number", "value": 8 },
  "--radius-lg":          { "type": "number", "value": 16 },
  "--radius-pill":        { "type": "number", "value": 9999 },
  "--font-primary":       { "type": "string", "value": "Inter" }
}
```

## Component Recipes

**Primary pill CTA**: `#0f0f0f` fill, `#fafafa` text, **9999 radius**, padding `[8,32]`, `1px solid #fafafa` border, 14 px Circular 500.

**Secondary pill**: same as primary but `1px solid #2e2e2e`, opacity 0.8.

**Ghost button**: transparent fill, `#fafafa` text, 6 px radius, padding `[8]`.

**Card**: `#171717` fill, `1px solid #2e2e2e`, 8-16 px radius, 16-24 px padding. **No `effect` shadows.**

**Pill tab**: 9999 radius, `1px solid #2e2e2e`. Active = green accent border `rgba(62,207,142,0.3)` or lighter surface.

**Code label**: Source Code Pro 12 px, UPPERCASE, letter-spacing +1.2 px, `#898989`.

**Hero heading**: 72 px Circular weight 400, **line-height 1.00**, `#fafafa`.

## Do / Don't

✓ Background ≤ `#171717` always · depth via border hierarchy `#242424 → #2e2e2e → #363636` · weight 400 baseline (500 only for nav/buttons) · hero line-height **1.00** · 9999 radius for primary, 6-16 for everything else · green only for logo/links/accent borders · uppercase Source Code Pro for technical labels.

✗ **No `effect` shadows** — they're invisible on dark and break the system · no weight 700 · no green on backgrounds/large surfaces · no warm colors as primary · no hero line-height > 1.00 · no medium radius (10-15) — pill or 6-16, nothing between · no surfaces lighter than `#171717`.
