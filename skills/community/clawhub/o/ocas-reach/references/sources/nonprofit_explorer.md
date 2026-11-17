# nonprofit_explorer — ProPublica Nonprofit Explorer (IRS 990 Data)

## What this source has

ProPublica's Nonprofit Explorer API provides data from IRS Form 990 filings for US tax-exempt organizations. Data includes:

- Organization name, EIN, and classification
- Revenue, expenses, assets, and liabilities
- Executive compensation
- Mission statement and program descriptions
- Filing history (annual 990s)

Use nonprofit_explorer for: researching organizations, checking nonprofit financials, Scout investigations of nonprofits, due diligence, and verifying charitable status.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

Free, no key required. Data is sourced from IRS filings (public record).

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | throttle to <1/sec |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `search` | Search nonprofits by name, keyword, or location | `q` (query string) |
| `organization` | Get detailed data for a specific nonprofit | `ein` (path param) |

## Worked examples

```bash
# Search for nonprofits by name
python3 scripts/reach.py query nonprofit_explorer search '{"q": "electronic frontier foundation"}'

# Get detailed data by EIN
python3 scripts/reach.py query nonprofit_explorer organization '{"ein": "04-3091885"}'

# Search by city
python3 scripts/reach.py query nonprofit_explorer search '{"q": "san francisco education"}'
```

## Response shape

**Search** returns:
```json
{
  "total_results": 42,
  "organizations": [
    {
      "ein": "043091885",
      "name": "Electronic Frontier Foundation",
      "sub_name": "",
      "city": "San Francisco",
      "state": "CA",
      "ntee_code": "A60",
      "raw_ntee_code": "A60",
      "subseccd": 3,
      "has_subseccd": true,
      "have_filings": true,
      "have_extracts": true,
      "have_pdfs": true
    }
  ]
}
```

**Organization** returns detailed financial data including revenue, expenses, compensation, and filing history.

## Pitfalls

- **EIN format.** EINs are 9 digits, often displayed as XX-XXXXXXX. The API accepts both formats.
- **Not all nonprofits file 990s.** Small organizations (revenue <$50k) file 990-N (e-postcard) which has minimal data. Churches are exempt from filing.
- **Data lags.** IRS processing means the most recent filing may be 1-2 years old.
- **Search is text-based.** Use specific names or keywords for best results. Fuzzy matching is limited.
- **NTEE codes** classify nonprofit activity areas. Use the NTEE code reference for filtering by category.

## Source links

- Nonprofit Explorer: https://projects.propublica.org/nonprofits/
- API docs: https://projects.propublica.org/nonprofits/api
- NTEE codes: https://nccs.urban.org/project/national-taxonomy-exempt-entities-ntee-codes
