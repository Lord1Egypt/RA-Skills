# Kadence Theme Free vs Pro Matrix

Use this matrix to avoid mismatched implementations.

## Quick rule

- If Pro is not explicitly confirmed, implement from **Free Baseline** only.
- Treat all Pro items as conditional enhancements.

## Free Baseline (safe defaults)

Commonly available in Kadence Theme Free and safe to assume:
- Global color palette usage
- Typography settings
- Page layout controls
- Archive layout controls
- Single post layout controls
- Header builder baseline items (logo, primary navigation, basic buttons/social/html/search)
- Mobile navigation customization
- Sticky/transparent header behaviors (where available in theme settings)
- Basic WooCommerce theme integration settings
- Performance settings in theme customizer

## Pro / Premium-leaning Features (require verification)

From Kadence docs and header item labeling, these should be treated as Pro-dependent unless verified otherwise:

1. **Kadence Elements system**
   - Hooked Elements
   - Fixed Elements
   - Content Elements
   - Template Elements
   - Element display conditions
2. **Conditional header logic / advanced display targeting**
3. **Header premium item set** (as documented in classic header items)
   - Free Shipping Cart Notice
   - Dividers
   - Search Bar (advanced header item)
   - Widget Area
   - Toggle Widget Area
   - Dark Mode Toggle
4. **Theme Kit Pro / Pro template flows**
5. **Advanced WooCommerce add-ons** beyond baseline styling

## Practical Decision Tree

1. Need only content pages + standard site shell?
   - Use Free baseline.
2. Need conditional injections, template overrides by rules, or global hook regions?
   - Requires Pro-capability check first.
3. Need premium header utilities (widget area, dark mode toggle, etc.)?
   - Mark as Pro-dependent and propose Free fallback.

## Free Fallback Patterns

When Pro is unavailable:
- Replace Hooked/Template element logic with native Gutenberg page/template composition.
- Replace conditional header behavior with a single universal header design.
- Replace premium header utilities with standard nav + button + icon links.
- Keep CTA bands and promos as reusable block patterns instead of dynamic elements.