# Mobile UX Audit Checklist

Complete checklist for quarterly audit. 42 items across 7 categories.

## 1. Performance (6 checks)

- [ ] Field LCP p75 measured (PageSpeed Insights or RUM)
- [ ] Field INP p75 measured
- [ ] Field CLS p75 measured
- [ ] Lab audit (Lighthouse) run on primary templates
- [ ] TTFB <600ms confirmed
- [ ] Third-party script budget reviewed (count, size, defer)

## 2. Navigation and tap targets (5 checks)

- [ ] All primary CTAs ≥44×44pt
- [ ] Spacing between targets ≥8pt
- [ ] Primary CTA in thumb zone (bottom third or sticky-bottom)
- [ ] Close buttons on modals visible and reachable
- [ ] Back navigation consistent (browser back + in-app back not conflicting)

## 3. PDP (product detail page) (6 checks)

- [ ] Hero image ≤200KB at mobile breakpoint
- [ ] Image carousel swipe works smoothly, no jank
- [ ] Add-to-cart button sticky-bottom or in bottom third
- [ ] Variant selector works with thumb, no accidental variant flips
- [ ] Quantity stepper has proper spacing
- [ ] Price, savings, stock status visible above fold

## 4. Cart (5 checks)

- [ ] Sticky checkout button
- [ ] Line item editing (qty, remove) works in one tap
- [ ] Shipping and tax estimates visible before checkout start
- [ ] Free shipping threshold progress shown
- [ ] Promo code field hidden by default but easy to reveal

## 5. Checkout (7 checks)

- [ ] Guest checkout default
- [ ] Express pay (Apple Pay / Google Pay / Shop Pay) offered
- [ ] ≤8 required form fields in total
- [ ] Proper `type` and `autocomplete` attributes on every field
- [ ] Inline validation with helpful error messages
- [ ] Order summary always visible (collapsible)
- [ ] Place-order button sticky-bottom, loading state on tap

## 6. Images, media, fonts (6 checks)

- [ ] All images have width/height attributes
- [ ] Below-fold images lazy-loaded
- [ ] WebP or AVIF formats served
- [ ] Responsive srcset per viewport
- [ ] Web fonts WOFF2, preloaded for critical text
- [ ] No autoplay video on mobile

## 7. Forms, keyboards, accessibility (7 checks)

- [ ] Labels associated with inputs
- [ ] Correct keyboard for each input type (email, tel, numeric, url)
- [ ] Autocomplete attributes used where applicable
- [ ] Color contrast ≥4.5:1 for text
- [ ] Focus visible when tabbing
- [ ] Errors announced to screen readers
- [ ] Tested with JavaScript partially disabled / slow network
