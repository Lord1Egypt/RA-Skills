# Elements and Template Architecture (Kadence)

Use this to decide structure, not just block selection.

## A) Site shell areas

1. Header
   - Identity (logo)
   - Primary navigation
   - Utility actions (CTA/login/contact)
2. Footer
   - Navigation/support links
   - Legal/company details
   - Optional CTA or lead capture
3. Content region
   - Page/post templates
   - Archive templates

## B) Template layers

Design each request across these layers:
- Global defaults (site-wide)
- Content type defaults (page/post/archive)
- Page-specific overrides (only when necessary)

Minimize overrides to reduce maintenance cost.

## C) Kadence Elements (Pro-capability)

When Pro is confirmed, use Elements for reusable conditional logic:
- Hooked Element: inject content into theme hook locations.
- Fixed Element: persistent UI region.
- Content Element: reusable content region with display controls.
- Template Element: override template areas under conditions.

If Pro is not confirmed, do not rely on this mechanism.

## D) Header architecture patterns

Free-safe patterns:
- Standard: logo + menu + CTA button
- Marketing: logo + menu + dual CTA
- Compact mobile: logo + off-canvas toggle + primary CTA

Pro-leaning enhancement patterns:
- Conditional header variants by context
- Premium header utilities (widget/search-bar/dark mode toggle/dividers)

## E) WooCommerce structure guidance

Baseline:
- Clean product/archive typography and spacing
- Consistent button and price styles
- Mobile-first cart/checkout readability

Advanced (verify Pro/add-ons):
- Additional WooCommerce add-ons and merchandising behavior

## F) Change management pattern

For any template/system change:
1. Snapshot current behavior.
2. Apply smallest viable configuration change.
3. Validate desktop/tablet/mobile.
4. Validate affected routes (home, key landing, blog/archive, single).
5. Document Free-safe fallback if Pro enhancement was requested.