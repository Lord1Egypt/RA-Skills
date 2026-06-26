# Search Strategy

Read this for `L2_GUIDED_STRATEGY`: the user asks how to search, says results are wrong or too few, sees suppliers instead of buyers, or needs a systematic buyer-route diagnosis.

## Contents

1. Minimal Prospecting Profile
2. Customer-Side Routes
3. Low-Yield Diagnosis
4. L2 Search Behavior
5. Source Discipline

## 1. Minimal Prospecting Profile

Build only the facts needed to choose one route:

- seller product/service
- capability boundary or application
- target geography
- exclusions
- temporary buyer type
- why that buyer might buy, resell, install, integrate, maintain, retrofit, specify, or use the offer
- what must be validated in result rows

Ask at most 1-2 blocking questions when route choice is impossible. Do not require a full Merchant Profile, PMF Gate, Success Customer Profile, or persisted Product Brief before a free search.

Current-turn user facts are source of truth. Optional Merchant Profile memory may help only when it is cheap and does not delay the first useful search.

## 2. Customer-Side Routes

Useful route families:

- channel/resale: importer, distributor, dealer, wholesaler, retailer
- installation/integration: installer, integrator, contractor, system house
- service/maintenance: repair, retrofit, maintenance, aftersales
- project/specification: project buyer, design firm, engineering contractor, OEM program
- direct operator/use: factory, fleet, hotel, school, clinic, venue, or other end user

Validate the buyer-side relationship before recommending or searching a route. A route is weak when it describes a supplier, peer producer, or adjacent company that does not plausibly buy or influence purchase.

## 3. Low-Yield Diagnosis

Use compact wrapper `discovery_health` when present.

Frame weak results as a search-route issue:

- current target-side projection may be too narrow
- Chinese index-language terms may need rewriting
- geography may be too narrow or mismatched
- buyer role may be hidden in another route
- email-only or `AND` may have over-constrained recall

Do not say OKKI Go has poor coverage or is not a search engine unless a hard API/system error proves it.

If `low_yield_batch_streak >= 2`, stop blind synonym changes and offer Mentor Guided route mapping.

## 4. L2 Search Behavior

1. State the provisional buyer route briefly.
2. Apply the Company Search Keyword Contract from `SKILL.md`.
3. Use a minimal keyword shape plus geography when supplied.
4. Put secondary route signals into local priority rules rather than hard filters when recall may suffer. Local priority rules guide analysis after the company discovery output contract; they do not change displayed result rows or counts.
5. Run or propose one free search route.
6. Present any new search result using `output-contracts.md`, then put the unlock/refine CTA before longer coaching.

A second graph path requires user confirmation or `references/expansion-playbook.md`.

## 5. Source Discipline

Mentor claims can come from:

- current user facts
- compact OKKI rows
- confirmed Merchant Profile fields
- explicit external sources only when the user explicitly asks for independent external research

External research is not a recovery path for ordinary OKKI prospecting, low-yield results, API errors, or system busy responses. It cannot authorize unlock, contact search, or email send, and it must not mutate OKKI search payloads without user confirmation.
