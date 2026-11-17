# institutional-ownership-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**5 endpoints across 2 platform group(s).**

## Datasets (2)

### `datasets_sec_institutional_positions_facets`

- **HTTP:** `GET /datasets/sec-institutional-positions/facets`
- **What:** Facet the SEC institutional positions dataset. Returns terms-aggregation counts for one facet of the SEC institutional positions dataset, scoped to the same filters as search. Facet enum: `manager`, `issuer`.
- **Params:** `cusip` (string, optional) — Exact CUSIP filter, max 16 characters; `facet` (string, **required**) — Facet enum: manager, issuer; `issuer_name` (string, optional) — Issuer-name text filter (best-effort match), max 256 characters; `manager_cik` (string, optional) — Exact institutional-manager CIK filter, numeric or zero-padded

### `datasets_sec_institutional_positions_search`

- **HTTP:** `GET /datasets/sec-institutional-positions/search`
- **What:** Search the SEC institutional positions dataset. Searches institutional investment managers' quarterly 13F portfolio holdings stored in a search index. Filter by manager_cik for a manager's full reported portfolio (an exact, reliable filter), or by issuer_name/cusip for a best-effort view of which managers reported a position in an issuer — SEC publishes no authoritative CUSIP-to-CIK mapping, so the issuer side is never a guaranteed-resolved join. Sort enum: `value_desc`, `value_asc`, `shares_desc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `cusip` (string, optional) — Exact CUSIP filter, max 16 characters; `issuer_name` (string, optional) — Issuer-name text filter (best-effort match, not a resolved CIK join), max 256 characters; `manager_cik` (string, optional) — Exact institutional-manager CIK filter, numeric or zero-padded; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `sort` (string, optional) — Sort enum: value_desc, value_asc, shares_desc

## SEC EDGAR (3)

### `sec_company_submissions`

- **HTTP:** `GET /sec/company/submissions`
- **What:** List a company's EDGAR filings. Returns a company's recent SEC filings (form, dates, primary document URL) filtered by form type and date range, plus company profile fields as reported by EDGAR: entity_type, former_names, exchanges, category, fiscal_year_end, state_of_incorporation. Provide cik or ticker.
- **Params:** `cik` (string, optional) — SEC CIK (numeric or zero-padded); `form` (string, optional) — Filter by form type, e.g. 10-K, 10-Q, 8-K; `from` (string, optional) — Earliest filing date (YYYY-MM-DD); `limit` (integer, optional) — Max filings, default 50, max 500; `ticker` (string, optional) — Ticker symbol (alternative to cik); `to` (string, optional) — Latest filing date (YYYY-MM-DD)

### `sec_filing`

- **HTTP:** `GET /sec/filing`
- **What:** Get a single filing by accession number. Returns a single SEC filing's metadata and primary document URL. Provide accession plus cik or ticker.
- **Params:** `accession` (string, **required**) — Accession number; `cik` (string, optional) — SEC CIK (numeric or zero-padded); `ticker` (string, optional) — Ticker symbol (alternative to cik)

### `sec_institutional_holdings`

- **HTTP:** `GET /sec/institutional-holdings`
- **What:** Institutional holdings (13F-HR). Returns the latest 13F-HR holdings for an institutional manager (by CIK): issuer, value, shares, sorted by value.
- **Params:** `cik` (string, **required**) — Institutional manager CIK; `limit` (integer, optional) — Max holdings, default 50, max 1000
