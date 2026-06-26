# Style: Notion

> Source: <https://getdesign.md/>
> Warm minimalism · whisper borders · 4-layer low-opacity shadows · paper-like feel.
> Best for productivity tools, documentation, content apps.

## Identity (1-line)

White (`#ffffff`) + alternating warm-white sections (`#f6f5f4`) + near-black text via 95% alpha (`rgba(0,0,0,0.95)`). Warm-gray neutrals carry yellow-brown undertones — never blue-gray. Borders are 1-px whispers at `rgba(0,0,0,0.1)`. Shadows accumulate in 4-5 layers, each ≤0.05 opacity. Notion blue (`#0075de`) is the only saturated color in core UI.

## Token Table

| Token | Value | Notes |
|-------|-------|-------|
| Background | `#ffffff` | Page bg |
| Background alt | `#f6f5f4` | Warm white — for section alternation |
| Primary text | `rgba(0,0,0,0.95)` | Near-black, soft |
| Secondary text | `#615d59` | Warm gray 500 |
| Muted text | `#a39e98` | Warm gray 300 |
| Dark surface | `#31302e` | Dark section bg (warm) |
| Notion Blue | `#0075de` | CTA / link |
| Active Blue | `#005bab` | Pressed state |
| Focus Blue | `#097fe8` | |
| Badge bg blue | `#f2f9ff` | Pill background |
| Badge text blue | `#097fe8` | Pill text |
| Border whisper | `rgba(0,0,0,0.1)` | Cards / dividers |
| Input border | `#dddddd` | Inputs |

## Typography

- Family: `NotionInter` (fallback `Inter`). Enable `"lnum","locl"` on display & heading text.
- Four weights: **400 (read) / 500 (UI) / 600 (emphasis) / 700 (display)**.
- Letter-spacing scale:

| Size | Spacing |
|------|---------|
| 64 px | -2.125 px |
| 54 px | -1.875 px |
| 48 px | -1.5 px |
| 26 px | -0.625 px |
| 22 px | -0.25 px |
| ≤ 16 px | normal |
| 12 px badge | **+0.125 px** (only positive tracking in system) |

## Radius & Shadow

- Radius: button 4 · small 8 · standard card 12 · hero card 16 · pill 9999.
- Standard card shadow (4 layers, max 0.04 opacity):
  ```
  rgba(0,0,0,0.04)  0 4px    18px,
  rgba(0,0,0,0.027) 0 2.025px 7.847px,
  rgba(0,0,0,0.02)  0 0.8px   2.925px,
  rgba(0,0,0,0.01)  0 0.175px 1.041px
  ```
- Deep modal shadow: 5 layers up to `rgba(0,0,0,0.05) 0 23px 52px`.

## Pencil `variables` block (copy-ready)

```json
"variables": {
  "--background":         { "type": "color", "value": "#ffffff" },
  "--background-alt":     { "type": "color", "value": "#f6f5f4" },
  "--card":               { "type": "color", "value": "#ffffff" },
  "--foreground":         { "type": "color", "value": "#0a0a0a" },
  "--muted-foreground":   { "type": "color", "value": "#615d59" },
  "--placeholder":        { "type": "color", "value": "#a39e98" },
  "--primary":            { "type": "color", "value": "#0075de" },
  "--primary-foreground": { "type": "color", "value": "#ffffff" },
  "--primary-active":     { "type": "color", "value": "#005bab" },
  "--ring":               { "type": "color", "value": "#097fe8" },
  "--badge-bg":           { "type": "color", "value": "#f2f9ff" },
  "--badge-fg":           { "type": "color", "value": "#097fe8" },
  "--border":             { "type": "color", "value": "#e6e4e0" },
  "--radius-sm":          { "type": "number", "value": 4 },
  "--radius-md":          { "type": "number", "value": 8 },
  "--radius-lg":          { "type": "number", "value": 12 },
  "--radius-xl":          { "type": "number", "value": 16 },
  "--radius-pill":        { "type": "number", "value": 9999 },
  "--font-primary":       { "type": "string", "value": "Inter" }
}
```

> Note: `rgba(0,0,0,0.1)` whisper borders cannot be variables; the solid `#e6e4e0` above approximates the look. For exact rgba, set `stroke.fill` directly on the frame.

## Component Recipes

**Primary blue button**: `#0075de` fill, white text, 4 px radius, padding `[8,16]`, 15 px Inter 600.

**Secondary button**: `rgba(0,0,0,0.05)` fill, near-black text, 4 px radius.

**Pill badge**: `#f2f9ff` fill, `#097fe8` text, 9999 radius, padding `[4,8]`, 12 px Inter 600, letter-spacing **+0.125 px**.

**Standard card**: white fill, `1px solid rgba(0,0,0,0.1)`, 12 px radius, 4-layer shadow.

**Hero heading**: 64 px Inter weight 700, line-height 1.00, letter-spacing -2.125 px.

## Do / Don't

✓ Warm gray neutrals (yellow-brown undertone) · alternating warm-white sections for rhythm · 4-layer shadows max 0.05 opacity · whisper borders · 4 px radius for buttons · 12 px for cards · positive tracking only on 12-px badges.

✗ No cool/blue grays · no heavy borders · no single-layer drop shadows · no pure black text · no pill (9999) on primary CTAs (pills = badges) · no saturated colors in chrome (only `#0075de`).
