---
name: Parking Radar
slug: parking
version: 1.0.0
homepage: https://clawic.com/skills/parking
description: Find, verify, and reserve parking worldwide with provider selection, live-signal triage, and local memory for favorite places and cities.
changelog: Initial release with global provider coverage, booking workflows, API notes, and local memory for favorite parking habits and discoveries.
metadata: {"clawdbot":{"emoji":"PARK","requires":{"bins":[],"config":["~/parking/"]},"os":["linux","darwin","win32"],"configPaths":["~/parking/"]}}
---

## When to Use

User needs parking now, wants to pre-book for an airport or event, needs the right local parking app for a city, or wants help comparing parking options across providers.

Use this skill when the agent should distinguish maps search from real reservations, choose the right operator or marketplace by country and city, track favorite parking spots, and remember hard-won parking discoveries for later.

## Architecture

Memory lives in `~/parking/`. If `~/parking/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/parking/
├── memory.md          # Activation defaults, home base, vehicle profile, and booking boundaries
├── favorites.md       # User-approved recurring car parks, venues, and trusted entrances
├── cities.md          # City-by-city provider choices, fallback order, and local quirks
├── findings.md        # User-confirmed discoveries, restrictions, scams, and quality signals
├── sessions/
│   └── YYYY-MM-DD.md  # Complex search trail when a trip or event needs multiple comparisons
└── archive/           # Older notes that should not stay in the hot path
```

## Quick Reference

Load only the smallest file needed for the current parking job.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory schema and local note templates | `memory-template.md` |
| Global provider and market matrix | `provider-registry.md` |
| Major city patterns and fallback order | `city-patterns.md` |
| Short workflows for search, booking, and verification | `execution-playbook.md` |
| Public and partner API notes | `api-notes.md` |
| Official research source ledger | `source-ledger.md` |

## Requirements

- No credentials are required for planning, provider selection, or official web research.
- Live bookings, plate entry, or payment flows require the user to approve the chosen provider and any data sent to it.
- Ask before creating persistent local parking memory. Offer a one-off mode when the user does not want favorites, city defaults, or discovery notes saved.
- Do not promise a guaranteed space unless the provider explicitly exposes reservation inventory or confirmed booking status.

## Coverage

This skill is built for the parking cases where generic map search is not enough:
- quick parking nearby right now
- airport, train-station, stadium, and venue parking that benefits from pre-booking
- repeated home-city parking where favorites, vehicle limits, and local operator habits matter
- travel planning where the correct provider changes by country or even by city
- parking platform research and API scouting for product or integration work

## Core Rules

### 1. Classify the parking mode before searching
- Separate the job into one of five modes: find-now, pre-book, recurring-city, operator research, or API scouting.
- Parking answers get worse fast when the agent mixes instant parking, on-street payment, and guaranteed reservation into one workflow.

### 2. Default to the lightest successful path
- If the user just needs parking now, start with map discovery plus the strongest official operator or aggregator for that city.
- Use deeper provider comparison only when the quick path is ambiguous, expensive, full, or clearly unreliable.
- Do not turn a simple "find me parking nearby" request into a long market audit.

### 3. Distinguish discovery, payment, and reservation surfaces
- Google Maps, Apple Maps, and Parkopedia are discovery surfaces first.
- Apps such as RingGo, PayByPhone, EasyPark, APCOA Connect, and Parking.sg often solve payment or session start, not guaranteed inventory.
- Reservation marketplaces such as SpotHero, ParkWhiz, JustPark EventPass, Onepark, Parclick, Q-Park Prebook, and many operator-native airport or venue flows are the right surfaces for guaranteed entry when available.

### 4. Verify reservation-critical constraints before recommending
- Check entry window, exit rules, in-and-out privileges, height limit, EV charging, motorcycle or van support, license-plate requirements, and cancellation terms.
- For airports and events, confirm walking distance, shuttle dependency, venue match, and whether the booking is for a specific car park or only a zone.
- A cheap parking option is wrong if the user's vehicle or timing cannot actually use it.

### 5. Be precise about availability language
- "Reservable now" means the provider is offering a booking path for the requested window.
- "Reported open" means a listing says the facility is operating, but not that a bay is guaranteed.
- "Real-time occupancy" should only be claimed when an official provider or city API exposes it directly.

