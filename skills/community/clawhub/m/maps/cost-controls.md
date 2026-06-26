# Cost Controls - Maps

Use these rules before sending live map requests.

## Query Hygiene

- Canonicalize address strings before geocoding so the same address is not billed twice.
- Reuse provider IDs once a place is confirmed instead of re-searching by free text.
- Keep place search bounded to the smallest useful area.

## Provider Escalation

- Start with the cheapest provider that can meet the precision requirement.
- Escalate to premium providers only when the task needs richer metadata, stronger confidence, or traffic-aware routing.
- Do not use premium routing for rough radius checks or brainstorming.

## Batch Discipline

- Prefer matrix endpoints over many single-route calls only when pair counts justify it.
- Cache recurring origins and destinations locally after user approval.
- Rate-limit retries and exponential backoff on quota or transient failure responses.

## Quota Red Flags

- repeated geocoding of the same address
- route recalculation after each wording tweak
- broad nearby searches without area bias
- static-map regeneration when only labels changed

If any red flag appears, stop and simplify before sending more requests.
