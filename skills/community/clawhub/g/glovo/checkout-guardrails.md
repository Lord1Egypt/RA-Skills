# Checkout Guardrails - Glovo

Treat these actions as increasingly sensitive:

## Browse Safe

- switching between category and store pages
- reading ETA, fees, minimums, and promo labels
- comparing stores without changing the cart

## Draft Cart Only If Requested

- adding items to an empty cart
- editing quantities on a fresh draft
- testing substitutions or notes for a candidate order

If the cart already contains items, ask whether to preserve, replace, or merge before editing.

## Explicit Confirmation Required

Always stop and summarize before:
- changing the delivery address
- clearing a non-empty cart
- applying a final promo that changes the total
- confirming payment and placing the order

## Final Summary Format

Before live checkout, confirm:
- store name
- items and quantities
- substitutions or special notes
- active delivery address
- ETA
- delivery fee, service fee, tip, and total
- payment method shown by Glovo

If any one of those is unclear on screen, do not place the order.
