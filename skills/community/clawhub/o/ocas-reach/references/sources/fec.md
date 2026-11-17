# fec — US campaign finance (candidates, committees, filings)

## What this source has

The FEC (Federal Election Commission) Open Data API exposes every report filed for federal elections from 1979 onward: candidates (presidential, House, Senate), committees (campaign committees, PACs, super PACs, party committees), itemized contributions and expenditures, financial summaries, and the raw filings. ~$30B+ in tracked political money per cycle.

Identifiers:
- **Candidate ID**: 9-character `<office><state><digits>`. Office: `H` (House), `S` (Senate), `P` (Presidential). State: 2-letter (`00` for President). Examples: `H8NY12345`, `S6CA00012`, `P80003353` (Obama 2008).
- **Committee ID**: `C` + 8 digits, e.g., `C00580100`.
- **Cycle**: even year (`2024`, `2026`).

Use FEC for: "who's funding candidate X", "top donors to committee Y", PAC/super-PAC tracking. Pair with `congress_gov` for the legislative side of money flows; pair with `usaspending` for federal contracts (different money, different rules).

## Auth

| | |
|---|---|
| Required | yes |
| Env var | `FEC_KEY` |
| Account URL | https://api.open.fec.gov/developers/ |
| Plan tier | free |

Reach is authorized to register at the URL above using `<agent-email>`. See `references/account_provisioning.md`. Key is via api.data.gov — same key as NASA/USDA/govinfo. Issued instantly.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 1,000 req/hour per key |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `candidates` | Search candidates | none |
| `candidate` | One candidate by ID | `candidate_id` |
| `committees` | Search committees | none |
| `committee` | One committee by ID | `committee_id` |
| `filings` | Filings search | none |

## Worked examples

```bash
# Find Senate candidates in California, 2026 cycle
python3 scripts/reach.py query fec candidates '{
  "office": "S",
  "state": "CA",
  "election_year": 2026,
  "per_page": 50
}'

# One candidate by ID
python3 scripts/reach.py query fec candidate '{"candidate_id": "S0CA00100"}'

# Super PACs (independent expenditure-only committees)
python3 scripts/reach.py query fec committees '{
  "committee_type": "O",
  "per_page": 100,
  "sort": "-receipts"
}'

# One committee
python3 scripts/reach.py query fec committee '{"committee_id": "C00580100"}'

# Recent filings for one committee
python3 scripts/reach.py query fec filings '{
  "committee_id": "C00580100",
  "per_page": 25,
  "sort": "-receipt_date"
}'
```

## Response shape

- `candidates` / `committees` / `filings`: `{api_version, pagination: {page, per_page, count, pages}, results: [...]}`. Each result is the full record for that resource.
- `candidate`: `{results: [{candidate_id, name, party, office, office_full, state, district, election_years: [...], cycles: [...], incumbent_challenge, incumbent_challenge_full, candidate_status, principal_committees: [{committee_id, name, ...}], ...}]}` — even single lookups return a list.
- `committee`: same `results: [...]` wrapping with `{committee_id, name, designation, committee_type, treasurer_name, party, party_full, organization_type, candidate_ids: [...], filing_frequency, ...}`.
- `filings`: `{results: [{file_number, form_type, receipt_date, coverage_start_date, coverage_end_date, total_receipts, total_disbursements, cash_on_hand_end_period, ...}]}`.

## Pitfalls

- **Candidate ID format.** `H<2-state><digits>`, `S<2-state><digits>`, `P<digits>` (no state for presidential). Common mistake: using a 2-letter state in a presidential ID — invalid.
- **Office codes are single letters.** `H`, `S`, `P`. Not `HOUSE` or `house`.
- **Committee types are letter codes.** `H` (House campaign cmte), `S` (Senate), `P` (Presidential), `Q` (PAC qualified), `N` (PAC non-qualified), `O` (Super PAC / IE-only), `Y` (party qualified), `X` (party non-qualified), `D` (delegate), `E` (electioneering), `I` (independent persons/groups), `U` (single-candidate IE-only), `V`/`W` (PAC with non-contribution accounts), `Z` (national party).
- **Cycle vs election year.** `cycle: 2024` covers Jan 2023–Dec 2024. `election_year` is the year of the actual election.
- **Wrappers always return arrays.** Even `candidate` and `committee` (single-lookup) return `results: [{...}]` with one element. Index `[0]`.
- **Pagination.** Default `per_page` is 20, max 100. For large pulls, paginate with `page` or use `last_index` (cursor-style) for very large result sets.
- **Sort syntax.** Prefix with `-` for descending: `sort: "-receipts"`. Sort field must be a valid field on the resource.
- **Independent expenditures aren't on these endpoints.** They live under `/schedules/schedule_e/` (not currently wrapped here).
- **`api.data.gov` shared rate limit.** Same quota across NASA/USDA/etc.

## Source links

- API docs: https://api.open.fec.gov/developers/
- Field reference: https://api.open.fec.gov/developers/swagger
- About the data: https://www.fec.gov/data/browse-data/
