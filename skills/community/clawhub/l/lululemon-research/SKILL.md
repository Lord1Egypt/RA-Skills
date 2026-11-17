---
name: lululemon-research
description: Researches Lululemon's catalog — category navigation, category listings, product detail with pricing/sizes/reviews, curated outfit recommendations, and the physical store directory — using the Crawlora API, returning clean JSON. Use when the user asks to browse a Lululemon category, look up a Lululemon product's price/sizes/reviews, find what a Lululemon item is styled with, or locate a nearby Lululemon store — instead of scraping shop.lululemon.com.
---

# Lululemon research

Browse Lululemon's category navigation and listings, pull full product
detail (sizes, colors, price, sale status, reviews), look up curated
outfit/style recommendations for a product color, and search the physical
store directory — all as normalized JSON from the Crawlora API, with no
HTML scraping.

## When to use this skill

- "What's in Lululemon's [department]?" / "browse this Lululemon category."
- "What does this Lululemon product cost, and what sizes/colors are in
  stock?"
- "What's this Lululemon item styled with?" / "show the outfit for this
  product color."
- "Find a Lululemon store near [city/zip]."
- "Pull the reviews for this Lululemon product."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Browse the nav** — `/lululemon/categories` (optional `section`) lists
   every navigable category with its display name, breadcrumb, and the
   `category`/`cdp_hash` pair the next step needs.
2. **List a category** — `/lululemon/category` (`category`, `cdp_hash`,
   paginated with `page`/`page_size`) returns that category's products with
   pricing, sale detection, sizes, colors, and style numbers — one
   representative color/price per product.
3. **Detail** — `/lululemon/product/{product_id}` (`product_id` from a
   category result's `id` field) fetches every purchasable color/size SKU
   with its own price, sale status, live availability, plus aggregate
   rating and reviews when the product has any.
4. **Outfit lookup** — `/lululemon/outfit` (`unified_id` from the product's
   `unified_id` field, `color_code` from one of its `colors[].code`
   entries) returns the anchor product plus every complementary item in
   each curated styled look.
5. **Stores** — `/lululemon/stores` (optional `country`/`state`, or
   `lat`+`lng`+`radius_miles`) returns the physical store directory with
   hours and amenities.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Browse a top-level nav section for its categories:
scripts/crawlora.sh /lululemon/categories section="Women" | jq '.'

# List a category's products (category + cdp_hash come from lululemon/categories):
scripts/crawlora.sh /lululemon/category category="women-new-styles" cdp_hash="n14f1wz6o10" page=1 | jq '.'

# Product detail (product_id is a path param):
scripts/crawlora.sh /lululemon/product/prod123456 | jq '.data'

# Outfit recommendations for one product color:
scripts/crawlora.sh /lululemon/outfit unified_id="abc123" color_code="0001" | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Lululemon
endpoint this skill uses (method, path, params, description).

## Examples

- **Category sweep:** `/lululemon/categories` to find a department's
  `category`/`cdp_hash`, then `/lululemon/category` paginated with
  `page`/`page_size` to list products, prices, and sale status.
- **Product due diligence:** `/lululemon/product/{product_id}` for full
  color/size availability, price, and reviews, using the `id` from a
  category listing result.
- **Outfit build:** `/lululemon/product/{product_id}` to get a product's
  `unified_id` and `colors[].code`, then `/lululemon/outfit` with those two
  to see what it's styled with.
- **Store lookup:** `/lululemon/stores` with `lat`/`lng`/`radius_miles`, or
  `country`/`state`, to find nearby locations and hours.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Lululemon storefront/store-directory pages;
  respect Lululemon's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **No free-text search endpoint** — discovery is category-based only:
  `/lululemon/categories` → `/lululemon/category`, not a keyword search.
- `product_id` is a **path** param on `/lululemon/product/{product_id}`,
  not a query param.
- `/lululemon/category` pagination is real: a `page` past the category's
  last page returns an empty `products` array, not an error. An
  unrecognized `category`/`cdp_hash` pair returns `404`.
- `unified_id`/`color_code` for `/lululemon/outfit` come from a
  `/lululemon/product` result — `unified_id` is a different id space than
  that same product's `product_id`. An unrecognized pair returns `404`.
- `/lululemon/stores` has no live geo-search API — filters (`country`,
  `state`, `lat`/`lng`/`radius_miles`) are applied locally over the full
  directory (480 US + 86 Canada locations as of this endpoint's own
  research); `lat`/`lng` must be passed together.
