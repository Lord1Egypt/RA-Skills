# Thumb Zones and Interaction Patterns

The phone is held in one hand. The thumb is the primary interaction tool. Design for it.

## The three zones

Imagine a typical 6-inch phone held in the right hand. Divide the screen into three horizontal bands:

1. **Natural zone** (bottom third): easy reach, comfortable tap without grip adjustment. Bottom of screen ≈ near thumb tip.
2. **Stretch zone** (middle third): reachable with a small thumb flex. Comfortable for secondary actions.
3. **Strain zone** (top third): requires reaching up or shifting the phone in hand. Uncomfortable and error-prone.

Right-handed vs. left-handed users use the same zones but mirrored for diagonal reach.

## What goes where

### Bottom third (natural zone)

- Primary CTA (Buy, Add to Cart, Checkout, Place Order).
- Tab bar / bottom navigation.
- Sticky "proceed" buttons.
- Keyboard suggestions and autocomplete row.

### Middle third (stretch zone)

- Product content, descriptions.
- Secondary CTAs.
- Inline CTAs within content.
- Variant selectors.

### Top third (strain zone)

- Brand logo / header.
- Search icon (open search to pull content into middle).
- Close / back buttons — these are necessary up top; users accept the reach for navigation actions.
- Status bar, OS navigation.

## Target sizing

- **Apple HIG**: minimum 44×44pt tap target.
- **Material Design**: minimum 48×48dp.
- **Real-world recommendation**: 44×44pt with ≥8pt spacing between targets.

Smaller targets cause mis-taps. On a list of filter chips or a grid of color swatches, give each at least 44pt regardless of how small the swatch visual is.

## Common thumb-reach anti-patterns

1. **Primary CTA in the header**: forces a stretch or two-hand grip. Move to sticky-bottom.
2. **Close button in the top-right of a modal**: on right-handed users, this is the worst corner. Use top-left or add a swipe-down dismiss gesture.
3. **Filter chips crowded into a 5-wide row**: tap targets are <32pt each. Use 3-wide with larger chips or horizontal scroll.
4. **Quantity stepper with tight +/− buttons**: users tap wrong button. Add spacing or use large swipe-to-decrement.
5. **Color swatch grid without padding**: 24×24 visual swatches need 44×44 tap areas behind them with padding.
6. **Sticky "save for later" floating over the "buy" button**: priority confusion and occluded target.

## Gestures vs. taps

Gestures are faster once learned but discoverable only if consistent with platform conventions:

- **Swipe to dismiss**: standard on iOS (left-to-right from edge = back). Use it.
- **Pull to refresh**: standard for list views.
- **Swipe on cart item to reveal actions**: nice, but always include a visible button as well.
- **Long-press**: invisible; don't use for primary actions.

For anything critical, have a visible tap target even if a gesture exists.

## Keyboard considerations

The keyboard covers the bottom third of the screen when active. Design so the active input field is visible above the keyboard, and the primary action (submit) is visible on the keyboard row or immediately above it.

- **Type attributes**: use `type="email"`, `type="tel"`, `type="number"` for correct keyboards.
- **Inputmode**: for finer control (`inputmode="numeric"` without the stepper controls).
- **Autocomplete**: use proper attributes so the browser offers saved values.
- **Next / Done buttons**: let the keyboard's enter key advance to the next field.

## Testing the thumb reach

1. Hold your phone in one hand as you normally would.
2. Without adjusting grip, tap each primary CTA on the page.
3. If you struggle, users will too.
4. For bonus rigor: test with a phone grip your users prefer — larger devices are held lower in the hand.

## Dark patterns to avoid

- **Tiny "no thanks" text under a giant "accept" button.** Equal-weight both.
- **Close button disguised in header chrome.** Make it visible.
- **Misleading CTA color** (e.g., green "subscribe" next to a grey "continue to order") — users tap the green and get a surprise opt-in.

Good mobile UX is visible choice. Hidden traps shorten sessions and lose trust.
