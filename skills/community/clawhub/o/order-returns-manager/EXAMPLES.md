# Order & Returns Manager — Examples

These examples show expected input/output for each workflow.
The agent should match or exceed this quality.

---

## Example 1 — Order lookup, fulfilled

**User:** "check order 1234"

**Agent:**
```
📦 Order #1234 — James Thornton

Status:    Fulfilled ✅
Placed:    08 Apr 2026, 14:32
Payment:   Paid · Stripe

Items:
  · Merino Wool Scarf — Navy (×1)        £34.99
  · Ceramic Plant Pot — Terracotta (×1)  £12.99
  ─────────────────────────────────────────────
  Subtotal                               £47.98
  Shipping — Standard                     £3.99
  Total                                  £51.97

Dispatch:
  Carrier:   Royal Mail Tracked 48
  Tracking:  TT123456785GB
  Sent:      09 Apr 2026
  Check live: https://www.royalmail.com/track-your-item#/tracking-results/TT123456785GB

Customer:
  james.thornton@email.com · +44 7700 900123
  4 orders · £234.50 lifetime · 0 returns

Reply: "return" · "exchange" · "cancel" · "edit" · "note" · "lost parcel"
```

---

## Example 2 — Return, within 14-day window, approved

**User:** "James wants to return order 1234, changed his mind"

**Agent:**
```
↩️ Return request — approval needed

Order:        #1234 — James Thornton
Items:        Merino Wool Scarf — Navy (×1)        £34.99
Reason:       Changed mind
Days:         12 days ✅ within 30-day window
Return ship:  Customer pays (changed mind)
Refund:       £34.99 + £3.99 shipping = £38.98 total
              (within 14-day cancellation right — full refund including shipping)
Restock:      +1 Merino Wool Scarf Navy

Customer:     4 orders · 0 prior returns · low risk
UK law:       ✅ Within 14-day right to cancel — legally must accept

YES · DENY · PARTIAL [amount]
```

**User:** "yes"

**Agent:**
```
✅ Return approved — #1234

Refund:   £38.98 → Stripe (James Thornton)
Restock:  +1 Merino Wool Scarf Navy ✅
Email:    Return instructions sent ✅
```

---

## Example 3 — Return denied, but UK law blocks it

**User:** "deny the return on order 1201, the scarf is faulty but it's been 35 days"

**Agent:**
```
⚠️ Legal alert — this denial is not safe

Order #1201 — 35 days since order date.

The customer reports the item is faulty. Under the Consumer Rights Act 2015:
  · Within 30 days: entitled to full refund for faulty goods
  · Within 6 months: merchant must offer repair or replacement, then refund
    if those fail — regardless of your return window policy

Denying risks: chargeback (£15–25 fee) + potential Trading Standards complaint.
Cost of refund is almost always less than the cost of disputing a chargeback.

Strongly recommended: accept the return.

APPROVE — process return and refund
OVERRIDE — deny anyway (you accept the legal risk)
```

---

## Example 4 — Exchange request

**User:** "customer wants to swap the scarf in order 1234 for forest green"

**Agent:**
```
↔️ Exchange request — #1234

Original:     Merino Wool Scarf — Navy (×1)          £34.99
Exchange for: Merino Wool Scarf — Forest Green (×1)  £34.99
Price diff:   £0.00

I'll process a return on the original and create a replacement order at £0.

DRAFT ORDER approach (recommended) — I handle the full exchange
MANUAL — I process the return, you create the replacement order yourself

Which?
```

**User:** "draft order"

**Agent:**
```
↔️ Exchange processed — #1234

Return:         Merino Wool Scarf — Navy refunded (£34.99 → Stripe)
Replacement:    Merino Wool Scarf — Forest Green → new draft order created
New order:      #1289
Customer:       Exchange confirmation sent ✅

Next: fulfil order #1289 when ready to dispatch the replacement.
```

---

## Example 5 — Fulfilment with tracking

**User:** "fulfil order 1271, royal mail, tracking RM456789123GB"

**Agent:**
```
✅ Order #1271 fulfilled

Carrier:   Royal Mail Tracked 48
Tracking:  RM456789123GB
Items:     Linen Tea Towel Set — Natural (×2)
Customer:  Dispatch notification sent to mike.patel@email.com ✅
```

---

## Example 6 — Cancel unfulfilled order

**User:** "cancel order 1272, anna wants to cancel"

**Agent:**
```
⚠️ Cancel order #1272?

Customer:  Anna Brooks · anna.brooks@email.com
Total:     £34.99
Status:    Unfulfilled ✅ — can be cancelled
Refund:    £34.99 → original payment method
Restock:   +1 Ceramic Plant Pot — White

YES / HOLD (cancel without refund)?
```

**User:** "yes"

**Agent:**
```
✅ Order #1272 cancelled

Refund:   £34.99 → Stripe (Anna Brooks)
Restock:  +1 Ceramic Plant Pot — White ✅
Email:    Cancellation confirmation sent ✅
```

---

