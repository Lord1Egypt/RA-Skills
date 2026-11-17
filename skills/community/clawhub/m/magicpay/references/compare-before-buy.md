# Compare Before Buy

Use this when a user has selected a retail product and might benefit from the
same item at a lower delivered price. The host agent researches current seller
pages with its normal search and browser tools; MagicPay handles the chosen
checkout. This is an optional suggestion, not a required stop before buying.

Offer a quick check once when the seller is flexible. If the user asks for a
cheaper source, compare directly. Keep the purchase direct when the user chose
a particular seller, speed matters, or payment is already in progress. Do not
silently change a chosen merchant.

Match the actual item: model, variant (such as size, color, or capacity),
condition, quantity, and bundle. Use product identifiers when available, but
do not invent them. A near match is an alternative, not the same item; suggest
alternatives only if the user wants them. For subscriptions or services, terms
and fulfillment rights also have to match.

Check a few credible current offers as useful. Compare the delivered total,
including shipping, tax, and fees when shown, along with stock, delivery time,
region, returns, and warranty. State what is unknown; a lower listing price
alone does not establish savings. Verify the chosen offer and final total on
the merchant's checkout page.

Present the original and any better offer with source links, comparable totals
or unknowns, and the trade-off that matters. Recommend when one choice is
clear. Use [choices](choices.md) only when a material user preference remains;
research or a choice is not payment approval.

Choose the item and merchant before starting [browser checkout](host-browser-payments.md).
An existing MagicPay session or approval cannot be transferred to another
seller. If payment is pending or uncertain, follow [statuses and recovery](statuses.md)
for the exact operation rather than starting a replacement. A later purchase
from another merchant needs its own checkout and approval after the original
is safely closed and the user authorizes it.