### 6. Keep a local parking memory only with consent
- Offer to remember home city, recurring venues, favorite facilities, vehicle constraints, and trusted providers locally in `~/parking/`.
- Store durable notes, not raw payment data or full booking receipts.
- Promote user-confirmed discoveries such as hidden entrances, repeat scams, and reliable operator patterns into the local favorites, cities, or findings notes.

### 7. Treat city and country as first-class routing signals
- Use `provider-registry.md` to choose the right platform family for the market before assuming Google results or one familiar app will work.
- Dense urban centers often use payment apps and operator-native garages, while airports and major venues often use reservation marketplaces.
- When entering a new market, verify the dominant local stack instead of assuming North American or UK patterns apply worldwide.

### 8. Keep research evidence attached to local discoveries
- Save only discoveries that came from the user, an official provider, or a clearly identified city or operator source.
- Tag low-confidence hearsay as unverified and keep it out of favorites until it repeats or gets confirmed.
- Use `source-ledger.md` and `api-notes.md` to separate facts, partnership-only APIs, and "no public API found" cases.

## Common Traps

- Treating a pay-by-phone parking app as proof that a space can be reserved -> many apps start a session only after the driver finds a bay.
- Claiming "spots available" from a static listing page -> open hours and active inventory are not the same thing.
- Ignoring plate, height, or vehicle-type restrictions -> the booking looks fine until gate entry fails.
- Recommending street parking for a high-stress event or airport drop -> uncertainty and enforcement risk overwhelm the small savings.
- Assuming one global app dominates every market -> parking is highly local and often city-specific.
- Saving raw booking confirmations or payment details -> keep reusable parking knowledge, not sensitive receipts.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://maps.google.com and https://maps.apple.com | place text, coordinates, route context | Quick parking discovery, map links, and local navigation handoff |
| https://www.parkopedia.com and Parkopedia parking data products | location, time window, optional vehicle filters | Global parking discovery, facility detail, and broad market coverage |
| https://spothero.com and https://api.parkwhiz.com | destination, venue, dates, time window, optional vehicle metadata | North America reservation search and parking booking APIs |
| https://www.justpark.com, https://eventpass.justpark.com, https://ringgo.co.uk, https://www.q-park.co.uk, https://www.apcoaconnect.com, https://www.paybyphone.com | location code, destination, plate, and time window | UK and Europe parking reservation or payment workflows |
| https://parclick.com, https://www.onepark.co, https://parkmobile.io, https://parkplus.io, https://parking.sg, and official city data portals such as https://api.data.gov.hk | destination, date range, vehicle type, plate when required, and occupancy query parameters | Regional booking, payment, or official parking data lookups |

No other data should be sent externally unless the user approves another official provider or city source.

## Security & Privacy

Data that may leave your machine:
- parking destination or venue
- city and time window
- coordinates and route context
- plate number only when the chosen provider requires it for entry or billing
- vehicle profile fields such as height or EV requirement when they change the result

Data that stays local:
- favorite parking places and entrances in the local favorites note
- home-city defaults and provider order in the local city notes
- user-confirmed discoveries and warnings in the local findings note
- activation rules and parking boundaries in `~/parking/memory.md`

This skill does NOT:
- store payment card data, account passwords, or unnecessary booking receipts
- claim guaranteed inventory without provider evidence
- use undeclared anti-bot scraping flows
- modify its own `SKILL.md`

## Trust

This skill can send parking queries, dates, route context, plate numbers, or vehicle constraints to the selected parking marketplace, operator, payment app, maps provider, or official city data source.
Only use live parking flows if you trust the chosen provider with that data.

## Scope

This skill ONLY:
- finds, compares, and explains parking options
- chooses the right provider family for each city and task
- verifies reservation-critical constraints before the user commits
- maintains lightweight local memory for favorites, cities, and discoveries after approval

This skill NEVER:
- invent live availability or occupancy
- assume a payment app guarantees entry
- treat one country's parking workflow as universal
- persist sensitive payment or identity data without a clear need

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `maps` - Use map providers, geocoding, and route links to ground parking search in real geography.
- `travel` - Fold parking choices into broader trip timing, lodging, and movement decisions.
- `booking` - Compare reservation terms, cancellation rules, and booking friction across providers.
- `compare` - Turn multiple parking options into a clear side-by-side decision.
- `car-rental` - Add pickup, return, and vehicle-access context when parking decisions sit inside a driving trip.

## Feedback

- If useful: `clawhub star parking`
- Stay updated: `clawhub sync`
