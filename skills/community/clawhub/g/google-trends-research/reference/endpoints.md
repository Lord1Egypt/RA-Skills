# google-trends-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**11 endpoints across 1 platform group(s).**

## Google (11)

### `google_trends_categories`

- **HTTP:** `GET /google/trends/categories`
- **What:** Google Trends categories. Returns the top-level Google Trends categories as id and name pairs, such as 0 for All and 20 for Sports. These are the ids accepted by the Trending Now category filter.
- **Params:** _none_

### `google_trends_enums`

- **HTTP:** `GET /google/trends/enums`
- **What:** Google Trends enum metadata. Returns supported Google Trends enum values for explore/trending filters, including locations, date ranges, search types, categories, statuses, and sort modes.
- **Params:** _none_

### `google_trends_explore`

- **HTTP:** `POST /google/trends/explore`
- **What:** Google Trends explore data. Returns Google Trends keyword analytics: interest over time, interest by region, related queries, and related topics when available.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_trends_explore_interest_by_region`

- **HTTP:** `POST /google/trends/explore/interest-by-region`
- **What:** Google Trends interest by region. Returns only the interest-by-region widget from the Google Trends Explore widget flow. Supports multiple comparison terms and returns an empty interest_by_region array when Google returns no rows.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_trends_explore_interest_over_time`

- **HTTP:** `POST /google/trends/explore/interest-over-time`
- **What:** Google Trends interest over time. Returns Google Trends interest over time for 1 to 5 `keywords`. Optional inputs are `geo` (default worldwide), `time_range` (default `today 12-m`), `hl`, `tz`, `category` and `type` (`web`, `image`, `news`, `youtube` or `shopping`). Each time point carries a value per keyword, with a `has_data` flag.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_trends_explore_related_topics`

- **HTTP:** `POST /google/trends/explore/related-topics`
- **What:** Google Trends related topics. Returns only the related topics widget from the Google Trends Explore widget flow. Returns an empty related_topics array when Google returns no topic rows for the requested term/filter combination.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_trends_explore_rising_queries`

- **HTTP:** `POST /google/trends/explore/rising-queries`
- **What:** Google Trends explore rising queries. Returns the Rising related queries widget for one or more Google Trends explore terms. Returns an empty queries array when Google returns no rows for the requested term/filter combination.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_trends_explore_top_queries`

- **HTTP:** `POST /google/trends/explore/top-queries`
- **What:** Google Trends explore top queries. Returns the Top related queries widget for one or more Google Trends explore terms. Returns an empty queries array when Google returns no rows for the requested term/filter combination.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_trends_locations`

- **HTTP:** `GET /google/trends/locations`
- **What:** Google Trends locations. Returns the list of location codes that Google Trends supports, such as `US`, `HK` and `GB`, in `locations`. The Explore endpoints also accept `WORLDWIDE`, which appears in the list. It takes no parameters.
- **Params:** _none_

### `google_trends_trending`

- **HTTP:** `GET /google/trends/trending`
- **What:** Google Trends trending now data. Returns Google Trends Trending Now for a country or territory (`geo`, default `US`): each trend's query, rank, search traffic, status, start and update time, related terms and news articles, with explore and share links. Filter by time window, category and status, and choose the sort order.
- **Params:** `category` (integer, optional) — Trending category id; `geo` (string, optional) — Country/territory location code; `hl` (string, optional) — Google Trends UI locale; `limit` (integer, optional) — Maximum rows to return; `sort_by` (string, optional) — Sort mode; `status` (string, optional) — Trend status filter; `time_range` (string, optional) — Alias for window; `tz` (integer, optional) — Timezone offset minutes; `window` (string, optional) — Trend window

### `google_trends_trending_detail`

- **HTTP:** `POST /google/trends/trending/detail`
- **What:** Google Trends trending term detail. Returns the Explore detail widgets for a single trending term, including interest over time, regional interest, top/rising related queries, and related topics when Google returns them.
- **Params:** `request` (object, **required**) — Trending detail request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.
