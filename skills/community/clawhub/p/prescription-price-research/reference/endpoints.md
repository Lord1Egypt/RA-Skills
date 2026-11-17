# prescription-price-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**3 endpoints across 1 platform group(s).**

## GoodRx (3)

### `goodrx_drug_options`

- **HTTP:** `GET /goodrx/drug-options`
- **What:** List a GoodRx drug's prescription options. Returns every brand and generic label, dosage form, strength, and quantity GoodRx prices for one drug, with GoodRx's default prescription. Use these values for /goodrx/drug-prices.
- **Params:** `slug` (string, **required**) — Drug slug from /goodrx/drugs

### `goodrx_drug_prices`

- **HTTP:** `GET /goodrx/drug-prices`
- **What:** Get GoodRx drug prices by pharmacy. Returns GoodRx coupon, membership, and mail-order prices by pharmacy for one drug and prescription (brand/generic label, form, dosage, quantity), plus the drug summary, the priced configuration, the location prices were computed for, and every available label/form/dosage/quantity. Omit label/form/dosage/quantity for GoodRx's default prescription; values must come from /goodrx/drug-options. Pass latitude and longitude (optionally zip_code and state) to price at a US location; otherwise prices reflect a US location chosen by GoodRx. Requests use US egress because GoodRx is US-only.
- **Params:** `dosage` (string, optional) — Dosage slug from /goodrx/drug-options; `form` (string, optional) — Form slug from /goodrx/drug-options; `label` (string, optional) — Brand or generic label slug from /goodrx/drug-options; `latitude` (number, optional) — Latitude of a US location to price at (requires longitude); `longitude` (number, optional) — Longitude of a US location to price at (requires latitude); `quantity` (integer, optional) — Quantity (1-999999); /goodrx/drug-options lists GoodRx's standard quantities; `slug` (string, **required**) — Drug slug from /goodrx/drugs, /goodrx/class, or /goodrx/condition-drugs; `state` (string, optional) — Two-letter state code of that location; `zip_code` (string, optional) — Five-digit ZIP code of that location

### `goodrx_drugs`

- **HTTP:** `GET /goodrx/drugs`
- **What:** List GoodRx drugs by letter. Lists the drugs GoodRx files under one letter of its A-Z directory, chosen with the required `letter` (`a` to `z`). Each drug has its name, price-page `slug`, GoodRx URL and drug-information URL. If GoodRx is unreachable, a retained copy up to about a day old is returned and flagged with an `X-Availability-Mode: stale` header.
- **Params:** `letter` (string, **required**) — Directory letter
