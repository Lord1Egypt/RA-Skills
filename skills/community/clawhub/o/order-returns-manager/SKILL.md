# Order & Returns Manager

## Overview
Manage Shopify and WooCommerce orders end-to-end via WhatsApp, Telegram, or any
OpenClaw channel. Check order status with live tracking, process returns and exchanges,
approve refunds, restock inventory, edit orders before dispatch, flag fraud, handle
lost parcels, and generate fulfilment reports — all from a single message.

UK-focused: Consumer Rights Act 2015 compliance enforced throughout. Royal Mail, DPD,
Evri, DHL, and Parcelforce carrier claim links included.

---

## Trigger Phrases
Activate this skill when the user says any of the following (or similar):

Order lookups:
- "check order [number/name/email]"
- "where is order [X]" / "has order [X] shipped"
- "find orders for [customer name/email]"
- "show today's orders" / "morning report"
- "show unfulfilled orders"
- "orders from the last [X] days"

Returns, refunds & exchanges:
- "process a return" / "customer wants to return [order]"
- "approve / deny return for [order]"
- "issue refund for [order]" / "partial refund on [order]"
- "customer wants to exchange [order]"
- "restock items from [order]"

Fulfilment & editing:
- "mark [order] as fulfilled" / "add tracking to [order]"
- "cancel [order]"
- "edit order [X]" / "change address on [order]" / "remove item from [order]"
- "add note to order [X]"

Reports & fraud:
- "returns report" / "show returns this week/month"
- "unfulfilled orders report"
- "flag suspicious orders" / "fraud check on [order]"

---

## Configuration (ask on first use if not set)
Check memory for the following before running any workflow.
If missing, ask the user once and store under `orders_config`:

```
STORE_PLATFORM              # shopify | woocommerce
SHOPIFY_STORE_HANDLE        # e.g. my-store (Shopify only)
SHOPIFY_ACCESS_TOKEN        # starts with shpat_ (Shopify only)
WC_DOMAIN                   # e.g. mystore.co.uk (WooCommerce only)
WC_CONSUMER_KEY             # ck_xxx (WooCommerce only)
WC_CONSUMER_SECRET          # cs_xxx (WooCommerce only)
SHOPIFY_API_VERSION         # Default: 2025-01
SHOPIFY_LOCATION_ID         # Fetched automatically on first inventory op
CURRENCY                    # Default: GBP
RETURN_WINDOW_DAYS          # Default: 30
AUTO_RESTOCK_ON_RETURN      # Default: true
REFUND_APPROVAL_REQUIRED    # Default: true
HIGH_VALUE_APPROVAL_FLOOR   # Default: £100 (always confirm refunds above this)
FRAUD_ALERT_THRESHOLD       # Default: £150
NOTIFY_CUSTOMER_ON_RETURN   # Default: true
RETURN_ADDRESS              # Store's full return postal address
PREFERRED_CARRIER           # Default carrier for fulfilment notes
```

Never log or repeat access tokens back to the user.

### Fetch location ID automatically (Shopify)
On first inventory operation:
```
GET https://{store}.myshopify.com/admin/api/{version}/locations.json
```
If multiple active locations exist, list them and ask which to use as default.
Store the chosen ID as `SHOPIFY_LOCATION_ID`.

---

## Workflow A — Order Lookup

