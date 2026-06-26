# Style: Apple

> Source: <https://getdesign.md/apple/design-md>
> Photography-first · SF Pro · single Action Blue · alternating full-bleed light/dark tiles · museum-gallery pacing.
> Best for premium consumer-product pages, cinematic marketing, single-accent luxury sites.

## Identity (1-line)

Edge-to-edge **product tiles** alternating light canvas (`#ffffff` / parchment `#f5f5f7`) with near-black tiles (`#272729`), each tile occupying ~one viewport. Type is SF Pro Display at weight 600 with **negative letter-spacing** (`-0.28 → -0.374 px`) — the signature "Apple tight" cadence. **One** interactive color across the entire system: Action Blue `#0066cc`. **One** drop shadow in the entire system, applied only to product photography (`rgba(0,0,0,0.22) 3px 5px 30px`). Body copy runs **17 px** (not 16) for an unmistakable reading pace. Pill-shaped (`9999`) primary CTA is the brand-action signal; everything else stays compact `8 / 11 / 18` radius. The wall disappears so the product can speak.

## Token Table

| Token | Value | Notes |
|-------|-------|-------|
| Action blue (primary) | `#0066cc` | The ONLY interactive color |
| Focus blue | `#0071e3` | Keyboard focus ring |
| Sky link blue (on dark) | `#2997ff` | Inline links on dark tiles only |
| Canvas | `#ffffff` | Pure white default |
| Canvas parchment | `#f5f5f7` | Signature off-white — alternating tiles, footer, sub-nav |
| Surface pearl | `#fafafc` | Ghost/secondary button fill |
| Surface tile 1 | `#272729` | Primary dark-tile bg |
| Surface tile 2 | `#2a2a2c` | Micro-step lighter (adjacent dark tile separation) |
| Surface tile 3 | `#252527` | Micro-step darker (player frames, stack bottom) |
| Surface black | `#000000` | True void — global nav, video |
| Chip translucent | `#d2d2d7` | Used at ~64% alpha over photography |
| Ink / body | `#1d1d1f` | Near-black — all text on light surfaces |
| Body on dark | `#ffffff` | Text on dark tiles |
| Body muted (dark) | `#cccccc` | Secondary copy on dark |
| Ink muted 80 | `#333333` | Pearl button body text |
| Ink muted 48 | `#7a7a7a` | Disabled & legal fine print |
| Divider soft | `#f0f0f0` | Soft button ring |
| Hairline | `#e0e0e0` | 1 px borders on utility cards / chips |

> **No decorative gradients exist.** Atmosphere is photographic — never CSS.

## Typography

- Display: `SF Pro Display, system-ui, -apple-system, sans-serif` (≥ 19 px).
- Text: `SF Pro Text, system-ui, -apple-system, sans-serif` (< 20 px).
- Fallback: `Inter` / `Inter Display` (variable). Tighten letter-spacing by `-0.01em` and line-height by `0.03` to match.
- **Weight ladder**: 300 / 400 / 600 / 700. **Weight 500 is deliberately absent.**

| Role | Size | Weight | Line height | Spacing |
|------|------|--------|-------------|---------|
| Hero display | 56 | 600 | 1.07 | **−0.28 px** |
| Display LG | 40 | 600 | 1.10 | 0 |
| Display MD | 34 | 600 | 1.47 | −0.374 px |
| Lead | 28 | 400 | 1.14 | +0.196 px |
| Lead airy | 24 | **300** | 1.50 | 0 (rare 300) |
| Tagline | 21 | 600 | 1.19 | +0.231 px |
| Body strong | 17 | 600 | 1.24 | −0.374 px |
| **Body** | **17** | **400** | **1.47** | **−0.374 px** |
| Dense link (footer) | 17 | 400 | **2.41** | 0 |
| Caption | 14 | 400 | 1.43 | −0.224 px |
| Caption strong | 14 | 600 | 1.29 | −0.224 px |
| Button large (store) | 18 | **300** | 1.00 | 0 (rare 300) |
| Button utility | 14 | 400 | 1.29 | −0.224 px |
| Fine print | 12 | 400 | 1.00 | −0.12 px |
| Nav link | 12 | 400 | 1.00 | −0.12 px |
| Micro legal | 10 | 400 | 1.30 | −0.08 px |

