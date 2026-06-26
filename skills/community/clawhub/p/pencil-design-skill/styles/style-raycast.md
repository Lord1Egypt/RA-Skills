# Style: Raycast

> Source: <https://getdesign.md/>
> macOS-native dark · physical multi-layer shadows · positive letter-spacing · red accent.
> Best for productivity tools, premium dark UI, developer launchers.

## Identity (1-line)

Near-black blue-tinted background (`#07080a`, NOT pure black) with macOS-native multi-layer shadow stacks (outer ring + inset highlight + inset shadow) that simulate physical depth — like glass cards on a dark desk. Inter with **positive letter-spacing** (+0.2 px) and weight 500 baseline for airy dark-mode readability. Raycast Red (`#FF6363`) appears as punctuation only — hero stripes, error states.

## Token Table

| Token | Value | Notes |
|-------|-------|-------|
| Background | `#07080a` | Near-black blue-tinted — NEVER `#000` |
| Surface | `#101111` | Card bg |
| Card surface 2 | `#1b1c1e` | Badges / tags |
| Button dark fg | `#18191a` | Text on light buttons |
| Primary text | `#f9f9f9` | Near-white |
| Secondary | `#cecece` | Body text |
| Tertiary | `#9c9c9d` | Links default / secondary nav |
| Disabled | `#6a6b6c` | |
| Border default | `rgba(255,255,255,0.06)` (≈`#252829`) | Card containment |
| Border interactive | `rgba(255,255,255,0.1)` (≈`#2f3031`) | Buttons |
| Brand Red | `#FF6363` | Hero stripe / error only |
| Interactive Blue | `hsl(202,100%,67%)` ≈ `#55b3ff` | Links / focus |
| Success Green | `hsl(151,59%,59%)` ≈ `#5fc992` | |

## Typography

- Family: `Inter`, mono `GeistMono`.
- Enable `font-feature-settings: "calt","kern","liga","ss03"` on all Inter text. (Hero: `"liga" 0, "ss02", "ss08"`.)
- **Positive letter-spacing** (+0.2 to +0.4 px) on body text — opposite of most dark UIs.
- Weight 500 baseline for body (not 400) — improves dark-mode legibility.

| Role | Size | Weight | Spacing |
|------|------|--------|---------|
| Hero | 64 | 600 | 0 |
| Section | 56 | 400 | +0.2 |
| Card title | 22 | 400 | 0 |
| Sub-heading | 20 | 500 | +0.2 |
| Body | 16 | **500** | +0.2 |
| Button | 16 | 600 | +0.3 |
| Caption | 14 | 500 | +0.2 |
| Small | 12 | 600 | 0 |

## Radius & Shadow

- Radius: micro 2-3 · keys 4-5 · button 6 · input 8 · card 12 · feature 16-20 · primary pill **86+** (full pill).
- macOS-native button shadow (signature):
  ```
  rgba(255,255,255,0.05) 0 1px  0 0 inset,
  rgba(255,255,255,0.25) 0 0    0 1px,
  rgba(0,0,0,0.2)        0 -1px 0 0 inset
  ```
- Card double-ring: `#1b1c1e 0 0 0 1px outer + #07080a 0 0 0 1px inset`.
- Hover transition: **opacity 0.6** (not color change) — Raycast signature.

## Pencil `variables` block (copy-ready)

```json
"variables": {
  "--background":         { "type": "color", "value": "#07080a" },
  "--card":               { "type": "color", "value": "#101111" },
  "--secondary":          { "type": "color", "value": "#1b1c1e" },
  "--foreground":         { "type": "color", "value": "#f9f9f9" },
  "--muted-foreground":   { "type": "color", "value": "#9c9c9d" },
  "--primary":            { "type": "color", "value": "#ffffff" },
  "--primary-foreground": { "type": "color", "value": "#18191a" },
  "--accent":             { "type": "color", "value": "#FF6363" },
  "--info":               { "type": "color", "value": "#55b3ff" },
  "--success":            { "type": "color", "value": "#5fc992" },
  "--border":             { "type": "color", "value": "#252829" },
  "--ring":               { "type": "color", "value": "#55b3ff" },
  "--radius-sm":          { "type": "number", "value": 4 },
  "--radius-md":          { "type": "number", "value": 6 },
  "--radius-lg":          { "type": "number", "value": 12 },
  "--radius-xl":          { "type": "number", "value": 16 },
  "--radius-pill":        { "type": "number", "value": 86 },
  "--font-primary":       { "type": "string", "value": "Inter" }
}
```

## Component Recipes

**Primary pill CTA**: `hsla(0,0%,100%,0.815)` fill, `#18191a` text, 86 radius, padding `[10,20]`. Hover → opacity 1.

**Secondary button**: transparent fill, `1px solid rgba(255,255,255,0.1)`, 6 px radius, white text. Hover → opacity 0.6.

**Card**: `#101111` fill, `1px solid rgba(255,255,255,0.06)`, 16 px radius. Optional double-ring effect.

**Keyboard key**: gradient `#121212→#0d0d0d`, multi-layer shadow, 4 px radius, 12 px Inter 600 text, `#cecece` color.

**Alert (error)**: `#101111` fill, left `2 px solid #FF6363` accent, glow `rgba(255,99,99,0.15)`.

## Do / Don't

✓ `#07080a` not `#000` · positive letter-spacing on body · weight 500 baseline · multi-layer shadows with inset highlights · `rgba(255,255,255,0.06)` borders · pill 86+ for primary, 6-8 for secondary · OpenType `calt,kern,liga,ss03` always · opacity-based hover transitions.

✗ No pure black bg · no negative tracking on body · no single-layer flat shadows · no Raycast Red as decoration (punctuation only) · no weight 400 body text when 500 available · no mixing warm/cool borders.
