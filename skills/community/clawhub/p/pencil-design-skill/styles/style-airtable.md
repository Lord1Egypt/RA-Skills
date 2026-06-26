# Style: Airtable

> Source: <https://getdesign.md/airtable/design-md>
> Light editorial · Haas Grotesk · near-black pill CTA · full-bleed signature surface cards.
> Best for data tools, multi-color SaaS marketing pages, structured-data UIs.

## Identity (1-line)

White canvas (`#ffffff`) with **near-black ink** (`#181d26`) as the primary brand color — both the hero type and the primary CTA share this single near-black hue. Brand voltage comes not from gradients or accent walls, but from **full-bleed signature surface cards** in coral (`#aa2d00`), forest (`#0a2e0e`), cream (`#f5e9d4`), and navy (`#181d26`) that punctuate long-scroll editorial pages every two or three viewports. Type runs Haas Grotesk at modest weights (400 for display, 500 for buttons / sub-titles) — display headlines never bolder than 500. The pricing surface speaks its own dialect: **Inter Display** at mid-weight 475 with **pill-shaped CTAs** (the only place pill radius appears).

## Token Table

| Token | Value | Notes |
|-------|-------|-------|
| Canvas | `#ffffff` | Default page surface |
| Surface soft | `#f8fafc` | Tabbed feature cards, featured pricing tier |
| Surface strong | `#e0e2e6` | Light-gray CTA banner near footer |
| Surface dark | `#181d26` | Dark navy mid-page CTA cards (same hex as ink) |
| Surface dark elevated | `#1d1f25` | Articles hero base |
| Hairline | `#dddddd` | 1px borders for inputs, secondary buttons, dividers |
| Border strong | `#9297a0` | Disabled secondary outline |
| Primary / Ink | `#181d26` | Near-black — primary CTA bg AND h1/h2 type |
| Primary active | `#0d1218` | Press state on primary buttons |
| Body | `#333840` | Default running text |
| Muted | `#41454d` | Footer links, captions |
| On primary / on dark | `#ffffff` | Text on primary buttons & dark surfaces |
| Signature coral | `#aa2d00` | Largest signature card (oxide red) |
| Signature forest | `#0a2e0e` | Deep-green signature card |
| Signature cream | `#f5e9d4` | Cream callout band |
| Signature peach | `#fcab79` | Demo-card surface |
| Signature mint | `#a8d8c4` | Demo-card surface |
| Signature yellow | `#f4d35e` | Demo-card surface |
| Signature mustard | `#d9a441` | Demo-card surface |
| Link | `#1b61c9` | Inline body links — **NOT** primary button color |
| Link active | `#1a3866` | Press state |
| Info border | `#458fff` | Focused-input outline |
| Success | `#006400` / border `#39bf45` | Confirmation states |

## Typography

- Family: `Haas Groot Disp` (display 24px+) / `Haas Grotesk` (≤ 24px). Fallback: `Inter Display` for display + `Inter` for text.
- Pricing sub-system: `Inter Display` at custom weight **475** (variable font).
- **Weight ladder**: 400 (display + body) / 500 (sub-titles, buttons) / 600 only for legal/cookie surfaces. **No 700**.

| Role | Size | Weight | Line height | Spacing |
|------|------|--------|-------------|---------|
| Display XL | 48 | 500 | 1.10 | 0 |
| Display LG (h1) | 40 | 400 | 1.20 | 0 |
| Display MD (h2) | 32 | 400 | 1.20 | 0 |
| Title LG | 24 | 400 | 1.35 | +0.12 px |
| Title MD | 20 | 400 | 1.50 | 0 |
| Title SM | 18 | 500 | 1.40 | 0 |
| Label / Button | 16 | 500 | 1.40 | 0 |
| Body | 14 | 400 | 1.25 | 0 |
| Caption | 14 | 500 | 1.35 | +0.16 px |
| Legal | 13.12 | 600 | 1.20 | 0 |
| Pricing display | 44.8 | 475 | 1.10 | 0 (Inter Display) |
| Pricing card title | 20 | 475 | 1.30 | 0 (Inter Display) |

## Radius & Depth

- Radius: `xs` 2 (legal/cookie) · `sm` 6 (inputs) · `md` 10 (content cards, demo grids, cream callouts) · `lg` 12 (primary CTA, signature cards, tabbed feature cards) · `pill` 9999 (pricing CTAs only) · `full` 9999 (icon buttons).
- **Color-block first, shadow second.** Depth comes from contrast between white canvas and signature surface cards. No card shadow language, no atmospheric mesh, no hero gradient.
- Section vertical rhythm: **96 px** top + 96 px bottom on every editorial band. Universal.

## Pencil `variables` block (copy-ready)

