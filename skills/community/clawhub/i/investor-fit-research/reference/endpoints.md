# investor-fit-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**12 endpoints across 2 platform group(s).**

## Datasets (9)

### `datasets_pitchbook_companies_facets`

- **HTTP:** `GET /datasets/pitchbook-companies/facets`
- **What:** Facet PitchBook companies dataset. Returns value counts for the PitchBook companies dataset by the required `facet`: `status`, `primary_industry`, `financing_status`, `ownership_status`, `hq_country`, `hq_state` or `run_id`. Filters such as `q`, `min_year_founded` and `min_investor_count` apply, and the top 50 values come back.
- **Params:** `facet` (string, **required**) — Facet enum: status, primary_industry, financing_status, ownership_status, hq_country, hq_state, run_id; `financing_status` (string, optional) — Exact financing status filter, max 128 characters; `hq_country` (string, optional) — Exact headquarters country filter, max 128 characters; `hq_state` (string, optional) — Exact headquarters state/region filter, max 128 characters; `max_year_founded` (integer, optional) — Maximum founding year; `min_investor_count` (integer, optional) — Minimum number of investors; `min_year_founded` (integer, optional) — Minimum founding year; `ownership_status` (string, optional) — Exact ownership status filter, max 128 characters; `primary_industry` (string, optional) — Exact primary industry filter, max 128 characters; `q` (string, optional) — Full-text query over name and description, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `status` (string, optional) — Exact status filter, max 128 characters

### `datasets_pitchbook_companies_item`

- **HTTP:** `GET /datasets/pitchbook-companies/items/{id}`
- **What:** Get a PitchBook company from dataset. Returns one PitchBook company from the dataset by `id`, such as `752821-12`. The record has name, description, status, primary industry, financing and ownership status, headquarters, founding year, employees, investor count, latest deal type, website, FAQs and data tables. An unknown id returns 404.
- **Params:** `id` (string, **required**) — PitchBook company id, e.g. 752821-12

### `datasets_pitchbook_companies_search`

- **HTTP:** `GET /datasets/pitchbook-companies/search`
- **What:** Search PitchBook companies dataset. Searches the crawled public PitchBook company profile catalog stored in a search index. Discovered from PitchBook's public sitemap. Sort enum: `relevance`, `name_asc`, `year_founded_desc`, `investor_count_desc`, `recently_crawled_desc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `financing_status` (string, optional) — Exact financing status filter, max 128 characters; `hq_country` (string, optional) — Exact headquarters country filter, max 128 characters; `hq_state` (string, optional) — Exact headquarters state/region filter, max 128 characters; `max_year_founded` (integer, optional) — Maximum founding year; `min_investor_count` (integer, optional) — Minimum number of investors; `min_year_founded` (integer, optional) — Minimum founding year; `ownership_status` (string, optional) — Exact ownership status filter, max 128 characters; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `primary_industry` (string, optional) — Exact primary industry filter, max 128 characters; `q` (string, optional) — Full-text query over name and description, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `sort` (string, optional) — Sort enum: relevance, name_asc, year_founded_desc, investor_count_desc, recently_crawled_desc; `status` (string, optional) — Exact status filter (e.g. Private, Public, Acquired, Out of Business), max 128 characters

### `datasets_pitchbook_funds_facets`

- **HTTP:** `GET /datasets/pitchbook-funds/facets`
- **What:** Facet PitchBook funds dataset. Returns value counts for the PitchBook funds dataset by the required `facet`: `fund_strategy`, `fund_status` or `run_id`. The search filters `q`, `fund_strategy`, `fund_status`, `min_vintage_year` and `max_vintage_year` apply to the counts, which list the top 50 values.
- **Params:** `facet` (string, **required**) — Facet enum: fund_strategy, fund_status, run_id; `fund_status` (string, optional) — Exact fund status filter, max 128 characters; `fund_strategy` (string, optional) — Exact fund strategy filter, max 128 characters; `max_vintage_year` (integer, optional) — Maximum vintage year; `min_vintage_year` (integer, optional) — Minimum vintage year; `q` (string, optional) — Full-text query over name and description, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters

### `datasets_pitchbook_funds_item`

- **HTTP:** `GET /datasets/pitchbook-funds/items/{id}`
- **What:** Get a PitchBook fund from dataset. Returns one PitchBook fund from the dataset by `id`, such as `19719-91F`. The record has name, strategy, status, fund size, vintage year, managing firm, contact details and data tables such as limited partners and benchmarks. An id not in the dataset returns 404.
- **Params:** `id` (string, **required**) — PitchBook fund id, e.g. 19719-91F

### `datasets_pitchbook_funds_search`

