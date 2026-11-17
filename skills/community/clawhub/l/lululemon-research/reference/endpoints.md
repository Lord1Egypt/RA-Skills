# lululemon-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**5 endpoints across 1 platform group(s).**

## Lululemon (5)

### `lululemon_categories`

- **HTTP:** `GET /lululemon/categories`
- **What:** Browse lululemon's storefront category navigation. Returns lululemon's own storefront category navigation, flattened out of the site's shared header nav: every navigable category with its display name, breadcrumb path, and the exact category/cdp_hash pair lululemon-category's own parameters expect (read directly from the nav's own URL, not guessed from the display label). section, when given, filters the result to one top-level nav section.
- **Params:** `section` (string, optional) — Filter to one top-level storefront nav section

### `lululemon_category`

- **HTTP:** `GET /lululemon/category`
- **What:** Browse a lululemon category's product listing. Returns one lululemon category's product listing page: products with pricing, sale detection, sizes, colors, and style numbers. category and cdp_hash are the two path segments of a lululemon category URL (https://shop.lululemon.com/c/{category}/{cdp_hash}), e.g. women-new-styles and n14f1wz6o10 -- both are also available from lululemon-categories's own category and cdp_hash fields. Pagination is page-based and real: requesting a page beyond the category's real last page returns a normal response with an empty products array rather than an error. An unrecognized category/cdp_hash pair returns 404.
- **Params:** `category` (string, **required**) — lululemon category slug, from a category URL's first path segment; `cdp_hash` (string, **required**) — lululemon category id, from a category URL's second path segment; `page` (integer, optional) — Page number, one-based, defaults to 1; `page_size` (integer, optional) — Results per page, 1 to 100, defaults to 24

### `lululemon_outfit`

- **HTTP:** `GET /lululemon/outfit`
- **What:** Get lululemon's outfit/style recommendations for a product color. Returns lululemon's own curated outfit/style recommendations for one product color: every complementary item in each styled look, plus the anchor product itself. unified_id and color_code are lululemon-product's own unified_id response field and a color's code field (from lululemon-product's colors[] or lululemon-category's style_numbers-paired colors[]) -- not lululemon-product's own product_id, which is a different id space. Recommended items' own id is a separate, third-party catalog id (not lululemon-product's product_id) -- use each item's url to reach its product page. An unrecognized unified_id/color_code pair returns 404.
- **Params:** `color_code` (string, **required**) — lululemon color code, from a lululemon-product result's colors[].code field; `unified_id` (string, **required**) — lululemon product unified id, from a lululemon-product result's unified_id field

### `lululemon_product`

- **HTTP:** `GET /lululemon/product/{product_id}`
- **What:** Get a lululemon product's full detail. Returns one lululemon product's full detail: every purchasable color/size SKU with its own price, sale status, and live availability, plus an aggregate rating and real customer reviews when the product has any -- none of which lululemon-category exposes (it only carries one representative color/price per product). product_id is the id from a lululemon-category result's id field or a lululemon product URL's trailing path segment (https://shop.lululemon.com/p/{slug}/{product_id}) -- the slug itself is not needed. An unrecognized product_id returns 404.
- **Params:** `product_id` (string, **required**) — lululemon product id, from a lululemon-category result's id field

### `lululemon_stores`

- **HTTP:** `GET /lululemon/stores`
- **What:** Browse lululemon's physical store directory. Returns lululemon's own complete physical store directory (480 US and 86 Canada locations), including regular weekly hours and in-store amenities. All filters are optional and applied to the full directory. country and state are free-text equality filters against the values this directory actually carries (2-letter codes, e.g. US/CA, NY/CA), not an enforced enum. lat and lng (both required together) filter to stores within radius_miles (1 to 500, defaults to 50), sorted nearest-first.
- **Params:** `country` (string, optional) — Filter to one country by its 2-letter code; `lat` (number, optional) — Latitude, requires lng; `lng` (number, optional) — Longitude, requires lat; `radius_miles` (number, optional) — Search radius in miles, 1 to 500, defaults to 50; `state` (string, optional) — Filter to one state/province by its 2-letter code
