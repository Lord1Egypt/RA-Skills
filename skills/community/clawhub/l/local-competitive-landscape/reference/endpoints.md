# local-competitive-landscape — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**10 endpoints across 4 platform group(s).**

## Datasets (3)

### `datasets_google_map_facets`

- **HTTP:** `GET /datasets/google-map-businesses/facets`
- **What:** Facet stored Google Maps businesses. Returns terms aggregation counts for Google Maps businesses. Facet enum: `category`, `country`, `state`, `state_code`, `county`, `county_code`, `city`, `town`, `website_status`. Category facet values are exact locale-specific Google Maps labels and can be localized, non-ASCII, or contain punctuation; pass a returned value unchanged to the category filter. `state` and `county` keep each country's own administrative vocabulary (e.g. `Provincia de Madrid`, `Département du Nord`); `state_code` and `county_code` are ISO 3166-2 codes populated today only for Canadian provinces and territories (e.g. `CA-ON`) and Irish counties (e.g. `IE-D`); every other record, including all US rows, carries no code and is absent from the code facets.
- **Params:** `category` (string, optional) — Exact locale-specific Google Maps category label; use the category facet to discover values, max 128 characters; `city` (string, optional) — Exact city filter, max 128 characters; `country` (string, optional) — Country filter. Accepts the full English name (\; `county` (string, optional) — Exact county filter, max 128 characters; `county_code` (string, optional) — Exact ISO 3166-2 county/district code filter, e.g. IE-D, max 128 characters. Only Irish counties carry a code today; filter other countries by county or city. Use facet=county_code to list values; `facet` (string, **required**) — Facet enum: category, country, state, state_code, county, county_code, city, town, website_status; `has_geo` (boolean, optional) — Filter by location presence: true keeps only mappable businesses with coordinates; false isolates locationless service-area businesses that have no map location; `has_phone` (boolean, optional) — Filter by phone presence; `has_website` (boolean, optional) — Filter by website presence; `lat` (number, optional) — Latitude for radius filtering; `lon` (number, optional) — Longitude for radius filtering; `min_rating` (number, optional) — Minimum rating, 0 through 5. Businesses with no aggregate Google rating are returned with rating null, so any min_rating above 0 excludes them.; `min_review_count` (integer, optional) — Minimum review count; `permanently_closed` (boolean, optional) — Closure filter. true keeps only businesses Google marks Permanently closed; false excludes them, keeping every business not known to be closed. Most rows have never been status-checked and are returned with permanently_closed null, which means unknown, not open.; `q` (string, optional) — Full-text business search query, max 256 characters; every term must match the name, address, headline or category (filler words such as in, near and the are ignored); `radius_m` (integer, optional) — Radius in meters, 1 through 50000; requires lat and lon when supplied; `sort` (string, optional) — Sort enum: relevance, updated_at_desc, rating_desc, review_count_desc, distance_asc; `state` (string, optional) — Exact state filter, max 128 characters; `state_code` (string, optional) — Exact ISO 3166-2 state/region code filter, e.g. CA-ON, max 128 characters. Only Canadian provinces and territories carry a code today, so US codes such as US-NV return no rows; filter other countries by state, county or city. Use facet=state_code to list values; `town` (string, optional) — Exact town filter, max 128 characters

### `datasets_google_map_item`

- **HTTP:** `GET /datasets/google-map-businesses/items/{place_id}`
- **What:** Get a stored Google Maps business. Returns one stored Google Maps business by Google place_id from dataset id enum value `google-map-businesses`. The `category` field contains the exact Google Maps category label returned for the business locale and can be localized, non-ASCII, or contain punctuation. A `rating` of `null` means no aggregate rating is available. A `review_count` of `null` means Google did not return a count; numeric `0` means Google confirmed zero reviews. Locationless service-area businesses (online/mobile/home-based) have a `null` `geo`. A `permanently_closed` of `true` means Google marks the business permanently closed; `false` means a crawl confirmed it does not; `null` means the business has not been status-checked since capture shipped on 2026-08-31 and is UNKNOWN, not open — so any total computed from this dataset includes an unknown number of closed businesses.
- **Params:** `place_id` (string, **required**) — Google Place ID, max 256 characters

### `datasets_google_map_search`

- **HTTP:** `GET /datasets/google-map-businesses/search`
- **What:** Search stored Google Maps businesses. Searches Google Maps business records stored in a search index. Sort enum: `relevance`, `updated_at_desc`, `rating_desc`, `review_count_desc`, `distance_asc`. `category` is the exact Google Maps category label returned for the business locale; it can be localized, non-ASCII, or contain punctuation, so use the category facet to discover exact filter values. A `rating` of `null` means no aggregate rating is available. A `review_count` of `null` means Google did not return a count; numeric `0` means Google confirmed zero reviews. `rating_desc` sorts unrated businesses last, and `min_rating` above 0 excludes them. Use `has_geo=false` to isolate locationless service-area businesses (which have a `null` `geo`). A `permanently_closed` of `true` means Google marks the business permanently closed; `false` means a crawl confirmed it does not; `null` means the business has not been status-checked since capture shipped on 2026-08-31 and is UNKNOWN, not open — so any total computed from this dataset includes an unknown number of closed businesses. Use `permanently_closed=false` to exclude the confirmed-closed ones. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `category` (string, optional) — Exact locale-specific Google Maps category label; use the category facet to discover values, max 128 characters; `city` (string, optional) — Exact city filter, max 128 characters; `country` (string, optional) — Country filter. Accepts the full English name (\; `county` (string, optional) — Exact county filter, max 128 characters; `county_code` (string, optional) — Exact ISO 3166-2 county/district code filter, e.g. IE-D, max 128 characters. Only Irish counties carry a code today; filter other countries by county or city. Use facet=county_code to list values; `has_geo` (boolean, optional) — Filter by location presence: true keeps only mappable businesses with coordinates; false isolates locationless service-area businesses that have no map location; `has_phone` (boolean, optional) — Filter by phone presence; `has_website` (boolean, optional) — Filter by website presence; `lat` (number, optional) — Latitude for radius filtering or distance sort; `lon` (number, optional) — Longitude for radius filtering or distance sort; `min_rating` (number, optional) — Minimum rating, 0 through 5. Businesses with no aggregate Google rating are returned with rating null, so any min_rating above 0 excludes them.; `min_review_count` (integer, optional) — Minimum review count; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `permanently_closed` (boolean, optional) — Closure filter. true keeps only businesses Google marks Permanently closed; false excludes them, keeping every business not known to be closed. Most rows have never been status-checked and are returned with permanently_closed null, which means unknown, not open.; `q` (string, optional) — Full-text business search query, max 256 characters; every term must match the name, address, headline or category (filler words such as in, near and the are ignored); `radius_m` (integer, optional) — Radius in meters, 1 through 50000; requires lat and lon when supplied; `sort` (string, optional) — Sort enum: relevance, updated_at_desc, rating_desc, review_count_desc, distance_asc; `state` (string, optional) — Exact state filter, max 128 characters; `state_code` (string, optional) — Exact ISO 3166-2 state/region code filter, e.g. CA-ON, max 128 characters. Only Canadian provinces and territories carry a code today, so US codes such as US-NV return no rows; filter other countries by state, county or city. Use facet=state_code to list values; `town` (string, optional) — Exact town filter, max 128 characters

## Google (3)

### `google_map_place`

- **HTTP:** `GET /google/map/place/{place_id}`
- **What:** Google Maps place details API. Returns the Google Maps details of one place by its Google `place_id`: name, categories, address, coordinates, phone, website, description, image, amenities, rating and review count. `rating` is `null` when the place has no aggregate rating on Google.
- **Params:** `place_id` (string, **required**) — Google Place ID

### `google_map_place_reviews`

- **HTTP:** `GET /google/map/place/{place_id}/reviews`
- **What:** Google Maps place reviews API. Returns the reviews Google shows on a specified place_id's Google Maps page — typically the 8 most relevant, each with its rating, text, reviewer, timestamp, and any photos the reviewer attached. Photo-only reviews return an empty `text`. This is the place page's first page of reviews, not the full review archive. Rate limit is enforced at 1 request per second.
- **Params:** `limit` (integer, optional) — Maximum number of reviews to return. Omit or 0 for all captured.; `place_id` (string, **required**) — Google Place ID

### `google_map_search`

- **HTTP:** `POST /google/map/search`
- **What:** Google Maps search API. Searches Google Maps with a request body of `keyword` (required) plus optional `language` (default `en`) and `country` (an ISO-2 code such as `us`, default `us`). Each place has its name, place id, categories, address, coordinates, phone, website, rating and review count. `rating` is `null` when Google has no aggregate rating.
- **Params:** `mapSearchOption` (object, **required**) — Search options
- **REST body:** Send the value of the MCP argument `mapSearchOption` directly as the JSON body; do not wrap it in a `mapSearchOption` property.

## Apple Maps (2)

### `apple_maps_place`

- **HTTP:** `GET /apple-maps/place`
- **What:** Get one Apple Maps place's full detail. Returns one Apple Maps place by its place ID: name, type, category taxonomy, coordinates, formatted and structured address, phone numbers, website, rating and review count, price level, weekly opening hours, amenities (payment, accessibility, parking, and similar yes/no attributes), photos, review snippets (text, rating, time, and source link, without reviewer identity), the business-claim link, and the IDs of Apple Guides that include the place. Accepts either the external place ID (starts with I, the place-id= value in a maps.apple.com/place URL) or the numeric ID from a search result.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code selecting Apple's regional catalog. Defaults to US.; `lang` (string, optional) — Display language as a BCP 47 tag, e.g. en-US, ja-JP, de-DE. Defaults to en-US.; `place_id` (string, **required**) — Apple place ID: external form (I594FECA0B369D14A) or numeric id from a search result

### `apple_maps_search`

- **HTTP:** `GET /apple-maps/search`
- **What:** Search Apple Maps places near a coordinate. Returns Apple Maps places matching a keyword, business name, category, or street address near a coordinate. Each place carries its Apple place ID (the value the place endpoint takes), name, category, coordinates, formatted and structured address, phone, website, rating and review count, price level, weekly opening hours, and a hero photo. Apple returns a bounded set per viewport (around 25 places for the default span) with no pagination; widen the span or move the center to cover more area. When nothing matches near the center Apple may relocate the search to a default region, reported by relocated=true and the region bounds. The response's filters block lists the refinement chips Apple offers for this query and area (open now, top rated, in guides, cuisines, price bands, amenities, accolades, sort); pass their keys back as filters and sort to refine the same search.
- **Params:** `country` (string, optional) — Two-letter ISO 3166-1 country code selecting Apple's regional catalog. Defaults to US.; `filters` (string, optional) — Comma-separated filter keys from the filters block of an unfiltered search for the same query and area, e.g. OPEN_NOW, TOP_RATED, FEATURED_IN_GUIDES, PRICE_RANGE_MODERATE, modern_pizza_restaurant, ACCEPTS_CREDIT_CARDS. Unknown keys return 400 listing the available keys. Costs a second upstream search.; `lang` (string, optional) — Display language as a BCP 47 tag, e.g. en-US, ja-JP, de-DE. Defaults to en-US.; `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Max places returned. Defaults to 25, maximum 100.; `longitude` (number, **required**) — Search center longitude; `query` (string, **required**) — Keyword, business name, category, or street address to search for; `sort` (string, optional) — Result order. Costs a second upstream search.; `span` (number, optional) — Search viewport size in degrees of latitude/longitude around the center. Defaults to 0.05 (roughly a 5km box); minimum 0.001, maximum 5.

## Yelp (2)

### `yelp_business`

- **HTTP:** `GET /yelp/business/{id}`
- **What:** Get Yelp business detail. Looks up a single Yelp business by alias or encoded id.
- **Params:** `id` (string, **required**) — Yelp business alias or encoded id

### `yelp_search`

- **HTTP:** `GET /yelp/search`
- **What:** Search Yelp businesses. Searches Yelp businesses for a term and location.
- **Params:** `limit` (integer, optional) — Max results to return, 1-50; `location` (string, **required**) — Neighborhood, city, state, or zip code; `offset` (integer, optional) — Pagination offset; `term` (string, **required**) — Search term
