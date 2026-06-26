# Mobile Checkout Audit Checklist

The checkout is where audit findings turn into revenue lift. Walk the flow field-by-field on a real mobile device.

## Pre-checkout (cart page)

- [ ] Cart has sticky bottom "Checkout" button on mobile
- [ ] Line items show image, title, size/variant, quantity, price
- [ ] Quantity stepper has ≥44×44pt buttons with ≥8pt spacing
- [ ] Item removal requires only 1 tap with confirmation
- [ ] Promo code field is hidden by default (collapsible) — otherwise every user hunts for one
- [ ] Shipping estimate visible before starting checkout
- [ ] Tax estimate visible for markets that include tax in price

## Checkout entry

- [ ] Guest checkout is the default; account creation is optional at the end
- [ ] Sign-in link is subtle, not prominent (defaults to guest)
- [ ] Express pay buttons visible first: Apple Pay, Google Pay, Shop Pay / PayPal
- [ ] Express pay buttons have correct height and spacing, native-feeling

## Contact information

- [ ] Email field uses `type="email"` for correct keyboard
- [ ] Email field has `autocomplete="email"`
- [ ] SMS / marketing opt-in is a checkbox, unchecked by default
- [ ] Phone number is optional (or clearly required with reason)

## Shipping address

- [ ] Country selector at the top so subsequent fields format correctly
- [ ] Address autocomplete (Google Places, Loqate, etc.) reduces typing
- [ ] `autocomplete` attributes on every field (`street-address`, `address-level2` for city, `postal-code`, `country`)
- [ ] ZIP/Postal field uses numeric keyboard where appropriate
- [ ] State/Province is a dropdown or autocomplete, not free text
- [ ] Address line 2 is optional and labeled as such

## Shipping method

- [ ] Options clearly labeled with price and delivery window
- [ ] Default selection is a reasonable middle option, not the most expensive
- [ ] Free-shipping threshold progress shown if applicable

## Payment

- [ ] Card number field uses `inputmode="numeric"` and `autocomplete="cc-number"`
- [ ] Card icons shown next to the field or inline as user types
- [ ] Expiry field uses `inputmode="numeric"` with auto-formatting (MM/YY)
- [ ] CVV uses `inputmode="numeric"` with appropriate length
- [ ] Billing address defaults to shipping address
- [ ] 3DS flow is inline, not a full-page redirect
- [ ] Apple Pay / Google Pay alternative visible as a fallback path

## Review and place order

- [ ] Order summary always visible (collapsible on mobile)
- [ ] Total, subtotal, shipping, tax clearly broken out
- [ ] Terms and conditions link is reachable without leaving checkout
- [ ] "Place order" button is sticky-bottom or clearly dominant
- [ ] After tapping "Place order," button shows loading state to prevent double-tap

## Confirmation page

- [ ] Order number and summary visible immediately
- [ ] Clear expectation of next steps (email confirmation, shipping time)
- [ ] Account creation offered post-checkout as a one-tap option
- [ ] Social share or referral offered (optional, post-sale)

## Performance

- [ ] Checkout pages load in ≤2s on 4G
- [ ] Transitions between steps feel immediate (no full-page reload on SPA)
- [ ] Validation errors appear inline, not at the top of the page
- [ ] Error messages are specific and helpful ("ZIP code doesn't match state" not "Invalid address")

## Accessibility

- [ ] All form labels are associated with inputs (`<label for=...>` or wrapping)
- [ ] Error state announced to screen readers (`aria-live`)
- [ ] Focus visible when tabbing through fields
- [ ] Color contrast ≥4.5:1 for all text
- [ ] Tap targets never smaller than 44×44pt
