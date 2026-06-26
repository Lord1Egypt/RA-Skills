# Branding, Logos, Icons, and Favicons

## Core Rule

- Keep the source of truth in vector form when possible.
- Export PNG fallbacks from the vector source instead of editing the raster fallback and letting quality drift.
- If a logo or icon must work at 16-32 px, design for that size explicitly instead of shrinking the desktop version and hoping.

## Logos and Marks

- Detailed wordmarks and tiny taglines usually do not survive favicon or avatar sizes.
- Prepare simplified marks for tiny surfaces: favicon, social avatar, app icon, browser tab, and notification icon are not the same job as hero branding.
- Test logos on light and dark backgrounds before declaring the export done.
- Thin outlines, hairline strokes, and low-contrast brand colors disappear first at small sizes.

## SVG Rules

- Preserve the vector master when the destination supports SVG.
- Keep the SVG simple: remove hidden layers, editor cruft, and unnecessary groups.
- Use a consistent viewBox and avoid accidental off-canvas whitespace.
- For icon sets, keep stroke width, caps, joins, padding, and optical weight consistent across the set.
- If the SVG is going to be styled by CSS, prefer `currentColor` over hardcoded fills when appropriate.

## Raster Fallbacks

- Export PNG when transparency matters and SVG is unsupported or blocked.
- Export JPEG only when the asset is photographic or the destination forbids alpha-safe formats.
- Do not let transparent logos pick up accidental matte colors during export.
- If a logo is going onto colored backgrounds, preview that exact background before final export.

## Favicons and App Icons

- A real favicon package often needs more than one file: SVG, ICO, apple-touch icon, and larger app icons.
- Apple touch icons need an opaque background; transparent icons can render badly or fill with black.
- Favicon or app-icon artwork should live in the central safe area, not touch edges.
- If the mark is not readable at 16 px, simplify it instead of sharpening it harder.

## Icon-Set Consistency

- Do not mix filled, outlined, rounded, and sharp-corner icons randomly in one set unless that contrast is intentional.
- Similar icons should share the same baseline geometry, padding, and visual weight.
- Curves often look optically thinner than straight segments, so balance by shape size, not random stroke-width overrides.
- Review icons at 1x and 2x sizes on both light and dark surfaces.

## Common Branding Traps

- Exporting one logo variant and using it everywhere.
- Using a horizontal logo where a square avatar or app icon is needed.
- Leaving too much transparent padding around the mark so it looks tiny in production.
- Converting a vector icon to JPEG and losing edges, alpha, and crispness.
- Shipping an icon set where every icon has slightly different stroke thickness or corner behavior.
- Forgetting that browser tabs, mobile home screens, and social avatars all crop and display branding differently.
