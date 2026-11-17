# My Hot Lunchbox endpoints — ready-to-run

All paths are relative to `$MHLB/api`. All need `Authorization: Bearer $MHLB_TOKEN`.
Assumes the `mhlb_get` helper from `SKILL.md` is defined.

## Account

```sh
# Account claims: name, role, student count, credit balances, subscription state
mhlb_get /auth/userinfo | jq .
```

## Students

```sh
mhlb_get /parent/childrenInfo | jq '.[] | {id, firstName, schoolName, gradeTeacher, hasOrders, isInactive, isInvited}'

# Editable profile for one student (also the model that POST /parent/editChild takes back)
mhlb_get '/parent/editChild?childId=456' | jq .

# Blank profile + dropdown options for adding a student
mhlb_get /parent/createChild | jq .
```

## Calendar and deliveries

```sh
# Lunch calendar for a range — a POST that reads
mhlb_post() {
  local endpoint=$1; shift   # NOT `path`: zsh ties $path to $PATH
  curl -sS -X POST "$MHLB/api$endpoint" -H "Authorization: Bearer $MHLB_TOKEN" \
    -H 'Content-Type: application/json' -d "${1:-{\}}"
}

# Fields are `start`/`end` — `startDate`/`endDate` silently returns zero events.
mhlb_post /calendar/studentSchoolData '{"start":"2026-09-01","end":"2026-09-30"}' | jq .

# Events carry the ids the ordering endpoints need:
mhlb_post /calendar/studentSchoolData '{"start":"2026-09-01","end":"2026-09-30"}' \
  | jq '.events[] | {studentId, eventId: .id, orderId, date: .start[0:10], className}'

# What one student has on one day
mhlb_get '/calendar/studentOrderItems?studentId=456&date=2026-09-14' | jq .
```

`/deliveryInfo/*` and `/calendar/viewMatchedVendors` look parent-facing in the
site's compiled client but return **403** for a parent account — they belong to
the school and vendor dashboards. Verified live; don't reach for them.

## Cart and menu

```sh
# Valid filter values first — periods (semesters) and status tabs
mhlb_get /event/ShoppingCartBaseData | jq '{periods: [.periods[] | {text, value, selected}]}'

# The cart itself; every filter is optional
mhlb_get '/event/shoppingCart' | jq .
mhlb_get '/event/shoppingCart?selectedStudentId=456' | jq .

# The orderable menu for a student on a date — vendor, items, sizes, prices, cutoff
mhlb_get '/event/orderBaseData?studentId=456&eventDate=2026-09-14' | jq .
```

## Transactions and subscriptions

```sh
mhlb_get /event/transactionsList              | jq .
mhlb_get '/event/transactionDetails?id=999' | jq .   # id comes from transactionsList
mhlb_get /event/subscription                  | jq .
mhlb_get '/event/upcomingSubscriptions'       | jq .
```

## Gift cards and coupons

```sh
mhlb_get /parent/giftCardDataTables | jq .
mhlb_get /parent/coupon             | jq .
```

## Printable reports

These stream a **binary PDF**, not JSON — pipe to a file, never to `jq`. Their
payloads are not date ranges.

```sh
mhlb_pdf() {  # usage: mhlb_pdf <endpoint> <json> <out.pdf>
  curl -sS -X POST "$MHLB/api$1" -H "Authorization: Bearer $MHLB_TOKEN" \
    -H 'Content-Type: application/json' -d "$2" -o "$3" && file "$3"
}

# Calendar — needs `middle` (the midpoint date, which titles the PDF) and a
# NON-EMPTY studentIds. There is no "all students" default: an empty or omitted
# list answers 500, same as printOrders.
mhlb_pdf /parentReports/printCalendar \
  '{"start":"2026-09-01","end":"2026-09-30","middle":"2026-09-15","studentIds":[111627]}' \
  'Lunch Calendar.pdf'

# Orders — ONE date, not a range. studentIds must be non-empty.
# orderStatus: 0 = Pending, 1 = Paid, 2 = Credited.
mhlb_pdf /parentReports/printOrders \
  '{"orderStatus":1,"eventDate":"2026-09-14","studentIds":[111627]}' \
  'Orders Details.pdf'

# One transaction receipt — send the record from transactionDetails.
# (A transactionsList ROW is a different shape and renders a thinner PDF;
#  the list is only used here to get the id.)
ID=$(mhlb_get /event/transactionsList | jq -r '.transactions[0].id')
mhlb_get "/event/transactionDetails?id=$ID" | jq -c '. + {isCreditType:false}' > tx.json
mhlb_pdf /parentReports/printTransactions "$(cat tx.json)" 'Transaction.pdf'
```

