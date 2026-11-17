# arxiv — preprint metadata for physics, math, CS, and more

## What this source has

arXiv hosts ~2.4M preprints across physics, math, CS, quantitative biology, statistics, electrical engineering, economics, and quantitative finance, going back to 1991. The API exposes metadata + PDF/abstract URLs; the actual full text is fetched separately from `arxiv.org/pdf/<id>.pdf`.

Each paper has an arXiv ID. New format (post-2007): `2401.12345` (YYMM.NNNNN, optionally with `vN` version suffix). Old format (pre-2007): `hep-th/0203101` (subject-prefix/YYMMNNN). Both work in the API.

Use arXiv for: cutting-edge research before peer review, CS / ML / physics literature, "latest paper by author X". Pair with `openalex` for citation counts (arXiv has none); pair with `semantic_scholar` for paper recommendations.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 1 request every 3 seconds (recommended); bursts above this risk a temporary block |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `search` | Atom feed of matching papers | `search_query` (or `id_list`) |

## Worked examples

```bash
# Search for transformer papers in cs.LG, sorted by submission date
python3 scripts/reach.py query arxiv search '{
  "search_query": "cat:cs.LG AND ti:transformer",
  "sortBy": "submittedDate",
  "sortOrder": "descending",
  "max_results": 10
}'

# Fetch specific papers by ID
python3 scripts/reach.py query arxiv search '{
  "id_list": "1706.03762,2005.14165"
}'

# All recent papers by a specific author
python3 scripts/reach.py query arxiv search '{
  "search_query": "au:\"Yann LeCun\"",
  "sortBy": "submittedDate",
  "max_results": 20
}'
```

## Response shape

**arXiv returns Atom XML, not JSON.** The connector returns the parsed feed as a dict. Top level: `{feed: {title, id, updated, opensearch:totalResults, opensearch:startIndex, opensearch:itemsPerPage, entry: [...]}}`. Each `entry`:

- `id`: full URL `http://arxiv.org/abs/2401.12345v1` — strip prefix + version for the bare ID
- `title`, `summary` (abstract), `published`, `updated`
- `author`: list of `{name, arxiv:affiliation?}` — affiliations rarely present
- `arxiv:primary_category.@term`: e.g. `cs.LG`
- `category`: list of `{@term}` (multiple subject tags possible)
- `link`: list including `{@rel: alternate, @href: abstract URL}` and `{@title: pdf, @href: PDF URL}`
- `arxiv:doi`, `arxiv:journal_ref`, `arxiv:comment`: optional metadata

## Pitfalls

- **XML, not JSON.** Plan for nested-list traversal. If you ask for one ID via `id_list`, `entry` is a single dict, not a list — check before iterating.
- **3-second pacing.** The arXiv team has historically blocked aggressive scrapers. Stay under 1 req every 3 sec for sustained loads.
- **Search query syntax is its own DSL.** `cat:cs.LG`, `ti:` (title), `au:` (author), `abs:` (abstract), `all:` (all fields). Combine with `AND`/`OR`/`ANDNOT`. Phrases need escaped quotes in JSON: `\"Yann LeCun\"`.
- **No citation count, no recommended-papers, no PDF text.** Use `semantic_scholar` for citation graph; fetch the PDF directly for full text.
- **Version suffix matters.** `2401.12345v1` and `2401.12345v3` are different documents. The bare ID resolves to the latest version.
- **`sortBy` values are case-sensitive.** Valid: `relevance`, `lastUpdatedDate`, `submittedDate`. Lower-case `submitteddate` returns a 400.
- **Pagination via `start` + `max_results`.** Maximum `max_results` per call is 2000, but practical ceiling for stability is around 200; window with date filters for larger pulls.

## Source links

- API user manual: https://info.arxiv.org/help/api/user-manual.html
- Query syntax: https://info.arxiv.org/help/api/user-manual.html#query_details
- Terms of use: https://info.arxiv.org/help/api/tou.html
