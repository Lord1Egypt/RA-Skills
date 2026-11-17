# meta-jobs-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**3 endpoints across 1 platform group(s).**

## Meta Jobs (3)

### `meta_jobs_job`

- **HTTP:** `GET /meta-jobs/job`
- **What:** Meta Jobs single posting. Returns one Meta Careers posting by its numeric job id (the `id` field returned by search or list).
- **Params:** `id` (string, **required**) — Meta job id

### `meta_jobs_list`

- **HTTP:** `GET /meta-jobs/list`
- **What:** Meta Jobs catalog listing. Returns a page of Meta's own public job sitemap -- every open requisition's id, canonical URL, and last-modified timestamp, with no team/location/keyword filtering. Use this for full-catalog enumeration or change tracking via last_modified; use search when you need to filter by team, technology, location, employment type, or keyword.
- **Params:** `page` (integer, optional) — Page number, 1-based, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 50, maxes at 200

### `meta_jobs_search`

- **HTTP:** `GET /meta-jobs/search`
- **What:** Meta Jobs search. Searches Meta's public careers site (metacareers.com) with the same team/technology/location/employment-type/keyword/remote/sort filters the live search page offers. All filters are optional and combine with AND semantics; an empty request returns Meta's entire open-requisition catalog in one response. `q` matches team, technology, location, or ref/req-code names -- it is NOT a free-text search over job titles or descriptions. `teams` enum (org teams + technologies, both use the same field): `Advertising Technology`, `AR/VR`, `Artificial Intelligence`, `Business Development & Partnerships`, `Communications & Public Policy`, `Creative`, `Data & Analytics`, `Data Center`, `Design & User Experience`, `Enterprise Engineering`, `Global Operations`, `Infrastructure`, `Internship - Business`, `Internship - Engineering, Tech & Design`, `Internship - PhD`, `Legal, Finance, Facilities & Admin`, `People & Recruiting`, `Product Management`, `Research`, `Sales & Marketing`, `Security`, `Software Engineering`, `Technical Program Management`, `University Grad - Business`, `University Grad - Engineering, Tech & Design`, `University Grad - PhD & Postdoc`, `Facebook`, `Messenger`, `Instagram`, `WhatsApp`, `Meta Quest`. `roles` enum: `Full time employment`, `Internship`, `Short term employment`. `results_per_page` enum: `all`, `five`, `ten`.
- **Params:** `is_remote_only` (boolean, optional) — Restrict to remote-only postings; `offices` (array, optional) — Repeatable location-id filter (OR) in Meta's own id format, e.g. menlo-park, london -- not a closed enum; `q` (string, optional) — Facet-name keyword: matches team, technology, location, or ref/req-code -- not a title/description search; `results_per_page` (string, optional) — Response size cap: all, five, ten; `roles` (array, optional) — Repeatable employment-type filter (OR); see roles enum above; `sort_by_new` (boolean, optional) — Sort newest-first instead of relevance; `teams` (array, optional) — Repeatable team-or-technology filter (OR); see teams enum above
