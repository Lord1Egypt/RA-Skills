# federal_register — daily US rules, proposed rules, notices, and presidential documents

## What this source has

The Federal Register is the daily journal of the US government — every rule, proposed rule, notice, and presidential document published by federal agencies since 1994 (with limited coverage back to 1936 in the public-inspection archive). ~80,000 documents per year. Each document has an FR document number (`2024-12345`), a publication date, an issuing agency, a CFR cite (when codifying), and full text.

Document types: `RULE` (final rule, has force of law), `PRORULE` (proposed rule, comment period open), `NOTICE` (informational, e.g., meeting announcements), `PRESDOCU` (executive orders, proclamations).

Use Federal Register for: tracking new federal regulations, comment-period deadlines, "what did agency X publish recently", presidential executive orders. Pair with `govinfo` for the CFR (codified version of finalized rules) and historical archives.

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
| Rate | ~1000 req/hour suggested ceiling; no auth required to hit it |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `documents` | Search documents | `conditions[term]` or other filter conditions |
| `document` | Fetch one document by FR number | `doc_id` |
| `agencies` | List agencies | none |

## Worked examples

```bash
# Recent EPA rules in 2026
python3 scripts/reach.py query federal_register documents '{
  "conditions[agencies][]": "environmental-protection-agency",
  "conditions[type][]": "RULE",
  "conditions[publication_date][year]": 2026,
  "per_page": 20
}'

# Search by free-text term
python3 scripts/reach.py query federal_register documents '{
  "conditions[term]": "PFAS drinking water",
  "per_page": 10
}'

# Fetch a specific document
python3 scripts/reach.py query federal_register document '{"doc_id": "2024-12345"}'

# Comment periods closing soon
python3 scripts/reach.py query federal_register documents '{
  "conditions[type][]": "PRORULE",
  "conditions[comments_close_on][gte]": "2026-04-26",
  "conditions[comments_close_on][lte]": "2026-05-26",
  "per_page": 25
}'
```

## Response shape

- `documents`: `{count, total_pages, next_page_url, results: [{document_number, title, type, abstract, publication_date, html_url, pdf_url, agencies: [{slug, name, url, raw_name, ...}], action, dates, effective_on, comments_close_on, citation, page_views}, ...]}`. `document_number` is the FR ID.
- `document` (single): same per-item fields plus `body_html_url`, `full_text_xml_url`, `regulations_dot_gov_info` (docket linkage).
- `agencies`: `[{id, name, short_name, slug, url, child_ids, parent_id, recent_articles_url}, ...]`.

## Pitfalls

- **Agency identifier is a slug**, not an acronym. Use `environmental-protection-agency`, not `epa`. Hit `agencies` once and cache the slug list.
- **`conditions[...]` query string is array-bracket syntax.** Multiple values for the same field repeat the bracket: `conditions[type][]=RULE&conditions[type][]=PRORULE`. The connector accepts these as parallel keys in JSON; pass distinct keys or a list.
- **`document_number` format is `YYYY-NNNNN`** with a dash, not the OFR receipt number. The dash matters — some downstream tools strip it.
- **`publication_date` is the spine.** Documents are released daily at midnight ET; same-day queries may return empty until ~6 AM ET.
- **Full text comes from a separate URL.** The `body_html_url` / `full_text_xml_url` fields point at the actual document body — the API response itself only carries metadata + abstract.
- **Comment periods extend.** A `PRORULE`'s `comments_close_on` may shift; recheck close to deadline.
- **Effective date ≠ publication date.** Rules typically take effect 30-60 days after publication; check `effective_on`.

## Source links

- API docs: https://www.federalregister.gov/developers/documentation/api/v1
- Conditions reference: https://www.federalregister.gov/developers/documentation/api/v1/index.html#fetching-multiple-documents
- Terms: https://www.federalregister.gov/reader-aids/legal-status
