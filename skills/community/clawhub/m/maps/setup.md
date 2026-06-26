# Setup - Maps

Use this file when `~/maps/` is missing or empty.
Keep onboarding short and centered on the real map task in front of you.

## Operating Posture

Be precise, provider-neutral, and privacy-aware.
Optimize for correct geography first, then cost, then convenience.

## Early Alignment

In the first exchanges, establish:
- activation preference: always on for place, route, geocode, and map-link tasks or explicit request only
- execution boundary: planning only, copy-paste API requests, live provider calls after confirmation, or app-link launch when helpful
- provider preference: richer proprietary data, open-data fallback, Apple-first app launching, or cheapest acceptable result
- locale defaults: miles vs kilometers, 12-hour vs 24-hour time, and preferred place-language bias

Store only the minimum reusable context that makes the next map task faster and safer.

## How to Start Work

Classify the task before asking for details:
- place search
- forward geocoding
- reverse geocoding
- route or ETA
- matrix or waypoint optimization
- static map or share link

Ask only for context that changes correctness:
- city, neighborhood, country, or coordinates
- origin and destination
- travel mode
- whether the user wants structured data, an open map, or both

Separate rough proximity from actual route questions immediately.
If the user shares recurring home, office, or travel hubs, ask whether local notes are acceptable before storing them.

## Personalization Rules

Adapt to the task shape:
- developers and operators: prioritize schema normalization, cost, and request determinism
- travel planners: prioritize route clarity, venue disambiguation, and shareable links
- local discovery: prioritize status checks, neighborhood context, and opening only the most relevant map
- logistics work: prioritize matrix calculations, recurring origins, and clear fallback paths

Use natural language and avoid long API-history lectures unless requested.

## Internal Notes Policy

Maintain concise records in `memory.md`:
- activation and execution preferences
- provider defaults and no-go providers
- units, locale, and recurring geography context
- privacy and cost boundaries
- repeated failure patterns and the fix that worked

Do not store API keys, raw itinerary dumps, or sensitive location history by default.

## Setup Completion

Setup is sufficient when activation preference, execution boundary, provider bias, and locale defaults are clear enough to help immediately.
Continue with the real map task and refine context through use.
