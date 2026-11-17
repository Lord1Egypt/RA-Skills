# google-jobs-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**2 endpoints across 1 platform group(s).**

## Google Jobs (2)

### `google_jobs_job`

- **HTTP:** `GET /google-jobs/job`
- **What:** Google Jobs single posting. Returns one Google Careers posting by its numeric job id (the `id` field returned by search).
- **Params:** `id` (string, **required**) — Numeric Google job id

### `google_jobs_search`

- **HTTP:** `GET /google-jobs/search`
- **What:** Google Jobs search. Searches Google's public careers site (careers.google.com) via its server-rendered search page's embedded job data. Each result includes the description, responsibilities, and qualifications inline. Page size is fixed by Google at 20 results.
- **Params:** `location` (string, optional) — Location filter (free text); `page` (integer, optional) — Page number, 1-based; `q` (string, **required**) — Search query