```json
"variables": {
  "--background":         { "type": "color", "value": "#ffffff" },
  "--card":               { "type": "color", "value": "#ffffff" },
  "--card-soft":          { "type": "color", "value": "#f8fafc" },
  "--card-strong":        { "type": "color", "value": "#e0e2e6" },
  "--popover":            { "type": "color", "value": "#ffffff" },
  "--foreground":         { "type": "color", "value": "#181d26" },
  "--body":               { "type": "color", "value": "#333840" },
  "--muted-foreground":   { "type": "color", "value": "#41454d" },
  "--primary":            { "type": "color", "value": "#181d26" },
  "--primary-foreground": { "type": "color", "value": "#ffffff" },
  "--primary-active":     { "type": "color", "value": "#0d1218" },
  "--accent-coral":       { "type": "color", "value": "#aa2d00" },
  "--accent-forest":      { "type": "color", "value": "#0a2e0e" },
  "--accent-cream":       { "type": "color", "value": "#f5e9d4" },
  "--accent-peach":       { "type": "color", "value": "#fcab79" },
  "--accent-mint":        { "type": "color", "value": "#a8d8c4" },
  "--accent-yellow":      { "type": "color", "value": "#f4d35e" },
  "--accent-mustard":     { "type": "color", "value": "#d9a441" },
  "--surface-dark":       { "type": "color", "value": "#181d26" },
  "--link":               { "type": "color", "value": "#1b61c9" },
  "--border":             { "type": "color", "value": "#dddddd" },
  "--border-strong":      { "type": "color", "value": "#9297a0" },
  "--ring":               { "type": "color", "value": "#458fff" },
  "--radius-xs":          { "type": "number", "value": 2 },
  "--radius-sm":          { "type": "number", "value": 6 },
  "--radius-md":          { "type": "number", "value": 10 },
  "--radius-lg":          { "type": "number", "value": 12 },
  "--radius-pill":        { "type": "number", "value": 9999 },
  "--font-primary":       { "type": "string", "value": "Inter" },
  "--font-pricing":       { "type": "string", "value": "Inter" }
}
```

## Component Recipes

**Primary CTA**: `#181d26` fill, `#ffffff` text, **12 px radius**, padding `[16, 24]`, 16 px Haas weight 500. One per viewport — scarcity is the design.

**Secondary CTA**: `#ffffff` fill, `#181d26` text, **12 px radius**, padding `[16, 24]`, 1 px solid `#dddddd` border. Pairs with primary as the signature button row.

**Signature coral card**: `#aa2d00` fill, `#ffffff` text, **12 px radius**, padding `48`, h2 at 32 px Haas 400. Carries `button-secondary-on-dark` (still white fill, never translucent).

**Signature forest card**: `#0a2e0e` fill, `#ffffff` text, 12 px radius, padding `48`. Same shape as coral.

**Hero dark card**: `#181d26` fill, `#ffffff` text, 12 px radius, padding `48`. Same hex as ink — primary doubles as dark surface.

**Tabbed feature card**: `#f8fafc` fill, **12 px radius**, padding `32`. Left rail = vertical tab labels in 20 px Haas 400; right pane = active content.

**Cream callout**: `#f5e9d4` fill, `#181d26` text, **10 px radius**, padding `24`.

**Demo-grid card**: `#ffffff` (or peach/mint/yellow/mustard) fill, **10 px radius**, padding `16`. **Heights deliberately uneven** — uniform reads as spec sheet.

**Article card**: `#ffffff`, 10 px radius, padding `16`, illustrated 16:9 thumbnail, 18 px title weight 500.

**Logo strip**: `#ffffff` bg, monochrome `#41454d` logos, 32 px vertical padding, 6-up desktop / 3-up mobile.

**Text input**: `#ffffff` fill, **6 px radius**, padding `[12, 16]`, 44 px height, 1 px `#dddddd` border. Focus → border `#458fff`.

**Pricing tier card**: `#ffffff` fill, **10 px radius**, padding `32`. Featured tier = `#f8fafc` bg (no border, no badge — tone shift IS the signal). Price block: 44.8 px Inter Display weight 475.

**Pricing pill CTA**: `#ffffff` fill, `#1d1f25` text, **9999 radius**, padding `[12, 24]`. Pill only appears on pricing — sub-system signal.

**CTA banner light**: `#e0e2e6` fill, `#181d26` text, 12 px radius, padding `48`. The "Start building" strip near footer.

**Section rhythm rule**: white → coral → white → cream → dark navy → light gray → footer. Never two whites in a row.

## Do / Don't

✓ Primary CTA always near-black `#181d26` (NEVER link blue) · one primary per viewport · whitespace is the hero atmosphere (no gradient/mesh/aurora) · signature cards in coral/forest/dark/cream for voltage moments · demo-grid heights deliberately uneven · pricing sub-system stays self-contained (Inter Display 475 + pill radius) · 96 px vertical rhythm on every editorial band · weight ladder stops at 500 (legal exception 600).

✗ **Don't make `#1b61c9` link blue the primary button** — it's the link color only · no hero gradient/aurora/mesh · no display type at weight 700 · no `pill` radius outside the pricing surface · no two consecutive white bands · no shadow language for cards (color-block first) · no extra accent colors beyond the documented signature palette · no inverted/translucent buttons on dark signature cards (white stays white).
