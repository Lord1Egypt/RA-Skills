---
name: india-food-ordering
description: Unified food ordering assistant for India that supports Swiggy and Zomato workflows with strict pre-order confirmation, cart preview, address checks, and vendor fallback logic.
metadata: {"openclaw":{"emoji":"🍽️","homepage":"https://clawhub.ai/regalstreak/swiggy"}}
---

# India Food Ordering (Swiggy + Zomato)

## What this skill does

Provides one consistent ordering workflow across both vendors:

- Swiggy
- Zomato

Additional vendor targets (when connector/MCP support exists):

- EatSure
- magicpin
- ONDC-compatible food apps
- Blinkit Bistro / Zepto Cafe style quick-food verticals

This skill focuses on safe, human-confirmed ordering operations.

## Disclaimer

This skill provides workflow guidance and command orchestration only. It does not guarantee availability, pricing, ETA, or cancellation rights on either platform. Vendor capabilities and policies can change without notice.

Use at your own risk. The skill author/publisher/developer is not liable for direct or indirect loss, wrong orders, payment issues, delays, cancellations, or other damages from use or misuse of this guidance.

## Core safety rules (non-negotiable)

1. **Never place an order without explicit user confirmation**
2. **Always show full cart preview before confirmation**
3. **Always confirm delivery address before placing order**
4. **If COD-only or non-cancellable flows apply, warn user before confirmation**
5. **If uncertain about item, price, or address, ask before proceeding**

## Standard workflow

### Step 1: Collect intent

- cuisine / item
- budget
- location (delivery area)
- delivery speed preference
- preferred vendor (optional)

### Step 2: Vendor discovery

- Search both vendors when possible.
- If only one vendor is available, continue with it.
- If both are available, compare and present best options.

### Step 3: Compare options

Return side-by-side:

- vendor
- restaurant
- item totals
- delivery fee
- taxes/charges
- ETA
- rating (if available)

### Step 4: Build cart

- add selected items
- show running subtotal
- check item availability

### Step 5: Mandatory confirmation prompt

Use this exact style:

```text
Ready to place order:
- Vendor: <Swiggy/Zomato>
- Restaurant: <name>
- Items: <list with qty>
- Total payable: <amount>
- Delivery address: <full address label>
- ETA: <time window>
- Notes: <COD only / non-cancellable / special terms if any>

Confirm order? (yes/no)
```

### Step 6: Place order only after "yes"

- Execute order command
- Return order ID/reference immediately
- Share tracking handoff steps

## Vendor routing logic

- If user specifies vendor, honor it unless unavailable.
- If unspecified, choose:
  1. lower final payable
  2. faster ETA
  3. higher reliability/rating
- If selected vendor fails, offer fallback on the other vendor and re-confirm.

## Error handling

- **No restaurants found**: broaden radius or cuisine terms.
- **Item unavailable**: propose equivalent items.
- **Cart mismatch**: re-fetch cart and re-confirm.
- **Auth/session issue**: ask user to re-authenticate vendor connector.
- **Payment/checkout failure**: do not auto-retry order placement; ask user.

## Output format

When helping user order, respond in this structure:

1. Top options (max 3)
2. Recommended vendor and reason
3. Cart summary
4. Confirmation question

## Setup

Read [setup.md](setup.md) on first use.

## Validation

Run [validation-checklist.md](validation-checklist.md) before production usage.

## References

- Operational notes: [vendor-playbook.md](vendor-playbook.md)
- Prompt examples: [examples.md](examples.md)
- Safety and QA checks: [validation-checklist.md](validation-checklist.md)
- Launch flow: [launch-playbook.md](launch-playbook.md)

