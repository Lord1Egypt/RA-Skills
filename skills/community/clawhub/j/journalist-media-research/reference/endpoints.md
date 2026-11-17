# journalist-media-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**6 endpoints across 3 platform group(s).**

## Datasets (3)

### `datasets_journalists_facets`

- **HTTP:** `GET /datasets/journalists/facets`
- **What:** Facet the journalists dataset. Returns distribution counts over the journalists index (dataset id enum value `journalists`), honoring the same filters as search. Facet enum: `outlet`, `vertical`, `topic`, `contact_type`, `record_type`, `role_type`, `email_kind`, `outreach_readiness_band`. `facet=outlet` returns every outlet (up to 1000) in one response; other facets return their top 50 values. Facets are not paginated: `page` and `page_size` are ignored.
- **Params:** `contact_type` (string, optional) — Contact-availability filter. Enum: email, social, none; `email_kind` (string, optional) — Email semantics filter. Enum: individual_work, individual_personal_public, shared_desk, tips_or_submissions, outlet_generic, unknown; `facet` (string, **required**) — Facet enum: outlet, vertical, topic, contact_type, record_type, role_type, email_kind, outreach_readiness_band; `min_outreach_readiness` (integer, optional) — Minimum outreach-readiness score, from 0 to 100; `outlet` (string, optional) — Exact outlet id filter; `q` (string, optional) — Full-text match on the journalist's name, title, and bio, max 256 characters; `record_type` (string, optional) — Record classification filter. Enum: person, desk, organization, syndicated_byline, unknown; `role_type` (string, optional) — Role classification filter. Enum: staff, editor, reporter, contributor, freelancer, columnist, non_editorial, unknown; `topic` (string, optional) — Exact topic filter; `vertical` (string, optional) — Exact beat-vertical filter. Enum: tech, crypto, marketing, consumer_tech, consumer_policy, cybersecurity, health, gaming, climate, business, entertainment, sports, legal, science, politics, real_estate, automotive, travel, food, education, design, film_tv, fashion, music, personal_finance, tech_independent, culture_independent, local_news, construction, banking, retail, aerospace_defense, energy, agriculture, local_business, general_news

### `datasets_journalists_item`

- **HTTP:** `GET /datasets/journalists/items/{outlet}/{slug}`
- **What:** Get a journalist from the journalists dataset. Returns one journalist by outlet id and slug from dataset id enum value `journalists`. Returns 404 when the outlet is not supported or the journalist is not in the index.
- **Params:** `outlet` (string, **required**) — Outlet id, e.g. techcrunch. Use the ids returned by facets?facet=outlet; `slug` (string, **required**) — Journalist slug within the outlet, e.g. zack-whittaker

### `datasets_journalists_search`

