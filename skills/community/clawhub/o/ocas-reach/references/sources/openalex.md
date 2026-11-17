# openalex — open scholarly graph (240M+ works)

## What this source has

OpenAlex is the open-access successor to Microsoft Academic Graph. ~240M scholarly works (papers, books, datasets), ~95M authors, ~250k journals/sources, plus institutions, funders, concepts. Citation graph included — every work links to its references and is back-linked from citing works.

Each entity has a stable W-id (`W2741809807`) plus DOIs/ROR/ORCID where applicable. Updated monthly.

Use OpenAlex for: paper search, citation analysis, "papers about X by author Y", author publication histories, journal metadata. Pair with `semantic_scholar` when you need higher-quality recommendations or richer abstracts (S2 has fewer works but more curation); pair with `crossref` for DOI metadata.

## Auth

| | |
|---|---|
| Required | none |
| Account | optional |

Adding `mailto=<agent-email>` (or any email) as a query param puts you in the **polite pool** — same rate, faster service in practice. The connector adds this automatically when an email is provided in the registry.

## Limits

| | |
|---|---|
| Daily | 100,000 |
| Monthly | — |
| Rate | 10 req/sec polite pool |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `works` | Find / list works | `search` or `filter` |
| `authors` | Find / list authors | `search` or `filter` |
| `sources` | Find / list venues (journals etc.) | `search` or `filter` |
| `concepts` | Find / list concept tags | `search` or `filter` |

## Worked examples

```bash
# Top-cited papers about "transformer architecture" since 2017
python3 scripts/reach.py query openalex works '{
  "search": "transformer architecture",
  "filter": "publication_year:>2016",
  "sort": "cited_by_count:desc",
  "per_page": 10
}'

# Author search
python3 scripts/reach.py query openalex authors '{"search": "Geoffrey Hinton", "per_page": 5}'

# Get a specific work by OpenAlex ID
python3 scripts/reach.py query openalex works '{"filter": "openalex_id:W2741809807"}'

# Works by a specific author
python3 scripts/reach.py query openalex works '{
  "filter": "author.id:A5023888391",
  "sort": "cited_by_count:desc",
  "per_page": 20
}'
```

## Response shape

Lists return: `{meta: {count, db_response_time_ms, page, per_page}, results: [{id, doi, title, ...}, ...]}`. The most useful per-work fields:

- `id`: OpenAlex URL form (`https://openalex.org/W123...`)
- `doi`: full DOI URL or null
- `title`, `abstract_inverted_index` (reconstructable to abstract text)
- `authorships`: ordered list of `{author: {id, display_name, orcid}, institutions: [...]}`
- `host_venue`: journal/conference info
- `cited_by_count`, `referenced_works`: integers + W-id list
- `publication_year`, `publication_date`
- `concepts`: tagged concepts with confidence scores

## Pitfalls

- **Abstracts are inverted indexes, not strings.** OpenAlex stores `abstract_inverted_index` as `{word: [pos1, pos2, ...]}` to comply with copyright. Reconstruct by sorting tokens by position.
- **Author IDs vs ORCIDs.** OpenAlex authors have `id` (their A-id) and optional `orcid`. The same human may have multiple A-ids if disambiguation is incomplete; ORCID, when present, is the cross-source canonical.
- **Filter syntax.** Filters use dotted-path keys: `author.id:A123`, `host_venue.publisher:Elsevier`, `publication_year:>2020`. Multiple filters comma-separated.
- **`per_page` max is 200.** Use cursor-paging via `cursor=*` for >10k results.
- **`search` is approximate.** It searches title + abstract + concepts, not full text. For precise lookups use `filter` on `doi` or `openalex_id`.
- **Concepts hierarchy.** Each concept has a level (0 = top, 5 = leaf). When tagging a paper, OpenAlex may pick concepts from multiple levels; filter by `level:1` to get high-level subject areas.

## Source links

- Docs: https://docs.openalex.org/
- API root: https://api.openalex.org/
- Rate / polite pool: https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication
