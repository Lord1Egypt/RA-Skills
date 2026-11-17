# congress_gov — bills, votes, members, committees from Congress.gov

## What this source has

The Congress.gov API is the Library of Congress's authoritative source for US Congressional data: every bill (HR, S, HJRES, SJRES, HRES, SRES, HCONRES, SCONRES) introduced from the 93rd Congress (1973) onward, every member of Congress (House + Senate), committee rosters and reports, House and Senate votes, the Congressional Record, treaties, and presidential nominations.

Data is keyed by congress number (the current is the 119th, covering 2025–2026), bill type + number, member bioguide ID (e.g., `S000148` for Schumer), or committee code. Bills carry text versions, sponsors, cosponsors, actions (every parliamentary step), summaries, related bills, subjects, and committee referrals.

Use Congress.gov for: tracking a specific bill's status, "who sponsors X", member voting records, committee membership. Pair with `govinfo` for the canonical published text (slip laws, USCODE) and with `federal_register` for executive-branch implementation.

## Auth

| | |
|---|---|
| Required | yes |
| Env var | `CONGRESS_KEY` |
| Account URL | https://api.congress.gov/sign-up/ |
| Plan tier | free |

Reach is authorized to register at the URL above using `<agent-email>`. See `references/account_provisioning.md`. The signup form asks for name + email + use case; a key is emailed within a few minutes.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 5,000 req/hour per key |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `bill` | Specific bill | `congress`, `type` (e.g. `hr`), `number` |
| `bills` | Bill listing/search | none (use `congress`, `fromDateTime`, `toDateTime`, etc.) |
| `member` | Specific member by bioguide ID | `bioguide_id` |
| `vote` | House vote by congress/session/vote number | `congress`, `session`, `vote` |
| `committee` | Committee listing | none |

## Worked examples

```bash
# Specific bill (HR 1 of the 119th Congress)
python3 scripts/reach.py query congress_gov bill '{
  "congress": 119,
  "type": "hr",
  "number": 1
}'

# Recent bills
python3 scripts/reach.py query congress_gov bills '{
  "congress": 119,
  "limit": 25,
  "sort": "updateDate+desc"
}'

# Member by bioguide ID (Chuck Schumer)
python3 scripts/reach.py query congress_gov member '{"bioguide_id": "S000148"}'

# House vote 100, 119th Congress, 1st session
python3 scripts/reach.py query congress_gov vote '{
  "congress": 119,
  "session": 1,
  "vote": 100
}'

# Committees
python3 scripts/reach.py query congress_gov committee '{"limit": 50}'
```

## Response shape

- `bill` (single): `{bill: {congress, number, type, title, originChamber, originChamberCode, introducedDate, latestAction: {actionDate, text}, sponsors: [{bioguideId, fullName, party, state, ...}], cosponsors: {count, url}, actions: {count, url}, committees: {url}, subjects: {url}, summaries: {url}, textVersions: {url}, ...}}`. Most nested collections are URL-stubs — follow with the URL to expand.
- `bills` (list): `{bills: [...summary objects...], pagination: {count, next}}`.
- `member`: `{member: {bioguideId, directOrderName, firstName, lastName, party, state, district, terms, depiction, sponsoredLegislation, cosponsoredLegislation, addressInformation, ...}}`.
- `vote`: `{houseVote: {congress, session, voteNumber, voteType, result, date, question, description, votes: {Republican, Democrat, Independent, total}, ...}}`.
- `committee`: `{committees: [{name, chamber, systemCode, url, ...}]}`.

## Pitfalls

- **`congress` is the integer** (119, 118, ...), not a name. The current Congress depends on the date — 119 covers Jan 2025–Jan 2027.
- **Bill `type` is lower-case** in the API path: `hr`, `s`, `hjres`, `sjres`, `hres`, `sres`. Upper-case 404s.
- **Bioguide IDs are 7-char**: 1 letter + 6 digits, e.g., `P000197` (Pelosi), `S000148` (Schumer). Case-sensitive in URLs.
- **Many fields are URL stubs**, not inline. `bill.cosponsors.url`, `bill.actions.url`, `bill.summaries.url` — follow each separately. The connector doesn't auto-expand.
- **Senate votes use a different path.** This connector wraps `/house-vote/...`; for Senate votes, the path is `/senate-vote/...` (not currently wrapped). File a follow-up if needed.
- **`fromDateTime` / `toDateTime` format** is ISO-8601 with timezone, e.g., `2026-01-01T00:00:00Z`.
- **Pagination via `offset` + `limit`**, max `limit` 250.
- **`format: json` is default** but specify it explicitly to avoid surprises if API defaults shift.
- **Bills span multiple Congresses.** A bill reintroduced in the next Congress has a different (congress, number) — they're tracked as related bills, not the same record.

## Source links

- API docs: https://api.congress.gov/
- Sign-up: https://api.congress.gov/sign-up/
- Data dictionary: https://github.com/LibraryOfCongress/api.congress.gov/
