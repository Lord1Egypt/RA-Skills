# courtlistener — federal + state case law and PACER docket archive

## What this source has

CourtListener (Free Law Project) is the largest free database of US case law. ~9M opinions across SCOTUS, all federal circuits and districts, and most state appellate courts; ~5M PACER dockets archived through the RECAP project. Each opinion has a unique numeric ID, a citation (`410 U.S. 113`), a case name, court, date, and full text (HTML + plain). Dockets have docket number, court, parties, every entry's filing date and document.

The search endpoint indexes opinions, oral arguments, dockets, RECAP documents, and judges as separate types — pass `type=o` for opinions, `type=r` for RECAP, `type=d` for dockets, `type=oa` for oral arguments, `type=p` for people (judges).

Use CourtListener for: case law search, full opinion text, federal docket history (RECAP). Pair with `congress_gov` and `govinfo` when the underlying matter involves statutes you want to cite alongside cases.

## Auth

| | |
|---|---|
| Required | yes |
| Env var | `COURTLISTENER_KEY` |
| Account URL | https://www.courtlistener.com/help/api/rest/ |
| Plan tier | free |

Reach is authorized to register at the URL above using `<agent-email>`. See `references/account_provisioning.md`. Sign-up creates a normal user account; the API token is generated from the profile page.

The auth header is `Authorization: Token <key>` — note the `Token ` prefix (with a space). The connector handles this automatically.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 5,000 req/hour per token |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `search` | Cross-type search (opinions/dockets/RECAP/judges) | `q` (and `type`) |
| `opinion` | Fetch one opinion | `id` |
| `docket` | Fetch one docket | `id` |
| `court` | Fetch a court record | `id` (e.g. `scotus`) |

## Worked examples

```bash
# Search SCOTUS opinions for "qualified immunity" since 2020
python3 scripts/reach.py query courtlistener search '{
  "q": "qualified immunity",
  "type": "o",
  "court": "scotus",
  "filed_after": "2020-01-01",
  "order_by": "score desc"
}'

# Fetch one opinion
python3 scripts/reach.py query courtlistener opinion '{"id": 1234567}'

# Search RECAP dockets
python3 scripts/reach.py query courtlistener search '{
  "q": "FTC v. Meta",
  "type": "r"
}'

# Court record
python3 scripts/reach.py query courtlistener court '{"id": "scotus"}'
```

## Response shape

- `search`: `{count, next, previous, results: [{id, absolute_url, caseName, dateFiled, court, court_id, citation: [...], snippet, opinion_id, type, ...}, ...]}`. Field set varies by `type`.
- `opinion`: `{id, resource_uri, absolute_url, cluster, author, date_created, date_modified, sha1, plain_text, html, html_lawbox, html_columbia, type, page_count, ...}`. The `cluster` URL points at the opinion cluster (case-level metadata).
- `docket`: `{id, court, case_name, docket_number, date_filed, date_terminated, parties, assigned_to_str, nature_of_suit, jurisdiction_type, source, ...}`.
- `court`: `{id, full_name, short_name, jurisdiction, position, in_use, has_opinion_scraper, has_oral_argument_scraper, ...}`.

## Pitfalls

- **Auth header prefix is `Token `, not `Bearer `.** With a trailing space before the token. The connector handles it; if you ever raw-curl, get the prefix right.
- **`type` is the most important search filter.** Without it the search defaults to `opinions` (`o`); for dockets pass `d`, for RECAP `r`, for oral arguments `oa`, for judges `p`. Mixing types in one call isn't supported — make separate calls.
- **Date filters use `filed_after` / `filed_before`** in `YYYY-MM-DD` format. Don't pass datetime.
- **Court IDs are lower-case slugs**: `scotus`, `ca9`, `cafc`, `nysd`, `cand`. The full list is at `/courts/`.
- **RECAP archive is separate from opinions.** RECAP documents are PACER scraped/uploaded by users; coverage is high for high-profile cases, sparse for routine ones.
- **`plain_text` vs `html` vs `html_lawbox` vs `html_columbia`.** Multiple representations from different scrape sources; pick `plain_text` for most processing or `html` for citation parsing.
- **`citation` is an array** — major cases have multiple parallel citations (e.g., `410 U.S. 113`, `93 S. Ct. 705`, `35 L. Ed. 2d 147`).
- **Pagination via `cursor` (newer endpoints) or `page` (older).** Watch for `next: null` to stop.
- **Opinion ID ≠ cluster ID.** A "case" has one cluster but possibly multiple opinions (majority, concurrence, dissent). Opinion endpoint returns one of them; for the case-level record, follow `cluster`.

## Source links

- API docs: https://www.courtlistener.com/help/api/rest/
- Search reference: https://www.courtlistener.com/help/api/rest/search/
- About RECAP: https://free.law/recap/
