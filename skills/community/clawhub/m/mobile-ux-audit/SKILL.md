---
name: mobile-ux-audit
description: Audit the mobile shopping experience of an ecommerce store for friction points including page load speed, thumb-reach interactions, form length, checkout flow, and pay-method breadth. Use when mobile conversion rate is lagging desktop, before a major redesign, or quarterly as a hygiene pass.
---

# Mobile UX Audit

Mobile is usually 65–80% of ecommerce traffic and ~50% of revenue. The gap between traffic share and revenue share is the audit's job: find the thumb-reach errors, the slow hero images, the checkout fields that kill the sale.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| LCP (Largest Contentful Paint) | ≤2.0s on 4G | 2.0–2.5s | >2.5s |
| INP (Interaction to Next Paint) | ≤150ms | 150–300ms | >300ms |
| CLS (Cumulative Layout Shift) | ≤0.05 | ≤0.1 | >0.1 |
| Tap targets | ≥44×44pt with ≥8pt spacing | 40pt with tight spacing | <40pt, close together |
| Checkout fields | ≤8 fields, one-page | 10–12 fields, 2 pages | 15+ fields, 3+ pages |
| Pay methods | Apple Pay, Google Pay, card, 1 local | Card + PayPal | Card only |
| Guest checkout | Default, no account required | Account optional after checkout | Forced account creation |

## Problems this skill solves

1. **Conversion rate 40% lower on mobile than desktop** with no clear diagnosis.
2. **Cart abandonment spiking at the address-entry step** — usually a mobile-keyboard/autofill problem.
3. **PDP hero image taking 4+ seconds to load** because the team uses the same 3000px-wide asset as desktop.
4. **Checkout buttons in the top third of the screen** requiring an awkward thumb stretch.
5. **Apple Pay / Google Pay not enabled** on a store where 70% of users are on iOS or Android.
6. **Modals and popups that cover the close button** on small screens.
7. **Tap targets smaller than the thumb pad**, producing fat-finger errors on filters and quantity steppers.

## Workflow

### Step 1 — Measure Core Web Vitals in the field

