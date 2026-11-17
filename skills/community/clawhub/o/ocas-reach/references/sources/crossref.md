# crossref — DOI metadata for ~150M scholarly works

## What this source has

Crossref is the largest DOI registration agency. ~150M registered works as of 2026: journal articles, books, book chapters, conference papers, datasets, preprints, dissertations, peer reviews. Each item has a DOI as the canonical ID; metadata includes title, authors, ORCIDs (when supplied), affiliation strings, references (when deposited), licenses, full-text URLs, funder data.

Crossref is the metadata layer — it does NOT store full text. The `link` array points at publisher full-text URLs, which may be paywalled. Records are deposited by publishers, so completeness varies wildly: a 2022 Wiley journal article is fully populated; a 1950s monograph may have title and DOI only.

Use Crossref for: DOI → metadata resolution, listing all works for a journal/publisher (member-id), reverse-lookup by ORCID, citation graph (when references are deposited). Pair with `openalex` for fuller citation networks; pair with `pubmed` for biomedical full-text linkages.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

The polite pool requires a `mailto` parameter on every request. Reach injects `mailto=<agent-email>` automatically; without it you're in the public pool with degraded latency.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 50 req/sec polite pool; public pool slower under load |

Crossref returns `X-Rate-Limit-Limit` / `X-Rate-Limit-Interval` headers — respect them.

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `works` | Search/list works | `query` or `filter` |
| `doi` | Fetch one work by DOI | `doi` |
| `members` | List/find publishers | `query` |

## Worked examples

```bash
# Resolve a single DOI
python3 scripts/reach.py query crossref doi '{"doi": "10.1038/nature14539"}'

# Search for "attention is all you need"
python3 scripts/reach.py query crossref works '{
  "query": "attention is all you need",
  "rows": 5
}'

# All journal articles by a specific ORCID
python3 scripts/reach.py query crossref works '{
  "query.author": "0000-0002-1825-0097",
  "filter": "type:journal-article",
  "rows": 25
}'

# Find publishers matching "elsevier"
python3 scripts/reach.py query crossref members '{"query": "elsevier"}'
```

## Response shape

- `works` (search): `{status, message-type, message: {total-results, items: [{DOI, title: [...], author: [{given, family, ORCID, affiliation: [...]}], container-title: [...], published: {date-parts: [[Y, M, D]]}, type, publisher, reference: [...], reference-count, is-referenced-by-count, link: [{URL, content-type, intended-application}]}, ...]}}`
- `doi` (single): same `message` but a single object, not a list of `items`.
- `members`: `{message: {items: [{id, primary-name, names: [...], counts: {total-dois, current-dois, backfile-dois}}]}}`.

The `title`, `container-title`, and `subject` fields are arrays of strings (sometimes single-element). Don't assume scalar.

## Pitfalls

- **Polite pool requires `mailto`.** Without it you're rate-limited harder. The connector injects it automatically.
- **DOI casing.** DOIs are case-insensitive but Crossref echoes them upper-cased after the slash. Normalize before comparing.
- **`published` vs `published-online` vs `published-print`.** A work can have all three; pick the earliest for "first available" or the print one for citation context.
- **`reference` array is opt-in.** Many publishers don't deposit references. `reference-count: 42` with `reference: undefined` means they exist but aren't shared.
- **Type filter is your friend.** `filter: "type:journal-article"` cuts noise substantially — books, components, and chapters dominate raw results otherwise.
- **`query` is full-text-ish, not exact.** For DOI-precise lookup use the `doi` action, not `works` with `query`.
- **Pagination via `cursor`, not offset.** Set `cursor=*` on first call, then pass back the returned `next-cursor` value. Offset paging caps at 10k.

## Source links

- API docs: https://api.crossref.org/swagger-ui/index.html
- REST API guide: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Etiquette / polite pool: https://api.crossref.org/swagger-ui/index.html#/Etiquette
