---
name: New Zealand
slug: new-zealand
version: 1.0.0
homepage: https://clawic.com/skills/new-zealand
changelog: "Initial release with island-aware routing, practical transport guidance, and deep New Zealand travel playbooks."
description: Discover New Zealand with island-aware routing, practical road-trip logistics, outdoor safety, and local food and region guidance.
metadata: {"clawdbot":{"emoji":"🇳🇿","requires":{"bins":[],"config":["~/new-zealand/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/new-zealand/` doesn't exist or is empty, read `setup.md` and start naturally.

## When to Use

User planning a trip to New Zealand or asking for local insights: which island to prioritize, where to base, how to drive safely, what to book early, and how to handle weather, food, costs, and outdoor logistics.

## Architecture

Memory lives in `~/new-zealand/`. See `memory-template.md` for structure.

```text
~/new-zealand/
└── memory.md     # Trip context
```

## Quick Reference

| Topic | File |
|-------|------|
| **Major Hubs and Regions** | |
| Auckland complete guide | `auckland.md` |
| Wellington complete guide | `wellington.md` |
| Rotorua and Taupo complete guide | `rotorua-taupo.md` |
| Queenstown complete guide | `queenstown.md` |
| Christchurch complete guide | `christchurch.md` |
| Nelson, Abel Tasman, and Marlborough | `nelson-marlborough.md` |
| Fiordland and Southland playbook | `fiordland-southland.md` |
| **Planning** | |
| Core itineraries | `itineraries.md` |
| Island and region differences | `regions.md` |
| Where to stay by style | `accommodation.md` |
| Entry and biosecurity planning | `entry-and-biosecurity.md` |
| Useful apps | `apps.md` |
| **Food and Drink** | |
| Regional dishes and restaurant strategy | `food-guide.md` |
| Wine regions and tasting logic | `wine.md` |
| **Experiences** | |
| Signature experiences | `experiences.md` |
| Beaches and coastal planning | `beaches.md` |
| Hikes and track safety | `hiking.md` |
| Nightlife by city type | `nightlife.md` |
| **Reference** | |
| Culture, etiquette, expectations | `culture.md` |
| Seasonality and climate strategy | `seasonality.md` |
| Traveling with children | `with-kids.md` |
| Wildlife and outdoor safety | `wildlife-safety.md` |
| Official source map | `sources.md` |
| **Practical** | |
| Flights, ferries, trains, and driving | `transport.md` |
| Phone and internet | `telecoms.md` |
| Payments and cost planning | `payment-and-costs.md` |
| Emergencies and safety | `emergencies.md` |

## Core Rules

### 1. Route by Island and Corridor
Do not build New Zealand like Europe. For short trips, choose one island or one dominant corridor:
- Upper North Island
- Wellington and central plateau
- Christchurch to Mackenzie and Queenstown
- Nelson and Abel Tasman
- Fiordland and deep south

### 2. Ask for Month Before Locking the Route
The right New Zealand plan changes with season:
- Summer = longer days, peak demand, busy roads
- Winter = ski strength but shorter daylight and alpine risk
- Shoulder season = best value in many regions
- Fiordland and West Coast weather can change the whole plan any month

### 3. Driving Reality Beats Map Fantasy
New Zealand roads are slower than visitors expect:
- Two-lane roads dominate
- One-lane bridges are common
- Night driving is tiring
- Mountain, rain, and gravel sections change timing fast
- Add buffer before ferries, flights, and Milford-type day trips

### 4. Biosecurity and Safety Are Real Constraints
Check `entry-and-biosecurity.md` before promising a frictionless arrival.
- Boots, food, hiking gear, and medications can matter at the border
- Track weather, surf flags, and DOC alerts before outdoor plans
- Great Walks and huts sell out early

### 5. Specific Over Generic
Do not say "see fjords and wineries." Say "base in Te Anau for Fiordland, book the Milford morning cruise, and put winery tasting in Gibbston on a separate Queenstown day."

### 6. Match the Trip Style

| Traveler | Focus on |
|----------|----------|
| Foodie | `food-guide.md`, `wine.md`, `wellington.md` |
| Road trip | `transport.md`, `regions.md`, `itineraries.md` |
| Hiking and outdoors | `hiking.md`, `wildlife-safety.md`, `fiordland-southland.md` |
| Family | `with-kids.md`, `accommodation.md`, `rotorua-taupo.md` |
| City plus nature | `auckland.md`, `wellington.md`, `christchurch.md` |
| Adventure | `queenstown.md`, `experiences.md`, `seasonality.md` |

## Common Traps

- Trying to "do both islands" in one week.
- Treating a 4-hour drive as an easy half-day with no stops.
- Booking Queenstown or Fiordland late in summer.
- Driving straight off a long-haul flight.
- Assuming beaches are always safe because the weather looks calm.
- Building outdoor days without rain, wind, or track-closure backup.
- Forgetting that small towns close earlier than big-city travelers expect.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/new-zealand/`

**This skill does NOT:** Access files outside `~/new-zealand/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structuring
- `booking` — Reservation and timing support workflows
- `car-rental` — Better self-drive planning and handoff logistics
- `food` — Deeper dining and cuisine recommendations
- `english` — Communication and booking clarity

## Feedback

- If useful: `clawhub star new-zealand`
- Stay updated: `clawhub sync`
