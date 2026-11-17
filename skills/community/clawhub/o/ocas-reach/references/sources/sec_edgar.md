# sec_edgar — every US public-company filing

## What this source has

EDGAR is the Securities and Exchange Commission's filing system. Every public US company filing — 10-K (annual), 10-Q (quarterly), 8-K (current report), proxy (DEF 14A), insider transactions (Form 4), beneficial ownership (13D/13G), S-1 (IPO), etc. — going back decades.

Two distinct surfaces are exposed by this connector:

1. **Submissions API** (`/submissions/CIK<10-digit>.json`) — recent filings index for one company, with accession numbers, form types, filing dates, primary document filenames.
2. **Company Facts API** (`/api/xbrl/companyfacts/CIK<10-digit>.json`) — pre-extracted XBRL fundamentals: revenue, EPS, assets, liabilities by period, with the source filing for each value.

Plus two helpers:
- `ticker_lookup` — resolve `AAPL` → `0000320193`
- `filing` — fetch the index of a specific accession

This connector deliberately does NOT fetch full filing documents (10-K text bodies are tens of MB). For prose, take the accession from `submissions` and have the agent fetch the specific HTML/PDF directly.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

But SEC enforces a strict rule: **every request must include a `User-Agent` identifying the caller** with a contact email. Anonymous or generic UAs return 403 and may earn an IP block. Reach sends `ocas-reach (contact: <agent-email>)` automatically.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 10 req/sec absolute (per IP); SEC publishes this as the hard cap |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `ticker_lookup` | Resolve a stock ticker to a CIK | `ticker` (e.g. `"AAPL"`) |
| `submissions` | Recent filings for one CIK | `cik` (digits or zero-padded) |
| `facts` | Company fundamentals from XBRL | `cik` |
| `filing` | Index of one specific filing | `cik`, `accession` (with or without dashes) |

## Worked examples

```bash
# Find Apple's CIK
python3 scripts/reach.py query sec_edgar ticker_lookup '{"ticker": "AAPL"}'
# → {"ticker": "AAPL", "cik": "0000320193", "title": "Apple Inc."}

# Get Apple's recent filings
python3 scripts/reach.py query sec_edgar submissions '{"cik": "0000320193"}'

# Get Apple's XBRL fundamentals
python3 scripts/reach.py query sec_edgar facts '{"cik": "0000320193"}'

# Fetch one specific filing's index
python3 scripts/reach.py query sec_edgar filing '{"cik": "0000320193", "accession": "0000320193-24-000123"}'
```

## Response shape

- `ticker_lookup`: `{ticker, cik, title}` or `{ticker, cik: null, error: "not_found"}`.
- `submissions`: `{cik, name, sic, sicDescription, filings: {recent: {accessionNumber: [...], form: [...], filingDate: [...], primaryDocument: [...]}}}`. The arrays are parallel — index `i` across them describes one filing.
- `facts`: `{cik, entityName, facts: {us-gaap: {Revenues: {label, units: {USD: [{val, end, fy, fp, form, filed}, ...]}}, ...}, dei: {...}}}`. Time series live under `facts.us-gaap.<concept>.units.USD`.
- `filing`: an HTML directory index in JSON form — list the docs inside the accession.

## Pitfalls

- **CIK zero-padding.** Internal SEC paths require 10-digit CIKs with leading zeros. `submissions` and `facts` accept either form; the connector pads automatically.
- **Accession format.** Sometimes shown as `0000320193-24-000123`, sometimes as `000032019324000123`. The connector strips dashes — pass either.
- **Form 4 high volume.** Insider transactions can flood `submissions.recent` for active filers. Filter on `form` index in your post-processing.
- **Amendments**. Look for `/A` suffix on form types (`10-K/A`). The original and amendment are separate filings.
- **`facts` returns periods, not statements.** A single fact like `Revenues` has many `(val, fy, fp)` rows — one per fiscal period reported. Pick the right `(fy, fp)` for the question.
- **No prose body.** This connector returns metadata + numerics. To read the actual 10-K text, take the `primaryDocument` filename from `submissions` and request it from `https://www.sec.gov/Archives/edgar/data/<int(cik)>/<accession-no-dashes>/<primaryDocument>`. That's bulky enough that we don't auto-fetch it.

## Source links

- Developer page: https://www.sec.gov/edgar/sec-api-documentation
- User-Agent rule: https://www.sec.gov/os/accessing-edgar-data
- XBRL concept reference: https://xbrl.us/data-rule/ele-0010/
