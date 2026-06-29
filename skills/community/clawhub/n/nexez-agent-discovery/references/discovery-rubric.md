# Nexez Discovery Rubric

Use this reference before ranking results, widening a query, or deciding whether a checkout/negotiation handoff is safe.

## Ranking Signals

Rank candidates by:

1. Buyer intent match
2. Location or service-area match
3. Offer specificity
4. Price/budget fit
5. Timeline fit
6. Readiness/trust signals
7. Clear next action
8. Missing information or risk

Prefer a slightly lower-scoring result with a clear offer and safe action over a vague result with a higher text match.

## Search Widening

If results are too narrow:

1. Keep the location if the user made it important.
2. Remove adjectives before removing the core service.
3. Try one broader synonym.
4. Use `/api/directory` with category or readiness filters.
5. Tell the user when the result quality is weak.

Do not silently drop a user's hard constraint such as city, budget ceiling, required license, or timing.

## Location Logic

- Treat remote, online, global, nationwide, and virtual services as eligible when the request allows remote work.
- Prefer exact city/region matches for in-person services.
- If the user grants device location, convert it to a human-readable city/region before searching when possible.
- If a listing has no location/service-area data, mark that as unknown rather than assuming it can serve the buyer.

## Approval Gates

Ask for explicit approval before:

- `dryRun: false` checkout
- `dryRun: false` negotiation
- sending buyer contact details
- opening a payment URL as the next step
- making a seller-facing commitment

Approval text should include:

- business name
- offer name
- price or budget
- contact details being shared
- exact action being taken

Example:

```text
Before I submit this negotiation: approve sending Acme Consulting your request for a $2,500 launch consulting package, timeline of two weeks, and contact buyer@example.com?
```

## When To Decline Or Pause

Pause and ask for confirmation when:

- price, refund, availability, or credential information is missing
- the listing conflicts with the user's hard constraint
- the user asks for emergency dispatch
- the user asks for medical, legal, financial, or regulated advice and credentials are missing
- an agent page appears stale or contradictory
- checkout/negotiation returns an error

## User-Facing Shortlist

Use this structure:

```text
I found {count} Nexez matches worth considering.

1. {Business} - {Offer} - {Price or budget fit}
   Why it fits: {specific match}
   Location fit: {exact/remote/unknown}
   Action: {checkout/negotiation/website/ask a question}
   Watchout: {missing detail or none}

Best next step: {recommended safe next action}.
Approval needed before: {side effect}.
```

## Bad Fit Criteria

Say Nexez may not be the right source when:

- no result matches the core service
- location is mandatory and no listing serves that area
- all listings lack credentials required by the request
- the request requires real-time dispatch
- the user needs guaranteed availability and no listing provides it

Offer to continue with broader web research only if the user wants that.