## Example 7 — Edit order shipping address

**User:** "change the address on order 1274, Tom gave the wrong postcode — it's BS1 2AB not BS12 AB"

**Agent:**
```
✏️ Address update — #1274

Current:  Tom Wright · 12 New Street · Bristol · BS12 AB
Updated:  Tom Wright · 12 New Street · Bristol · BS1 2AB

Confirm? YES / cancel
```

**User:** "yes"

**Agent:**
```
✅ Address updated — #1274

New postcode: BS1 2AB
Customer notified ✅
```

---

## Example 7b — Request to edit line items (not supported via REST)

**User:** "remove the plant pot from order 1274"

**Agent:**
```
⚠️ Line item edits need Shopify's GraphQL API which this skill doesn't support.

Options:
  1. Cancel order #1274 (Workflow D) and ask Tom to re-order the scarf only
  2. Use the Exchange workflow to swap the pot for something else
  3. Edit directly in Shopify Admin:
     https://{store}.myshopify.com/admin/orders/1274
```

---

## Example 8 — Fraud alert, HIGH risk

**User:** "fraud check on order 1567"

**Agent:**
```
🚨 Fraud alert — Order #1567

Risk:      HIGH — hold before dispatching
Value:     £347.00 (above £150 threshold)
Customer:  New — no order history

Signals:
  🔴 Shipping to freight forwarder postcode (E1W 1AB)
  🔴 Disposable email domain (throwam.com)
  🟡 Billing ≠ shipping address
  🟡 First order, high value
  🟢 Payment authorised by card issuer
  🟢 Phone number provided

Shopify risk: MEDIUM

HOLD · CANCEL · APPROVE
```

**User:** "hold"

**Agent:**
```
🔒 Order #1567 held

Tagged "fraud-review" — will not appear in standard fulfilment queue.
Note added to order: "[10 Apr 2026] Held for fraud review — freight forwarder postcode, disposable email"

Reply "approve 1567" to proceed, or "cancel 1567" to cancel and refund.
```

---

## Example 9 — Lost parcel

**User:** "customer on order 1234 says the parcel hasn't arrived"

**Agent:**
```
📦 Possible lost parcel — #1234

Dispatched:   06 Apr via Royal Mail Tracked 48
Tracking:     TT123456785GB
Last scan:    07 Apr, London MC — no movement (4 days)
Expected:     08 Apr (2 days overdue)
Value:        £34.99 + £3.99 shipping = £38.98

UK law: merchant bears delivery risk — customer entitled to full refund
if not delivered within a reasonable timeframe.

RESHIP  — send replacement (inventory unchanged)
REFUND  — full refund £38.98 → Stripe
WAIT    — message customer to allow 2 more working days

Royal Mail claim link (after 10 working days):
https://www.royalmail.com/help/claims
```

---

## Example 10 — Morning report

**User:** "morning report"

**Agent:**
```
📊 Orders — 10 Apr 2026

Today:      12 orders · £847.50 · £70.63 avg
Fulfilled:   7 ✅  Unfulfilled: 4 ⏳  Cancelled: 1 ❌

Action needed:
  ⚠️ #1267 · Sarah Chen   · £124.00 · 2 days unfulfilled (overdue)
  ⏳ #1271 · Mike Patel   · £67.99  · today
  ⏳ #1272 · Anna Brooks  · £34.99  · today
  ⏳ #1274 · Tom Wright   · £89.00  · today

Returns awaiting decision:  1
Fraud holds:                1 (order #1265)

Reply "fulfil #[order]" to dispatch, or "returns" for the returns queue.
```

---

## Example 11 — Returns report

**User:** "returns report for April"

**Agent:**
```
↩️ Returns — April 2026 (1–10 Apr)

8 returns · £423.50 refunded · 6.2% return rate

By reason:
  Changed mind:       4    £198.00
  Wrong size/colour:  2    £134.50
  Arrived damaged:    1     £67.99
  Not as described:   1     £23.01

Most returned:
  1. Merino Wool Scarf — Navy    3 returns  ⚠️ 18% return rate
  2. Leather Bifold Wallet       2 returns      8% return rate

⚠️ Scarf return rate is high (18%). Top reason: wrong size (×2).
   Suggestion: add measurements to the product listing.

Avg processing: 1.4 days · Restocked: 7/8 · Outstanding: 0
```

---

## Example 12 — Partial refund, goodwill

**User:** "partial refund of £10 on order 1234 — scarf arrived with a small snag"

**Agent:**
```
Partial refund — #1234

Order:   James Thornton · Merino Wool Scarf Navy · £34.99
Reason:  Item arrived with defect (small snag)
Amount:  £10.00

Note: item arrived damaged — UK law supports this claim.
A £10 partial refund is a reasonable goodwill resolution.

Confirm £10.00 partial refund? YES / change amount
```

**User:** "yes"

**Agent:**
```
✅ Partial refund — #1234

£10.00 → Stripe (James Thornton)
Note: "Partial refund — item arrived with snag"
Customer notified ✅
```