### Step 1 — Identify the order
Accept: order number (#1234 or 1234), customer email, or customer name.

By order number:
```
GET https://{store}.myshopify.com/admin/api/{version}/orders.json?name=%23{number}&status=any
```

By customer email:
```
GET .../customers/search.json?query=email:{email}&limit=5
→ GET .../customers/{id}/orders.json?status=any&limit=10
```

By customer name:
```
GET .../customers/search.json?query={name}&limit=5
```

Multiple matches → show compact list, ask user to confirm:
```
Found 2 orders for "James":
  #1234 · James Thornton · £67.98 · 08 Apr ✅ Fulfilled
  #1198 · James Okafor   · £34.99 · 02 Apr ✅ Fulfilled
Which one?
```

### Step 2 — Display order summary
```
📦 Order #1234 — James Thornton

Status:    Fulfilled ✅
Placed:    08 Apr 2026, 14:32
Payment:   Paid via Stripe

Items:
  · Merino Wool Scarf — Navy (×1)        £34.99
  · Ceramic Plant Pot — Terracotta (×1)  £12.99
  ──────────────────────────────────────────────
  Subtotal                               £47.98
  Shipping — Standard                     £3.99
  Total                                  £51.97

Dispatch:
  Carrier:     Royal Mail Tracked 48
  Tracking:    TT123456785GB
  Sent:        09 Apr 2026
  Live status: [fetched from carrier — see Step 3]

Customer:
  Email:    james.thornton@email.com
  Phone:    +44 7700 900123
  History:  4 orders · £234.50 lifetime · 0 prior returns

Reply: "return" · "exchange" · "refund" · "cancel" · "edit" · "add tracking" · "note" · "lost parcel"
```

### Step 3 — Live tracking lookup
Attempt `web_fetch` on the carrier tracking URL. Use the carrier name stored in
`order.fulfillments[0].tracking_company` to select the correct URL:

| Carrier | Tracking URL | web_fetch reliable? |
|---------|-------------|-------------------|
| Royal Mail | https://www.royalmail.com/track-your-item#/tracking-results/{tracking_number} | ⚠️ No — hash fragment is client-side JS |
| DPD | https://www.dpd.co.uk/apps/tracking/redirect?reference={tracking_number} | ⚠️ Unreliable |
| Evri | https://www.evri.com/track-a-parcel/results/{tracking_number} | ⚠️ Unreliable |
| DHL | https://www.dhl.com/gb-en/home/tracking/tracking-express.html?submit=1&tracking-id={tracking_number} | ⚠️ Unreliable |
| Parcelforce | https://www.parcelforce.com/track-trace?trackNumber={tracking_number} | ⚠️ Unreliable |

**Important:** All major UK carrier tracking pages load status via client-side JavaScript
after the initial page load. `web_fetch` retrieves the HTML shell only, not the rendered
tracking status. Do not claim to show "live status" — instead:

1. Attempt `web_fetch` and check if any status text is parseable in the raw HTML
2. If parseable: show the status clearly labelled as "last fetched status"
3. If not parseable (most cases): show the tracking number and a direct link so the
   merchant can check in one tap:
   ```
   Tracking: TT123456785GB (Royal Mail Tracked 48)
   Check live: https://www.royalmail.com/track-your-item#/tracking-results/TT123456785GB
   ```

Never silently skip tracking or claim "In transit ✅" without actual data to support it.

---

## Workflow B — Return Request

Follow every step precisely. UK law is enforced throughout.

### Step 1 — Find the order (Workflow A, Step 1)

### Step 2 — Eligibility check

Calculate days since **delivery** (not order date) for the 14-day cancellation right:
```
dispatch_date  = order.fulfillments[0].created_at  (date dispatched)
days_since_order    = today - order.created_at
days_since_dispatch = today - dispatch_date
```

The 14-day cancellation right runs from the delivery date. Since the exact delivery date
is rarely recorded, use `days_since_dispatch` as the conservative estimate (errs toward
customer's favour, which is legally safer for the merchant). If the merchant knows the
actual delivery date, use that instead.

Check all of the following:
- `days_since_order` vs `RETURN_WINDOW_DAYS` (flag if outside, but UK law overrides — see below)
- Is the order `fulfillment_status: fulfilled`? If null/unfulfilled → route to cancel (Workflow D)
- Has a return already been processed? Check `order.refunds[]` — if non-empty, warn and ask if this is an additional partial return
- Are any line items non-returnable?
  - Digital products (`requires_shipping: false`) → not returnable under distance selling regs
  - Personalised / custom items → not returnable (flag and ask owner to confirm)
  - Opened hygiene products, perishables → not returnable
  - Note these exceptions in the approval summary

UK statutory minimums (always apply, regardless of store policy):
- Within 14 days of **delivery**: customer can cancel for any reason (Consumer Contracts Regs 2013)
  → Full refund including standard delivery cost must be given
- Within 30 days of **delivery**: faulty or not-as-described goods → full refund
- Within 6 months of **delivery**: if fault is proven to have existed at sale → repair/replace/refund

### Step 3 — Return reason
Parse from user message if present. If not, ask in one message:

```
Reason for return?
  1 · Changed mind
  2 · Wrong size or colour ordered
  3 · Item arrived damaged
  4 · Item not as described
  5 · Faulty / stopped working
  6 · Item not received → I'll open a lost parcel claim (Workflow F) instead
```

Return shipping cost responsibility (UK law):
- Reasons 1–2 → customer pays return shipping
- Reasons 3–5 → merchant pays (provide prepaid label or reimburse cost)
- Reason 6 → exit to Workflow F — this is not a return

### Step 4 — Owner approval (if REFUND_APPROVAL_REQUIRED = true)

Always require approval if refund amount > HIGH_VALUE_APPROVAL_FLOOR, regardless of config.

```
↩️ Return request — approval needed

Order:        #1234 — James Thornton
Items:        Merino Wool Scarf — Navy (×1)        £34.99
Reason:       Changed mind
Days:         12 days ✅ within {RETURN_WINDOW_DAYS}-day window
Return ship:  Customer pays (changed mind)
Refund:       £34.99 item only — original shipping (£3.99) not refunded
              [If within 14-day cancellation window: full refund incl. shipping]
Restock:      +1 Merino Wool Scarf Navy

Customer:     4 orders · 0 prior returns ✅ · low risk
UK law:       ✅ Within 14-day right to cancel — legally must accept

YES · DENY · PARTIAL [amount]
```

Auto-approve (skip this step) only if REFUND_APPROVAL_REQUIRED = false AND
refund amount ≤ HIGH_VALUE_APPROVAL_FLOOR.

### Step 5a — Approve: create return and refund

**Step 1 of 3 — Create the return record (Shopify Returns API):**
```
POST https://{store}.myshopify.com/admin/api/{version}/orders/{order_id}/returns.json
Content-Type: application/json
X-Shopify-Access-Token: {token}

{
  "return": {
    "refund_line_items": [
      {
        "line_item_id": {line_item_id},
        "quantity": {qty},
        "restock_type": "return",
        "location_id": {SHOPIFY_LOCATION_ID}
      }
    ],
    "note": "{return_reason}"
  }
}
```

This creates the return record and handles restocking for the returned line items.
Save the returned `return.id` for reference.

**Step 2 of 3 — Issue the refund (separate API call):**
```
POST https://{store}.myshopify.com/admin/api/{version}/orders/{order_id}/refunds.json

{
  "refund": {
    "notify": true,
    "note": "Return approved — {reason}",
    "refund_line_items": [
      {
        "line_item_id": {line_item_id},
        "quantity": {qty},
        "restock_type": "no_restock"
      }
    ],
    "shipping": {
      "full_refund": {true_if_within_14_day_cancellation_window}
    },
    "transactions": [
      {
        "parent_id": {order.transactions[0].id},
        "amount": "{refund_amount}",
        "kind": "refund",
        "gateway": "{order.transactions[0].gateway}"
      }
    ]
  }
}
```

Important: set `restock_type: "no_restock"` in the refund body — restocking was
already handled in the returns API call above. Double-restocking will inflate inventory.

**Step 3 of 3 — Send return instructions to customer:**
(Only if NOTIFY_CUSTOMER_ON_RETURN = true)

Compose and send via Shopify email or the configured email tool:

```
Subject: Return approved — Order #{order_name}

Hi {first_name},

Your return request for order #{order_name} has been approved.

Items to return:
{list each item with qty — e.g. "· Merino Wool Scarf — Navy (×1)"}

Please send your return to:
{RETURN_ADDRESS}

{IF reason is 3, 4, or 5 — merchant pays shipping}
We've arranged a prepaid Royal Mail return label. Please see the
attachment, or visit your local Post Office and quote the reference below:
[label reference or attach label]
{ELSE}
Please use a tracked postal service and keep your proof of postage.
We recommend Royal Mail Tracked 48 (available at any Post Office).
{ENDIF}

Once we receive your return, we'll process your refund of £{refund_amount}
to your original payment method within 3–5 business days.

Any questions? Just reply to this email.

{store_name}
```

**Confirm to owner:**
```
✅ Return approved — #1234

Refund:   £34.99 issued → Stripe (James Thornton)
Restock:  +1 Merino Wool Scarf Navy at {location_name} ✅
Email:    Return instructions sent to james.thornton@email.com ✅
Note:     Added to order internally
```

### Step 5b — Deny return

Before composing denial, run UK law check:

| Condition | Block denial? |
|-----------|--------------|
| Within 14 days of delivery (any reason) | ✅ Block — statutory cancellation right |
| Within 30 days, item faulty or not as described | ✅ Block — Consumer Rights Act |
| Within 6 months, fault provable at time of sale | ✅ Block — must offer repair/replace first |
| Beyond return window, item not faulty, item as described | Allow denial |

If block applies:
```
⚠️ Legal alert — this denial is not safe

Reason: {specific law that applies}
Risk: chargeback (£15–25 fee) and/or Trading Standards complaint

Strongly recommended: accept the return.

APPROVE — accept and process return
OVERRIDE — deny anyway (not recommended, you accept legal risk)
```

If denial is legally safe:
Fetch existing note first, then append (same null guard as Workflow G):
```
GET .../orders/{order_id}.json?fields=id,note
PUT .../orders/{order_id}.json
{
  "order": {
    "note": "{existing_note is null ? '' : existing_note + '\n'}[{DD MMM YYYY}] Return denied — {reason}"
  }
}
```

Send denial email:
```
Subject: Your return request — Order #{order_name}

Hi {first_name},

Thank you for contacting us about order #{order_name}.

Unfortunately we're unable to process this return:
{denial_reason}

{IF outside_window}
Our return window is {RETURN_WINDOW_DAYS} days from the order date.
This order was placed on {order_date}, which is outside this period.
{ENDIF}

If you think this is an error, or if there's anything else we can help
with, please reply to this email.

{store_name}
```

### Step 5c — Partial refund (goodwill or damaged item)

Ask for the amount if not in the user's message.
Partial refunds do not create a return record and do not restock inventory.

```
POST .../orders/{order_id}/refunds.json
{
  "refund": {
    "notify": true,
    "note": "Partial refund — {reason}",
    "transactions": [
      {
        "parent_id": {order.transactions[0].id},
        "amount": "{partial_amount}",
        "kind": "refund",
        "gateway": "{order.transactions[0].gateway}"
      }
    ]
  }
}
```

Confirm:
```
✅ Partial refund — #1234

Amount:  £{partial_amount} → {gateway} ({customer_name})
Reason:  {reason}
Note:    Added to order
Customer notified: ✅
```

---

## Workflow C — Exchange (Return + Replacement)

Triggered by: "customer wants to exchange", "swap size on [order]", "different colour"

Exchanges are a two-part process: issue a return/refund for the original item,
then create a new order or manually adjust the replacement.

### Step 1 — Find original order (Workflow A)

### Step 2 — Confirm exchange details
```
↔️ Exchange request — #1234

Original:    Merino Wool Scarf — Navy (×1)        £34.99
Exchange for: [ask user] — e.g. "same scarf in Forest Green"

Options:
  DRAFT ORDER — create a new draft order for the replacement (recommended)
  MANUAL — I'll just process the return and you'll create the new order yourself

Which approach?
```

### Step 3a — Draft order approach (recommended)
Create a draft order for the replacement item at £0 (or at cost if different price):
```
POST .../draft_orders.json
{
  "draft_order": {
    "line_items": [
      {
        "variant_id": {replacement_variant_id},
        "quantity": {qty},
        "price": "0.00",
        "title": "{product title} — exchange for order #{original_order_name}"
      }
    ],
    "customer": { "id": {customer_id} },
    "shipping_address": {original_order.shipping_address},
    "shipping_line": {
      "custom": true,
      "title": "{PREFERRED_CARRIER} — exchange shipping",
      "price": "0.00"
    },
    "note": "Exchange — original order #{original_order_name}",
    "send_invoice": false
  }
}
```

Complete the draft order to create the replacement order:
```
PUT .../draft_orders/{draft_id}/complete.json
```

Then process the return/refund for the original item (Workflow B, Step 5a).

Confirm:
```
↔️ Exchange processed — #1234

Return:       Merino Wool Scarf — Navy refunded (£34.99)
Replacement:  Merino Wool Scarf — Forest Green dispatched
New order:    #{new_order_name}
Customer:     Exchange confirmation sent ✅
```

### Step 3b — Manual approach
Just process the return (Workflow B) and note to owner:
```
↩️ Return processed — #1234

Refund: £34.99 → {customer_name}
Next step: create a new order manually for the replacement item.
Draft orders → New order in your Shopify admin.
```

---

## Workflow D — Cancel an Order

Triggered by: "cancel order [X]", "customer wants to cancel"

### Step 1 — Check cancellability
```
GET .../orders/{order_id}.json?fields=id,name,status,fulfillment_status,financial_status,total_price,line_items,transactions,customer,email
```
- `fulfillment_status: fulfilled` → cannot cancel via API → route to Workflow B (return)
- `status: cancelled` → already cancelled → inform user (note: use `status`, not `financial_status`, to check cancellation)
- `fulfillment_status: null` (unfulfilled) → proceed

### Step 2 — Confirm
```
⚠️ Cancel order #1234?

Customer:  James Thornton · james.thornton@email.com
Total:     £51.97
Status:    Unfulfilled ✅ — can be cancelled
Refund:    £51.97 → original payment method (Stripe)
Restock:   +2 items → inventory

Reply YES to cancel and refund in full.
Reply HOLD to cancel without refund (non-standard — confirm reason first).
```

### Step 3 — Cancel (two API calls)

**Call 1 — Cancel the order:**
```
POST .../orders/{order_id}/cancel.json
{
  "reason": "customer",
  "email": true
}
```

Note: the cancel endpoint does NOT process refunds. It only sets order status to cancelled.

**Call 2 — Issue the refund separately:**
```
POST .../orders/{order_id}/refunds.json
{
  "refund": {
    "notify": true,
    "note": "Order cancelled at customer request",
    "refund_line_items": [
      {
        "line_item_id": {id},
        "quantity": {qty},
        "restock_type": "cancel"
      }
    ],
    "shipping": { "full_refund": true },
    "transactions": [
      {
        "parent_id": {order.transactions[0].id},
        "amount": "{order.total_price}",
        "kind": "refund",
        "gateway": "{order.transactions[0].gateway}"
      }
    ]
  }
}
```

Confirm:
```
✅ Order #1234 cancelled

Refund:   £51.97 → Stripe (James Thornton)
Restock:  2 items returned to inventory ✅
Email:    Cancellation confirmation sent ✅
```

---

## Workflow E — Fulfil an Order

Triggered by: "mark [order] as fulfilled", "add tracking to [order]", "dispatch [order]"

### Step 1 — Get fulfillment order ID
```
GET .../orders/{order_id}/fulfillment_orders.json
```
Use the `fulfillment_order.id` (not the order ID) in the fulfilment creation call.
Only fulfil line items where `fulfillment_order.status` is `open`.

### Step 2 — Ask for tracking (single message)
- Carrier: Royal Mail / DPD / Evri / DHL / Parcelforce / Other (specify)
- Tracking number

### Step 3 — Create fulfilment
```
POST .../fulfillments.json
{
  "fulfillment": {
    "line_items_by_fulfillment_order": [
      {
        "fulfillment_order_id": {fulfillment_order_id},
        "fulfillment_order_line_items": [
          { "id": {fulfillment_order_line_item_id}, "quantity": {qty} }
        ]
      }
    ],
    "tracking_info": {
      "number": "{tracking_number}",
      "company": "{carrier_name}",
      "url": "{carrier_tracking_url_with_number}"
    },
    "notify_customer": true
  }
}
```

Note: use the top-level `/fulfillments.json` endpoint, not the order-scoped one.
The order-scoped `/orders/{id}/fulfillments.json` is deprecated as of API version 2022-07.

Confirm:
```
✅ Order #1234 fulfilled

Carrier:   Royal Mail Tracked 48
Tracking:  TT123456785GB
Items:     Merino Wool Scarf — Navy (×1), Ceramic Plant Pot — Terracotta (×1)
Customer:  Dispatch notification sent ✅
```

---

## Workflow F — Edit an Order

Triggered by: "edit order [X]", "change address on [order]", "remove item from [order]",
"add item to [order]"

Order editing is only available on unfulfilled orders.

### Important: two different edit paths

**Shipping address changes** → use REST API (simple, always works)
**Line item changes (add/remove items)** → Shopify Order Editing API is GraphQL-only.
The REST API has no endpoint for editing line items on existing orders.
If the user needs line item edits, advise them to use Shopify Admin directly,
or use the exchange workflow (Workflow C) to cancel + recreate.

### Change shipping address (REST)
```
PUT https://{store}.myshopify.com/admin/api/{version}/orders/{order_id}.json
{
  "order": {
    "shipping_address": {
      "first_name": "{first_name}",
      "last_name": "{last_name}",
      "address1": "{address1}",
      "address2": "{address2_or_empty_string}",
      "city": "{city}",
      "province": "{county_or_empty_string}",
      "zip": "{postcode}",
      "country": "United Kingdom",
      "country_code": "GB",
      "phone": "{phone_or_empty_string}"
    }
  }
}
```

Always confirm before updating:
```
✏️ Address update — #1234

Current:  James Thornton · 12 Old Street · London · E1 1AA
Updated:  James Thornton · 12 New Street · Bristol · BS1 2AB

Confirm? YES / cancel
```

### Line item edits (add/remove products)
Shopify's line item editing requires the GraphQL Admin API (`orderEditBegin`,
`orderEditAddLineItem`, `orderEditRemoveLineItem`, `orderEditCommit` mutations).
This is beyond the scope of this skill's REST-based implementation.

When the user asks to add or remove items from an existing order, respond:
```
⚠️ Line item edits require Shopify's GraphQL API which this skill doesn't
currently support via REST.

Options:
  1. Cancel this order (Workflow D) and ask the customer to re-order
  2. Use the Exchange workflow (Workflow C) to handle a product swap
  3. Edit line items directly in Shopify Admin:
     https://{store}.myshopify.com/admin/orders/{order_id}
```

---

## Workflow G — Add Note to Order

Triggered by: "add note to order [X]", "note on [order]"

Always fetch the existing note first to avoid overwriting:
```
GET .../orders/{order_id}.json?fields=id,note
```

Then append with a null guard:
```
PUT .../orders/{order_id}.json
{
  "order": {
    "note": "{existing_note is null ? '' : existing_note + '\n'}[{DD MMM YYYY}] {new_note}"
  }
}
```

If `order.note` is null or empty string, the new note becomes the full value with no leading newline.
If `order.note` has content, append with a newline separator.

Confirm:
```
📝 Note added — #1234
"[10 Apr 2026] {note_text}"
```

---

## Workflow H — Fraud Detection

Run automatically on new orders above FRAUD_ALERT_THRESHOLD, or on demand.

### Step 1 — Fetch order with risk assessment
Explicitly request the `risks` field — it is not included in default order responses:
```
GET .../orders/{order_id}.json?fields=id,name,email,total_price,financial_status,fulfillment_status,billing_address,shipping_address,customer,tags,note,browser_ip,risks,transactions,line_items,fulfillments
```
Fields to check: `order.risks[]`, `order.financial_status`, `order.browser_ip`,
`order.billing_address`, `order.shipping_address`, `order.email`,
`order.customer.orders_count`, `order.tags`.

### Step 2 — Score signals

| Signal | Risk |
|--------|------|
| Shipping to freight forwarder postcode | 🔴 High |
| Disposable/temporary email domain | 🔴 High |
| Multiple orders same day, different payment methods, same shipping address | 🔴 High |
| Shopify risk level = HIGH | 🔴 High |
| Billing address ≠ shipping address | 🟡 Medium |
| First order, value above threshold | 🟡 Medium |
| Express shipping on high-value order | 🟡 Medium |
| Shopify risk level = MEDIUM | 🟡 Medium |
| Phone number missing | 🟢 Low |
| Order placed 01:00–05:00 UK time | 🟢 Low |

UK freight forwarder postcodes (common): E1W, IG11, UB3, SL3, EN3, RM9, UB8.
Disposable email domains: mailinator.com, guerrillamail.com, tempmail.com,
throwam.com, yopmail.com, sharklasers.com (extend list in memory as you encounter more).

Overall risk score:
- Any 🔴 signal = HIGH
- 2+ 🟡 signals and no 🔴 = MEDIUM
- Only 🟢 signals = LOW

### Step 3 — Action by risk level

HIGH:
```
🚨 Fraud alert — Order #{order_name}

Risk:      HIGH — recommend holding before dispatch
Value:     £{total} (above £{threshold} threshold)
Customer:  {new/returning} — {order_count} previous orders

Signals:
  🔴 {signal}
  🟡 {signal}
  🟢 {signal}

Shopify risk: {LOW/MEDIUM/HIGH}

HOLD · CANCEL · APPROVE
```

MEDIUM → notify owner but don't block:
```
⚠️ Order #{order_name} — moderate risk signals

{signals list}

REVIEW before fulfilling? YES / APPROVE to proceed
```

LOW → no action, process normally.

### Step 4 — HOLD action
First fetch existing tags to avoid overwriting them:
```
GET .../orders/{order_id}.json?fields=id,tags,note
```
Then append the fraud-review tag and note:
```
PUT .../orders/{order_id}.json
{
  "order": {
    "tags": "{existing_tags}, fraud-review",
    "note": "{existing_note}\n[{date}] Held for fraud review — {signals summary}"
  }
}
```
If `existing_tags` is empty, use `"tags": "fraud-review"` only (no leading comma).
If `existing_note` is null, use `"note": "[{date}] Held for fraud review — {signals summary}"` only.

Confirm: `🔒 Order #{name} held — tagged "fraud-review". Will not appear in standard fulfilment queue.`

---

## Workflow I — Lost Parcel Claim

Triggered by: "order not received", "customer hasn't received [order]", "missing parcel"

This is NOT a return. No item is coming back. Handle separately.

### Step 1 — Verify tracking status (Workflow A, Step 3)

### Step 2 — Assess situation

| Tracking status | Assessment | Action |
|----------------|-----------|--------|
| Shows delivered | Possible misdelivery | Ask customer to check neighbours, safe place, building reception |
| In transit, within expected window | Early | Ask customer to wait — share tracking URL |
| In transit, 3–5 days overdue | Delayed | Raise with carrier, give 2 more days before escalating |
| No movement for 7+ days | Likely lost | Present resolution options |
| No tracking at all | Untracked order | Resolution options immediately |

### Step 3 — Resolution options
```
📦 Possible lost parcel — Order #1234

Dispatched:   06 Apr via Royal Mail Tracked 48
Tracking:     TT123456785GB
Last scan:    07 Apr, London MC — no movement (4 days)
Expected:     08 Apr (2 days overdue)
Value:        £34.99

UK law: merchant bears risk of non-delivery — customer entitled to full refund
if goods not delivered in agreed or reasonable timeframe.

RESHIP  — send replacement now (no inventory adjustment needed)
REFUND  — full refund incl. original shipping (total: £38.98)
WAIT    — message customer, allow 2 more working days before escalating

Carrier claim links (for your records):
  Royal Mail: https://www.royalmail.com/help/claims (claim after 10 working days)
  DPD:        https://www.dpd.co.uk/content/products_services/claims.jsp
  Evri:       https://www.evri.com/help/claim-for-a-parcel
  DHL:        https://www.dhl.com/gb-en/home/our-divisions/parcel/customer-service/submit-a-claim.html
  Parcelforce: https://www.parcelforce.com/help-and-advice/sending/compensation-claims
```

---

## Workflow J — Daily Orders Report

Triggered by: "morning report", "show today's orders", "orders summary", or heartbeat.

```
GET .../orders.json?status=any&created_at_min={today_start_iso8601}&limit=250
```

Also fetch orders older than 1 day that are still unfulfilled:
```
GET .../orders.json?fulfillment_status=unfulfilled&created_at_max={yesterday_start_iso8601}&limit=50
```

```
📊 Orders — 10 Apr 2026

Today:          12 orders · £847.50 revenue · £70.63 avg
Fulfilled:       7 ✅ · Unfulfilled: 4 ⏳ · Cancelled: 1 ❌

Action needed:
  ⚠️ #1267 · Sarah Chen   · £124.00 · 2 days unfulfilled
  ⏳ #1271 · Mike Patel   · £67.99  · placed today
  ⏳ #1272 · Anna Brooks  · £34.99  · placed today
  ⏳ #1274 · Tom Wright   · £89.00  · placed today

Returns awaiting your decision:  1
Fraud holds:                      1 (order #1265 — tagged fraud-review)
High-value orders (>£{FRAUD_ALERT_THRESHOLD}): 2

Reply "fulfil #[order]" to dispatch, or "returns" for the returns queue.
```

---

## Workflow K — Returns Report

Triggered by: "returns report", "show returns this week/month"

Fetch refunded orders AND filter out cancellations:
```
GET .../orders.json?financial_status=refunded&updated_at_min={period_start_iso8601}&limit=250
```

Filter: exclude orders where `order.cancel_reason` is non-null (those are cancellations, not returns).

**Important — return reason data:** Shopify's API does not store return reasons as a structured field.
Reasons only exist if they were recorded in order notes or the `common_return_reasons` memory map
(updated each time Workflow B runs). Pull reason breakdown from `common_return_reasons` memory.
If no memory data exists yet, omit the "by reason" breakdown and note: "Reason tracking begins
after your first processed return via this skill."

```
↩️ Returns — April 2026 (1–10 Apr)

Total returns:    8 · £423.50 refunded
Return rate:      6.2% of 129 orders

By reason:
  Changed mind:       4    £198.00   50%
  Wrong size/colour:  2    £134.50   25%
  Arrived damaged:    1     £67.99   13%
  Not as described:   1     £23.01   13%

Most returned products:
  1. Merino Wool Scarf — Navy         3 returns  ⚠️  18% return rate
  2. Leather Bifold Wallet — Brown    2 returns       8% return rate

⚠️ Merino Wool Scarf — Navy has an 18% return rate.
   Top reason: "wrong size" (×2). Consider adding a size guide or more
   detailed measurements to the product listing.

Processing speed:   avg 1.4 days from request to refund
Restocked:          7 of 8 items
Outstanding refunds: 0
```

---

## UK Consumer Law Reference

Enforce throughout. Never advise actions that violate these:

| Situation | Customer right | Time limit | Merchant obligation |
|-----------|---------------|------------|-------------------|
| Cancel any distance sale | Full refund incl. standard shipping | Within 14 days of delivery | Refund within 14 days of receiving goods back |
| Faulty or not as described | Full refund | Within 30 days of delivery | Cannot refuse, cannot charge restocking fee |
| Fault at time of sale | Repair or replacement; if fails, refund | Within 6 months | One repair/replacement attempt then must refund |
| Item not delivered | Full refund | Reasonable timeframe (usually 30 days) | Merchant bears delivery risk |
| Goods not matching description | Full refund | No time limit | No restocking fee |

Sources: Consumer Rights Act 2015, Consumer Contracts (Information, Cancellation and
Additional Charges) Regulations 2013.

Key practical notes:
- Merchants cannot charge a restocking fee on any return within statutory rights
- The 14-day cancellation right applies from the date of delivery, not the order date
- "Not as described" applies if listing photos or text materially misled the buyer
- Chargeback cost (£15–25 + potential account risk) nearly always exceeds refund cost

---

## Error Handling

| HTTP Error | Common cause | Action |
|-----------|-------------|--------|
| 401 Unauthorized | Invalid/expired token | Ask user to regenerate in Shopify Admin → Apps |
| 403 Forbidden | Missing API scope | Name the exact missing scope from the required list |
| 422 — already refunded | Duplicate refund attempt | Fetch and display existing refund details |
| 422 — amount exceeds order total | Refund amount too large | Ask user for the correct amount |
| 422 — order not editable | Order is fulfilled or cancelled | Inform user, suggest alternative action |
| 404 Order not found | Wrong order number | Suggest searching by customer email instead |
| 429 Too Many Requests | Rate limit hit | Auto-retry after 2 seconds, up to 3 attempts |
| 503 Service Unavailable | Shopify outage | Wait 30 seconds, retry once, then report |

Required Shopify API scopes for this skill:
- `read_orders` and `write_orders`
- `read_fulfillments` and `write_fulfillments`
- `read_customers`
- `read_inventory` and `write_inventory`
- `read_draft_orders` and `write_draft_orders` (for exchange workflow)

---

## WooCommerce Support

When STORE_PLATFORM = woocommerce:

Base URL: `https://{WC_DOMAIN}/wp-json/wc/v3`
Auth header: `Authorization: Basic {base64(WC_CONSUMER_KEY:WC_CONSUMER_SECRET)}`

### Key endpoints and request bodies

**Get order:**
```
GET /orders/{id}
```

**List orders:**
```
GET /orders?status={status}&per_page=50&page=1
```

**Update order status:**
```
PUT /orders/{id}
{ "status": "completed" }
```

**Create refund:**
```
POST /orders/{id}/refunds
{
  "amount": "{refund_amount}",
  "reason": "{reason}",
  "line_items": [
    {
      "id": {order_line_item_id},
      "quantity": {qty},
      "refund_total": "{line_item_refund_amount}",
      "restock_items": true
    }
  ],
  "api_refund": true
}
```

**Update product stock:**
```
PUT /products/{product_id}
{ "stock_quantity": {new_qty} }
```

For variable products (with variants):
```
PUT /products/{product_id}/variations/{variation_id}
{ "stock_quantity": {new_qty} }
```

**WooCommerce status map:**

| WooCommerce status | Display |
|-------------------|---------|
| pending | Unpaid ⏸️ |
| processing | Unfulfilled ⏳ |
| on-hold | On hold ⏸️ |
| completed | Fulfilled ✅ |
| cancelled | Cancelled ❌ |
| refunded | Refunded ↩️ |
| failed | Payment failed ❌ |

---

## Memory Instructions

After each interaction, update memory with:

- `preferred_approval_words`: the words this owner uses to approve (e.g. "yes", "go", "do it", "approved") — learn from pattern so the skill recognises their shorthand
- `preferred_denial_words`: same for denials
- `RETURN_ADDRESS`: store once, use in every return email without asking again
- `SHOPIFY_LOCATION_ID`: store once, avoid re-fetching every session
- `PREFERRED_CARRIER`: the carrier this merchant most often uses — pre-fill in fulfilment prompts
- `FRAUD_THRESHOLD_ADJUSTED`: if owner ever says "change my fraud threshold to £X", update and store
- `common_return_reasons`: running tally of return reasons for monthly reports — store as `{reason: count}` map
- `freight_forwarder_postcodes_seen`: any new freight forwarder postcodes the owner flags — append to detection list

---

## Tone & Communication

- ✅ fulfilled · ⏳ pending · ❌ cancelled · ↩️ return · ↔️ exchange · 🚨 fraud · 📊 report · ⚠️ warning · 📝 note · 🔒 hold
- Dates always DD MMM YYYY (e.g. 08 Apr 2026) — never MM/DD/YYYY or ISO format shown to user
- Currency always £ GBP — never USD or unadorned numbers
- For fraud: present signals factually, no drama — owner makes the call
- For refunds above HIGH_VALUE_APPROVAL_FLOOR: always confirm with owner even if REFUND_APPROVAL_REQUIRED = false
- For UK law blocks on denials: firm but not preachy — one clear warning, then respect the owner's decision
- For partial refunds on damaged items: acknowledge it's goodwill and note UK law supports the claim
- Keep action prompts short: "YES · DENY · PARTIAL" — not paragraphs
- If the owner is clearly busy (short messages, quick replies), be more concise and skip explanatory text
