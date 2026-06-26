---
name: Greece
slug: greece
version: 1.0.0
homepage: https://clawic.com/skills/greece
changelog: "Initial release with island-mainland routing, ferry logistics, and practical Greece travel playbooks."
description: Plan Greece trips with island-mainland routing, ferry logistics, verified entry rules, and practical seasonal safety.
metadata: {"clawdbot":{"emoji":"🇬🇷","requires":{"bins":[],"config":["~/greece/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/greece/` does not exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a Greece trip and needs practical guidance beyond generic island lists: Schengen entry checks, island vs mainland choices, ferry and driving tradeoffs, seasonality, costs, and on-the-ground execution.

## Architecture

Memory lives in `~/greece/`. See `setup.md` for first activation flow and `memory-template.md` for the file structure.

```text
~/greece/
└── memory.md     # Trip context and evolving constraints
```

## Quick Reference

| Topic | File |
|-------|------|
| **Entry and Compliance** | |
| Schengen, passport, border, ferry docs | `entry-and-documents.md` |
| **Planning Backbone** | |
| Regions and route selection | `regions.md` |
| Sample itineraries | `itineraries.md` |
| Where to stay by trip style | `accommodation.md` |
| Budget planning | `budget-and-costs.md` |
| Cards, cash, and tips | `payments-and-tipping.md` |
| **Transport** | |
| Flights, KTEL, rail, Athens transport | `transport-domestic.md` |
| Ferry strategy and island hopping | `island-hopping-and-ferries.md` |
| Driving and car rental strategy | `road-trips-and-driving.md` |
| **History and Place Logic** | |
| Archaeological sites and museum planning | `archaeology-and-museums.md` |
| Athens and Attica playbook | `athens-and-attica.md` |
| Cyclades playbook | `cyclades.md` |
| Crete playbook | `crete.md` |
| Ionian Islands playbook | `ionian-islands.md` |
| Peloponnese and mainland south playbook | `peloponnese-and-mainland.md` |
| Northern Greece and Meteora playbook | `northern-greece-and-meteora.md` |
| **Lifestyle and Execution** | |
| Food by region and meal style | `food-guide.md` |
| Nightlife strategy by destination type | `nightlife.md` |
| Traveling with children | `family-travel.md` |
| Accessibility strategy | `accessibility.md` |
| **Safety and Conditions** | |
| Emergencies, fire, heat, sea conditions | `safety-and-emergencies.md` |
| Seasonality and weather planning | `weather-and-seasonality.md` |
| **Tools** | |
| Connectivity and practical apps | `telecoms-and-apps.md` |
| Official source map | `sources.md` |

## Core Rules

### 1. Route by Cluster, Not by Postcard Count
Keep one macro-cluster per week: Athens plus nearby mainland, one island group, or one larger island plus one city base. Ferry time and wind risk destroy overpacked plans.

### 2. Confirm Entry and Border Friction Before Booking
Use `entry-and-documents.md` first: Schengen stay limits, passport validity, visa pathway when relevant, and whether the traveler may face extra border processing during current EU rollout changes.

### 3. Match Transport to Geography
Always offer at least two movement models:
- Island-first with ferries and short hops
- Mainland or big-island route with car or bus logic

### 4. Make Every Plan Season-Aware
Use `weather-and-seasonality.md` before promising beaches, ferries, hikes, or archaeology-heavy daytime plans. Meltemi wind, heat, wildfire risk, and winter service reductions are trip-shaping factors.

### 5. Reserve High-Friction Items Early
Lock the hard pieces first:
- Key ferries on popular dates
- Acropolis or headline archaeological slots when timing matters
- Car rental for islands or remote mainland routes
- Premium sunset or beach-club zones in peak season

### 6. Budget for Full Greece Math
Price the real trip, not the hotel headline:
- Ferry seat vs cabin vs car cost
- Port transfers and taxi exposure
- Beach setup fees in some areas
- City tax, parking, and snack-day spend on islands

### 7. Always Build a Wind or Heat Backup
Every output should include:
- Primary route
- Buffer plan if ferries are disrupted
- Midday heat adaptation for summer
- Last-night-in-departure-city protection before flight home

## Common Traps

- Treating Santorini, Mykonos, Naxos, Crete, and Athens as a short seamless loop.
- Booking island hops without wind or port-transfer buffers.
- Assuming rail covers Greece well outside a few mainland corridors.
- Staying one night per stop and losing half the trip to packing and check-in friction.
- Planning archaeology-heavy days in July or August with no shade or hydration strategy.
- Choosing a car by habit when a compact walkable base is better.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/greece/`

**This skill does NOT:** Access files outside `~/greece/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` - General trip planning and itinerary structure
- `booking` - Reservation workflow and confirmation hygiene
- `car-rental` - Better island and mainland rental strategy
- `food` - Deeper restaurant and cuisine planning
- `greek` - Language support for bookings, menus, and local interactions

## Feedback

- If useful: `clawhub star greece`
- Stay updated: `clawhub sync`