## Radius & Depth

- Radius: `none` 0 (full-bleed tiles) · `xs` 5 · `sm` 8 (dark utility buttons, nav cluster) · `md` 11 (Pearl Button) · `lg` 18 (utility cards, accessory grid) · `pill` 9999 (primary CTA, search input, configurator chip, sticky CTA) · `full` 9999 (icon chips).
- **Exactly ONE shadow** in the entire system: `rgba(0,0,0,0.22) 3px 5px 30px 0` — applied only to product photography, never to cards/buttons/text.
- Depth signals:
  - Surface-color change between tiles (light ↔ dark) IS the section divider — no borders, no rules.
  - `backdrop-filter: blur(20px) saturate(180%)` on parchment-80% for sub-nav and floating sticky bar.
  - 1 px `rgba(0,0,0,0.08)` border on utility cards / configurator chips.
- Active/press state on every button: `transform: scale(0.95)` — the system-wide micro-interaction.

## Pencil `variables` block (copy-ready)

```json
"variables": {
  "--background":         { "type": "color", "value": "#ffffff" },
  "--background-parchment": { "type": "color", "value": "#f5f5f7" },
  "--card":               { "type": "color", "value": "#ffffff" },
  "--card-pearl":         { "type": "color", "value": "#fafafc" },
  "--popover":            { "type": "color", "value": "#ffffff" },
  "--surface-tile-light": { "type": "color", "value": "#ffffff" },
  "--surface-tile-dark":  { "type": "color", "value": "#272729" },
  "--surface-tile-dark-2":{ "type": "color", "value": "#2a2a2c" },
  "--surface-tile-dark-3":{ "type": "color", "value": "#252527" },
  "--surface-black":      { "type": "color", "value": "#000000" },
  "--foreground":         { "type": "color", "value": "#1d1d1f" },
  "--foreground-on-dark": { "type": "color", "value": "#ffffff" },
  "--muted-foreground":   { "type": "color", "value": "#7a7a7a" },
  "--muted-on-dark":      { "type": "color", "value": "#cccccc" },
  "--ink-muted-80":       { "type": "color", "value": "#333333" },
  "--primary":            { "type": "color", "value": "#0066cc" },
  "--primary-foreground": { "type": "color", "value": "#ffffff" },
  "--primary-focus":      { "type": "color", "value": "#0071e3" },
  "--primary-on-dark":    { "type": "color", "value": "#2997ff" },
  "--ink":                { "type": "color", "value": "#1d1d1f" },
  "--border":             { "type": "color", "value": "#e0e0e0" },
  "--border-soft":        { "type": "color", "value": "#f0f0f0" },
  "--ring":               { "type": "color", "value": "#0071e3" },
  "--radius-xs":          { "type": "number", "value": 5 },
  "--radius-sm":          { "type": "number", "value": 8 },
  "--radius-md":          { "type": "number", "value": 11 },
  "--radius-lg":          { "type": "number", "value": 18 },
  "--radius-pill":        { "type": "number", "value": 9999 },
  "--radius-none":        { "type": "number", "value": 0 },
  "--font-primary":       { "type": "string", "value": "Inter" },
  "--font-display":       { "type": "string", "value": "Inter" }
}
```

## Component Recipes

**Primary pill CTA**: `#0066cc` fill, `#ffffff` text, **9999 radius (pill)**, padding `[11, 22]`, 17 px SF Pro Text weight 400. The full-pill IS the brand-action signal.

**Secondary ghost pill**: transparent fill, `#0066cc` text, `1px solid #0066cc`, 9999 radius, padding `[11, 22]`. Pairs as second CTA ("Learn more" / "Buy").

**Dark utility button** (nav cluster): `#1d1d1f` fill, `#ffffff` text, **8 px radius**, padding `[8, 15]`, 14 px weight 400.

