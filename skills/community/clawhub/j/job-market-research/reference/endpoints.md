# job-market-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**59 endpoints across 10 platform group(s).**

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

## Google Jobs (2)

### `google_jobs_job`

- **HTTP:** `GET /google-jobs/job`
- **What:** Google Jobs single posting. Returns one Google Careers posting by its numeric job id (the `id` field returned by search).
- **Params:** `id` (string, **required**) — Numeric Google job id

### `google_jobs_search`

- **HTTP:** `GET /google-jobs/search`
- **What:** Google Jobs search. Searches Google's public careers site (careers.google.com) via its server-rendered search page's embedded job data. Each result includes the description, responsibilities, and qualifications inline. Page size is fixed by Google at 20 results.
- **Params:** `location` (string, optional) — Location filter (free text); `page` (integer, optional) — Page number, 1-based; `q` (string, **required**) — Search query

## Amazon Jobs (3)

### `amazon_jobs_categories`

- **HTTP:** `GET /amazon-jobs/categories`
- **What:** Amazon Jobs category discovery. Lists every value amazon-jobs/search's `category` parameter accepts, each with its current live job count. Live-queries amazon.jobs's own search category facet rather than a static list, so counts and coverage stay current.
- **Params:** _none_

### `amazon_jobs_job`

- **HTTP:** `GET /amazon-jobs/job`
- **What:** Amazon Jobs single posting. Returns one Amazon.jobs posting by its numeric job id (the `id` field returned by search).
- **Params:** `id` (string, **required**) — Numeric Amazon job id

### `amazon_jobs_search`

- **HTTP:** `GET /amazon-jobs/search`
- **What:** Amazon Jobs search. Searches Amazon's public careers site (amazon.jobs). Each result includes the full description and qualifications inline. `sort` accepts `relevant` (default, relevance ranking) or `recent` (newest posted first). Either `q` or `category` (or both) must be given -- `category` filters by Amazon's own job-category taxonomy and works with no text query at all. See `amazon-jobs-categories` for the full, live-verified list of accepted `category` values.
- **Params:** `category` (string, optional) — Amazon's own job-category taxonomy slug, case-insensitive. Either q or category is required; `country` (string, optional) — ISO 3166-1 alpha-3 country code filter; `limit` (integer, optional) — Results per page, max 100 (default 20); `page` (integer, optional) — Page number, 1-based; `q` (string, optional) — Search query. Either q or category is required; `sort` (string, optional) — Sort order

## Apple Jobs (3)

### `apple_jobs_job`

- **HTTP:** `GET /apple-jobs/job`
- **What:** Apple Jobs single posting. Returns one Apple Careers posting by its job id (the `id` field returned by search, e.g. `200674676-0836` for a specific requisition or `PIPE-200314122` for an evergreen/pipeline retail role).
- **Params:** `id` (string, **required**) — Apple job id

### `apple_jobs_locations`

- **HTTP:** `GET /apple-jobs/locations`
- **What:** Apple Jobs location discovery. Discovery endpoint for apple-jobs-search's `location` parameter, whose accepted values are a closed set Apple itself defines (its own `<slug>-<CODE>` location ids -- free-text location names are rejected). Apple exposes no bulk "list everything" option for this; the only lookup is a fuzzy search capped at 10 results per call covering four granularities (country, state/province, metro area, city) with no empty-input listing mode. With no `q`, this returns the full country-level value space (206 values, live-verified) as a static list -- the granularity apple-jobs-search's own examples use and nearly every caller needs. With `q` supplied, this instead looks up Apple's own location filter live so callers can discover state/metro/city-level values for finer filtering; results at those deeper levels may include more than one candidate and are ranked by Apple's own relevance, not alphabetically.
- **Params:** `q` (string, optional) — Optional free-text location search. Omit to get the full country-level list; supply to live-search state/metro/city-level values too (e.g. a city name).

### `apple_jobs_search`