Both `printCalendar` and `printOrders` answer **500** — not a 4xx — when
`studentIds` is empty, and `printOrders` also 500s when no order matches the
date and status. Treat a 500 from either as a bad request, not an outage.

`printTransactions` wants the record from `/event/transactionDetails`, **not** a
row from `/event/transactionsList` — both render, but they are different shapes
and different documents. The list is only used to get the id, as the recipe
above does.

## Writes — all UNVERIFIED

Paths and verbs are read out of the site's compiled client and are reliable.
The **request bodies** have not been exercised against a live account. Fetch the
model, edit it, post it back whole, then re-read to confirm.

| Action | Read the model | Post it back |
|---|---|---|
| Place an order | `GET /event/createOrder?eventId=&studentId=` | `POST /event/createOrder` |
| Change an order | `GET /event/editOrder?orderId=` | `POST /event/editOrder` |
| Cancel an order | — | `POST /event/deleteOrder` — body below, **not** the order model |
| Add a student | `GET /parent/createChild` | `POST /parent/createChild` |
| Edit a student | `GET /parent/editChild?childId=` | `POST /parent/editChild` |
| Remove a student | — | `POST /parent/deleteChild?id=` |
| Apply a gift card | — | `POST /parent/applyGiftCard?giftCardCode=` |
| Apply a coupon | — | `POST /parent/applyCoupon?couponCode=` |
| Remove the coupon | — | `POST /parent/removeCoupon` |
| Toggle subscriptions | `GET /event/subscription` | `POST /parent/changeSubscriptionStatus?isEnableSubscription=` |
| Stop one subscription | `GET /event/upcomingSubscriptions` | `POST /event/unsubcribeOrder` — same body as deleteOrder |
| Price the cart | — | `POST /payment/initCheckout` |
| **Pay** | — | `POST /payment/checkout` |

`POST /event/unsubcribeOrder` is spelled that way upstream — the typo is theirs.

Cancelling and unsubscribing take a small identifier payload, **not** the order
model that create/edit round-trip. Captured from the site's own `order-mixin`:

```sh
# isRepeated: true acts on the whole recurring series, not just this date.
mhlb_post /event/deleteOrder \
  '{"orderId":17284377,"eventDate":"2026-08-26","studentId":111627,"isRepeated":false,"isSubscribed":false}'
```

Checkout takes `{orderIds, checkoutType, couponCode, giftCardCode, schoolDonations}`,
with the nulls sent explicitly, plus `{availableCredits, idempotencyKey, stripeToken}`
on `/payment/checkout`:

```sh
mhlb_post /payment/initCheckout \
  '{"orderIds":[123],"checkoutType":null,"couponCode":null,"giftCardCode":null,"schoolDonations":null}'
```

Two things about paying:

- **`stripeToken` cannot be produced outside a browser.** The site mints it with
  Stripe.js, and only when paying by a NEW card. Server-side you can only pay
  with a card already saved on the account.
- **`idempotencyKey` is yours to generate** — the site uses
  `"$(uuidgen | tr A-Z a-z)-$(date +%s000)"`. Reuse the SAME key when retrying an
  ambiguous checkout; a fresh one risks a second charge.

`POST /payment/checkout` charges a real payment method. Price with
`initCheckout` first, read the total it returns, and confirm that figure before
paying.

## Endpoints a parent account cannot reach

The same bundle serves school-admin and vendor roles. These return `403` for a
parent and are listed only so a `403` is not mistaken for a broken session:
`/school`, `/schoolManagement`, `/schoolOnboarding`, `/vendor`, `/vendorReports`,
`/schoolVendorReports`, `/item`, `/adminTasks`, `/quickbooks`, `/docusign`,
`/interactiveDistributionReport`, `/upload`, `/deliveryInfo`, and
`/calendar/viewMatchedVendors`.
