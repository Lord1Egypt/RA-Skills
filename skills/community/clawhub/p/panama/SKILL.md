---
name: Panama
slug: panama
version: 1.0.0
homepage: https://clawic.com/skills/panama
changelog: "Initial release with verified Panama entry guidance, region playbooks, and practical trip logistics."
description: Plan Panama trips with region-aware routing, verified entry rules, island and highland logistics, and practical tourist safety.
metadata: {"clawdbot":{"emoji":"🇵🇦","requires":{"bins":[],"config":["~/panama/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/panama/` doesn't exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a Panama trip and needs practical guidance beyond generic inspiration: entry rules, region choice, transport logic, seasonality, safety, and day-to-day execution.

## Architecture

Memory lives in `~/panama/`. See `memory-template.md` for structure.

```
~/panama/
└── memory.md     # Trip context and evolving constraints
```

## Quick Reference

| Topic | File |
|-------|------|
| **Entry and Border** | |
| Passport, visa, solvency, return ticket | `entry-and-documents.md` |
| Customs, affidavit, cash, airport arrival logic | `customs-and-border.md` |
| **Planning Backbone** | |
| Regions and trip-shape strategy | `regions.md` |
| Sample itineraries from 4 to 14 days | `itineraries.md` |
| Where to stay by trip style | `accommodation.md` |
| Budget realities and cost pressure points | `budget-and-costs.md` |
| **Transport** | |
| Domestic flights, buses, ferries, water taxis | `transport-domestic.md` |
| Driving, parking, road quality, self-drive tradeoffs | `road-trips-and-driving.md` |
| Connectivity, SIMs, cards, practical apps | `telecoms-and-apps.md` |
| **Major Regions and Bases** | |
| Panama City playbook | `panama-city.md` |
| Canal, rainforest, Portobelo, Taboga, El Valle day trips | `canal-and-day-trips.md` |
| Bocas del Toro islands playbook | `bocas-del-toro.md` |
| Guna Yala and San Blas logistics | `guna-yala-and-san-blas.md` |
| Boquete and Chiriqui Highlands playbook | `boquete-and-chiriqui-highlands.md` |
| Santa Catalina and Coiba strategy | `santa-catalina-and-coiba.md` |
| Azuero, Playa Venao, Pedasi, Cambutal | `azuero-and-pacific-coast.md` |
| **Lifestyle and Execution** | |
| Food and regional specialties | `food-guide.md` |
| Nightlife by destination type | `nightlife.md` |
| Traveling with children | `family-travel.md` |
| Accessibility and mobility realities | `accessibility.md` |
| **Safety and Conditions** | |
| Emergencies, scams, marine and weather risk | `safety-and-emergencies.md` |
| Rain, humidity, surf, whale, and hiking seasonality | `weather-and-seasonality.md` |
| **Tools** | |
| Research map and official sources | `sources.md` |

## Core Rules

### 1. Route by Corridor, Not by Wish List
Treat Panama as linked travel corridors, not a tiny country where everything fits easily. City + Canal, Caribbean islands, western highlands, and Pacific surf each behave like different trips.

### 2. Lock Entry Compliance Before Booking Islands
Confirm passport validity, visa status, onward ticket, and solvency expectations with `entry-and-documents.md` before locking island stays or domestic connections.

### 3. Ask for Month First
Use `weather-and-seasonality.md` before building routes. Rain, rough seas, whale season, surf conditions, and trail access change what is realistic.

### 4. Always Offer Two Logistics Models
For most trips, provide two workable approaches:
- Low-friction model using flights or direct transfers
- Lower-cost model using buses, boats, and fewer bases

### 5. Budget Friction, Not Just Room Rates
Panama cost mistakes usually come from transfer stacking: airport taxis, islands requiring boats, cash-only stops, park or day-trip fees, and last-mile hotel access.

### 6. Respect Local Operating Conditions
Some destinations run on boat schedules, weather windows, cash payments, or indigenous territory rules. Treat those as hard constraints, not optional details.

### 7. Deliver Actionable Plans
Output should include:
- Base strategy
- Transfer plan with realistic buffers
- Reservation timing
- Weather or sea-state fallback
- Quick safety notes for the exact route

## Common Traps

- Trying to combine Panama City, San Blas, Bocas, and Boquete in one short trip.
- Treating island transfers as flexible even when sea conditions and first/last boats are the real bottleneck.
- Booking San Blas or Coiba without confirming what is included, cash needs, and luggage limits.
- Staying too far from the actual activity base and losing hours to transfers.
- Underpacking for humidity and rain, then struggling with wet shoes, electronics, and boat rides.
- Assuming cards work everywhere outside Panama City and major hotels.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/panama/`

**This skill does NOT:** Access files outside `~/panama/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `car-rental` — Better rental, pickup, and road-trip decisions
- `booking` — Reservation workflows and confirmation hygiene
- `food` — Deeper restaurant and cuisine recommendations
- `english` — Language backup for calls, bookings, and service interactions

## Feedback

- If useful: `clawhub star panama`
- Stay updated: `clawhub sync`
