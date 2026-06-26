# Kadence Design System Foundation

This is the practical design-system layer for Kadence sites.

## 1) Token hierarchy

Always design in this order:
1. Palette tokens (brand + neutral + semantic)
2. Typography scale (display, h1-h6, body, small)
3. Spacing rhythm (section, component, inline)
4. Container/layout width rules
5. Component variants (primary/secondary/ghost etc.)

Avoid hardcoded one-off values when a global token exists.

## 2) Global color strategy

- Define a small intentional palette:
  - Primary brand
  - Secondary accent
  - Text strong / text muted
  - Surface / surface-alt
  - Border subtle
  - Success / warning / error where needed
- Reuse palette slots consistently across blocks and templates.

## 3) Typography strategy

- Keep heading and body families coherent.
- Use predictable type scale and line-height.
- Preserve contrast and readability over stylistic novelty.

## 4) Layout system

- Set one content max-width and one wider marketing width.
- Use repeatable section spacing presets.
- Prefer stacked, responsive section patterns over custom breakpoint CSS.

## 5) Component conventions

Standardize these primitives:
- Hero sections
- Card grids
- Feature rows
- FAQ blocks
- CTA strips
- Buttons and links

Keep variant count low; consistency beats novelty.

## 6) Accessibility defaults

- One H1 per page.
- Logical heading nesting.
- Adequate color contrast.
- Clear focus states and usable nav labels.
- Avoid text embedded inside decorative images.

## 7) SEO-aware structure

- Semantic sectioning and heading hierarchy.
- Internal links where intent aligns.
- Clear page intro above the fold.
- Scannable blocks with concise paragraphs and bullets.