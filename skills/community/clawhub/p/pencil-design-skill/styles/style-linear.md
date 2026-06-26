# Style: Linear

> Source: <https://getdesign.md/>
> Deep dark · indigo accent · Inter weight 510 · ultra-minimal SaaS.
> Best for SaaS apps, task management, dark-mode UI.

## Identity (1-line)

Near-black canvas (`#08090a`) where content emerges from darkness. Inter Variable with `"cv01","ss03"` features and a signature **weight 510** (between regular and medium). Borders are semi-transparent white whispers; elevation comes from background-luminance stepping, not shadow opacity. Single brand color: indigo `#5e6ad2` / `#7170ff`.

## Token Table

| Token | Value | Notes |
|-------|-------|-------|
| Marketing bg | `#08090a` | Page background |
| Panel bg | `#0f1011` | Sidebar / panel |
| Surface (card) | `#191a1b` | Elevated surface |
| Surface 2 | `#28282c` | Hover state |
| Primary text | `#f7f8f8` | Near-white — never `#fff` |
| Body text | `#d0d6e0` | Silver gray |
| Tertiary | `#8a8f98` | Placeholder / metadata |
| Quaternary | `#62666d` | Disabled / timestamps |
| Brand indigo | `#5e6ad2` | CTA bg |
| Accent violet | `#7170ff` | Links / active |
| Hover violet | `#828fff` | Hover only |
| Border (default) | `rgba(255,255,255,0.08)` | Cards / inputs |
| Border (subtle) | `rgba(255,255,255,0.05)` | Lightest separator |
| Button bg | `rgba(255,255,255,0.02)`–`0.05` | Translucent ghost |
| Success | `#10b981` | Pill / status only |

## Typography

- Family: `Inter Variable` with `font-feature-settings: "cv01","ss03"` on **all text** (this IS Linear's typeface — without it, generic Inter).
- Mono: `Berkeley Mono` for code/technical labels.
- Three weights: **400 (read) / 510 (UI/emphasis) / 590 (announce)**. Weight 300 only for de-emphasized text. Never use 700.
- Letter-spacing scale:

| Size | Spacing |
|------|---------|
| 72 px | -1.584 px |
| 64 px | -1.408 px |
| 48 px | -1.056 px |
| 32 px | -0.704 px |
| 24 px | -0.288 px |
| ≤ 16 px | normal |

## Radius & Elevation

- Radius: micro 2 · small 4 · button 6 · card 8 · panel 12 · large 22 · pill 9999.
- **Elevation by luminance step**, not shadow opacity:
  - Card: `rgba(255,255,255,0.02)` bg + `1px solid rgba(255,255,255,0.08)`
  - Inset: `rgba(0,0,0,0.2) 0 0 12px 0 inset`
  - Ring border: `rgba(0,0,0,0.2) 0 0 0 1px`

## Pencil `variables` block (copy-ready)

```json
"variables": {
  "--background":         { "type": "color", "value": "#08090a" },
  "--card":               { "type": "color", "value": "#191a1b" },
  "--popover":            { "type": "color", "value": "#0f1011" },
  "--foreground":         { "type": "color", "value": "#f7f8f8" },
  "--muted-foreground":   { "type": "color", "value": "#8a8f98" },
  "--secondary":          { "type": "color", "value": "#28282c" },
  "--primary":            { "type": "color", "value": "#5e6ad2" },
  "--primary-foreground": { "type": "color", "value": "#ffffff" },
  "--accent":             { "type": "color", "value": "#7170ff" },
  "--border":             { "type": "color", "value": "#23252a" },
  "--ring":               { "type": "color", "value": "#7170ff" },
  "--success":            { "type": "color", "value": "#10b981" },
  "--radius-sm":          { "type": "number", "value": 4 },
  "--radius-md":          { "type": "number", "value": 6 },
  "--radius-lg":          { "type": "number", "value": 8 },
  "--radius-pill":        { "type": "number", "value": 9999 },
  "--font-primary":       { "type": "string", "value": "Inter" }
}
```

> Note: rgba borders cannot be expressed as variable values in `.pen`. Use the solid `#23252a` border above as a close approximation, OR put the rgba string directly into `stroke.fill` per-frame when you need the translucent look.

## Component Recipes

**Ghost button**: `rgba(255,255,255,0.02)` fill, `1px solid rgba(255,255,255,0.08)`, 6 px radius, 14 px Inter 510, color `#e2e4e7`.

**Brand CTA**: `#5e6ad2` fill, white text, 6 px radius, padding `[8,16]`, 14 px Inter 510.

**Card**: `rgba(255,255,255,0.02)` fill, `1px solid rgba(255,255,255,0.08)`, 8 px radius, 24 px padding.

**Pill badge**: transparent bg, `1px solid #23252a`, 9999 radius, padding `[0,10]`, 12 px Inter 510, `#d0d6e0` text.

## Do / Don't

✓ `"cv01","ss03"` on every Inter element · weight 510 default · luminance stepping for elevation · `#f7f8f8` not `#fff` · semi-transparent white borders · indigo only on CTAs.

✗ No pure white text · no solid colored button bg (translucent only) · no decorative use of indigo · no positive letter-spacing · no weight 700 · no warm colors in chrome.
