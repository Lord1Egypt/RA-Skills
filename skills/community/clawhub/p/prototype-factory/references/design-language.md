# Design Language Snapshot

Use this when the user hasn't provided explicit branding.

## Palette
- **Core neon**: `#00FF99`
- **Accent purple**: `#6C63FF`
- **Carbon background**: `#050B0F`
- **Surface elevation**: `#0F1C26`
- **Warning highlight**: `#FF8C42`

## Typography
- Headings: "Space Grotesk", 600 weight
- Body: "Inter" or "Urbanist", 400 weight, 1.5 line height
- Numerics/UI chrome: tabular figures via `font-variant-numeric: tabular-nums;`

## Components
- Primary buttons: 52px height, 16px radius, gradient from `#00FF99` → `#00B377`
- Cards: 24px radius, 1px border `rgba(255,255,255,0.08)`, inner padding 24px
- Iconography: duotone outlines, 24px baseline grid

## Motion
- Micro-interactions: 200ms ease-out
- Page transitions: 350ms fade/slide, delay heavy assets until after hero anim completes

Use these defaults when user only says "modern, clean, minimal" so prototypes feel cohesive.
