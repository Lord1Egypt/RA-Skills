# google-maps-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**4 endpoints across 1 platform group(s).**

## Google (4)

### `google_map_place`

- **HTTP:** `GET /google/map/place/{place_id}`
- **What:** Google Maps place details API. Returns the Google Maps details of one place by its Google `place_id`: name, categories, address, coordinates, phone, website, description, image, amenities, rating and review count. `rating` is `null` when the place has no aggregate rating on Google.
- **Params:** `place_id` (string, **required**) — Google Place ID

### `google_map_place_photos`

- **HTTP:** `GET /google/map/place/{place_id}/photos`
- **What:** Google Maps place photos API. Returns the photos Google publishes for a specified place_id — the imagery shown on the place's Google Maps page, typically dozens of images for a well-covered business. Each entry carries the image URL as served plus its pixel dimensions when reported; swap the trailing size suffix on the URL (e.g. `=w203-h100-k-no`) to request other dimensions. Contributor avatars and review-attached photos are excluded. This is the place page's image set, not a paginated archive feed. Rate limit is enforced at 1 request per second.
- **Params:** `limit` (integer, optional) — Maximum number of photos to return. Omit or 0 for all captured.; `place_id` (string, **required**) — Google Place ID

### `google_map_place_reviews`

- **HTTP:** `GET /google/map/place/{place_id}/reviews`
- **What:** Google Maps place reviews API. Returns the reviews Google shows on a specified place_id's Google Maps page — typically the 8 most relevant, each with its rating, text, reviewer, timestamp, and any photos the reviewer attached. Photo-only reviews return an empty `text`. This is the place page's first page of reviews, not the full review archive. Rate limit is enforced at 1 request per second.
- **Params:** `limit` (integer, optional) — Maximum number of reviews to return. Omit or 0 for all captured.; `place_id` (string, **required**) — Google Place ID

### `google_map_search`

- **HTTP:** `POST /google/map/search`
- **What:** Google Maps search API. Searches Google Maps with a request body of `keyword` (required) plus optional `language` (default `en`) and `country` (an ISO-2 code such as `us`, default `us`). Each place has its name, place id, categories, address, coordinates, phone, website, rating and review count. `rating` is `null` when Google has no aggregate rating.
- **Params:** `mapSearchOption` (object, **required**) — Search options
- **REST body:** Send the value of the MCP argument `mapSearchOption` directly as the JSON body; do not wrap it in a `mapSearchOption` property.