- **HTTP:** `GET /datasets/journalists/search`
- **What:** Search the journalists dataset. Searches the journalists index (dataset id enum value `journalists`) — public journalist and reporter records crawled from news outlets' own staff/author pages, for PR outreach. Each record carries the outlet, title, best-effort beat topics, and any public contact info found on that outlet's own page, plus deterministic record_type, role_type, email_kind, and outreach-readiness quality signals. There is no cross-outlet upstream search; this dataset is built by crawling a curated roster of outlets ourselves. vertical enum: `tech`, `crypto`, `marketing`, `consumer_tech`, `consumer_policy`, `cybersecurity`, `health`, `gaming`, `climate`, `business`, `entertainment`, `sports`, `legal`, `science`, `politics`, `real_estate`, `automotive`, `travel`, `food`, `education`, `design`, `film_tv`, `fashion`, `music`, `personal_finance`, `tech_independent`, `culture_independent`, `local_news`, `construction`, `banking`, `retail`, `aerospace_defense`, `energy`, `agriculture`, `local_business`. contact_type enum: `email`, `social`, `none`. record_type enum: `person`, `desk`, `organization`, `syndicated_byline`, `unknown`. role_type enum: `staff`, `editor`, `reporter`, `contributor`, `freelancer`, `columnist`, `non_editorial`, `unknown`. email_kind enum: `individual_work`, `individual_personal_public`, `shared_desk`, `tips_or_submissions`, `outlet_generic`, `unknown`. sort enum: `relevance`, `name_asc`, `outlet_asc`, `crawled_desc`, `readiness_desc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `contact_type` (string, optional) — Contact-availability filter. Enum: email, social, none; `email_kind` (string, optional) — Email semantics filter. Enum: individual_work, individual_personal_public, shared_desk, tips_or_submissions, outlet_generic, unknown; `min_outreach_readiness` (integer, optional) — Minimum outreach-readiness score, from 0 to 100; `outlet` (string, optional) — Exact outlet id filter, e.g. techcrunch, coindesk. Use the ids returned by facets?facet=outlet; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `q` (string, optional) — Full-text match on the journalist's name, title, and bio, max 256 characters; `record_type` (string, optional) — Record classification filter. Enum: person, desk, organization, syndicated_byline, unknown; `role_type` (string, optional) — Role classification filter. Enum: staff, editor, reporter, contributor, freelancer, columnist, non_editorial, unknown; `sort` (string, optional) — Sort enum: relevance, name_asc, outlet_asc, crawled_desc, readiness_desc; `topic` (string, optional) — Exact topic filter, e.g. security, stablecoins. Use the values returned by facets?facet=topic; `vertical` (string, optional) — Exact beat-vertical filter. Enum: tech, crypto, marketing, consumer_tech, consumer_policy, cybersecurity, health, gaming, climate, business, entertainment, sports, legal, science, politics, real_estate, automotive, travel, food, education, design, film_tv, fashion, music, personal_finance, tech_independent, culture_independent, local_news, construction, banking, retail, aerospace_defense, energy, agriculture, local_business, general_news

## Bing (2)

### `bing_news`

- **HTTP:** `GET /bing/news`
- **What:** Search Bing news results. Returns Bing news search results for a query string. Locale defaults to country=us and lang=en-us. Returns 503 when Bing serves a challenge page or unusable results.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Bing UI language; defaults to en-us; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, **required**) — Search query

### `bing_search`

- **HTTP:** `GET /bing/search`
- **What:** Search Bing web results. Returns Bing web search results for a query string, including organic results, optional context panel data, related queries, people-also-ask questions, news modules, video modules, and page-based pagination. Empty optional blocks are omitted from the JSON response. Locale defaults to country=us and lang=en-us. Returns 503 on a genuine transport failure or challenge page. Bing occasionally serves a well-formed page whose results share no significant term with the query; when every attempt hits this, the response is still returned as 200 with data.low_confidence set to true (and the X-Low-Confidence header) instead of being withheld, so callers get Bing's real answer plus an honest signal to double-check it rather than nothing. Queries that use the site: operator (for example site:gov.hu) are not supported: Bing serves a bot-verification challenge for them, so they are rejected with 400 before any request is made. Use the DuckDuckGo (/api/v1/duckduckgo/search), Brave (/api/v1/brave/search), or Yahoo (/api/v1/yahoo-search/search) search endpoints for domain-restricted searches instead.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Bing UI language; defaults to en-us; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, **required**) — Search query

## Web (1)

### `web_scrape`

- **HTTP:** `POST /web/scrape`
- **What:** Scrape a URL into markdown, HTML, links or metadata. Fetches a single public URL and returns clean content in the requested formats (markdown, html, raw_html, links, metadata). The request body IS the ScrapeOption object itself — e.g. {"url": "https://example.com"} — do not wrap it in an extra key. With render=auto the request starts as a fast HTTP fetch and escalates to a real browser when the page is blocked or rendered with JavaScript. only_main_content (default true) strips navigation, headers, footers and other boilerplate before conversion. Only public pages are supported; respect each site's terms of use and robots directives. A handful of popular sites (Amazon, Reddit, Yelp, LinkedIn, and others) already have a dedicated, more reliable endpoint elsewhere in this API — a failed scrape against one of them names it. A Reddit URL that maps onto a dedicated Reddit endpoint (listings, search, comment threads, user and domain pages) is answered by that endpoint instead, and its response is returned as-is in data with an X-Routed-To header; send dedicated=false to always get the scraped page.
- **Params:** `scrapeOption` (object, **required**) — Scrape options
- **REST body:** Send the value of the MCP argument `scrapeOption` directly as the JSON body; do not wrap it in a `scrapeOption` property.
