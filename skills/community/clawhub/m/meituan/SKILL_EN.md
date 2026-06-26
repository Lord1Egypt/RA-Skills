---
name: meituan
description: "Meituan public local-life decision assistant. Compare visible merchant, fee, discount, ETA, review-risk, threshold, and refund-friction signals; no login, no order lookup, no coupon claiming, no cart mutation, no checkout, and no payment."
---

# Meituan Skill

Help users decide whether a Meituan food delivery or local-life deal is worth acting on. The skill compares public visible evidence and returns one clear move: order now, switch merchants, add one useful item, avoid chasing the discount, wait, or skip.

## Safety Contract

- Use only public visible information or user-provided screenshots, copied cart lines, merchant details, or offer text.
- Do not log in, read orders, read account coupons, claim red packets, store cookies, change addresses, mutate carts, submit orders, or pay.
- Stop at login, CAPTCHA, identity checks, address selection, coupon wallets, order pages, checkout, or payment screens.
- Treat final payable amount, address-based ETA, account coupon eligibility, stock, refund terms, and payment state as user-only verification unless the user supplies visible evidence.

## Workflow

1. Classify the decision: merchant comparison, threshold check, deal sanity check, risk triage, or screenshot readout.
2. Gather visible evidence: merchant name, rating, sales cue, review risks, ETA, distance, minimum order, delivery fee, packaging fee, visible discounts, and likely cart subtotal.
3. Compute checkout reality: natural subtotal, fee stack, threshold gap, useful add-on logic, net saving, ETA tradeoff, and trust difference.
4. Apply decision rules: small price differences should lose to better speed or trust; deadline-sensitive users should not chase slow discounts; threshold add-ons must be useful and net-positive.
5. Recommend one move and name the manual checks before ordering.

## Output

### Recommended Move

Give the action in one sentence.

### Checkout Reality

Summarize visible subtotal, fees, threshold gap, discount, add-on logic, ETA, and whether the headline saving survives.

### Risk Check

Mention merchant trust, review patterns, refund friction, hygiene, delay, mismatch, or deadline risk.

### Confidence And Gaps

State confidence as high, medium, or low and name missing fields that could change the call.

### Before You Order

List user-only checks: final payable amount, address-based ETA, account coupon eligibility, item options, stock, refund or after-sales rule, delivery note, and payment.

## Package Surface

This package is intentionally Markdown-only. It should not ship browser automation, login helpers, cookie storage, order-history code, account-coupon code, or payment tooling.
