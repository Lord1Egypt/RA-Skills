---
name: investor-fit-research
description: Build investor and fund shortlists from Crawlora public PitchBook profiles and stored investor, fund, and company records. Use for fundraising research based on observed strategy, geography, stage clues, and portfolio evidence with incomplete public coverage explicitly preserved.
---

# Investor fit research

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound requests by the requested scope and credit budget. Preserve
source IDs, URLs, source dates, and retrieval/crawl times separately.

Build a source-attributed fundraising shortlist for a specified company/round.
Establish business model, sector, geography, stage, round size, desired investor
type, and explicit exclusions. A shortlist is research evidence for qualification,
not confirmation of available capital or willingness to invest.

## Discover firms, funds, and relevant portfolio clues

- Discover investor and fund filter values through their dataset facets. Search
  names/descriptions and exact returned geography/type/strategy/status values.
  Headquarters geography is not the same as an investment mandate. A full-text
  match on a sector/stage phrase is a lead, not a verified mandate filter.
- Resolve returned profile IDs and `kind` before item/live detail. Investors
  (manager firms), funds, and companies have different namespaces; keep each
  identity separate. Live profile routes require exactly one of `id` or `url`,
  even though those fields are individually optional in the schema.
- Read stored item records with their `crawled_at`, then refresh shortlisted
  investor/fund/company profiles only as needed. A missing stored item does not
  establish the firm is absent, closed, or unwilling to invest.
- Use public descriptions, overview fields, and visible investment/company
  rows as attributed evidence. PitchBook tables are public previews: `total`
  can exceed the number of visible rows. Blank check sizes, stages, dry powder,
  performance figures, or relationships stay unknown; do not reconstruct them
  from profile popularity or aggregate portfolio counts.
- Match company names/IDs and actual relationship rows before inferring a
  portfolio link. Similar firm names and fund-family branding are not proof
  that a particular fund made the investment. A past investment does not prove
  current focus, lead-investor appetite, exclusivity, or conflict policy.

```sh
scripts/crawlora.sh /datasets/pitchbook-investors/facets facet=investor_type
scripts/crawlora.sh /datasets/pitchbook-funds/facets facet=fund_strategy
scripts/crawlora.sh /datasets/pitchbook-investors/search q="climate" page=1 page_size=10
# Resolve a returned investor/fund ID and kind before live detail:
# scripts/crawlora.sh /pitchbook/investor id="$INVESTOR_ID"
```

## Qualify fit and present the shortlist

Build a criterion matrix with supported, contradicted, and unknown states for
sector/business fit, geography, stage, size, strategy, and relationship clues.
Show the source excerpt/field, date, and entity behind each state. Unknown
criteria are not silently zero; a critical unknown keeps a candidate conditional.
Disclose weights if a numeric ranking is requested. Do not rank by exits or
portfolio counts as a proxy for fit or performance.

Return firm/fund identity, evidence-backed fit, relevant visible investments,
public business contact channels if supplied, unresolved questions, and a
bounded rejected/conditional list. A source's 'active' status or vintage year
is not verified current fundraising, uncommitted capital, or an open application
process. Preparing a shortlist does not authorise contacting investors, sending
company information, registering for paid data, or making investment decisions.