Pull the last 28 days of real-user metrics from PageSpeed Insights (CrUX), Google Search Console, or your RUM tool (Datadog, New Relic, Sentry, or Shopify's built-in). Record p75 LCP, INP, CLS for mobile. Compare to the Quick Reference table. Lab-test tools (Lighthouse) give consistent scores but do not reflect real users — always lead with field data.

### Step 2 — Walk the funnel on a real device

Not an emulator, not Chrome DevTools device mode. Use an actual iPhone and an actual mid-range Android (Pixel 6a or similar — not the latest flagship). Walk: home → category → PDP → add to cart → cart → checkout → payment. Note every friction: slow load, mis-sized tap target, layout shift, confusing state, keyboard-covers-field moment.

### Step 3 — Audit thumb reach

The comfortable thumb zone on a 6-inch phone is the bottom two-thirds of the screen. Anything in the top third (headers, close buttons, primary CTAs) requires a reach or a hand shift. Map every primary CTA on the funnel and flag anything above the middle.

### Step 4 — Audit form fields

List every field in the checkout. Score each: required or optional, keyboard type (email, tel, numeric), autocomplete attribute, inline validation. Target ≤8 required fields total. Common kill-fields: "confirm password," "phone number for delivery updates," "how did you hear about us."

### Step 5 — Audit the payment step

List enabled pay methods. For every market the store serves:

- Apple Pay enabled with domain verification? Required for iOS conversion.
- Google Pay enabled? Required for Android conversion.
- One local method per region (iDEAL in NL, Bancontact in BE, Klarna / Afterpay for installments, SEPA in EU, Pix in BR, UPI in IN).
- Card fields with proper keyboard (numeric, cardtype icons, CVV as numeric).
- 3DS flow is not full-page redirect (use inline 3DS).

### Step 6 — Image and asset audit

- Hero images: served as WebP or AVIF, responsive srcset, ≤200KB at mobile breakpoint.
- Below-fold images: lazy-loaded.
- Fonts: WOFF2, subset to used characters, preloaded for critical text.
- No layout shift from image or ad loads (`width` and `height` attributes or aspect-ratio boxes).
- Video: don't autoplay. If used, poster image first, lazy-load the `<video>` element.

### Step 7 — Document findings with priority

Produce a ranked list: P0 (blocks checkout), P1 (measurably hurts conversion), P2 (polish). Each item gets the friction described, the screen(s) affected, and a concrete fix.

## Example 1 — Shopify store, 62% mobile traffic, 28% mobile conversion rate vs. desktop

Findings from a 2-hour audit:

- **P0**: Apple Pay not enabled despite 58% of mobile users on iOS. Domain unverified in Apple Pay portal. Estimated impact: +8–12% mobile checkout completion.
- **P0**: Checkout has 14 fields including optional company name, phone "for delivery," and a captcha that fails 30% of the time on mobile. Impact: +5–8% checkout completion from field reduction.
- **P1**: Hero image is a 4000px JPEG at 1.2MB. Re-export at 1200px WebP (~120KB). LCP drops from 3.8s to 1.9s.
- **P1**: Add-to-cart button top-right of PDP on mobile, requiring thumb reach. Move to sticky-bottom.
- **P1**: Filter modal on category page covers the close-X behind the OS status bar on iPhone. Add 44pt top padding.
- **P2**: "Suggested for you" section loads below the hero with a 300ms layout shift (CLS 0.18). Reserve space.
- **P2**: Login prompt appears after 15 seconds on every page. Reduce to once-per-session.

Estimated combined lift: 20–30% on mobile conversion over 4–6 weeks after deployment.

## Example 2 — Headless store (Next.js + commerce API), strong desktop, poor mobile INP

The team already optimizes LCP and CLS and has green Core Web Vitals on desktop. Mobile INP is 420ms — users tap and nothing happens for nearly half a second.

- **P0**: Main-thread blocked by an analytics bundle firing synchronously on every route change. Move to a web worker or defer 2 seconds after route settle. Expected INP drop: 420ms → 180ms.
- **P0**: The "add to cart" handler calls three tracking scripts synchronously before showing the cart drawer. Fire tracking async, show drawer immediately. Expected: drawer opens in <100ms instead of 600ms.
- **P1**: Image carousel on PDP uses a heavy library (40KB) that blocks interaction. Swap for CSS-scroll-snap approach, 2KB, same UX.
- **P1**: Variant selector re-renders the entire PDP on each change. Memoize properly or split into a sibling component.
- **P2**: Service worker caches stale HTML for 24h, so bug fixes don't reach users fast. Reduce TTL to 1h and add a "fresh version available" toast.

Strong teams still have mobile-INP debt. The fix is usually "less JavaScript on tap," not "smaller hero image."

## Common mistakes

1. **Auditing only on the latest iPhone.** A mid-range Android at 4G is the real median user.
2. **Using Lighthouse as the only signal.** Lab scores miss cold-start jank and main-thread contention.
3. **Treating mobile as "desktop minus width."** The thumb pattern, keyboard behavior, and attention span are fundamentally different.
4. **Fixing LCP with a CDN and declaring victory.** LCP is three factors: server response, render-blocking resources, and hero-asset size. The CDN only touches one.
5. **Forcing account creation before checkout.** This is a 20%+ conversion hit on cold traffic.
6. **Modals with no visible close button on 4-inch screens.** Test on a small device; buttons crop out.
7. **Infinite-scroll product listing without pagination cues.** Users feel lost and leave.
8. **Autoplay video on mobile.** Eats data, battery, and autoplay policies often block it anyway.
9. **Sticky headers that eat 20% of vertical real estate.** On a phone, every pixel counts.
10. **Not testing with JavaScript disabled.** Many mobile users have flaky JS loading; a site that only works with full JS is broken for them.

## Resources

- `references/output-template.md` — Audit report template with P0/P1/P2 structure.
- `references/core-web-vitals.md` — How to measure and interpret LCP, INP, CLS in the field.
- `references/checkout-checklist.md` — Mobile checkout audit checklist with field-by-field notes.
- `references/thumb-zones.md` — Thumb-reach diagrams and interaction patterns.
- `assets/mobile-audit-checklist.md` — Full pre-publish audit checklist.
