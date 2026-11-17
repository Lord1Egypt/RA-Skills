# patent-landscape-analysis — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**8 endpoints across 2 platform group(s).**

## Google Patents (6)

### `googlepatents_classification`

- **HTTP:** `GET /googlepatents/classification`
- **What:** Look up a Cooperative Patent Classification (CPC) symbol. Returns a CPC classification symbol's official title, its position in the classification tree (parent/child symbols), related symbols, and its full scope-note description. Accepts a symbol at any level, e.g. a section ("A"), a class ("A61"), a subclass ("A61K"), or a full group/subgroup ("A61K31/00"). Public data, sourced from Google Patents' own search API.
- **Params:** `code` (string, **required**) — CPC classification symbol

### `googlepatents_coverage`

- **HTTP:** `GET /googlepatents/coverage`
- **What:** Google Patents database coverage: grants and applications indexed per country per year. Returns how many patent grants and applications Google Patents has indexed, per patent office/country, per year, across every authority it covers. Public data, sourced from Google Patents' own search API.
- **Params:** _none_

### `googlepatents_detail`

- **HTTP:** `GET /googlepatents/detail`
- **What:** A single patent's bibliographic data, abstract, claims, description, citations, and family. Returns a single patent's detail: title, abstract, inventors, assignees, dates, legal status, CPC/IPC classifications, claims, description, patent citations, cited-by patents, family members, and similar documents. `number` is a publication number such as `US10758101B2`, `EP1000000A1`, or `WO2020123456A1`. To search or browse by keyword, inventor, or assignee instead of a known publication number, use `/googlepatents/search`.
- **Params:** `lang` (string, optional) — Language code for the translated page, default en; `number` (string, **required**) — Publication number, e.g. US10758101B2

### `googlepatents_recent`

- **HTTP:** `GET /googlepatents/recent`
- **What:** Browse patent publications indexed by Google Patents for one ISO week. Returns the patent publications Google Patents' bulk sitemap indexes for one ISO 8601 week (format YYYY-Www, e.g. "2026-W20"): publication number, title, and detail-page URL for each. Useful for browsing recently published patents without a search query. Public data, sourced from Google Patents' own sitemap.
- **Params:** `week` (string, **required**) — ISO 8601 week, format YYYY-Www

### `googlepatents_search`

- **HTTP:** `GET /googlepatents/search`
- **What:** Search Google Patents by keyword, inventor, assignee, and other filters. Searches Google Patents' full index by free-text query, with optional inventor, assignee, patent office, status, type, language, and date filters. Returns a page of hits plus top-assignee/top-inventor/top-classification breakdowns over the full result set.
- **Params:** `after` (string, optional) — Only results dated on or after this date (YYYY-MM-DD); `assignee` (string, optional) — Filter by assignee/applicant name; `before` (string, optional) — Only results dated on or before this date (YYYY-MM-DD); `country` (string, optional) — Filter by patent office/authority code, e.g. US, EP, WO, CN, JP; `date_field` (string, optional) — Which date before/after filter. Allowed values: priority, filing, publication. Defaults to priority when before/after is set; `inventor` (string, optional) — Filter by inventor name; `language` (string, optional) — Filter by document language. Allowed values: ENGLISH, GERMAN, CHINESE, FRENCH, SPANISH, ARABIC, JAPANESE, KOREAN, PORTUGUESE, RUSSIAN, ITALIAN, DUTCH, SWEDISH, FINNISH, NORWEGIAN, DANISH; `num` (integer, optional) — Results per page, default 10, max 100; `page` (integer, optional) — Page number, 0-indexed, default 0; `q` (string, **required**) — Free-text search query; `sort` (string, optional) — Sort order. Allowed values: relevance, new, old. Defaults to relevance; `status` (string, optional) — Filter by legal status. Allowed values: GRANT, APPLICATION; `type` (string, optional) — Filter by document type. Allowed values: PATENT, DESIGN

### `googlepatents_suggest`

- **HTTP:** `GET /googlepatents/suggest`
- **What:** Autocomplete an inventor or assignee name for Google Patents search. Returns Google Patents' own autocomplete suggestions for an inventor or assignee name as the user types, the same suggestions shown by the Inventor/Assignee fields on Google Patents' advanced search page. Public data, sourced from Google Patents' own search API.
- **Params:** `field` (string, **required**) — Which field to autocomplete. Allowed values: inventor, assignee; `value` (string, **required**) — Partial name typed so far

## USPTO Patent Public Search (2)

### `usptoppubs_detail`

- **HTTP:** `GET /usptoppubs/detail`
- **What:** Fetch a document's full bibliographic data, abstract, description, and claims. Fetches a single USPTO Patent Public Search record's full text -- bibliographic data, abstract, description, and claims -- by GUID and source database. guid and source normally come straight from a prior /usptoppubs/search result's guid and database fields. Public data, sourced from USPTO's own official search tool.
- **Params:** `guid` (string, **required**) — Document GUID, e.g. from a prior search result's guid field; `source` (string, **required**) — Source database. Allowed values: US-PGPUB, USPAT, USOCR

### `usptoppubs_search`

- **HTTP:** `GET /usptoppubs/search`
- **What:** Search USPTO's own patent full-text search index. Searches USPTO Patent Public Search's full-text index of granted patents and published applications, returning bibliographic results (title, applicant/assignee, inventors, filing and publication dates, application number, IPC/CPC classifications, page count). q accepts USPTO's full Advanced Search query syntax -- field-specific search (e.g. battery.ti., Microsoft.as.), date ranges (@pd>=20200101<=20241231), boolean and proximity operators, and wildcards -- see the markdown doc for the full field-code table and syntax reference.
- **Params:** `databases` (string, optional) — Comma-separated subset of databases to search. Allowed values: US-PGPUB, USPAT, USOCR. Defaults to all three; `num` (integer, optional) — Results to return, default 20, max 100; `page` (integer, optional) — Results page, 0-indexed, default 0; `q` (string, **required**) — Search query text -- accepts USPTO's full Advanced Search (BRS) query syntax: field codes, date ranges, boolean/proximity operators, wildcards
