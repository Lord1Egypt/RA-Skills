# kohls-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**4 endpoints across 1 platform group(s).**

## Kohl's (4)

### `kohls_category`

- **HTTP:** `GET /kohls/category`
- **What:** Browse a Kohl's category or curated campaign page. Returns a Kohl's category or curated campaign page's product grid (page 1 only), with products (title, image, colors, pricing, rating, availability) and facets for discovering further category values. category is Kohl's own catalog taxonomy string, e.g. "Room:Dorm" or "Department:Kitchen & Dining" -- combine multiple dimensions with a literal "+", percent-encoded as "%2B" so it survives as "+" rather than being decoded to a space (e.g. "Room%3ADorm%2BDepartment%3ABedding"). Every facets[].options[].category value in a response is a ready-to-use category string for a follow-up call, so a caller can discover the full taxonomy by starting from a known category (e.g. "Room:Dorm") and following facets. A category value Kohl's does not recognize returns a 404 rather than an unfiltered listing; a recognized dimension with no matching products returns a genuine zero-result response instead.
- **Params:** `category` (string, **required**) — Kohl's catalog taxonomy string, e.g. \

### `kohls_product_reviews`

- **HTTP:** `GET /kohls/product/reviews`
- **What:** Browse a Kohl's product's customer reviews. Returns one page of a Kohl's product's customer reviews (title, text, rating, secondary ratings such as quality/durability/value/style, reviewer name and location, submission date, and photo URLs). web_id is the same identifier a GET /kohls/category response's products[].web_id field carries. A web_id with zero reviews returns a genuine zero-result response rather than an error.
- **Params:** `page` (integer, optional) — Page number, 10 reviews per page (default 1); `web_id` (string, **required**) — Kohl's product web id, e.g. from a GET /kohls/category response's products[].web_id

### `kohls_stores`

- **HTTP:** `GET /kohls/stores`
- **What:** Find nearby Kohl's store locations. Returns physical Kohl's store locations near a free-text location (city/state, zip code, or address): address, phone, weekly hours, distance, and store badges/services. A search with no results returns a genuine empty list rather than an error.
- **Params:** `search` (string, **required**) — Free-text location: city/state, zip code, or address

### `kohls_suggest`

- **HTTP:** `GET /kohls/suggest`
- **What:** Kohl's search-box typeahead suggestions. Returns Kohl's own search-box typeahead result for a partial query: a flat list of suggested search phrases (no product data). A nonsense query returns a genuine, well-formed empty list rather than an error.
- **Params:** `query` (string, **required**) — Partial search text, e.g. \
