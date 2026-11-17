# hiring-demand-analysis — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**6 endpoints across 2 platform group(s).**

## Datasets (5)

### `datasets_jobs_companies`

- **HTTP:** `GET /datasets/jobs/companies`
- **What:** Find which companies are hiring. Searches the discovered company board registry — which companies are hiring, on which ATS (or, for the 5 single-company big-tech providers, which platform), with how many open roles. Set sponsors_visa=true to keep companies with certified employer filings in recent public U.S. Department of Labor LCA disclosure data. This is company-level historical evidence, not a guarantee for a specific role or candidate. provider enum: `greenhouse`, `lever`, `ashby`, `workday`, `smartrecruiters`, `workable`, `recruitee`, `rippling`, `personio`, `teamtailor`, `oracle`, `ukg`, `icims`, `eightfold`, `gem`, `pinpoint`, `amazon-jobs`, `apple-jobs`, `google-jobs`, `meta-jobs`, `tesla-jobs`. status enum: `active`, `empty`, `gone`, `blocked`, `pending`, `invalid`. sort enum: `open_desc`, `company_asc`, `crawled_desc`. Billing: this endpoint costs 1 credit per 10 records returned, rounded up, with a minimum of 1 (up to 10 records cost 1, a full page of 100 costs 10).
- **Params:** `min_open_roles` (integer, optional) — Minimum open roles; `page` (integer, optional) — Page number, default 1; `page_size` (integer, optional) — Page size, default 20, max 100; `provider` (string, optional) — Provider filter; `q` (string, optional) — Match on company name / domain; `sort` (string, optional) — Sort enum: open_desc, company_asc, crawled_desc; `sponsors_visa` (boolean, optional) — Keep companies with recent certified DOL LCA filings (default false); `status` (string, optional) — Board status. Enum: active, empty, gone, blocked, pending, invalid

### `datasets_jobs_company_item`

- **HTTP:** `GET /datasets/jobs/companies/{id}`
- **What:** Get a single company by board id. Returns one discovered company board by its dataset board id. When the company name matches recent public U.S. Department of Labor LCA disclosure data, the response includes `lca_sponsorship` with filing counts and observed fiscal-quarter range; this is company-level historical evidence, not a guarantee for a specific role or candidate. When the board carries a known domain, the response also includes a `tech_stack` firmographic hint. Returns 404 when the board id is not in the registry.
- **Params:** `id` (string, **required**) — Dataset board id

### `datasets_jobs_facets`

- **HTTP:** `GET /datasets/jobs/facets`
- **What:** Facet the jobs dataset (hiring market aggregates). Aggregations over all open postings: top companies hiring, breakdown by provider (every provider filterable via /datasets/jobs/search's `provider` param), department, location, employment type, skill, benefit, education, security clearance, seniority, and ESCO/ISCO job family, plus the remote share — a live hiring-market snapshot. Seniority uses one mutually exclusive value: `entry`, `mid`, or `senior`; ambiguous occupations are omitted from job-family buckets.
- **Params:** `size` (integer, optional) — Buckets per facet, default 20, max 100

### `datasets_jobs_item`

- **HTTP:** `GET /datasets/jobs/items/{id}`
- **What:** Get a single posting from the jobs dataset. Returns one crawled job posting by its dataset posting id, the `posting_id` of a search result. Alongside the posting itself, `seniority_level` is `entry`, `mid` or `senior`, and occupation fields appear only when title and skills support a reliable match. An id not in the index returns 404.
- **Params:** `id` (string, **required**) — Dataset posting id

### `datasets_jobs_search`

- **HTTP:** `GET /datasets/jobs/search`
- **What:** Search the jobs dataset (all companies' live postings). Full-text + faceted search over every job posting crawled from every discovered company ATS board (Greenhouse, Lever, Ashby, Workday, SmartRecruiters, Workable, Recruitee, Rippling, Personio, Teamtailor, Oracle, UKG, iCIMS, Eightfold, Gem, Pinpoint) plus 5 single-company big-tech careers platforms (Amazon, Apple, Google, Meta, Tesla). Open roles only by default (set include_closed=true for historical/filled roles). Salary is parsed from a structured field when the provider has one, or from an explicit pay figure stated in the description otherwise, so coverage varies by posting rather than by provider; min_salary/max_salary filter on it and require salary_currency, since comparing raw compensation numbers across currencies is meaningless. Location is also exposed as structured city/state/country fields alongside the free-text location string, so city/state/country filter on an exact match of those parsed components rather than substring-matching the display string. job_family is an exact level-2 ISCO family label assigned from ESCO occupation evidence; ambiguous postings remain unclassified and do not match that filter. employment_type is never populated for google-jobs/meta-jobs, and posted_at (so sort=posted_desc) is never populated for meta-jobs/tesla-jobs -- their upstream APIs expose no such field. provider enum: `greenhouse`, `lever`, `ashby`, `workday`, `smartrecruiters`, `workable`, `recruitee`, `rippling`, `personio`, `teamtailor`, `oracle`, `ukg`, `icims`, `eightfold`, `gem`, `pinpoint`, `amazon-jobs`, `apple-jobs`, `google-jobs`, `meta-jobs`, `tesla-jobs`. workplace_type enum: `onsite`, `hybrid`, `remote`. sort enum: `relevance`, `posted_desc`, `company_asc`. Billing: this search costs 1 credit per 10 records returned, rounded up, with a minimum of 1 (up to 10 records cost 1, a full page of 100 costs 10).
- **Params:** `city` (string, optional) — Exact city filter (parsed location component); `company` (string, optional) — Company name match; `country` (string, optional) — Exact country filter (parsed location component); ISO country code or name, matched case-insensitively; `department` (string, optional) — Exact department filter; `employment_type` (string, optional) — Exact employment-type filter; `include_closed` (boolean, optional) — Include closed/filled roles (default false = open only); `job_family` (string, optional) — Exact ESCO/ISCO job-family label filter; `location` (string, optional) — Location match; `max_salary` (number, optional) — Maximum salary (matches postings whose range starts at or below this); requires salary_currency; `min_salary` (number, optional) — Minimum salary (matches postings whose range reaches at least this); requires salary_currency; `page` (integer, optional) — Page number, default 1; `page_size` (integer, optional) — Page size, default 20, max 100; page*page_size must be <= 10000; `provider` (string, optional) — Provider filter; `q` (string, optional) — Full-text over title, company, description; `remote` (boolean, optional) — Filter by remote (true or false); `salary_currency` (string, optional) — 3-letter ISO currency code (e.g. USD) the min_salary/max_salary bounds are in; required when either bound is set; `sort` (string, optional) — Sort enum: relevance, posted_desc, company_asc; `state` (string, optional) — Exact state/region filter (parsed location component); `workplace_type` (string, optional) — Workplace type filter

## Google (1)

### `google_jobs`

- **HTTP:** `POST /google/jobs`
- **What:** Search Google Jobs. Searches Google Jobs for the `query` in the request body, optionally narrowed by `location` and paged with `page`. Each result has the job title, company, location, employment type, posting time, snippet, source and URL. The response echoes the query, location and page.
- **Params:** `option` (object, **required**) — Google Jobs search payload
- **REST body:** Send the value of the MCP argument `option` directly as the JSON body; do not wrap it in a `option` property.