**Pearl capsule button**: `#fafafc` fill, `#333333` text, **11 px radius**, padding `[8, 14]`, 14 px caption, 3 px solid `#f0f0f0` border (functions as a soft ring).

**Store hero CTA**: `#0066cc` fill, `#ffffff` text, 9999 radius, padding `[14, 28]`, **18 px SF Pro Text weight 300** (rare).

**Icon circular**: 44 × 44 px, `#d2d2d7` at 64% alpha, `#1d1d1f` icon, 9999 radius. Floats over photography.

**Global nav**: `#000000` fill, height 44 px, links 12 px / 400 / `−0.12 px`, white text. The only place pure black appears on most pages.

**Frosted sub-nav**: `#f5f5f7` at 80% opacity + `backdrop-filter: blur(20px) saturate(180%)`, height 52 px. Left = product name 21 px weight 600. Right = inline 14 px links + persistent primary pill.

**Product tile (light)**: `#ffffff`, **0 radius (full-bleed)**, vertical padding **80 px**. Centered stack: name (40 / 600) → tagline (28 / 400) → two pill CTAs → product render with the system shadow.

**Product tile (parchment)**: same as light tile but on `#f5f5f7`. Used to break two consecutive whites.

**Product tile (dark)**: `#272729`, full-bleed, padding 80 px. Same content stack with `text-link-on-dark` (`#2997ff`). Variants `-2` (`#2a2a2c`) and `-3` (`#252527`) for adjacent stacking.

**Store utility card**: `#ffffff`, 1 px solid `#e0e0e0`, **18 px radius**, padding `24`. Image 1:1 (8 px inner radius) → name 17 px / 600 → price 17 px / 400 → text-link.

**Configurator chip**: `#ffffff`, **9999 pill radius**, padding `[12, 16]`, 14 px caption. Selected = 2 px `#0071e3` border (no fill change).

**Search input**: `#ffffff`, **9999 pill radius** (search is also pill — matches CTA grammar), padding `[12, 20]`, 44 px height, 17 px body, 1 px `rgba(0,0,0,0.08)` border.

**Floating sticky bar** (buy page bottom): `#f5f5f7` at 80% + backdrop blur, height 64 px, padding `[12, 32]`. Right cluster = primary pill CTA.

**Footer**: `#f5f5f7` bg, link columns at **17 px / 400 / line-height 2.41** (the relaxed leading is what makes dense columns scannable). Headings 14 px / 600. Legal 12 px in `#7a7a7a`.

**Section rhythm rule**: light → dark tile → light → dark → parchment footer. The color change IS the divider (no border, no rule).

## Theme Mode

Mixed — the system alternates light and dark **tiles** within a single page, but the page chassis (nav, sub-nav, footer) is light-dominant by default. For Pencil: keep top-level frame `theme: { "Mode": "Light" }`. Apply `Mode: "Dark"` only on `surface-tile-dark` frames where you want true tile inversion.

## Do / Don't

✓ One accent only — Action Blue `#0066cc` carries every interactive element · headlines at SF Pro Display 600 with negative letter-spacing (`−0.28 → −0.374 px`) — the signature "Apple tight" cadence · body at **17 px / 400 / 1.47 / −0.374 px** (NEVER 16 px) · alternate light/dark tiles for section rhythm — the color change IS the divider · pill radius (9999) reserved for "this is an action" elements (primary CTA, search, configurator chip, sticky CTA) · the single product shadow is for product imagery only · `transform: scale(0.95)` as universal active state · keep global nav `#000000` (the only pure black on most pages).

✗ **No second accent color** — every "click me" is `#0066cc` · no shadows on cards/buttons/text — shadow is reserved for product photography · no decorative gradients — atmosphere is photographic · **no weight 500** anywhere — the ladder is 300 / 400 / 600 / 700 · no rounded corners on full-bleed tiles · no body line-height tighter than 1.47 · no mixing of radii grammars (sm 8 / lg 18 / pill — nothing in between except the rare 11 Pearl) · don't use `#2997ff` Sky Blue on light surfaces — it's the dark-tile-only variant.
