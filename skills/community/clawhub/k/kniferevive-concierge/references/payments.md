# Payments

Contact/address sharing and payment authority are separate. The private first-party
form obtains booking-specific sharing approval; installing a skill or being logged
in provides neither. A saved native card/token still requires the human's eligible
provider confirmation. Delegated card spending is unsupported. Host wallet grants
are unknown unless a supported independent wallet interface verifies their scope.
Never interpret merchant acceptance flags or quote approval as wallet authority.

## Native marketplace listings

Use the listing reference for private intents/quotes and protected buyer review.
The accepted cart goes to first-party WooCommerce checkout. Its actual native
gateway owns payment, webhooks, refunds and seller payouts. The adapter creates
no Stripe Checkout session or Lightning invoice for marketplace sellers. Google
Pay/Lightning is conditional on the native gateway and device. Use scoped status;
`refund_recorded` is a WooCommerce record, not independently proven reimbursement.
Sharpening SKU payment remains `not_booked`. Do not automate approval or payment.

The remaining sections describe the separately enabled operator-service flow.

All browsing and quoting is free. The merchant creates payable artifacts only
after customer consent and server reservation. Never send a shopper's payment
credentials to this API.

## Stripe and Google Pay

`stripe_checkout` returns a merchant-bound URL at the exact HTTPS host
`checkout.stripe.com`. Open it without forwarding session/API headers. The
customer completes payment and any wallet/3DS authorization there. Google Pay
is conditional on Stripe settings and customer device; the adapter does not
provide autonomous Google account spending. Test sessions are labeled `test`.
Do not call a Stripe PaymentIntent API with merchant credentials from the skill.

A success page, browser redirect, or checkout URL proves no payment. Use the
merchant's verified status. Keep an unknown result on the original attempt.

## Bitcoin Lightning

For the separate booking workflow, follow [Booking requests](booking.md): an
explicitly authorized host wallet may pay the original scoped native invoice
only when `authorized_wallet_payment_enabled=true`. Order/invoice preparation
still uses native buyer checkout; autonomous order creation is unavailable.
No new wallet or merchant key access is required. The remaining section describes
the separately gated legacy operator-service flow.

The deployed bridge supplies an order-bound mainnet BOLT11 invoice with satoshi
amount, payment hash, expiry, and locked fiat total. Use the host's existing
wallet tools to decode/check the invoice. Match the expected mainnet network,
amount, unexpired time, payment hash, trusted merchant checkout provenance, and
wallet payee policy. A descriptive memo is not proof of merchant identity.
If validation or an independent wallet approval control is unavailable, show a
manual invoice/payment-page handoff and wait for the customer.

An explicit mandate must cover this merchant, items/service, rail, all-in total,
fulfillment, expiry, and maximum routing fee. The merchant consent reference is
not authorization to spend from a wallet. Pay an invoice at most once; a wallet
timeout requires checking that wallet's original payment status before retrying.
Never create/fund a node, open a channel, expose a seed, or use admin macaroons.

Confirm via merchant settlement reconciliation. If a hold expired, the payment
may require manual rescheduling/refund review. Do not say booked until booking
state is confirmed. Fee waivers come from the server's rail-specific quote.

## Changes and refunds

Only request cancellation/rescheduling through the scoped merchant endpoint.
Customer requests do not issue processor refunds. Stripe refunds use the existing
operator order-refund workflow through this adapter's gateway. Lightning refunds
remain manual, with authorized recipient and evidence supplied to the operator.
Never automatically issue refunds or send additional funds from the skill.
