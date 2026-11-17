# Sharpening and physical handoff

Seller-owned published SKUs may use [native listing checkout](listing-checkout.md)
only with individually verified fulfillment terms. It does not reserve service
appointments or infer transport fees from shipping labels. Missing/conflicting
terms mean merchant review. The workflow below is the separate operator-service
booking path; never change product ownership or grant sellers administrator rights.

Use current catalog service definitions. Do not invent small/large size cutoffs,
restoration scope, or handling rules. Unsupported damage or assessment work must
be priced by an operator before prepayment. Version 1 excludes mixed tech/service
carts, gift-card balances, and automatic inspection surcharges.

Specify both legs:

| Leg | Options |
|---|---|
| Intake | `customer_dropoff`, `courier_pickup` |
| Return | `customer_collection`, `courier_delivery` |

Customer handoff uses the configured merchant location. Courier legs require
separate configured fees and merchant address verification; preliminary ZIP
eligibility cannot validate a street address. Do not change a requested courier
service to drop-off silently when transport is unavailable.

Scheduling mode `scheduled` requires one available `slot_id` for each leg.
Capacity counts jobs per window; the return window must follow intake.
Show date/time in America/Los_Angeles with offset or timezone abbreviation.
The server reserves the windows only at authorized checkout, then confirms them
after payment verification. Catalog/quote availability is not a reservation.

Mode `pending_scheduling` is available only when explicitly configured. Clearly
say that payment prepays the named service and the appointment still needs to be
arranged. The customer must accept that mode and its policies before paying.

Present fees for both transport legs, service scope, taxes, total, timing,
cancellation/rescheduling/refund terms, and the merchant location before approval.
Check payment and booking separately. A late payment can be `paid` with
`pending_scheduling`; give the merchant follow-up path without inventing a time.
