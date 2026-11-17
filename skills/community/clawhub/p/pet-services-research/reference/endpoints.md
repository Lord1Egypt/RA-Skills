# pet-services-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**4 endpoints across 1 platform group(s).**

## Rover (4)

### `rover_sitter_profile`

- **HTTP:** `GET /rover/sitter/{slug}`
- **What:** Get Rover sitter profile. Returns a Rover sitter/walker profile: name, photo, bio, star rating, review count, repeat-client count, years of experience, neighborhood/city/state, starting price, Star Sitter status, the services offered with per-service pricing, and public review excerpts from the sitter's own profile page.
- **Params:** `slug` (string, **required**) — Rover sitter profile slug, the trailing path segment of a search result's profile_url field

### `rover_sitter_search`

- **HTTP:** `GET /rover/search`
- **What:** Search Rover sitters and walkers. Searches Rover's public sitter/walker listings by location and service type, returning sitter summaries (name, profile image, rating, review count, repeat-client count, years of experience, neighborhood/city/state, starting price, Star Sitter status, and a short bio).
- **Params:** `location` (string, **required**) — Free-text address, city, or zip code, e.g. \; `max_price` (integer, optional) — Maximum starting rate in whole dollars.; `min_price` (integer, optional) — Minimum starting rate in whole dollars.; `page` (integer, optional) — 1-based result page. Defaults to 1.; `pet_type` (string, optional) — Filter by pet species. One of: `dog`, `cat`.; `service_type` (string, **required**) — Service category to search. One of: `overnight-boarding`, `overnight-traveling`, `drop-in`, `doggy-day-care`, `dog-walking`.; `star_sitter_only` (boolean, optional) — Restrict results to Rover's \

### `rover_trainer_profile`

- **HTTP:** `GET /rover/trainer/{slug}`
- **What:** Get Rover dog trainer profile. Returns a Rover dog trainer profile: name, photo, headline, experience and availability details, training methodology, rating, review count, repeat-client count, years of training, skill/behavior tags, and education credentials.
- **Params:** `slug` (string, **required**) — Rover trainer profile slug, the trailing path segment of a trainer search result's profile_url field

### `rover_trainer_search`

- **HTTP:** `GET /rover/trainer-search`
- **What:** Search Rover dog trainers. Searches Rover's public dog trainer listings by location, returning trainer summaries (name, profile image, headline, experience details, rating, review count, repeat-client count, years of experience, city/state/zip, starting price, training methodology, and skill/behavior tags).
- **Params:** `location` (string, **required**) — Free-text address, city, or zip code, e.g. \
