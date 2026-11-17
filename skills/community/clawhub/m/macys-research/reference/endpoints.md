# macys-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**3 endpoints across 1 platform group(s).**

## Macy's (3)

### `macys_product`

- **HTTP:** `GET /macys/product/{productId}`
- **What:** Get a Macy's product's full detail. Returns one Macy's product's full detail: name, brand, description, department/division, category breadcrumb, pricing (with sale detection), availability, images, aggregate rating, and every purchasable color variant with its own price. productId is a numeric id, taken from a Macy's product page's ?ID= query parameter.
- **Params:** `productId` (string, **required**) — Numeric Macy's product id, from a product page's ?ID= query parameter

### `macys_product_reviews`

- **HTTP:** `GET /macys/product/reviews`
- **What:** Get a Macy's product's customer reviews. Returns one page of a Macy's product's customer reviews, plus a site-wide rating summary (rating count, average rating, recommended ratio, rating histogram) for the product. product_id is a numeric id, the same one used by GET /macys/product/{productId}. A product with zero reviews, or a well-formed but unrecognized product_id, returns a normal, empty result rather than an error.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `product_id` (string, **required**) — Numeric Macy's product id, from a product page's ?ID= query parameter

### `macys_suggest`

- **HTTP:** `GET /macys/suggest`
- **What:** Get Macy's search-box suggestions. Returns Macy's own search-box suggestions (typeahead) for a partial query: a flat list of suggested search phrases, no product data. A partial query with no real matches returns a normal, empty result rather than an error.
- **Params:** `query` (string, **required**) — Partial search query