- **HTTP:** `GET /datasets/pitchbook-funds/search`
- **What:** Search PitchBook funds dataset. Searches the crawled public PitchBook fund profile catalog stored in a search index. Discovered from PitchBook's public sitemap. Sort enum: `relevance`, `name_asc`, `vintage_desc`, `recently_crawled_desc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `fund_status` (string, optional) — Exact fund status filter (e.g. Closed, Raising), max 128 characters; `fund_strategy` (string, optional) — Exact fund strategy filter (e.g. Early Stage VC, Buyout), max 128 characters; `max_vintage_year` (integer, optional) — Maximum vintage year; `min_vintage_year` (integer, optional) — Minimum vintage year; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `q` (string, optional) — Full-text query over name and description, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `sort` (string, optional) — Sort enum: relevance, name_asc, vintage_desc, recently_crawled_desc

### `datasets_pitchbook_investors_facets`

- **HTTP:** `GET /datasets/pitchbook-investors/facets`
- **What:** Facet PitchBook investors dataset. Returns value counts for the PitchBook investors dataset by the required `facet`: `status`, `investor_type`, `hq_country`, `hq_state` or `run_id`. The counts follow search filters including `q`, `min_portfolio_count` and `min_exits_count`, and show the top 50 values.
- **Params:** `facet` (string, **required**) — Facet enum: status, investor_type, hq_country, hq_state, run_id; `hq_country` (string, optional) — Exact headquarters country filter, max 128 characters; `hq_state` (string, optional) — Exact headquarters state/region filter, max 128 characters; `investor_type` (string, optional) — Exact investor type filter, max 128 characters; `min_exits_count` (integer, optional) — Minimum number of exits; `min_portfolio_count` (integer, optional) — Minimum current portfolio size; `q` (string, optional) — Full-text query over name and description, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `status` (string, optional) — Exact status filter, max 128 characters

### `datasets_pitchbook_investors_item`

- **HTTP:** `GET /datasets/pitchbook-investors/items/{id}`
- **What:** Get a PitchBook investor from dataset. Returns one PitchBook investor from the dataset by `id`, such as `294471-37`. The record has name, description, investor type, status, headquarters, investment, portfolio and exit counts, contact and website, FAQs and data tables. An unknown id returns 404.
- **Params:** `id` (string, **required**) — PitchBook investor id, e.g. 294471-37

### `datasets_pitchbook_investors_search`

- **HTTP:** `GET /datasets/pitchbook-investors/search`
- **What:** Search PitchBook investors dataset. Searches the crawled public PitchBook investor (fund manager/firm) profile catalog stored in a search index. Discovered from PitchBook's public sitemap. Sort enum: `relevance`, `name_asc`, `portfolio_count_desc`, `recently_crawled_desc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `hq_country` (string, optional) — Exact headquarters country filter, max 128 characters; `hq_state` (string, optional) — Exact headquarters state/region filter, max 128 characters; `investor_type` (string, optional) — Exact investor type filter (e.g. Venture Capital, Private Equity, Angel), max 128 characters; `min_exits_count` (integer, optional) — Minimum number of exits; `min_portfolio_count` (integer, optional) — Minimum current portfolio size; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `q` (string, optional) — Full-text query over name and description, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `sort` (string, optional) — Sort enum: relevance, name_asc, portfolio_count_desc, recently_crawled_desc; `status` (string, optional) — Exact status filter (e.g. Active, Inactive), max 128 characters

## PitchBook (3)

### `pitchbook_company`

- **HTTP:** `GET /pitchbook/company`
- **What:** PitchBook company profile. Returns the free/teaser content of a PitchBook company profile page (overview, description, contact/HQ, industry, funding-round history without dollar amounts, a preview of investors, acquisitions, and subsidiaries). PitchBook gates most numeric figures (deal amounts, cap tables, full investor/LP lists) behind a paid subscription; those come through as empty cells rather than being fabricated. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — PitchBook company id; `url` (string, optional) — Absolute https://pitchbook.com/profiles/company/<id> URL

### `pitchbook_fund`

- **HTTP:** `GET /pitchbook/fund`
- **What:** PitchBook fund profile. Returns the free/teaser content of a PitchBook fund profile page (strategy, status, manager, size, vintage, and a preview of limited partners and benchmark peer funds). PitchBook gates most numeric figures (returns/IRR, full LP lists) behind a paid subscription; those come through as empty cells rather than being fabricated. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — PitchBook fund id; `url` (string, optional) — Absolute https://pitchbook.com/profiles/fund/<id> URL

### `pitchbook_investor`

- **HTTP:** `GET /pitchbook/investor`
- **What:** PitchBook investor profile. Returns the free/teaser content of a PitchBook investor (fund manager/firm) profile page (overview, description, contact/HQ, and a preview of investments, exits, and co-investors). PitchBook gates most numeric figures and full lists behind a paid subscription; those come through as empty cells rather than being fabricated. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — PitchBook investor id; `url` (string, optional) — Absolute https://pitchbook.com/profiles/investor/<id> URL