- **HTTP:** `GET /apple-jobs/search`
- **What:** Apple Jobs search. Searches Apple's public careers site (jobs.apple.com) via its server-rendered search page's embedded job data. Page size is fixed by Apple at 20 results. Search results carry identity/location/team metadata only — call the job endpoint for the full description and qualifications.
- **Params:** `location` (string, optional) — Location filter in Apple's own slug format, e.g. united-states-USA or singapore-SGP. Free-text location names are not accepted -- call apple-jobs-locations to discover valid values.; `page` (integer, optional) — Page number, 1-based; `q` (string, **required**) — Search query

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

## Tesla Jobs (2)

### `tesla_jobs_job`

- **HTTP:** `GET /tesla-jobs/job`
- **What:** Tesla Jobs single posting. Returns one Tesla Careers posting by its numeric job id (the `id` field returned by the list endpoint).
- **Params:** `id` (string, **required**) — Tesla job id

### `tesla_jobs_list`

- **HTTP:** `GET /tesla-jobs/list`
- **What:** Tesla Jobs listing. Searches Tesla's public careers site (tesla.com/careers) via its own careers-state JSON endpoint. Tesla's own endpoint always returns its entire global job dataset regardless of query parameters; this filters and paginates that snapshot server-side. Listings carry identity/department/location metadata only — call the job endpoint for the full description, responsibilities, and requirements.
- **Params:** `location` (string, optional) — Filter by location, case-insensitive substring match; `page` (integer, optional) — Page number, 1-based; `page_size` (integer, optional) — Results per page, up to 100; `query` (string, optional) — Filter by title or department, case-insensitive substring match

## Jobs (30)

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

### `jobs_hiring_signals`

- **HTTP:** `GET /jobs/hiring-signals`
- **What:** Aggregate hiring signals for a company's board. Aggregates a company's ATS board into a hiring snapshot: total open roles, breakdowns by department/location/title, remote share, and how many roles are new in the last 7/30 days — a leading indicator of company growth. Supply provider plus that provider's slug params (token / company / org / tenant+datacenter+site / domain). Breakdowns are computed over the fetched postings.
- **Params:** `board` (string, optional) — ukg job-board UUID; `company` (string, optional) — lever / smartrecruiters / workable / recruitee / rippling / personio / teamtailor / gem / pinpoint company slug; `datacenter` (string, optional) — workday datacenter shard; `domain` (string, optional) — icims careers domain / eightfold organization domain; `host` (string, optional) — oracle cloud host (*.oraclecloud.com); `org` (string, optional) — ashby org slug; `provider` (string, **required**) — ATS provider; `site` (string, optional) — workday / oracle career site; `tenant` (string, optional) — workday / eightfold tenant; `token` (string, optional) — greenhouse board token

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

## Tes (7)

### `tes_job_detail`

- **HTTP:** `GET /tes/jobs/detail`
- **What:** Get a Tes teaching job. Returns detail for one job posting by its numeric id (the id field returned by tes-job-search): employer, location, salary, contract terms/types, dates, and application contact/URL, plus a short excerpt of the listing description rather than the full long-form HTML copy.
- **Params:** `id` (string, **required**) — Tes job id

### `tes_job_employer`

