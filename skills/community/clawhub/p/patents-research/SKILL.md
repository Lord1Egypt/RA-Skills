---
name: patents-research
description: Researches patents and patent applications via the Crawlora API — Google Patents (full-text search by keyword/inventor/assignee, bibliographic detail, claims/citations/family, CPC classification lookup, recent-publications browse, database coverage) and USPTO Patent Public Search (full-text search with USPTO's own Advanced Search syntax, document detail) — returning clean JSON. Use when the user wants prior-art search, a specific patent's claims/citations/family, an inventor's or company's patent portfolio, or freedom-to-operate research.
---

# Patent research

Search and look up patents across Google Patents and USPTO Patent Public
Search — full-text search, bibliographic detail, claims, citations, patent
family, and classification lookup — all as normalized JSON from the
Crawlora API, no scraping of patent-office pages.

## When to use this skill

- "Find patents about X" / "prior-art search for X" (keyword, inventor, or
  assignee).
- "What does patent US10758101B2 claim?" / "Show me this patent's citations
  and family members."
- "What's this company's / inventor's patent portfolio?"
- "What CPC classification covers X?" (e.g. `A61K31/00`).
- "What patents were published this week?" (recent-publications browse).
- Freedom-to-operate or landscape research needing both Google Patents'
  broader index and USPTO's own official full-text search with its
  field-code query syntax.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Google Patents search** — `/googlepatents/search` (`q`, plus optional
   `inventor`/`assignee`/`country`/`status`/`type`/`language`/`sort`/date
   filters via `before`+`after`+`date_field`) returns normalized hits plus
   top-assignee/top-inventor/top-classification breakdowns over the full
   result set.
2. **Google Patents detail** — `/googlepatents/detail` (`number`, a
   publication number like `US10758101B2`) returns title, abstract,
   inventors, assignees, dates, legal status, CPC/IPC classifications,
   claims, description, citations, cited-by patents, family members, and
   similar documents.
3. **Google Patents helpers** — `/googlepatents/suggest`
   (`field=inventor|assignee`, `value`) for autocomplete;
   `/googlepatents/classification` (`code`, e.g. `A61K31/00`, or any
   section/class/subclass level) for a CPC symbol's title and tree
   position; `/googlepatents/recent` (`week`, ISO 8601 `YYYY-Www`) to
   browse one week's indexed publications; `/googlepatents/coverage` for
   per-country per-year grant/application counts.
4. **USPTO Patent Public Search** — `/usptoppubs/search` (`q`, USPTO's own
   Advanced Search / BRS syntax: field codes like `battery.ti.` or
   `Microsoft.as.`, date ranges like `@pd>=20200101<=20241231`,
   boolean/proximity operators, wildcards; optional `databases` to scope to
   `US-PGPUB`/`USPAT`/`USOCR`) returns bibliographic results, then
   `/usptoppubs/detail` (`guid`+`source`, both taken from a search result)
   fetches one document's full text — abstract, description, and claims.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Google Patents keyword search:
scripts/crawlora.sh /googlepatents/search q="solid state battery" | jq '.'

# Filter by assignee + date range:
scripts/crawlora.sh /googlepatents/search q="battery" assignee="Tesla" after="2020-01-01" | jq '.'

# Patent detail (claims, citations, family):
scripts/crawlora.sh /googlepatents/detail number=US10758101B2 | jq '.'

# CPC classification lookup:
scripts/crawlora.sh /googlepatents/classification code=A61K31/00 | jq '.'

# USPTO full-text search (BRS field-code syntax):
scripts/crawlora.sh /usptoppubs/search q='battery.ti. AND @pd>=20200101<=20241231' | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Google
Patents and USPTO Patent Public Search endpoint this skill uses.

## Examples

- **Prior-art search:** `/googlepatents/search` with a keyword + `assignee`/
  `inventor` filters, then `/googlepatents/detail` on the strongest hits for
  full claims and citations.
- **Portfolio research:** `/googlepatents/search` scoped to one `assignee`,
  sorted `new`, to see a company's recent filings; `/googlepatents/detail`
  on any individual patent for its full family (continuations, divisionals,
  foreign counterparts).
- **Cross-source verification:** run the same query through both
  `/googlepatents/search` (broader index, easier free-text) and
  `/usptoppubs/search` (USPTO's own authoritative full-text index with
  precise field-code queries) to cross-check coverage.
- **Landscape/trend view:** `/googlepatents/coverage` for indexing volume by
  country/year, or `/googlepatents/recent` to sample one week's publications
  in a technology area.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public patent-office search/detail pages.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **USPTO's `q` syntax is not free text** — it's USPTO's own Advanced
  Search (BRS) query language (field codes, date-range operators, boolean/
  proximity operators, wildcards). Google Patents' `q` is plain free-text
  with separate structured filter params instead.
- `/usptoppubs/detail`'s `guid`/`source` must come from a prior
  `/usptoppubs/search` result — they aren't guessable identifiers.
- Search results are paginated (`page`/`num`, 0-indexed) — walk pages for
  full coverage beyond the first page.
