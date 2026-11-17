# indeed-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**3 endpoints across 1 platform group(s).**

## Indeed (3)

### `indeed_job`

- **HTTP:** `GET /indeed/job`
- **What:** Indeed job detail. Returns one Indeed job posting by its job key (the `job_key` field returned by search).
- **Params:** `jk` (string, **required**) — Indeed job key (16-character hex)

### `indeed_locations_suggest`

- **HTTP:** `GET /indeed/locations/suggest`
- **What:** Indeed location suggestions. Returns Indeed's own location-search autocomplete suggestions for a partial location string -- the same suggestions the app's search bar offers -- for building a valid `l` value for search.
- **Params:** `limit` (integer, optional) — Max suggestions to return, defaults to 10, maxes at 25; `q` (string, **required**) — Partial location text

### `indeed_search`

- **HTTP:** `GET /indeed/search`
- **What:** Indeed job search. Searches Indeed job postings by keyword and location. `sort` enum: `relevance` (default), `date`.
- **Params:** `fromage` (integer, optional) — Only jobs posted within this many days; `l` (string, optional) — Location (city, state, or zip); `page` (integer, optional) — Page number, 1-based, defaults to 1; `q` (string, **required**) — Search keywords; `radius` (integer, optional) — Search radius in miles; `sort` (string, optional) — Sort order: relevance, date