- **HTTP:** `GET /tes/jobs/employer`
- **What:** Get a Tes jobs employer profile. Returns detail for one jobs employer profile by its numeric id (the trailing id in tes-job-detail's employer_url field, e.g. .../jobs/employer/epsom-college-1039424 -- the 1039424): name, location, school type/phase/funding status/gender/age range, an about description, its postal address, and every currently-open position listed on the employer's own profile page (id, title, url -- call tes-job-detail with each id for the full posting).
- **Params:** `id` (string, **required**) — Tes employer id

### `tes_job_search`

- **HTTP:** `GET /tes/jobs/search`
- **What:** Search Tes teaching jobs. Searches Tes's (tes.com) teaching-jobs board. Returns listing facts (title, employer, location, salary, contract terms/types) plus a short excerpt of the listing description, not the full long-form job-description copy, and the same live faceted-search breakdown (position/subject/workplace category trees with counts, plus contract type/term counts) the real search page renders as its filter sidebar. location is a free-text place name (a UK town/city, an international city, or a bare country name) resolved to coordinates; omit for Tes's own default market, "United Kingdom". radius_miles selects the search radius around location. contract_type and contract_term are validated against Tes's own small, closed label sets. position, subject, and workplace are comma-separated filters -- Tes's own category labels are numerous and can change, so read a prior response's own facets.positions[].value (and facets.positions[].children[].value)/facets.subjects[].value/facets.workplaces[].children[].value for the live, current set rather than guessing. salary_min filters to jobs with an advertised salary at or above that amount (in the searched market's local currency); Tes's own filter panel offers only a minimum, no maximum.
- **Params:** `contract_term` (string, optional) — Contract term; `contract_type` (string, optional) — Contract type; `keywords` (string, optional) — Job title or keyword; `location` (string, optional) — Free-text place name resolved via Tes's own location autocomplete; `page` (integer, optional) — One-based page; `page_size` (integer, optional) — Results per page; `position` (string, optional) — Comma-separated position category label(s) -- see the endpoint markdown; `radius_miles` (integer, optional) — Search radius around location, in miles; `salary_min` (integer, optional) — Minimum advertised salary, in the searched market's local currency; `sort` (string, optional) — Sort order; `subject` (string, optional) — Comma-separated subject label(s) -- see the endpoint markdown; `workplace` (string, optional) — Comma-separated workplace/organisation-type label(s) -- see the endpoint markdown

### `tes_resource_detail`

- **HTTP:** `GET /tes/resources/detail`
- **What:** Get a Tes teaching resource. Returns detail for one teaching resource by its numeric id (the id field returned by tes-resource-search). Descriptive facts (title, subject, age range, resource type, author, price, rating, licence label), a per-file attachment list (file type, size, and a preview thumbnail -- metadata only), and the most recent page of reviews are returned -- not the downloadable resource file itself.
- **Params:** `country` (string, optional) — Storefront market for pricing/currency; `id` (string, **required**) — Tes resource id

### `tes_resource_search`

- **HTTP:** `GET /tes/resources/search`
- **What:** Search Tes teaching resources. Searches Tes's (tes.com) teaching-resources marketplace. Returns listing facts (title, author, price, rating, downloads) -- not full listing descriptions. query is optional: omit it (alone, or combined with key_stage/subject/on_sale) for pure filter-driven or fully unfiltered browsing. sort mirrors the real search page's own Sort by dropdown; key_stage and subject mirror its left-hand Refine by filters (both closed, validated enums taken from Tes's own facet taxonomy, and always resolved against Tes's own single GB-taxonomy regardless of country). country controls result currency/localisation only (confirmed live for all seven values); it does not change which key_stage/subject values are valid.
- **Params:** `country` (string, optional) — Storefront market; `key_stage` (string, optional) — Filter by age range; `on_sale` (boolean, optional) — Filter to discounted resources only; `page` (integer, optional) — One-based page; `page_size` (integer, optional) — Results per page; `query` (string, optional) — Search keywords -- omit for filter-driven or unfiltered browsing; `sort` (string, optional) — Sort order; `subject` (string, optional) — Filter by subject -- one of Tes's own top-level subject facet labels; see the endpoint markdown for the full list (two of the 29 values contain a comma, which is why this parameter is not expressed as a Swagger Enums() list)

### `tes_resource_shop`

