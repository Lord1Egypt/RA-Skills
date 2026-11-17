# pubmed — biomedical literature via NCBI E-utilities

## What this source has

PubMed indexes ~36M biomedical citations: MEDLINE (peer-reviewed life-science journals back to 1966, with selective coverage to 1809), PubMed Central full-text articles, and NCBI Bookshelf. Each record has a PMID (integer, the canonical key) plus DOI when available, MeSH headings (controlled vocabulary), abstract text, author affiliations.

Access is via NCBI's E-utilities — a 3-step pattern: `esearch` returns PMIDs for a query, `efetch` returns full records (XML by default), `esummary` returns lightweight JSON metadata. This connector wraps that into single calls.

Use PubMed for: clinical evidence, biomedical literature search, drug/disease/gene lookups. Pair with `openalex` for broader scholarly coverage; pair with `crossref` when you need DOI-level metadata for a non-biomedical citation.

## Auth

| | |
|---|---|
| Required | none |
| Env var | `NCBI_API_KEY` (optional, raises rate to 10/sec) |
| Account | optional |
| Account URL | https://www.ncbi.nlm.nih.gov/account/ |

If a key is desired, Reach is authorized to register at the URL above using `<agent-email>`. See `references/account_provisioning.md`. Anonymous access works fine for typical query loads.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 3 req/sec without key; 10 req/sec with key |

NCBI enforces rate limits per IP for anonymous callers and per API key when one is present.

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `search` | esearch + return PMID list (and optionally fetch summaries) | `term` |
| `fetch` | efetch full records by PMID list | `pmids` (array) |
| `summary` | esummary lightweight JSON for PMIDs | `pmids` (array) |

## Worked examples

```bash
# Search for recent CRISPR papers
python3 scripts/reach.py query pubmed search '{
  "term": "CRISPR cas9 gene editing",
  "limit": 20
}'

# Filter with PubMed query syntax (MeSH + date)
python3 scripts/reach.py query pubmed search '{
  "term": "diabetes mellitus[MeSH] AND 2024[PDAT]",
  "limit": 10
}'

# Fetch full records for specific PMIDs
python3 scripts/reach.py query pubmed fetch '{"pmids": ["38123456", "38123457"]}'

# Cheap summary for a batch
python3 scripts/reach.py query pubmed summary '{"pmids": ["38123456", "38123457"]}'
```

## Response shape

- `search`: `{count, retmax, retstart, idlist: ["38123456", ...], translation_set, query_translation}`. `query_translation` shows how PubMed expanded your terms — useful for debugging zero-hit queries.
- `fetch`: returns parsed XML as nested dicts under `PubmedArticleSet.PubmedArticle[]`. Each article has `MedlineCitation.Article` with `ArticleTitle`, `Abstract.AbstractText`, `AuthorList`, `MeshHeadingList`, plus `PubmedData.ArticleIdList` (DOI, PMC, PMID).
- `summary`: `{result: {<pmid>: {uid, pubdate, source, authors: [...], title, fulljournalname, sortpubdate, doi, ...}, uids: [...]}}`.

## Pitfalls

- **`efetch` returns XML by default for `pubmed`.** JSON isn't supported for the `pubmed` db on `efetch`; you must parse XML. The connector does this for you but the returned shape mirrors XML structure with arrays where elements repeat.
- **PMID vs PMCID vs DOI.** PMID is the integer (`38123456`); PMCID is the full-text identifier (`PMC10456789`); DOI is publisher's. PMCIDs are only present when the article is in PubMed Central.
- **`AbstractText` may be a list of structured sections.** Each section has a `@Label` (Background, Methods, Results, Conclusions) and text. Don't assume a single string.
- **Date fields vary.** `PubDate` may be `Year/Month/Day`, `Year/Month`, `Year`, or `MedlineDate` ("2024 Spring"). Parse defensively.
- **Author affiliations are per-author per-affiliation strings, not normalized.** No ROR IDs.
- **Search term expansion.** PubMed automatically maps free text to MeSH; `query_translation` exposes what it actually searched. If results are surprising, check that field.
- **Batch `efetch` cap.** 200 PMIDs per call is the soft ceiling; over that, NCBI may truncate or 414.

## Source links

- E-utilities docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- PubMed search syntax: https://pubmed.ncbi.nlm.nih.gov/help/
- API key registration: https://www.ncbi.nlm.nih.gov/account/settings/
