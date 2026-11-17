# job-posting-comparison — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**37 endpoints across 4 platform group(s).**

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

## Jobs (29)

### `jobs_ashby_board`

- **HTTP:** `GET /jobs/ashby/board`
- **What:** List an organization's Ashby job board. Lists an organization's public Ashby board postings with inline detail (description, compensation when include_compensation=true). The org is the Ashby slug from its careers URL. An unknown org returns an empty board (Ashby does not 404).
- **Params:** `include_compensation` (boolean, optional) — Include compensation summary; `org` (string, **required**) — Ashby org slug (careers URL)

### `jobs_company_search`

- **HTTP:** `GET /jobs/company-search`
- **What:** Find which ATS a company uses by slug. Probes Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Recruitee, Rippling, Teamtailor, and Pinpoint in parallel for a slug and reports the providers where it resolves to a non-empty board (with the open-role count and board URL). Workday is excluded (its board needs tenant + datacenter + site).
- **Params:** `slug` (string, **required**) — Company careers slug to probe

### `jobs_eightfold_board`

- **HTTP:** `GET /jobs/eightfold/board`
- **What:** List an Eightfold tenant's job board. Lists a company's public Eightfold AI job board, paged via limit/offset. tenant is the {tenant}.eightfold.ai subdomain from the careers URL; domain is the hiring organization's own domain (e.g. microsoft.com), also visible on the tenant's careers page.
- **Params:** `domain` (string, **required**) — Hiring organization domain; `limit` (integer, optional) — Page size, default 10, max 10 (upstream caps results per page regardless of a larger value); `location` (string, optional) — Filter: location contains; `offset` (integer, optional) — Page offset, default 0; `query` (string, optional) — Free-text search; `tenant` (string, **required**) — Eightfold tenant subdomain (careers URL)

### `jobs_eightfold_job`

- **HTTP:** `GET /jobs/eightfold/job`
- **What:** Get a single Eightfold position. Returns a single Eightfold position with its full HTML/text description. id is the position id from a board listing; tenant/domain as in the board endpoint.
- **Params:** `domain` (string, **required**) — Hiring organization domain; `id` (string, **required**) — Eightfold position id from a board listing; `tenant` (string, **required**) — Eightfold tenant subdomain

### `jobs_gem_board`

- **HTTP:** `GET /jobs/gem/board`
- **What:** List a company's Gem job board. Lists a company's public Gem (gem.com) board postings with inline detail (full HTML description, and compensation when the company publishes a pay range). The company is the Gem vanity URL slug from its careers URL.
- **Params:** `company` (string, **required**) — Gem vanity URL slug (careers URL)

### `jobs_greenhouse_board`

- **HTTP:** `GET /jobs/greenhouse/board`
- **What:** List a company's Greenhouse job board. Lists a company's public Greenhouse board postings in the shared Job shape. Set content=true to include each job's full HTML description in one call. The token is the company's Greenhouse board slug from its careers URL.
- **Params:** `content` (boolean, optional) — Include full HTML description per job; `token` (string, **required**) — Greenhouse board token (careers URL slug)

### `jobs_greenhouse_job`

- **HTTP:** `GET /jobs/greenhouse/job`
- **What:** Get a single Greenhouse job. Returns one Greenhouse job, identified by the board `token` and job `id`, both required. The response has the title, company, department, team, location and offices, workplace type, employment type, posting and apply URLs, posting date, compensation, and the description as HTML and plain text. An unknown token or id returns `404`.
- **Params:** `id` (string, **required**) — Greenhouse job id; `token` (string, **required**) — Greenhouse board token

### `jobs_icims_board`

