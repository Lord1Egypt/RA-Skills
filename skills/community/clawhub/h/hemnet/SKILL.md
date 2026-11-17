---
name: hemnet
description: >-
  Search and analyse Swedish real estate on hemnet.se — active for-sale
  listings, sold prices (slutpriser), full listing details, photos, market
  statistics, address resolution, and a Swedish mortgage calculator. Use
  when the user asks about Swedish property, Hemnet, bostäder, lägenheter,
  villor, or slutpriser.
---

# Hemnet (hemnet.se)

Tools for Sweden's largest property portal. All reads go through Hemnet's
public GraphQL API (no login, no configuration). Money is in **SEK**,
areas in **m²**, rooms as a number.

## Start with a location

Hemnet searches take numeric **location ids**, not place names. Resolve
first:

1. `hemnet_autocomplete_location` — `{ query: "Vasastan" }` →
   `{ location_id, full_name, parent_full_name }` hits.

Then pass a `location_id` into the search tools — or pass a free-text
`location` and the tool resolves the top hit for you.

## For-sale listings

- `hemnet_search_listings` — search by `location`/`location_ids` plus
  optional `price_min`/`price_max` (SEK), `rooms_min`/`rooms_max`,
  `living_area_min`/`living_area_max` (m²), `housing_form_groups`
  (`HOUSES`, `APARTMENTS`, `ROW_HOUSES`, `VACATION_HOMES`, `PLOTS`,
  `OTHERS`), `keywords`, `sort` (`NEWEST`/`OLDEST`).
- `hemnet_get_listing` — full detail by id or `/bostad/` URL: price, fee
  (avgift), yearly running costs, m², rooms, tenure, energy class,
  broker, description, status labels, coordinates, and photo URLs.
- `hemnet_get_listing_photos` — just the gallery URLs.
- `hemnet_compare_listings` — several listings at once (≤20).
- `hemnet_get_by_address` — resolve a street address (+ city/area) to a
  live listing. Scans up to 500 listings in the location; a miss with
  `truncated: true` is not definitive — add `price_min`/`price_max`.

## Sold prices (slutpriser) — Hemnet's signature dataset

- `hemnet_search_sold` — sold listings with achieved **final price**,
  the **asking price**, and the **over/under-asking %**. The comps for
  valuation.
- `hemnet_get_sold_listing` — full detail for one sold listing.
- `hemnet_get_market_stats` — median/average final price and price-per-m²
  for a location (accepts the same filters as the sold search). It
  aggregates the most recent `max_sales` sales (default 200, max 500;
  the old `limit` still works as an alias and `offset` is ignored), so
  compare `sampled_sales` with `total_matching_sales`, and check
  `sample_size` before trusting thin medians.

## Local calculation

- `hemnet_calculate_mortgage` — Swedish monthly cost (SEK): interest +
  mandated amortisation (amorteringskrav from LTV; rules as of 1 April
  2026, no debt-ratio rule) + BRF fee/operating cost, with both gross and
  after-tax (ränteavdrag) totals. Down payment defaults to the legal 10%
  minimum. No network.

## In context groups

Hemnet is a member of the **home** group. It has no canonical read and no
subjects: there is no account, so nothing lists the person's homes or
saved searches, and every search needs a place the person names. A
compound ask ("what's on at home, and anything new on Hemnet?") gets no
Hemnet line from the group's intent tools; ask a direct question with a
place instead ("new apartments for sale in Vasastan?", "what did villas
sell for in Täby?"), which the group routes to these lookups by their
aliases (for sale, bostad, slutpris, mortgage, …). When Hemnet's
Cloudflare wall forces the browser-bridge leg and no hemnet.se tab is
open, the group answers "needs your browser open" for Hemnet.

## Diagnostics

- `hemnet_healthcheck` — one-call check that the GraphQL endpoint is
  reachable.

## Notes

- Tenure: `Bostadsrätt` (co-op apartment, has a monthly `fee`/avgift),
  `Äganderätt` (owned house), `Hyresrätt` (rental).
- `price_per_sqm` is always derived when price + living area allow it,
  even when Hemnet omits it (common on houses).
- This project is developed and maintained by AI (Claude). Use within
  hemnet.se's terms of service.
