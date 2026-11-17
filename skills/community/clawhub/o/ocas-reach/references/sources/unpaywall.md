# unpaywall — Open Access Paper Lookup

## What this source has

Unpaywall provides open-access status and legal free PDF links for ~30 million academic papers. It aggregates open-access copies from repositories, journals, and preprint servers worldwide. Does NOT bypass paywalls — only returns legally available open-access versions.

Coverage: DOI-registered scholarly content. ~30M articles, ~40% have an OA copy available. Best for finding legal free versions of papers that are behind paywalls.

## Auth

| | |
|---|---|
| Required | none |
| Env var | — |
| Account URL | — |
| Plan tier | free (polite pool with email) |

When making API calls, include `?email=<agent-email>` for polite pool access (higher rate limits).

## Limits

| | |
|---|---|
| Daily | ~100k requests polite pool |
| Monthly | — |
| Rate | No hard cap documented; keep reasonable |

## Endpoints

```bash
# Look up a paper by DOI — returns OA status + best PDF URL
python3 scripts/reach.py query unpaywall doi '{"doi": "10.1038/nature09492"}'

# Search for papers by title/keyword
python3 scripts/reach.py query unpaywall search '{"query": "transformer attention mechanism", "is_oa": true}'
```

## Worked examples

```bash
# Find OA version of a paper by DOI
python3 scripts/reach.py query unpaywall doi '{"doi": "10.1145/3442381.3449852"}'

# Search for recent OA papers on a topic
python3 scripts/unpaywall search '{"query": "mixture of experts language model", "is_oa": true, "year": "2024"}'
```

## Response shape

`doi` action returns:
```json
{
  "doi": "10.1038/nature09492",
  "title": "Bottom-up effects of plant diversity...",
  "is_oa": true,
  "oa_status": "green",
  "journal_name": "Nature",
  "year": 2010,
  "best_oa_location": {
    "url": "https://resolver.sub.uni-goettingen.de/purl?gro-2/6837",
    "url_for_pdf": "https://.../paper.pdf",
    "host_type": "repository",
    "license": "cc-by",
    "version": "submittedVersion"
  },
  "oa_locations": [...]
}
```

`search` action returns a list of paper objects with the same shape.

## Integration with scihub

Use `unpaywall` first to check if a legal OA copy exists. Only fall back to `scihub` if `is_oa: false` or no PDF URL is available. This is the preferred ordering:

1. `unpaywall` → check for OA copy (legal)
2. `scihub` → get PDF from mirror (if no OA copy)

## Pitfalls

- **Not all papers have OA copies:** ~60% of papers have no OA version. Check `is_oa` before expecting a PDF URL.
- **PDF URL may be null:** Even when `is_oa: true`, `best_oa_location.url_for_pdf` can be null (landing page only). Check both `url_for_pdf` and `url`.
- **Version matters:** OA copies may be the "submittedVersion" (preprint) not the published version.
- **Email parameter:** Always include `?email=` for polite pool. Without it, rate limits are much stricter.
- **Search is via CrossRef:** The search action queries CrossRef, not Unpaywall directly. Results are metadata-only; use the `doi` action for OA status per result.
