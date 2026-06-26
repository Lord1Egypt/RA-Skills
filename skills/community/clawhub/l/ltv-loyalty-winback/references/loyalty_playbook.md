# LTV & loyalty win-back playbook

For `ltv-loyalty-winback` when you need cutoffs, copy angles, or workflow skeletons.

---

## 1. Silence risk (illustrative)

| Label | Signal (customize) | Interpretation |
|-------|--------------------|----------------|
| Healthy | Order within 60d or expected category cadence | Maintain |
| At-risk | No order 90d; was repeat | Win-back |
| High-risk | No order 120d+ or steep frequency drop | Stronger offer + CS for VIP |
| Churned | No order 180d+ | Re-onboarding or sunset segment |

Cadence varies by category (consumables vs durable).

---

## 2. VIP vs standard (branching)

**VIP / high-value** (example rules — align with merchant):

- Top 10% by 12m spend, or
- LTV above $X, or
- Tier: Gold/Platinum

**VIP care playbook**

- Personal subject line; human sender if possible.
- "We noticed you haven’t shopped in a while" + **specific** past purchase reference.
- Offer: early access, free shipping on next order, small gift with purchase — avoid deep blanket % unless strategic.
- Optional: outbound call or chat for highest LTV.

**Standard bait playbook**

- Percent or fixed off with **hard end date**.
- Free shipping threshold nudge.
- Second email: social proof or bestseller tie-in.

---

## 3. Points pre-expiry sequence

| Send | Timing | Focus |
|------|--------|--------|
| 1 | T-14 | Balance + what it buys |
| 2 | T-7 | Basket suggestion + reminder |
| 3 | T-2 | Last chance; partial redeem if allowed |

Comply with program rules and local marketing law.

---

## 4. Workflow automation (conceptual)

- **Entry**: last_order_at > 90d AND consent = true.
- **Exit**: placed_order OR unsubscribed OR max sends reached.
- **Holdout**: 5–10% no offer to measure lift.

---

## 5. What not to do

- Blast same deep discount to VIPs (margin + brand).
- Ignore consent / frequency caps.
- Confuse one-off order confirmation with win-back (should-not-trigger).
