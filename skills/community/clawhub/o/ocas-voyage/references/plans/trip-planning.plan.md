# Bundled Plan: trip-planning

Full trip planning pipeline for a destination or trip request: destination research → itinerary → accommodation.

## Parameters

- `destination` (required)
- `dates` (optional — check-in / check-out window)
- `budget` (optional)
- `companions` (optional)

## Steps

1. **Destination research** — use `sift` for destination info, top attractions, neighborhoods, local knowledge.
2. **Accommodation** — use HotelOracle (price-calendar trends, cross-site price comparison, area guides, nearby attractions) for hotel shortlist sorted by budget + preference fit (via `taste`).
3. **Itinerary** — build day-by-day plan mapping attractions → meals → logistics, grounded in destination research.
4. **Flights/transit** — surface flight options / airport-transfer context from local knowledge + user preference.
5. **Brief delivery** — write the confirmed trip brief to `ocas-vesper`'s intake (`{agent_root}/commons/data/ocas-vesper/intake/`;see `references/vesper-intake-delivery.md`) so bohr the morning briefing aggregates it.
6. **Journal** — write an Action Journal for the planning run with `entities_observed`, `preferences_observed` (user-relevant).

## Output

A structured itinerary + hotel shortlist + a delivered Vesper trip brief. Every recommendation carries a source reference (sift search result / HotelOracle data).