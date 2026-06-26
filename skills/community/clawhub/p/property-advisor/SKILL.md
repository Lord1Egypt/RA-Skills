---
name: property-advisor
description: |
  Property search, screening, comparison, map enrichment, profile memory, watched listings, and listing publishing orchestration. Use when the user asks to rent, buy, search, compare, shortlist, analyze commute, amenities, neighborhood risk, save housing preferences, watch listings, or prepare/publish a property listing. This is an execution-layer orchestrator, not a native crawler: it obtains listings through executable upstream skills/plugins/clients such as ok-core-skill, gt-core-skill, or optional external providers, then normalizes results into the Property Advisor contract.
---

# Property Advisor

## Core Role

Act as an execution-layer property advisor. Do not stop at generic advice when an executable path exists.

This skill does not contain native platform crawlers. It routes to upstream skills/plugins/clients, validates them, normalizes their output, enriches listings with bundled map context, and returns a fixed decision table.

## Consumer Search Workflow

For rent/buy/search/compare/shortlist/commute/amenity/neighborhood requests:

1. Read local profile memory when available.
2. Let explicit user input override memory.
3. Route to a real `source_id` adapter while preserving legacy `market=ok|gt` compatibility.
4. Preflight the selected upstream source before fetching.
5. Fetch listing results and hydrate priority details when supported.
6. Preserve raw listing snapshots.
7. Run `public-osm-map-context-skill/scripts/cli.py` unless map enrichment is explicitly skipped.
8. Return the fixed 8-column candidate table.

Never claim full-market coverage unless every claimed platform was actually queried and returned source links.

## Business Publish Workflow

For publish/rent out/sell/listing-ad requests:

1. Classify the request as `business_publish` vs consumer search.
2. Infer `mode=sale|rent`.
3. Route UK/Gumtree/postcode signals to `gt-core-skill publish-listing`; otherwise use `ok-core-skill publish-property`.
4. Extract only user-provided facts: target market, property type, location, price, contact fields, images, bedrooms, bathrooms, area, amenities.
5. Run bundled map context when location/address/postcode exists.
6. Use the CLI-generated title/description and readiness report; do not freehand ad copy.
7. Block publishing when required fields are missing.
8. Only submit when the user explicitly confirms real submission.

Do not invent price, area, address, contact details, amenities, pet policy, security, wardrobes, gym/pool, landmarks, or transit distance.

## Profile Memory

Use `~/property-advisor/` by default:

- `profile.md`: role, country, city, destination, budget range, bedrooms, preferred sources, hard requirements.
- `searches/`: search history.
- `watched/`: watched listing records.
- `alerts/`: reserved for future alert jobs.

When profile and current request conflict, current request wins.

Do not store passwords, bank details, full loan files, full contracts, or other highly sensitive documents in profile memory.

## Source Routing

Use `source=auto` by default and keep `market=auto|ok|gt` as a compatibility layer.

Prefer installed, preflight-passing upstream sources that can return original listing URLs. Current implemented adapters:

- `ok`: delegates fetching to `ok-core-skill`.
- `gt`: delegates fetching to `gt-core-skill`.

Known external platforms such as Zillow, Redfin, Realtor.com, Rightmove, Zoopla, Domain, realestate.com.au, PropertyGuru, 99.co, Idealista, ImmoScout24, Bayut, Dubizzle, and Property Finder are routing knowledge, not coverage promises.

If the user explicitly asks for an external platform and no executable adapter/provider is available, do not silently fall back to OK/GT. Explain the missing source and, when applicable, suggest the optional provider setup.

For upstream paths, optional plugin rules, and source-specific fallback behavior, read [references/upstream-sources.md](references/upstream-sources.md).

## Map Enrichment

Use the bundled public OSM map context skill for search by default and for publishing when location/address/postcode exists.

Map failures must degrade the result rather than block the whole search:

- Address-level evidence can support first-pass ranking.
- Area-level evidence can only support neighborhood-level conclusions.
- Missing/degraded geocoding must produce a map-missing or manual-review candidate status in the report.
- Never replace a listing URL with a Google Maps or OSM verification URL.

For the exact map input/output contract, read [references/map-context-contract.md](references/map-context-contract.md).

## Output Contract

Default search output is table-first with these 8 columns:

1. Candidate listing
2. Status
3. Price
4. Location
5. Satisfied requirements
6. Missing or unknown facts
7. Elimination reasons or risks
8. Listing URL

The current JSON/Markdown report may render these labels in localized Chinese for downstream compatibility. Preserve the fixed column semantics even when labels are localized.

Rules:

- The listing URL column must contain the original listing URL.
- Listings without original URLs stay in `hidden_candidates`; do not name them in the final table.
- Satisfied requirements, missing/unknown facts, and risks must be traceable to listing facts, source degradation, budget checks, price anomalies, or map assessments.
- If only one upstream source was searched, say the result uses available sources and does not represent all platforms.

For detailed schemas and examples, read:

- [references/data-contract.md](references/data-contract.md)
- [references/output-contract.md](references/output-contract.md)
- [references/response-examples.md](references/response-examples.md)

## CLI Entrypoints

Use the root CLI for deterministic execution and debugging:

```bash
python3 scripts/cli.py doctor --skip-browser-smoke
python3 scripts/cli.py route --query-text "I want to rent out a 1BR in Dubai Marina"
python3 scripts/cli.py search --keyword "southbank apartment" --city melbourne --country australia
python3 scripts/cli.py search --keyword "studio flat" --query-text "Find a studio flat in London" --market auto
python3 scripts/cli.py publish --query-text "I want to rent out a furnished 1BR apartment in Dubai Marina near metro" --country uae --price 8000 --phone 501234567 --image "/absolute/path/photo.jpg" --dry-run
```

For decision heuristics and viewing checks, load references only when needed:

- [references/decision-dimensions.md](references/decision-dimensions.md)
- [references/region-profiles.md](references/region-profiles.md)
- [references/viewing-checklist.md](references/viewing-checklist.md)
