# Style: Vercel

> Source: <https://getdesign.md/>
> Monochrome precision · Geist font · shadow-as-border · minimal engineering aesthetic.
> Best for dev tools, deployment platforms, technical landing pages.

## Identity (1-line)

White canvas (`#ffffff`) + near-black text (`#171717`) + Geist Sans with **aggressive negative letter-spacing** at display sizes. CSS borders replaced by `box-shadow 0 0 0 1px rgba(0,0,0,0.08)` (shadow-as-border). Workflow accents (Red/Pink/Blue) only mark pipeline stages.

## Token Table

| Token | Value | Notes |
|-------|-------|-------|
| Background | `#ffffff` | Pure white |
| Foreground | `#171717` | Slightly warm — never `#000` |
| Muted text | `#4d4d4d` (gray-600) / `#666666` (gray-500) | Body / tertiary |
| Border (shadow) | `rgba(0,0,0,0.08)` | Used as `0 0 0 1px` shadow |
| Border (light) | `#ebebeb` | Image / tab ring |
| Card surface | `#ffffff` | Same as bg |
| Subtle surface | `#fafafa` | Inner-ring highlight |
| Primary | `#171717` | Black CTA on white |
| Primary fg | `#ffffff` | |
| Link | `#0072f5` | |
| Focus ring | `hsla(212,100%,48%,1)` | 2 px outline |
| Workflow Ship | `#ff5b4f` | Red — production marker only |
| Workflow Preview | `#de1d8d` | Pink — preview marker only |
| Workflow Develop | `#0a72ef` | Blue — dev marker only |

## Typography

- Family: `Geist`, mono `Geist Mono`. Enable `"liga"` globally on all Geist text.
- Weights: **400 / 500 / 600** (no 700 except 7-px micro badges).
- Letter-spacing scale (tighter at larger sizes):

| Size | Spacing |
|------|---------|
| 48 px | -2.4 to -2.88 px |
| 32 px | -1.28 px |
| 24 px | -0.96 px |
| 16 px | -0.32 px (semibold) / normal |
| ≤ 14 px | normal |

## Radius & Shadow

- Radius: buttons 6 · cards 8 · image cards 12 · pills 9999.
- Card stack (the famous Vercel shadow):
  ```
  rgba(0,0,0,0.08) 0 0 0 1px,
  rgba(0,0,0,0.04) 0 2px 2px,
  rgba(0,0,0,0.04) 0 8px 8px -8px,
  #fafafa 0 0 0 1px
  ```
  The inner `#fafafa` ring is what makes the card "glow" — never skip it.

## Pencil `variables` block (copy-ready)

```json
"variables": {
  "--background":         { "type": "color", "value": "#ffffff" },
  "--foreground":         { "type": "color", "value": "#171717" },
  "--muted-foreground":   { "type": "color", "value": "#4d4d4d" },
  "--primary":            { "type": "color", "value": "#171717" },
  "--primary-foreground": { "type": "color", "value": "#ffffff" },
  "--card":               { "type": "color", "value": "#ffffff" },
  "--border":             { "type": "color", "value": "#ebebeb" },
  "--ring":               { "type": "color", "value": "#0072f5" },
  "--accent-ship":        { "type": "color", "value": "#ff5b4f" },
  "--accent-preview":     { "type": "color", "value": "#de1d8d" },
  "--accent-develop":     { "type": "color", "value": "#0a72ef" },
  "--radius-md":          { "type": "number", "value": 6 },
  "--radius-lg":          { "type": "number", "value": 8 },
  "--radius-pill":        { "type": "number", "value": 9999 },
  "--font-primary":       { "type": "string", "value": "Geist" }
}
```

## Component Recipes

**Primary button**: `#171717` bg, white text, 6 px radius, padding `[8,16]`, 14 px Geist 500.

**Outlined button**: white bg, 6 px radius, no `stroke` — use `effect` shadow `0 0 0 1px rgba(0,0,0,0.08)` (when supported), or fall back to `stroke: { thickness: 1, fill: "$--border" }`.

**Pill badge**: `#ebf5ff` bg, `#0068d6` text, 9999 radius, padding `[0,10]`, 12 px weight 500.

## Do / Don't

✓ Negative letter-spacing at display · `"liga"` always on · 3-weight system · `#171717` not `#000` · multi-layer card shadow with inner `#fafafa` ring.

✗ No positive tracking on Geist · no weight 700 on body · no traditional CSS `border` on cards · no warm colors in chrome · no pill (9999) on primary buttons (pills = badges only).
