---
description: Travel planning, itinerary construction, reservation management, lodging
  search, and flight search. Parallel lodging search across Expedia, Marriott Bonvoy,
  Marriott AI, Google Hotels, 1Stay, and HotelsByDay (day-use rooms). Flight search
  via Google Flights. Uses Sift for destination research and optionally GoPlaces for
  location enrichment. HotelOracle (Google Hotels) used for price trends, area guides,
  and price comparison research. NOT for generic travel inspiration, visa advice, or
  points-only optimization.
includes:
- references/**
- scripts/**
license: MIT
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "3.0.0"
name: ocas-voyage
source: https://github.com/<agent-handle>/voyage
tags:
- travel
- itinerary
- flights
- hotels
- booking
triggers:
- travel planning
- itinerary construction
- flight search
- hotel booking
- travel reservation
---
## Interactive Menu

When invoked interactively, present a two-level menu. See `references/interactive-menu.md` for the full menu structure.

## When to Use

- Travel planning and itinerary construction
- Flight, hotel, and activity research
- Booking coordination across multiple providers
- Travel document and requirement checking
- When any skill needs travel-related data
- Plan a multi-day trip with itinerary; build or optimize a travel itinerary
- Search for flights (one-way, round-trip, multi-city); find cheapest dates to fly
- Recommend lodging, restaurants, or activities for a trip
- Manage reservation planning and checklists

## When NOT to Use

- Calendar management (use Sands)
- Restaurant reservations (use Spot)
- General web research (use Sift)
- Travel insurance or financial planning
- Generic travel inspiration with no planning intent
- Points-only optimization (use Rally)
- Visa, customs, or medical-travel compliance as primary task

# Voyage

Voyage builds complete, constraint-aware travel itineraries — taking a destination, dates, budget, dietary preferences, and pace, then assembling lodging, dining, and activity recommendations into a logistics-optimized plan that is ready for reservation without auto-booking anything. It never presents uncertain operating hours or availability as confirmed fact, and surfaces cost implications throughout so the plan remains honest about what it actually knows.

## Responsibility boundary

Voyage owns travel planning, itinerary construction, and reservation management.

Voyage does not own: web research (Sift), preference persistence (Taste), communications (Dispatch).


## Lodging search

When the user needs lodging recommendations, all configured sources fire in parallel. Results are merged into a unified comparison table.

| Source | Provides | Requires |
|--------|----------|----------|
| **Expedia web** | Hotel/package search, total-cost breakdown | None — always available |
| **Marriott Strider MCP** | Real Bonvoy inventory, award nights, elite upgrades, mobile key | `mcp-marriott` installed + configured (profile `marriott` MCP server) + Bonvoy OAuth login (`login` tool or MARRIOTT_EMAIL/MARRIOTT_PASSWORD env) |
| **Marriott AI / FlyAI** | ~~Package bundling~~ **DEAD (2026-08-23, DNS NXDOMAIN) — do not use** | — |
| **Google Hotels** | Structured results table (price/rating/amenities), search-only | `agent-browser` CLI |
| **1Stay** | Real hotel booking with confirmation numbers, loyalty program eligible, 300K+ properties in 140+ countries. Full lifecycle: search → details → book → lookup/cancel | MCP connector `1stay` configured (Streamable HTTP) + Bearer API key for booking |
| **HotelOracle** | Price trends (calendar), area guides, cross-site price comparison, nearby attractions — research enrichment only, no booking | Direct Streamable HTTP: `https://tooloracle.io/hotel/mcp/` (free tier, no key); configured as profile `hoteloracle` MCP server |
| **HotelsByDay** | Day-use rooms (10AM–5PM) and work passes — unique vertical not on other platforms. Python harness: `scripts/hotelsbyday_search.py`. Also night stays (beta, limited inventory) | No credentials required; uses web harness |
| **LetsFG** | Flight + hotel search with real booking (real PNR / confirmation); free-cancellation pay-later hotel rates, 5%-now/rest-to-hotel | `letsfg auth` card-on-file token (nothing charged); see `references/letsfg.md` |
| **Sift** | Destination info, activities, local knowledge, anything platforms don't cover | Sift skill installed |

Results ranked by: total real cost → loyalty/points value → cancellation flexibility → location fit.

See `references/lodging-sources.md` for per-source patterns and failure modes.

**GoPlaces cooperation (optional):** If `ocas-goplaces` is installed, Voyage calls it to resolve ambiguous location input before search (geocoding, distance checks, neighborhood context). If not installed, Voyage surfaces unresolved location ambiguity to the user rather than guessing. Voyage checks for GoPlaces at runtime using the platform skill registry.

**Total cost rule:** Always surface headline price + taxes + mandatory fees + cancellation flexibility before recommending. Never present a listing price as booking-final. See `references/total-cost.md`.

**Booking gate rule:** Never present an option as "ready to book" without: price re-check complete, cancellation terms stated, and explicit user approval. See `references/booking-gates.md`.


## Flight search

When the user needs flight options, Voyage uses the `fli` library to query Google Flights data directly. No API key or browser required.

**LetsFG (booking-capable complement):** For the broadest price scan (budget carriers, OTAs, stable repeat pricing) and actual booking without OTA checkout redirects — flights and free-cancellation pay-later hotels — use LetsFG (`pip install letsfg`, one-time `letsfg auth` card-on-file setup, nothing charged; NEVER use `letsfg register`/`setup-payment`, those create a paid Developer API billing account). Hotel bookings carry a 5% non-refundable reservation fee. Run `fli` first (no credentials); add LetsFG results when a token exists or the task involves booking. See `references/letsfg.md`.

For quick searches, use the bundled script:
```bash
$HERMES_PY ~/.hermes/skills/ocas-voyage/scripts/flight_search.py SFO JFK 2026-06-16
$HERMES_PY ~/.hermes/skills/ocas-voyage/scripts/flight_search.py SFO LGA 2026-06-16 SFO 2026-06-18 --limit 5
```

See `references/flight-search.md` for the full fli API calling convention (including common pitfalls) and `references/flights.md` for date search, multi-airport, and multi-city patterns.


## Ontology types

Voyage works with these types from `spec-ocas-ontology.md`:

- **Place** — venues, airports, hotels, restaurants, attractions. Extracted during destination research and itinerary construction.
- **Concept/Event** — trips and travel events (departure, arrival, check-in, activity). Stored in itinerary records.
- **Concept/Action** — booking actions (reserved, cancelled, modified). Recorded in Action Journals.
- **Entity/Person** — travel companions mentioned during trip planning.

Voyage maintains its own trip and itinerary state in `{agent_root}/commons/data/ocas-voyage/`. Entity observations are recorded in journal outputs for downstream Chronicle ingestion.


## Commands

- `voyage.plan.trip` — create a full trip plan from destination, dates, and constraints
- `voyage.recommend.lodging` — parallel lodging search across Expedia, Marriott Strider, Marriott AI, Google Hotels, 1Stay, and HotelsByDay (day-use rooms). HotelOracle used for price calendar and cross-site comparison research. Returns unified comparison table with total-cost breakdown and booking-gate summary.
- `voyage.recommend.flights` — search Google Flights for one-way, round-trip, multi-city, or date-range queries. Returns structured flight options with pricing, timing, and airline details.
- `voyage.recommend.food` — restaurant recommendations based on route and preferences
- `voyage.recommend.activities` — activity recommendations based on interests and logistics
- `voyage.optimize.itinerary` — optimize an existing itinerary for feasibility and logistics
- `voyage.status` — current plan state, pending reservations, open decisions
- `voyage.journal` — write journal for the current run; called at end of every run
- `voyage.update` — pull latest from GitHub source; preserves journals and data


## Workflow

The Voyage pipeline follows: **research → search → compare → recommend → persist**.

1. Research destination via Sift (example: "best neighborhoods in Lisbon for food lovers")
2. Search lodging in parallel across all providers; HotelsByDay covers day-use rooms (10AM–5PM), HotelOracle enriches with price calendars and cross-site comparison where available, 1Stay provides booking
3. Search flights via Google Flights
4. Compare options with total-cost breakdown
5. Recommend with evidence-linked rationale (because each recommendation names the specific attributes that justify it)
6. Persist plan state and write journal

## Run completion

After every Voyage command:

1. Persist plan state, recommendations, and reservation details to local files
2. Log material decisions to `decisions.jsonl`
3. Write journal via `voyage.journal`

## Invariants

- Never present uncertain operating hours or availability as confirmed
- Respect dietary constraints in all food recommendations
- Budget awareness throughout — surface cost implications
- Reservation-ready means actionable, not auto-booked (unless explicitly enabled)

## Error Handling

| Failure | Detection | Response |
|---------|-----------|----------|
| Lodging source unavailable | API timeout or error from any MCP/lodging source | Skip source; continue with remaining sources; log warning |
| Flight search failure | fli library raises exception or returns empty | Report error; suggest manual Google Flights check |
| Docker unavailable (Inception) | Docker daemon not running | Log `degraded: docker`; return error with diagnostic info |
| GoPlaces unavailable | Skill registry check fails | Surface location ambiguity to user; do not guess |
| Google Places API unavailable | API key missing or quota exceeded | Surface warning; ask for manual estimate |


## Storage layout

See `references/storage-and-config.md` for the directory structure and default config.json.

## OKRs

See `references/okrs.md`.

## Optional skill cooperation

- **Sift** — all open web research: destination info, restaurant picks, activity recommendations, local knowledge. Voyage delegates to Sift via Sift's search stack; does not do raw web searches itself.
- **GoPlaces** (`ocas-goplaces`) — location enrichment: geocoding, distance-to-airport/center, neighborhood context, disambiguation of ambiguous location input. Check at runtime: `platform skill registry query | grep goplaces`. If not installed, flag ambiguity to user.
- **HotelOracle** (`io.tooloracle/hoteloracle` via Glama MCP Gateway) — price calendar trends, cross-site price comparison, area guides, nearby attractions. Research-only; no booking capability. Enriches hotel details with Google Hotels data.
- **Taste** — preference-aware recommendations (read-only)
- **Weave** — trip companion context from social graph (read-only)
- **Chronicle** — entity observations emitted via journal signal payloads
- **Vesper** — travel schedule briefs delivered directly to `ocas-vesper`'s intake directory (`{agent_root}/commons/data/ocas-vesper/intake/`) so the morning/evening briefing aggregates pending trip details. See `references/vesper-intake-delivery.md`.


## Journal outputs

Action Journal — all planning, recommendation, and reservation runs.

When entities are encountered during a run, include structured entity observations in `decision.payload`:

- `entities_observed` — list of entities encountered (Place, Concept/Event, Concept/Action, Entity/Person), each with type, name, and context
- `relationships_observed` — connections between entities (e.g., a person associated with a trip, a restaurant located in a destination)
- `preferences_observed` — user preferences inferred from planning choices (e.g., budget range, dietary needs, pace preference)

Each entity observation must include a `user_relevance` field:
- `user` — entity is directly related to the user's world (destinations, hotels, companions, reservations). Most Voyage entities are `user`-relevant since they represent the user's actual travel plans and destinations.
- `agent_only` — entity encountered incidentally (e.g., a landmark mentioned only as a routing waypoint, not as a destination)
- `unknown` — relevance is unclear


## Initialization

On first invocation of any Voyage command, run `voyage.init`. See `references/initialization.md` for the full 10-step procedure including Marriott MCP setup, Google Hotels setup, flights library install, optional credentials, and GoPlaces check.

## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `voyage:update` | cron | `0 0 * * *` (midnight daily) | `voyage.update` |

```
# Task declared in SKILL.md frontmatter metadata.{platform}.cron
```


## Self-update

`voyage.update` pulls the latest package from the `source:` URL in frontmatter. Runs silently — no output unless the version changed or an error occurred. See `references/self-update.md` for the full 7-step procedure.


## Visibility

public


## Gotchas

- **GoPlaces is optional, not required** — If `ocas-goplaces` is not installed, Voyage surfaces unresolved location ambiguity to the user rather than guessing. The skill works normally but location resolution depends on user input.
- **Total cost rule is mandatory** — Always surface headline price + taxes + mandatory fees + cancellation flexibility before recommending. Presenting a listing price as booking-final violates the booking gate rule.
- **Flight prices are volatile** — Always include an "as of" timestamp in flight search results. Prices change frequently and are never guaranteed. The `fli` library queries Google Flights in real-time.
- **Multi-city searches may time out** — For complex multi-leg itineraries, search legs individually and combine results rather than using a single multi-city query.
- **Reference files are authoritative over SKILL.md** — If a concept is described in both SKILL.md and a reference file, the reference file wins. Always read the relevant reference before executing a workflow.
- **Integration hygiene (operator, 2026-08-22):** after integrating any new service into Voyage, run a rationalization/health scan over ALL integrated APIs and MCPs — verify each is healthy and working, and document what each is used for in the reference files. Fix broken ones rather than leaving them listed.

## Support File Map

| File | When to read |
|------|-------------|
| `references/voyage_schemas.md` | Before creating plans, itineraries, or reservations; when validating data structures |
| `references/itinerary_constraints.md` | Before constraint application or optimization; when checking feasibility rules |
| `references/recommendation_style.md` | Before generating recommendations; when checking tone and format guidelines |
| `references/journal.md` | Before calling voyage.journal; at end of every run |
| `references/flights.md` | Before any flight search; when checking API patterns, airport resolution, or failure modes |
| `references/letsfg.md` | Before using LetsFG for flight/hotel search or booking; auth setup, guardrails, SDK patterns |
| `references/lodging-sources.md` | Before lodging search; when checking per-source patterns and failure modes |
| `references/flight-search.md` | Before any flight search; when checking API patterns, airport resolution, or failure modes |
| `references/storage-and-config.md` | When inspecting or configuring the on-disk data files and default config |
| `references/okrs.md` | When reviewing OKR definitions or scoring skill performance |
| `references/initialization.md` | On first use; Marriott MCP setup, flights library install, GoPlaces check |
| `references/self-update.md` | When running voyage.update; full 7-step update procedure |
| `references/vesper-intake-delivery.md` | After a trip is confirmed; write the brief to Vesper's intake directory |
| `references/plans/trip-planning.plan.md` | Before a multi-step trip-planning request; destination research → itinerary → accommodation bundling |
| `scripts/hotelsbyday_search.py` | Bundled HotelsByDay harness for day-use rooms,and night stays; call via venv Python for quick searches |
| `scripts/flight_search.py` | Reusable flight search script; call via venv Python for quick one-off searches |

## Update command

This skill self-updates every 24 hours via:

```bash
voyage.update
```

This pulls the latest version from GitHub. Voyage has no background operational tasks, so there is nothing to restart.