- **HTTP:** `GET /tes/resources/shop`
- **What:** Get a Tes teaching-resources author shop. Returns detail for one teaching-resources author/seller shop by its username (from tes-resource-search/tes-resource-detail's author field, or the trailing path segment of author_url): display name, average rating, upload/view/download counts, a bio, and a page of that author's resource listing (id, title, price, thumbnail -- call tes-resource-detail with each id for subject/age-range/resource-type/rating/description). subject narrows the listing to one of the subject tabs shown on the shop's own page; these vary per author and are not a curated enum.
- **Params:** `page` (integer, optional) — One-based page; `subject` (string, optional) — Subject tab to filter the listing to -- see the shop's own page for the current set; `username` (string, **required**) — Tes author username

### `tes_school_search`

- **HTTP:** `GET /tes/schools/search`
- **What:** Search the Tes Schools Directory. Searches Tes's (tes.com) public Schools Directory by school name or location. Returns listing facts (name, logo, a short description, address) for each matching school/employer. Each result's id is the same employer id tes-job-employer accepts, so a caller can go straight from a name/location search to a full employer profile (school type/phase/funding status/gender/age range, and its currently-open positions) without first needing a job posting to discover the id.
- **Params:** `page` (integer, optional) — One-based page; `page_size` (integer, optional) — Results per page; `query` (string, **required**) — School name or location

## Upwork (3)

### `upwork_freelancer`

- **HTTP:** `GET /upwork/freelancer/{id}`
- **What:** Get Upwork freelancer profile. Returns an Upwork freelancer profile: name, title, verification badge, overview, hourly rate, rating and review count, Job Success Score, location and local time, total jobs/hours worked, and recent client feedback (title, comment, date, client name, rating).
- **Params:** `id` (string, **required**) — Upwork freelancer id, the value after \

### `upwork_job`

- **HTTP:** `GET /upwork/job/{id}`
- **What:** Get Upwork job posting detail. Returns an Upwork job posting: title, full description, employment type, budget (hourly range or fixed amount), location/remote type, experience level, duration, project type, proposal count, allowed applicant countries, and a summary of the posting client (member since, location, total spend, hires, hours, industry, company size).
- **Params:** `id` (string, **required**) — Upwork job id, e.g. from a search result's id field

### `upwork_search`

- **HTTP:** `GET /upwork/search`
- **What:** Search Upwork job postings. Searches Upwork's public job listings by free-text keyword, returning job summaries (title, budget, experience level, duration, posted date, description snippet, skill tags).
- **Params:** `page` (integer, optional) — 1-based result page. Defaults to 1.; `q` (string, **required**) — Free-text job search keyword

## Fiverr (3)

### `fiverr_gig`

- **HTTP:** `GET /fiverr/gig/{username}/{slug}`
- **What:** Get Fiverr gig detail. Returns a Fiverr gig detail page: title, description, category, pricing packages (basic/standard/premium tiers with price and delivery time), rating, review count, orders in queue, tags, gallery images, and a seller summary (level, rating, response time, languages). Seller level uses the same values on the search, seller and gig endpoints: level_one_seller, level_two_seller, top_rated_seller, or new_seller.
- **Params:** `slug` (string, **required**) — Fiverr gig URL slug, the trailing path segment after the username in a gig URL; `username` (string, **required**) — Fiverr seller username, e.g. from a search result's seller_username field

### `fiverr_search`

- **HTTP:** `GET /fiverr/search`
- **What:** Search Fiverr gigs. Searches Fiverr's public gig listings by free-text keyword, returning gig summaries (title, seller username, seller level, rating, review count, starting price, category, thumbnail image). Seller level uses the same values on the search, seller and gig endpoints: level_one_seller, level_two_seller, top_rated_seller, or new_seller.
- **Params:** `page` (integer, optional) — 1-based result page. Defaults to 1.; `q` (string, **required**) — Free-text gig search keyword

### `fiverr_seller`

- **HTTP:** `GET /fiverr/seller/{username}`
- **What:** Get Fiverr seller profile. Returns a Fiverr seller profile: display name, one-liner title, description, country, seller level, verification status, hourly rate, spoken languages, join date, and the seller's gig ids. Seller level uses the same values on the search, seller and gig endpoints: level_one_seller, level_two_seller, top_rated_seller, or new_seller.
- **Params:** `username` (string, **required**) — Fiverr seller username, e.g. from a search result's seller_username field
