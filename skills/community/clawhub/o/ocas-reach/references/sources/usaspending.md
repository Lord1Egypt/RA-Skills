# usaspending — federal contracts, grants, loans, and direct payments

## What this source has

USAspending.gov is the public face of the DATA Act — every prime federal award (contracts, grants, loans, direct payments, insurance) reported by federal agencies, plus first-tier subawards. Coverage is FY2008 onward, with data quality improving steadily. ~$7T+ in tracked obligations annually.

Each award has a unique award ID (PIID for contracts, FAIN for grants); recipients are keyed by UEI (Unique Entity ID, the SAM.gov successor to DUNS). Awards link to obligations (point-in-time commitments) and outlays (actual cash going out the door). Federal agencies are identified by toptier code (e.g., `097` = DOD).

Use USAspending for: "who got money from agency X", "what is recipient Y's federal contract history", spending trends by NAICS code or geography, prime → subaward chains. Pair with `fec` for campaign-finance angles on the same recipients; pair with `federal_register` when an award stems from a published notice.

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
| Rate | no published cap; throttle below 5 req/sec under load |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `awards_search` | Search awards with filter object (POST) | `filters` |
| `award` | Fetch a single award by ID | `award_id` |
| `agencies` | List toptier agencies | none |

## Worked examples

```bash
# DOD contracts > $10M in FY2025 to Lockheed Martin
python3 scripts/reach.py query usaspending awards_search '{
  "filters": {
    "award_type_codes": ["A", "B", "C", "D"],
    "agencies": [{"type": "awarding", "tier": "toptier", "name": "Department of Defense"}],
    "recipient_search_text": ["Lockheed Martin"],
    "time_period": [{"start_date": "2024-10-01", "end_date": "2025-09-30"}],
    "award_amounts": [{"lower_bound": 10000000}]
  },
  "fields": ["Award ID", "Recipient Name", "Award Amount", "Description", "Awarding Agency"],
  "limit": 25
}'

# Fetch a specific award
python3 scripts/reach.py query usaspending award '{"award_id": "CONT_AWD_FA8675-22-D-0001_9700_-NONE-_-NONE-"}'

# Top-tier agency list
python3 scripts/reach.py query usaspending agencies '{}'
```

## Response shape

- `awards_search`: `{limit, results: [{Award ID, Recipient Name, Award Amount, ...field-keyed columns...}, ...], page_metadata: {page, hasNext, hasPrevious, next, previous}}`. The `fields` list you pass *is* the column set returned — pick deliberately.
- `award`: `{id, generated_unique_award_id, type, type_description, category, piid (or fain), parent_award_piid, total_obligation, total_outlay, recipient: {recipient_name, recipient_unique_id, business_categories, ...}, period_of_performance: {start_date, end_date}, place_of_performance: {city_name, state_code, country_name}, awarding_agency, funding_agency, executive_details, ...}`.
- `agencies`: `{results: [{agency_id, toptier_code, abbreviation, agency_name, congressional_justification_url, ...}]}`.

## Pitfalls

- **`awards_search` is POST with a JSON body**, not GET with query params. Pass `filters` as a nested object — the connector forwards it as-is.
- **Award type codes matter.** `A`/`B`/`C`/`D` are contracts; grants are `02`/`03`/`04`/`05`; loans `07`/`08`. Mixing without intent gives nonsensical totals.
- **`fields` is mandatory in practice.** Without it, the response uses a default subset that may not include what you need. Specify explicit columns.
- **Obligation vs outlay.** Obligations are commitments at award time; outlays are actual cash. They diverge — a 5-year contract may obligate $500M day one but outlay $100M/year.
- **Recipient names are not normalized.** "Lockheed Martin Corp" and "LOCKHEED MARTIN CORPORATION" appear separately. Use UEI for cross-award joins.
- **Subawards live on a separate endpoint.** `awards_search` returns only prime awards; subaward search is `/search/spending_by_subaward/` (not yet wrapped here).
- **Time periods.** Filter by `action_date` (when the obligation occurred) for spending velocity; by `period_of_performance.start_date` for award timing. They differ.
- **Award ID format is opaque.** `CONT_AWD_<piid>_<dept>_-NONE-_-NONE-` is the generated unique ID; the human-friendly PIID is shorter. Both work in `award`.

## Source links

- API docs: https://api.usaspending.gov/
- Endpoint reference: https://github.com/fedspendingtransparency/usaspending-api/tree/master/usaspending_api/api_contracts
- Data dictionary: https://www.usaspending.gov/data-dictionary
