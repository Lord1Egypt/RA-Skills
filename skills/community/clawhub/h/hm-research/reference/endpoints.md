# hm-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**7 endpoints across 1 platform group(s).**

## H&M (7)

### `hm_categories`

- **HTTP:** `GET /hm/categories`
- **What:** Browse H&M's storefront category navigation. Returns H&M's own storefront category navigation, department by department: every direct nav item and subcategory currently shown in the site's own menu, with its display name and storefront URL. Where this build has separately verified the value against hm-listing's own category_id parameter, that id is included too; category_id is omitted for entries not yet verified rather than guessed, since the visible category label is confirmed NOT a reliable way to derive H&M's real listing category ids for every category. department, when given, filters the result to one department.
- **Params:** `department` (string, optional) — Filter to one storefront department

### `hm_listing`

- **HTTP:** `GET /hm/listing`
- **What:** Browse an H&M category's product listing. Returns one H&M category's product listing page: products with pricing, images, colors, and per-size stock. category_id is an H&M category slug (e.g. ladies_newarrivals_all, men_newarrivals_all, ladies_jeans) -- there is no category/nav-tree discovery endpoint, so category_id values come from known H&M storefront paths rather than a lookup call. Pagination is page-based and real: requesting a page beyond the category's real last page returns a normal response with an empty products array rather than an error.
- **Params:** `category_id` (string, **required**) — H&M category slug; `is_new` (boolean, optional) — Optional filter for newly added items only; `page` (integer, optional) — Page number, one-based, defaults to 1; `page_size` (integer, optional) — Results per page, 1 to 72, defaults to 36; `sort` (string, optional) — Sort order, defaults to RELEVANCE

### `hm_product`

- **HTTP:** `GET /hm/product/{product_id}`
- **What:** Get an H&M product's full detail. Returns one H&M product's full detail: every purchasable color grouped with its own per-size price and live availability, plus an aggregate rating and real customer reviews (author label, date, body, rating, and any fit-feedback tags the reviewer left, such as "True to Size") when the product has any. This data is not available from hm-listing or hm-search, which only carry one representative price and a per-color stock count. product_id is the numeric id from a listing/search result's id field or its url field's productpage.<id>.html segment. An unrecognized product_id returns 404.
- **Params:** `product_id` (string, **required**) — Numeric H&M product id, from a listing/search result's id field

### `hm_product_related`

- **HTTP:** `GET /hm/product/{product_id}/related`
- **What:** Get an H&M product's related items. Returns every product-detail recommendation list H&M's own app shows for one product (which lists are present genuinely varies by product -- for example "more from series" and "style with" appear only when the product has one, while "alternatives" and "upsell" are more consistently present). An unrecognized product_id returns a well-formed empty result rather than an error.
- **Params:** `product_id` (string, **required**) — Numeric H&M product id, from a listing/search result's id field

### `hm_search`

- **HTTP:** `GET /hm/search`
- **What:** Search H&M product listings by free-text keyword. Runs a free-text keyword search on H&M and returns products with pricing, images, colors, and per-size stock, plus search-quality metadata (a spelling-correction suggestion, related searches, and a content-filter flag). Unlike category browsing, an obscure or nonsense keyword returns a genuine empty result (zero products) rather than a fallback set. Pagination is page-based and real: requesting a page beyond the real last page returns a normal response with an empty products array rather than an error.
- **Params:** `page` (integer, optional) — Page number, one-based, defaults to 1; `page_size` (integer, optional) — Results per page, 1 to 72, defaults to 36; `query` (string, **required**) — Free-text search keyword

### `hm_search_suggestions`

- **HTTP:** `GET /hm/search/suggestions`
- **What:** Get H&M search-box suggestions. Returns H&M's own search-box typeahead suggestions. When query is given, returns spelling-complete phrase suggestions and merchandised content results. When query is omitted or empty, instead returns trending searches and popular-search shortcuts (phrase/content suggestions are both empty in that mode). search_history is not session-scoped -- it returns the identical list for every request, so treat it as fixed default content rather than a real per-caller history.
- **Params:** `query` (string, optional) — Free-text search-box input; omit or leave empty for trending/popular searches instead

### `hm_stores`

- **HTTP:** `GET /hm/stores`
- **What:** Find nearby H&M physical stores. Returns H&M physical retail store locations near a point: name, phone, full address, and coordinates. Either search, or both lat and lng, is required. search is a free-text zip code or place name that is first resolved to coordinates; if it does not resolve to any location, a well-formed empty result is returned rather than an error. lat and lng, when given directly, skip that resolution step. radius_meters is optional (1000 to 50000, defaults to 10000). A location with no stores within the radius returns a well-formed empty result rather than an error.
- **Params:** `lat` (number, optional) — Latitude, requires lng; `lng` (number, optional) — Longitude, requires lat; `radius_meters` (integer, optional) — Search radius in meters, 1000 to 50000, defaults to 10000; `search` (string, optional) — Free-text zip code or place name to resolve to coordinates
