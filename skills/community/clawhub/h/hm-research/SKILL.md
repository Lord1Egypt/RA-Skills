---
name: hm-research
description: Researches H&M's catalog — storefront categories, product listings, product detail, free-text search, and nearby physical stores — using the Crawlora API, returning clean JSON. Use when the user asks to find a product on H&M, browse an H&M category, search H&M's catalog by keyword, pull an H&M product's colors/sizes/reviews, or find a nearby H&M store — instead of scraping hm.com.
---

# H&M research

Browse H&M's storefront categories, list or search products, and pull full
product detail (colors, per-size stock, reviews) and nearby physical
stores — all as normalized JSON from the Crawlora API, with no HTML
scraping.

## When to use this skill

- "What does X cost on H&M?" or "find X on H&M."
- "Browse H&M's {department} category" / "what's new in H&M's {department}?"
- "Search H&M for {keyword}."
- "Pull the colors/sizes/reviews for this H&M product."
- "Find the nearest H&M store to {zip/place}."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Browse categories** — `/hm/categories` returns H&M's own storefront
   nav, department by department (optionally scoped with `department`).
   Entries include a verified `category_id` only where it's been confirmed
   against `/hm/listing`; not every category has one yet.
2. **List or search** — `/hm/listing` (`category_id`, an H&M category slug
   like `ladies_newarrivals_all` or `men_newarrivals_all`) or `/hm/search`
   (`query`, free-text) both return normalized products with pricing,
   images, colors, and per-size stock, paginated with `page`/`page_size`.
3. **Detail** — `/hm/product/{product_id}` (numeric id, taken from a
   listing/search result's `id` field or the `productpage.<id>.html`
   segment of its `url`) fetches every purchasable color with its own
   per-size price/availability, plus aggregate rating and real customer
   reviews with fit-feedback tags (e.g. "True to Size").
4. **Stores** — `/hm/stores` finds nearby physical H&M stores by `search`
   (zip/place, resolved to coordinates) or by `lat`/`lng` directly, within
   an optional `radius_meters`.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Browse a category:
scripts/crawlora.sh /hm/listing category_id=ladies_newarrivals_all page=1 | jq '.'

# Free-text search:
scripts/crawlora.sh /hm/search query="linen shirt" | jq '.'

# Product detail (colors, sizes, reviews):
scripts/crawlora.sh /hm/product/1234567 | jq '.data'

# Nearby stores:
scripts/crawlora.sh /hm/stores search="98101" radius_meters=15000 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every H&M
endpoint this skill uses (method, path, params, description).

## Examples

- **Category browse with detail:** `/hm/categories` (optionally filtered by
  `department`) to find a `category_id`, then `/hm/listing` paginated to
  list products, then `/hm/product/{product_id}` for the picks worth a
  closer look.
- **Keyword search with reviews:** `/hm/search` for a query, then
  `/hm/product/{product_id}` on the top results to compare per-color
  pricing/stock and summarize customer reviews before recommending one.
- **Local store check:** `/hm/stores` with a `search` zip/place (or
  `lat`/`lng`) to list nearby stores before telling a shopper where to try
  something on.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public H&M product/category/store pages; respect H&M's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **No category-tree lookup endpoint** — `/hm/listing`'s `category_id`
  values come from known H&M storefront slugs, not a discovery call;
  `/hm/categories` only exposes a verified `category_id` for the subset of
  nav entries this build has confirmed.
- **Colors/sizes/reviews only come from product detail** — `/hm/listing`
  and `/hm/search` carry one representative price and a per-color stock
  count each, not the full per-size breakdown or reviews.
- Pagination is real on `/hm/listing` and `/hm/search` — requesting a page
  past the last one returns an empty `products` array, not an error.
