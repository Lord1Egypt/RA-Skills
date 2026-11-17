# nike-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**9 endpoints across 1 platform group(s).**

## Nike (9)

### `nike_categories`

- **HTTP:** `GET /nike/categories`
- **What:** List Nike's category and subcategory taxonomy. Returns Nike's full Men/Women/Kids/Jordan category and subcategory taxonomy tree, sourced directly from Nike.com's own nav mega-menu. Each top-level entry (Men, Women, Kids, Jordan) breaks down into named groups (e.g. Shoes, Clothing, Accessories, Shop By Sport -- Women additionally carries a Shop by Color group, and Jordan is organized by Men/Women/Kids instead of by product type), each with its own subcategory entries. Every subcategory (and most groups) carries a slug usable as a future category-browse endpoint's path/slug input, and is directly browsable today at https://www.nike.com/w/<slug>. This mirrors the live nav exactly, including its seasonal/promotional groups (e.g. Limited Time, New & Featured) alongside the stable structural ones -- Nike's own markup does not distinguish the two.
- **Params:** _none_

### `nike_product`

- **HTTP:** `GET /nike/product`
- **What:** Get a Nike product. Returns product-detail data for one color variant: title, description, pricing, images, every offered size, and every other available color. slug and style_color together reproduce Nike's own product page URL (nike.com/t/<slug>/<style_color>) and are both returned by nike-search's product colors[].slug and colors[].style_color fields.
- **Params:** `slug` (string, **required**) — Product-detail URL slug, from a search result's colors[].slug field; `style_color` (string, **required**) — Style-color id, from a search result's colors[].style_color field

### `nike_product_availability`

- **HTTP:** `GET /nike/product/availability`
- **What:** Get Nike product size availability. Returns per-size shipping availability for one product, sourced from the same anonymous mobile backend Nike's own app uses. group_key is the product's rollup key (from a search result's products[].group_key field). Each size carries its label, localized label, the color variant it belongs to, a GTIN, an available flag, Nike's own shipping-availability level (HIGH/LOW/MEDIUM/OOS), and the width grouping (Regular/Wide). Per-store pickup availability is not included -- this reflects online shipping availability.
- **Params:** `group_key` (string, **required**) — Product rollup key, from a search result's products[].group_key field

### `nike_product_details`

- **HTTP:** `GET /nike/product/details`
- **What:** Get full Nike product details. Returns full product-group detail for one product's rollup key, sourced from the same anonymous mobile backend Nike's own app uses: shared product copy plus every purchasable color variant (across width groupings), each with its own pricing, sizes, and images. group_key is the product's rollup key, the same value nike-search returns as a products[].group_key field. Unlike nike-product (which returns one color variant by slug/style_color), this returns every color of the product in one response.
- **Params:** `group_key` (string, **required**) — Product rollup key, from a search result's products[].group_key field

### `nike_product_recommendations`

- **HTTP:** `GET /nike/product/recommendations`
- **What:** Get Nike product recommendations. Returns Nike's own related-product ("Shop Similar") recommendations for one product, sourced from the same anonymous mobile backend Nike's own app uses. style_color is the anchor product's style-color id (from a search result's colors[].style_color field). Each recommendation carries the product's style-color, rank, title/subtitle, image, PDP URL, and current pricing. Recommendations are Nike's own ranking, not a guaranteed keyword match: an unrecognized style_color returns Nike's fallback recommendations rather than an empty list or an error.
- **Params:** `style_color` (string, **required**) — Anchor product's style-color id, from a search result's colors[].style_color field

### `nike_product_reviews`

- **HTTP:** `GET /nike/product/reviews`
- **What:** Get Nike product reviews. Returns one page of a Nike product's customer reviews, plus an aggregate rating summary (average rating and a per-star rating breakdown) that Nike's own product-detail endpoint does not otherwise expose. slug and style_color are the same values nike-product accepts (from a search result's colors[].slug/colors[].style_color fields). A product with no reviews yet returns a well-formed empty result rather than an error. Requesting a page beyond the available result pages returns a not-found error.
- **Params:** `page` (integer, optional) — One-based page number, defaults to 1; `slug` (string, **required**) — Product-detail URL slug, from a search result's colors[].slug field; `style_color` (string, **required**) — Style-color id, from a search result's colors[].style_color field

### `nike_search`

- **HTTP:** `GET /nike/search`
- **What:** Search or browse Nike products. Searches Nike.com product listings by keyword, or browses a category/subcategory listing by slug, with real pagination. Exactly one of keyword or category is required. Returns product groups with pricing, colorway images, and every purchasable color variant, plus filter and subcategory navigation data (facet_nav) already present on the same response -- both keyword search and a category listing's first page include filter groups (Gender, Color, Price, Size, and similar); only a category listing includes a breadcrumb trail and subcategory drill-down options, and only its first page (a category listing's later pages do not repeat navigation data). Keyword search is best-effort relevance, not a guaranteed keyword match: for an obscure or nonsense keyword, Nike's own search index falls back to its own recommended results instead of returning an empty list, and there is currently no reliable signal in the response to distinguish a true keyword match from that fallback behavior. A keyword Nike's own search router treats as structurally empty (for example a punctuation-only query) does return a genuine empty result. Category values come from nike-categories' own slug field, or from a prior response's own facet_nav navigation paths (with the leading /w/ stripped). Requesting a page beyond the available result pages returns a not-found error.
- **Params:** `category` (string, optional) — Category/subcategory browse slug, from nike-categories' own slug field or a prior response's facet_nav navigation. Exactly one of keyword or category is required.; `keyword` (string, optional) — Search keyword. Exactly one of keyword or category is required.; `page` (integer, optional) — One-based page number, defaults to 1

### `nike_stores`

- **HTTP:** `GET /nike/stores`
- **What:** Find nearby Nike stores. Searches Nike's physical retail store locator by coordinates and radius. Returns each nearby store's name, address, phone, coordinates, distance, and store page URL. A location with no nearby stores within the given radius returns a well-formed empty result.
- **Params:** `lat` (number, **required**) — Latitude, -90 to 90; `lng` (number, **required**) — Longitude, -180 to 180; `page` (integer, optional) — One-based page number, defaults to 1; `radius_miles` (integer, optional) — Search radius in miles, defaults to 50

### `nike_suggest`

- **HTTP:** `GET /nike/suggest`
- **What:** Get Nike search-box suggestions. Returns Nike's own search-box suggestions (typeahead) for a partial query, the same "Top Suggestions" list shown while typing into Nike's search box: a flat list of suggested search phrases, no product data.
- **Params:** `query` (string, **required**) — Partial search query
