# oldnavy-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**7 endpoints across 1 platform group(s).**

## Old Navy (7)

### `oldnavy_categories`

- **HTTP:** `GET /oldnavy/categories`
- **What:** List Old Navy storefront categories. Lists Old Navy's own storefront navigation as name/cid pairs, resolving the cid-discovery gap oldnavy-search, oldnavy-product, and oldnavy-category all document. Omit cid to list Old Navy's top-level divisions (e.g. Women, Men, Boys, Toddler). Pass a cid (a division's own, or any deeper category's) to list the related categories for that part of the storefront instead, in the same order the live storefront menu shows them -- this is section-level, not necessarily unique per leaf category. Currently only available for brand=on (Old Navy).
- **Params:** `brand` (string, optional) — Storefront to list -- only on (Old Navy) is currently supported; `cid` (string, optional) — Category id to list related categories for; omit to list the top-level divisions

### `oldnavy_category`

- **HTTP:** `GET /oldnavy/category`
- **What:** Browse an Old Navy, Gap, Banana Republic, or Athleta category. Returns a category/browse listing for one storefront category id (cid). cid is an opaque Gap Inc category id assigned by the storefront's own navigation -- neither oldnavy-search nor oldnavy-category currently surface a category-id list, so find one from the storefront's own category page URLs (the cid query parameter on a /browse/... page) for now. Select the storefront with the brand parameter (`on` for Old Navy, `gap` for Gap, `br` for Banana Republic, `at` for Athleta; defaults to `on`) -- it must match the brand the cid was found under. Returns the category's subcategory breakdown, product summaries with per-color inventory data, and available search facets with live counts.
- **Params:** `brand` (string, optional) — Storefront to browse; `cid` (string, **required**) — Category id, from a storefront category page's own cid query parameter; `page` (integer, optional) — One-based page

### `oldnavy_product`

- **HTTP:** `GET /oldnavy/product`
- **What:** Get an Old Navy, Gap, Banana Republic, or Athleta product. Returns product-detail data for one color variant: name, description, images, aggregate rating, and every size offered in that color as a separate priced offer. pid is a color-specific product id, as returned by oldnavy-search's product colors[].id field (not the bare base product id). Select the storefront with the brand parameter (`on` for Old Navy, `gap` for Gap, `br` for Banana Republic, `at` for Athleta; defaults to `on`) -- it must match the brand the pid was found under.
- **Params:** `brand` (string, optional) — Storefront the pid belongs to; `pid` (string, **required**) — Color-specific product id, from a search result's colors[].id field

### `oldnavy_product_availability`

- **HTTP:** `GET /oldnavy/product/availability`
- **What:** Check in-store pickup stock for an Old Navy, Gap, Banana Republic, or Athleta product. Checks per-size, in-store pickup stock status for one color (pid) at one or more physical stores. pid matches oldnavy-product's own color-level id. Give store location either directly with store_id (one or more comma-separated store ids, e.g. from a prior call to this endpoint or a value you already have) or with zip or both lat and lng, which resolves the nearest stores automatically. Select the storefront with the brand parameter (`on` for Old Navy, `gap` for Gap, `br` for Banana Republic, `at` for Athleta; defaults to `on`). Each returned store lists every offered size's stock status: `in_stock`, `out_of_stock`, or `low_stock`.
- **Params:** `brand` (string, optional) — Storefront to check; `lat` (number, optional) — Latitude to resolve the nearest stores from (must be given together with lng); `lng` (number, optional) — Longitude to resolve the nearest stores from (must be given together with lat); `pid` (string, **required**) — Color-level Old Navy/Gap/Banana Republic/Athleta product id; `store_id` (string, optional) — One or more comma-separated numeric store ids; `zip` (string, optional) — Zip code to resolve the nearest stores from

### `oldnavy_product_reviews`

- **HTTP:** `GET /oldnavy/product/reviews`
- **What:** Get reviews for an Old Navy, Gap, Banana Republic, or Athleta product. Returns one page of a product's customer reviews (author, date, rating, headline, body, and verified-purchase flag), plus the product's overall rating summary (average rating, rating count, per-star histogram, and recommended ratio). pid is a color-specific product id, as returned by oldnavy-search's product colors[].id field (not the bare base product id) -- the same pid oldnavy-product accepts. Select the storefront with the brand parameter (`on` for Old Navy, `gap` for Gap, `br` for Banana Republic, `at` for Athleta; defaults to `on`) -- it must match the brand the pid was found under. A product with no reviews yet returns a well-formed empty result, not an error.
- **Params:** `brand` (string, optional) — Storefront the pid belongs to; `page` (integer, optional) — One-based page, 10 reviews per page; `pid` (string, **required**) — Color-specific product id, from a search result's colors[].id field

### `oldnavy_search`

- **HTTP:** `GET /oldnavy/search`
- **What:** Search Old Navy, Gap, Banana Republic, or Athleta products. Searches product listings across Old Navy, Gap, Banana Republic, and Athleta -- select the storefront with the brand parameter (`on` for Old Navy, `gap` for Gap, `br` for Banana Republic, `at` for Athleta; defaults to `on`). Returns product summaries with pricing, review scores, and every purchasable color variant. This search is best-effort relevance, not a guaranteed keyword match: for an obscure or nonsense keyword the upstream search index falls back to its own recommended results instead of returning an empty list, and there is currently no reliable signal in the response to distinguish a true keyword match from that fallback behavior.
- **Params:** `brand` (string, optional) — Storefront to search; `keyword` (string, **required**) — Search keyword; `page` (integer, optional) — One-based page

### `oldnavy_stores`

- **HTTP:** `GET /oldnavy/stores`
- **What:** Find Old Navy, Gap, Banana Republic, or Athleta store locations. Searches physical store locations for one storefront by free-text search (zip code or city) and/or coordinates. Provide search, or both lat and lng. Select the storefront with the brand parameter (`on` for Old Navy, `gap` for Gap, `br` for Banana Republic, `at` for Athleta; defaults to `on`). Returns each nearby store's name, full address, phone number, coordinates, distance, and specialties (e.g. "In-Store Shopping", "Outlet"). This is location search only -- it does not report per-item, per-store stock levels; use oldnavy-product-availability for that.
- **Params:** `brand` (string, optional) — Storefront to search; `lat` (number, optional) — Latitude (must be given together with lng); `lng` (number, optional) — Longitude (must be given together with lat); `search` (string, optional) — Zip code or city to search near
