# Harris Teeter atlas requests (live-verified 2026-11-11)

Base: `https://www.harristeeter.com/atlas/v1`. Full notes: `docs/HT-API.md` in harristeeter-mcp.

Every call: `-H 'x-kroger-channel: WEB'` (uppercase).

## Store context → `x-laf-object`

```sh
fpx post-json 'https://www.harristeeter.com/atlas/v1/modality/preferences?filter.restrictLafToFc=true' '{}' -p harristeeter \
  -H 'x-kroger-channel: WEB' | jq -c '.data.modalityPreferences.lafObject'     # → the x-laf-object header value
```
(GET answers 405.) Pickup `locationId` (8 digits, division+store):
`.data.modalityPreferences | (.primaryModality.PICKUP) as $id | .modalities[] | select(.id==$id) | .destination.locationId`.

Calls that need `x-laf-object`: search, products, cart PUT, timeslots, purchase history.
Timeslots also need `user-time-zone: America/New_York` (else `MISSING_TIMEZONE_HEADER`).

## Search + price

```sh
LAF=…; LOC=…
fpx get "https://www.harristeeter.com/atlas/v1/search/v1/products-search?filter.query=milk&filter.locationId=$LOC&filter.fulfillmentMethods=PICKUP&page.size=5&page.offset=0&option.monetization=NONE" \
  -p harristeeter -H 'x-kroger-channel: WEB' -H "x-laf-object: $LAF" | jq '.data.productsSearch[] | {upc, description}'
fpx get "https://www.harristeeter.com/atlas/v1/product/v2/products?filter.gtin13s=0001111042852&filter.verified=true&projections=items.full" \
  -p harristeeter -H 'x-kroger-channel: WEB' -H "x-laf-object: $LAF" \
  | jq '.data.products[] | {upc: .item.upc, description: .item.description, price: .price.storePrices.regular.price}'
```
`filter.keyword` returns nothing — use `filter.query`. `projections=items.compact` has no price.

## Cart

```sh
fpx get https://www.harristeeter.com/atlas/v1/carts -p harristeeter -H 'x-kroger-channel: WEB' | jq '.data.carts[0] | {id, lineItems}'
```
`PUT /carts/<cartId>` with `{"lineItems":[…]}` merges — only named lines change:
- add/set: `{"gtin13":"…","channel":"WEB","modalityType":"PICKUP","quantity":N,"substitutionPolicy":"SHOPPER_CHOICE","id":"<line id if present>"}`
- remove: `{"id":"<line id>","gtin13":"…","quantity":0,"modalityType":"PICKUP"}`

## Pickup windows

`POST /promising/v4/timeslots` body `{"items":[{"gtin13":"…","quantity":N}]}` with
`x-laf-object` + `user-time-zone` → `.data.timeslots.days[].times[] | {displayString, window.value, cost}`.

## Read-only extras

- `GET /checkout/v1/checkouts` — drafts: `.summary.cost.total`, `.fulfillment.promise.selections[0].window.value`.
- `GET /post-order/v1/purchase-history-search?pageNo=1&pageSize=20&startDate=YYYY-MM-DD&endDate=YYYY-MM-DD` (needs `x-laf-object`).
- `GET /customer-profile/v1/profile` — contains personal data; don't dump it.
