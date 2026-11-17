# microsoft-store-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**14 endpoints across 1 platform group(s).**

## Microsoft Store (14)

### `microsoftstore_categories`

- **HTTP:** `GET /microsoftstore/categories`
- **What:** Get the full Microsoft Store category (and subcategory) taxonomy for a department. Returns every accepted category for a department, and -- apps only -- each category's own finer subcategories (e.g. Books & reference -> E-reader, Fiction, Nonfiction, Reference). This is the discovery endpoint for the category/subcategory values accepted by /microsoftstore/search, /microsoftstore/category, and /microsoftstore/charts. Subcategories are apps-only: games categories have none.
- **Params:** `media_type` (string, optional) — Department to list categories for

### `microsoftstore_category`

- **HTTP:** `GET /microsoftstore/category`
- **What:** Browse a Microsoft Store category without a keyword. Returns a page of a single department+category listing, cursor-paginated, with no search keyword required -- the way to list an entire category (search requires a non-empty query and returns nothing for an empty one). category is required; the accepted set depends on media_type (see /microsoftstore/search's markdown doc for the full per-department lists). media_type defaults to apps; all is not accepted here since it has no category filter.
- **Params:** `category` (string, **required**) — Category to browse; `country` (string, optional) — Store country/region code (ISO-2); `cursor` (string, optional) — Opaque pagination cursor from a previous response's next_cursor; `locale` (string, optional) — Display locale (BCP-47); `media_type` (string, optional) — Department to browse

### `microsoftstore_charts`

- **HTTP:** `GET /microsoftstore/charts`
- **What:** Get a curated Microsoft Store chart. Returns a curated Microsoft Store chart (top free, top paid, top grossing, trending, deals, new releases, getting-started picks, or -- apps only -- most popular), optionally scoped to a category/subcategory and, for games, by Xbox Game Pass availability or player count. Some charts (notably NewAndRising) can legitimately return fewer items than page_size even at the first page -- that reflects real sparsity for that chart.
- **Params:** `category` (string, optional) — Optional category to scope the chart to further; `country` (string, optional) — Store country/region code (ISO-2); `discount_filter` (string, optional) — Optional discount filter; `list` (string, **required**) — Chart to fetch; `locale` (string, optional) — Display locale (BCP-47); `media_type` (string, optional) — Department to scope the chart to; `num_players_filter` (string, optional) — Optional player-count filter (games only); `page` (integer, optional) — 1-based page number; `page_size` (integer, optional) — Items per page (max 24); `subcategory` (string, optional) — Optional finer subcategory within category (apps only; requires category to also be set); `subscription_filter` (string, optional) — Optional subscription filter (games only)

### `microsoftstore_editorial`

- **HTTP:** `GET /microsoftstore/editorial`
- **What:** Get a Microsoft Store editorial article by id. Returns a Microsoft Store editorial article (currently only seen in the wild as a per-product Microsoft Store Awards writeup). There is no discovery endpoint for editorial ids: they are only found embedded in a product's own award.editorial_id field, returned by /microsoftstore/search, /microsoftstore/category, /microsoftstore/charts, /microsoftstore/publisher, and /microsoftstore/related when that product carries an award. An unknown/invalid id returns a 503 upstream error, not a clean 404 -- the upstream itself does not distinguish the two.
- **Params:** `country` (string, optional) — Store country/region code (ISO-2); `editorial_id` (string, **required**) — Editorial content id, from a product's award.editorial_id field; `locale` (string, optional) — Display locale (BCP-47)

### `microsoftstore_events`

- **HTTP:** `GET /microsoftstore/events`
- **What:** Get a Microsoft Store department's special-events shelf. Returns a department's "Special events" promotional shelf -- featured/limited-time products, distinct from the ranked charts (/microsoftstore/charts) and the curated home/department spotlight (/microsoftstore/spotlight). Only apps and games have this shelf; any other media_type is rejected.
- **Params:** `country` (string, optional) — Store country/region code (ISO-2); `locale` (string, optional) — Display locale (BCP-47); `media_type` (string, optional) — Department to fetch special events for; `page` (integer, optional) — 1-based page number; `page_size` (integer, optional) — Items per page (max 24)

### `microsoftstore_product`

- **HTTP:** `GET /microsoftstore/product`
- **What:** Get Microsoft Store details for a single product. Returns Microsoft Store listing details for a single product id: title, description, publisher, category, media type, aggregate rating and content-rating breakdown, price and SKU summary, size, supported platforms/languages, capabilities, version/release/update timestamps, feature callouts, and media (icon, poster art, screenshots, trailers).
- **Params:** `country` (string, optional) — Store country/region code (ISO-2); `locale` (string, optional) — Display locale (BCP-47); `product_id` (string, **required**) — Microsoft Store product id

### `microsoftstore_publisher`

- **HTTP:** `GET /microsoftstore/publisher`
- **What:** List a Microsoft Store publisher's full catalog. Returns every product a publisher/developer has listed on the Microsoft Store, cursor-paginated. publisher_name must match the publisher name exactly as shown on a listing (e.g. the publisher field returned by /microsoftstore/product or /microsoftstore/search).
- **Params:** `country` (string, optional) — Store country/region code (ISO-2); `cursor` (string, optional) — Opaque pagination cursor from a previous response's next_cursor; `locale` (string, optional) — Display locale (BCP-47); `publisher_name` (string, **required**) — Exact publisher/developer name

### `microsoftstore_recommended`

- **HTTP:** `GET /microsoftstore/recommended`
- **What:** Get the Microsoft Store's default recommendation shelf. Returns the store's default, query-less "Recommended for you" shelf -- the same recommendations the search box shows before a caller types anything. No query parameters beyond region/locale.
- **Params:** `country` (string, optional) — Store country/region code (ISO-2); `locale` (string, optional) — Display locale (BCP-47)

### `microsoftstore_related`

- **HTTP:** `GET /microsoftstore/related`
- **What:** Get products related to a Microsoft Store product. Returns products related to a seed product id, paginated. product_type must match the seed product's own media type (apps -> Application, games -> Game, passes -> Passes) -- any other value is rejected upstream. Omit product_type to have it resolved automatically from product_id via one extra lightweight lookup; pass it explicitly to skip that lookup.
- **Params:** `country` (string, optional) — Store country/region code (ISO-2); `locale` (string, optional) — Display locale (BCP-47); `page` (integer, optional) — 1-based page number; `page_size` (integer, optional) — Related products per page (max 24); `product_id` (string, **required**) — Seed Microsoft Store product id; `product_type` (string, optional) — The seed product's own type. Omit to auto-resolve from product_id.

### `microsoftstore_reviews`

- **HTTP:** `GET /microsoftstore/reviews`
- **What:** Get paginated Microsoft Store reviews for a product. Returns one page of written Microsoft Store reviews for a product id, each with rating, title, text, submission time, helpful-vote counts, and device/OS info. sort controls ordering (MostHelpful or MostRecent -- the only two values the upstream API itself accepts; any other value is rejected).
- **Params:** `country` (string, optional) — Store country/region code (ISO-2); `locale` (string, optional) — Display locale (BCP-47); `page` (integer, optional) — 1-based page number; `page_size` (integer, optional) — Reviews per page (max 50); `product_id` (string, **required**) — Microsoft Store product id; `sort` (string, optional) — Review sort order

### `microsoftstore_reviews_summary`

- **HTTP:** `GET /microsoftstore/reviews/summary`
- **What:** Get a Microsoft Store product's aggregate rating summary. Returns a product's aggregate rating: average rating, total review count, a 1-5 star rating distribution, and the upstream-selected most critical and most favorable written reviews.
- **Params:** `country` (string, optional) — Store country/region code (ISO-2); `locale` (string, optional) — Display locale (BCP-47); `product_id` (string, **required**) — Microsoft Store product id

### `microsoftstore_search`

- **HTTP:** `GET /microsoftstore/search`
- **What:** Search the Microsoft Store. Returns a page of Microsoft Store search results (apps, games, devices, and other listings) for a keyword, with cursor-based pagination and per-item publisher, rating, price, and media. media_type selects the department (apps, games, devices, passes, fonts, themes, tencent-android, tencent-mini, or all); category further filters within that department (the accepted set depends on media_type -- see the markdown doc for the full per-department lists). Pass the previous response's next_cursor to fetch the next page.
- **Params:** `age` (string, optional) — Maximum-age filter; `category` (string, optional) — Category to filter by (accepted set depends on media_type); `country` (string, optional) — Store country/region code (ISO-2); `cursor` (string, optional) — Opaque pagination cursor from a previous response's next_cursor; `locale` (string, optional) — Display locale (BCP-47); `media_type` (string, optional) — Department to search; `price` (string, optional) — Price filter; `query` (string, **required**) — Search keyword

### `microsoftstore_spotlight`

- **HTTP:** `GET /microsoftstore/spotlight`
- **What:** Get the Microsoft Store home page or department spotlight. Returns the curated hero/spotlight shelf shown at the top of the store's home page or one department's landing page (the large featured banners, not the ranked charts or the smaller "Special events" shelf). Only home, apps, and games have a spotlight; any other media_type is rejected.
- **Params:** `country` (string, optional) — Store country/region code (ISO-2); `locale` (string, optional) — Display locale (BCP-47); `media_type` (string, optional) — Which spotlight to fetch

### `microsoftstore_suggest`

- **HTTP:** `GET /microsoftstore/suggest`
- **What:** Get Microsoft Store search suggestions for a prefix. Returns typeahead-style Microsoft Store search suggestions for a partial search term: plain-text completions plus a short list of matching products (id, title, icon, department, and store URL).
- **Params:** `country` (string, optional) — Store country/region code (ISO-2); `locale` (string, optional) — Display locale (BCP-47); `prefix` (string, **required**) — Partial search term to autocomplete