- **HTTP:** `GET /jobs/icims/board`
- **What:** List an iCIMS tenant's job board. Lists a company's public iCIMS job board (served through the tenant's white-labeled careers domain, e.g. careers.costco.com — not the bare {company}.icims.com subdomain, which is an OAuth-gated employee portal), paged via page/limit, with the full description inline per job. domain is the tenant's careers domain from its careers URL.
- **Params:** `domain` (string, **required**) — iCIMS tenant careers domain (careers URL); `keywords` (string, optional) — Free-text keyword search; `limit` (integer, optional) — Page size, default 20, max 50; `location` (string, optional) — Filter: location contains; `page` (integer, optional) — Page number, default 1

### `jobs_icims_job`

- **HTTP:** `GET /jobs/icims/job`
- **What:** Get a single iCIMS job. Returns a single iCIMS job with its full HTML/text description, department, and benefits. id is the req_id/slug from a board listing; lang defaults to en-us.
- **Params:** `domain` (string, **required**) — iCIMS tenant careers domain; `id` (string, **required**) — iCIMS job req_id/slug from a board listing; `lang` (string, optional) — Language code, default en-us

### `jobs_lever_posting`

- **HTTP:** `GET /jobs/lever/posting`
- **What:** Get a single Lever posting. Returns one Lever posting, identified by the `company` slug and posting `id`, both required. The response has the title, department, team, location, workplace type, employment type, posting and apply URLs, posting date, compensation, and the description as HTML and plain text. An unknown company or id returns `404`.
- **Params:** `company` (string, **required**) — Lever company slug; `id` (string, **required**) — Lever posting id

### `jobs_lever_postings`

- **HTTP:** `GET /jobs/lever/postings`
- **What:** List a company's Lever postings. Lists a company's public Lever postings (detail is inline), optionally filtered by department, location, or remote. The company is the Lever slug from its careers URL.
- **Params:** `company` (string, **required**) — Lever company slug (careers URL); `department` (string, optional) — Filter: department contains; `location` (string, optional) — Filter: location contains; `remote` (boolean, optional) — Filter by remote (true or false)

### `jobs_oracle_board`

- **HTTP:** `GET /jobs/oracle/board`
- **What:** List an Oracle Recruiting (ORC) tenant's job board. Lists an Oracle Recruiting Cloud tenant's public requisitions, paged via limit/offset. host and site both come from the careers URL https://{host}/hcmUI/CandidateExperience/en/sites/{site}/ (host must be an *.oraclecloud.com hostname; site looks like CX_1). The listing carries a short description; use the single-job endpoint for full detail.
- **Params:** `host` (string, **required**) — Oracle Cloud host (careers URL, *.oraclecloud.com); `limit` (integer, optional) — Page size, default 25, max 50; `offset` (integer, optional) — Page offset, default 0; `search` (string, optional) — Free-text keyword search; `site` (string, **required**) — Oracle career site number

### `jobs_oracle_job`

- **HTTP:** `GET /jobs/oracle/job`
- **What:** Get a single Oracle Recruiting (ORC) requisition. Returns a single Oracle Recruiting requisition with its full HTML/text description (description, responsibilities, qualifications). id is the requisition Id from a board listing; host/site as in the board endpoint.
- **Params:** `host` (string, **required**) — Oracle Cloud host (*.oraclecloud.com); `id` (string, **required**) — Oracle requisition Id from a board listing; `site` (string, **required**) — Oracle career site number

### `jobs_personio_feed`

- **HTTP:** `GET /jobs/personio/feed`
- **What:** List a company's Personio job board. Lists a company's public Personio board feed in the shared Job shape with detail inline, optionally filtered by department, location, or remote. The company is the Personio subdomain from its careers URL https://{company}.jobs.personio.de/.
- **Params:** `company` (string, **required**) — Personio subdomain (careers URL); `department` (string, optional) — Filter: department contains; `location` (string, optional) — Filter: location contains; `remote` (boolean, optional) — Filter by remote (true or false)

### `jobs_phenom_board`

- **HTTP:** `GET /jobs/phenom/board`
- **What:** Search a Phenom People tenant's job board. Searches a company's public Phenom People career site (a white-labeled domain such as careers.whataburger.com or jobs.cvshealth.com). domain is the tenant's careers domain from its careers URL. Paged via offset/limit; limit is a best-effort page-size hint some tenants ignore, so count always reflects what actually came back.
- **Params:** `category` (string, optional) — Filter: category contains; `domain` (string, **required**) — Phenom tenant careers domain (careers URL); `keywords` (string, optional) — Free-text keyword search; `limit` (integer, optional) — Page size hint, default 10, max 100 (some tenants ignore this and return their own configured page size regardless); `location` (string, optional) — Filter: location contains; `offset` (integer, optional) — Page offset, default 0; `sort` (string, optional) — Sort order, default relevant

### `jobs_phenom_job`

- **HTTP:** `GET /jobs/phenom/job`
- **What:** Get a single Phenom People job. Returns a single Phenom People job with its full HTML/text description, category, and apply URL. domain is the tenant's careers domain (as in the board endpoint); id is the jobId/reqId from a board listing (e.g. JR10002958).
- **Params:** `domain` (string, **required**) — Phenom tenant careers domain; `id` (string, **required**) — Phenom job id from a board listing

### `jobs_pinpoint_board`

- **HTTP:** `GET /jobs/pinpoint/board`
- **What:** List a tenant's Pinpoint job board. Lists a tenant's public Pinpoint (pinpointhq.com) board postings with inline detail (full HTML description, key responsibilities, skills, and benefits, plus structured compensation when the tenant publishes a pay range). The company is the tenant subdomain from its careers URL https://{company}.pinpointhq.com/.
- **Params:** `company` (string, **required**) — Pinpoint tenant subdomain (careers URL)

### `jobs_recruitee_offer`

- **HTTP:** `GET /jobs/recruitee/offer`
- **What:** Get a single Recruitee offer. Returns a single Recruitee offer with its full HTML/text description and structured compensation when the board exposes it.
- **Params:** `company` (string, **required**) — Recruitee subdomain; `id` (string, **required**) — Recruitee offer id

### `jobs_recruitee_offers`

- **HTTP:** `GET /jobs/recruitee/offers`
- **What:** List a company's Recruitee offers. Lists a company's public Recruitee offers (detail is inline), optionally filtered by department, location, or remote. The company is the Recruitee subdomain from its careers URL https://{company}.recruitee.com/.
- **Params:** `company` (string, **required**) — Recruitee subdomain (careers URL); `department` (string, optional) — Filter: department contains; `location` (string, optional) — Filter: location contains; `remote` (boolean, optional) — Filter by remote (true or false)

### `jobs_rippling_board`

- **HTTP:** `GET /jobs/rippling/board`
- **What:** List a company's Rippling job board. Lists a company's public Rippling board postings (thin listing — title, department, work location). The company is the Rippling board slug from its careers URL https://ats.rippling.com/{company}/jobs. Detail (full description, employment type) is fetched per job via the single-job endpoint.
- **Params:** `company` (string, **required**) — Rippling board slug (careers URL); `department` (string, optional) — Filter: department contains; `location` (string, optional) — Filter: location contains; `remote` (boolean, optional) — Filter by remote (true or false)

### `jobs_rippling_job`

- **HTTP:** `GET /jobs/rippling/job`
- **What:** Get a single Rippling job. Returns a single Rippling job with its full HTML/text description, employment type, and work locations. The id is the job uuid from a listing.
- **Params:** `company` (string, **required**) — Rippling board slug; `id` (string, **required**) — Rippling job uuid

### `jobs_smartrecruiters_posting`

- **HTTP:** `GET /jobs/smartrecruiters/posting`
- **What:** Get a single SmartRecruiters posting. Returns one SmartRecruiters posting, identified by the `company` id and posting `id`, both required. The response has the title, department, location, employment type, posting and apply URLs, posting date, compensation, and the job ad description as HTML and text. Recruiter personal data is left out. An unknown company or id returns `404`.
- **Params:** `company` (string, **required**) — SmartRecruiters company id; `id` (string, **required**) — SmartRecruiters posting id

### `jobs_smartrecruiters_postings`

- **HTTP:** `GET /jobs/smartrecruiters/postings`
- **What:** List a company's SmartRecruiters postings. Lists a company's public SmartRecruiters postings, paged via limit/offset. The company is the SmartRecruiters identifier from its careers URL.
- **Params:** `company` (string, **required**) — SmartRecruiters company id (careers URL); `limit` (integer, optional) — Page size, default 100, max 100; `offset` (integer, optional) — Page offset, default 0

### `jobs_teamtailor_jobs`

- **HTTP:** `GET /jobs/teamtailor/jobs`
- **What:** List a company's Teamtailor job board. Lists a company's public Teamtailor board feed in the shared Job shape with detail inline, optionally filtered by department, location, or remote. The company is the Teamtailor subdomain from its careers URL https://{company}.teamtailor.com/.
- **Params:** `company` (string, **required**) — Teamtailor subdomain (careers URL); `department` (string, optional) — Filter: department contains; `location` (string, optional) — Filter: location contains; `remote` (boolean, optional) — Filter by remote (true or false)

### `jobs_ukg_board`

- **HTTP:** `GET /jobs/ukg/board`
- **What:** List a UKG Pro Recruiting tenant's job board. Lists a UKG Pro Recruiting (formerly UltiPro) tenant's public opportunities, paged via limit/offset. tenant and board both come from the careers URL https://recruiting.ultipro.com/{tenant}/JobBoard/{board}. Each posting carries a brief description inline.
- **Params:** `board` (string, **required**) — UKG job-board UUID (careers URL); `limit` (integer, optional) — Page size, default 25, max 50; `offset` (integer, optional) — Page offset, default 0; `search` (string, optional) — Free-text keyword search; `tenant` (string, **required**) — UKG tenant code (careers URL)

### `jobs_workable_posting`

- **HTTP:** `GET /jobs/workable/posting`
- **What:** Get a single Workable posting. Returns a single Workable posting with its full HTML/text description. The id is the posting shortcode from a listing.
- **Params:** `company` (string, **required**) — Workable account slug; `id` (string, **required**) — Workable posting shortcode

### `jobs_workable_postings`

- **HTTP:** `GET /jobs/workable/postings`
- **What:** List a company's Workable postings. Lists a company's public Workable postings in the shared Job shape, optionally filtered by department, location, or remote. The company is the Workable account slug from its careers URL https://apply.workable.com/{company}/. Detail (full description) is fetched per job via the single-posting endpoint.
- **Params:** `company` (string, **required**) — Workable account slug (careers URL); `department` (string, optional) — Filter: department contains; `location` (string, optional) — Filter: location contains; `remote` (boolean, optional) — Filter by remote (true or false); `search` (string, optional) — Free-text search

### `jobs_workday_board`

- **HTTP:** `GET /jobs/workday/board`
- **What:** List a Workday tenant's job board. Lists a company's public Workday (CXS) postings, paged via limit/offset. tenant, datacenter (wd1/wd3/wd5/...), and site all come from the careers URL https://{tenant}.wd5.myworkdayjobs.com/{site}.
- **Params:** `datacenter` (string, **required**) — Workday datacenter shard (wd1, wd3, wd5, ...); `limit` (integer, optional) — Page size, default 20, max 20; `offset` (integer, optional) — Page offset, default 0; `search` (string, optional) — Free-text search; `site` (string, **required**) — Workday career site; `tenant` (string, **required**) — Workday tenant

### `jobs_workday_job`

- **HTTP:** `GET /jobs/workday/job`
- **What:** Get a single Workday job. Returns a single Workday posting's full detail (description, location, req id). path is the externalPath from a board listing. tenant/datacenter/site as in the board endpoint.
- **Params:** `datacenter` (string, **required**) — Workday datacenter shard; `path` (string, **required**) — Job externalPath from a board listing; `site` (string, **required**) — Workday career site; `tenant` (string, **required**) — Workday tenant

## Indeed (2)

### `indeed_job`

- **HTTP:** `GET /indeed/job`
- **What:** Indeed job detail. Returns one Indeed job posting by its job key (the `job_key` field returned by search).
- **Params:** `jk` (string, **required**) — Indeed job key (16-character hex)

### `indeed_search`

- **HTTP:** `GET /indeed/search`
- **What:** Indeed job search. Searches Indeed job postings by keyword and location. `sort` enum: `relevance` (default), `date`.
- **Params:** `fromage` (integer, optional) — Only jobs posted within this many days; `l` (string, optional) — Location (city, state, or zip); `page` (integer, optional) — Page number, 1-based, defaults to 1; `q` (string, **required**) — Search keywords; `radius` (integer, optional) — Search radius in miles; `sort` (string, optional) — Sort order: relevance, date

## Web (1)

### `web_scrape`

- **HTTP:** `POST /web/scrape`
- **What:** Scrape a URL into markdown, HTML, links or metadata. Fetches a single public URL and returns clean content in the requested formats (markdown, html, raw_html, links, metadata). The request body IS the ScrapeOption object itself — e.g. {"url": "https://example.com"} — do not wrap it in an extra key. With render=auto the request starts as a fast HTTP fetch and escalates to a real browser when the page is blocked or rendered with JavaScript. only_main_content (default true) strips navigation, headers, footers and other boilerplate before conversion. Only public pages are supported; respect each site's terms of use and robots directives. A handful of popular sites (Amazon, Reddit, Yelp, LinkedIn, and others) already have a dedicated, more reliable endpoint elsewhere in this API — a failed scrape against one of them names it. A Reddit URL that maps onto a dedicated Reddit endpoint (listings, search, comment threads, user and domain pages) is answered by that endpoint instead, and its response is returned as-is in data with an X-Routed-To header; send dedicated=false to always get the scraped page.
- **Params:** `scrapeOption` (object, **required**) — Scrape options
- **REST body:** Send the value of the MCP argument `scrapeOption` directly as the JSON body; do not wrap it in a `scrapeOption` property.
