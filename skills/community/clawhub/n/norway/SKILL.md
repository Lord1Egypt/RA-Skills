---
name: Norway
slug: norway
version: 1.0.0
homepage: https://clawic.com/skills/norway
changelog: "Initial release with verified Norway entry rules, fjord and Arctic routing, and practical travel logistics."
description: Plan Norway trips with fjord and Arctic routing, verified entry rules, multimodal logistics, and practical seasonal safety.
metadata: {"clawdbot":{"emoji":"🇳🇴","requires":{"bins":[],"config":["~/norway/"]},"os":["linux","darwin","win32"]}}
---

## When to Use

User is planning a Norway trip and needs operational guidance beyond generic scenery lists: Schengen entry checks, fjord vs Arctic route choice, train-ferry-flight-car tradeoffs, seasonal risk, budget reality, and on-the-ground execution.

## Architecture

Memory lives in `~/norway/`. If `~/norway/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/norway/
└── memory.md     # Trip context, route logic, and evolving constraints
```

## Data Storage

- `~/norway/memory.md` stores durable trip context, route decisions, and constraints for future Norway planning.
- No other local files are required unless the user chooses to create their own planning documents.

## Quick Reference

Use this map to load only the Norway subtopic that changes the decision in front of you.

| Topic | File |
|-------|------|
| **Entry and Compliance** | |
| Tourist entry, Schengen stays, ID checks | `entry-and-documents.md` |
| **Planning Backbone** | |
| Macro-regions and route logic | `regions.md` |
| Sample itineraries for 5-18 days | `itineraries.md` |
| Where to stay by trip style | `accommodation.md` |
| Budget framing and cost traps | `budget-and-costs.md` |
| Cards, cash, tax-free, alcohol pricing | `payments-and-tax-free.md` |
| **Transport and Outdoors** | |
| Flights, trains, ferries, buses, airport moves | `transport-domestic.md` |
| Self-drive, ferries, tolls, mountain-road reality | `road-trips-and-driving.md` |
| Fjord routes and scenic-road strategy | `fjords-and-scenic-routes.md` |
| Hikes, cabins, right-to-roam, outdoor planning | `hiking-and-outdoors.md` |
| **Major Regions and Bases** | |
| Oslo and nearby base strategy | `oslo-and-oslofjord.md` |
| Bergen and the classic western fjords | `bergen-and-western-fjords.md` |
| Stavanger, Lysefjord, and the southwest | `stavanger-and-southwest.md` |
| Trondheim and central Norway | `trondheim-and-central-norway.md` |
| Lofoten and Vesteralen route logic | `lofoten-and-vesteralen.md` |
| Tromso, Senja, Alta, and the Arctic north | `tromso-and-arctic-north.md` |
| Svalbard practical planning | `svalbard.md` |
| **Lifestyle and Execution** | |
| Food strategy, supermarkets, alcohol reality | `food-guide.md` |
| Traveling with children or mixed ages | `family-travel.md` |
| Accessibility and low-mobility planning | `accessibility.md` |
| Emergencies, weather alerts, outdoor risk | `safety-and-emergencies.md` |
| Climate, aurora, and daylight logic | `weather-and-seasonality.md` |
| Connectivity, apps, tickets, and payments | `telecoms-and-apps.md` |
| Official source map | `sources.md` |

## Core Rules

### 1. Route by Corridor, Not by Postcard Count
For short trips, choose one main corridor: Oslo plus west, Bergen and fjords, Trondheim plus central coast, or Arctic north. Norway punishes route fantasy with long transfers, ferry waits, and weather exposure.

### 2. Ask for Month Before Naming a Route
The same map behaves differently in January, May, July, and October. Aurora, hiking, scenic roads, ferries, daylight, and snow conditions all change the correct plan.

### 3. Confirm Entry and Identity Friction Early
Before booking non-refundables, use `entry-and-documents.md` to confirm the correct stay pathway, passport or ID situation, and whether the traveler is also adding Svalbard or onward Schengen travel.

### 4. Always Offer Two Logistics Models
For any multi-stop trip, give at least two workable movement patterns:
- Rail and ferry heavy: more scenery, fewer long drives, more timetable dependence
- Self-drive or regional-flight heavy: more freedom, higher cost, more weather and toll exposure

### 5. Budget for Full Norway Math
Do not price the trip from hotel headlines alone. Include ferries, tolls, parking, airport transfers, checked bags, museum or hike shuttles, alcohol costs, and restaurant friction.

### 6. Protect the User from Arctic and Fjord Overreach
Flag bad combos early:
- Oslo, Bergen, Lofoten, and Tromso in one short trip
- Winter self-drive by travelers with no snow-road experience
- Tight same-day chains across ferries, mountain roads, and flights
- Iconic hikes without weather, fitness, or backup logic

### 7. Deliver Operational Plans
Output should include:
- Best base or base pair
- Day-by-day flow with realistic transfer windows
- Booking deadlines or low-inventory warnings
- Weather backup and downgrade options
- Safety notes for road, sea, and outdoor exposure

## Common Traps

- Treating Norway as a compact country where Oslo, fjords, Lofoten, and Tromso fit naturally into one week.
- Building fjord drives from map distance instead of actual ferry and road time.
- Assuming aurora is guaranteed just because the user goes north in winter.
- Choosing a rental car before checking whether trains, ferries, and one smart base solve the trip better.
- Ignoring Sunday, shoulder-season, and remote-area service reductions.
- Planning iconic hikes or viewpoints without checking weather, road openings, or local transport.
- Underestimating how much food, alcohol, and casual dining change the budget.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/norway/`

**This skill does NOT:** Access files outside `~/norway/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `booking` — Reservation workflows and confirmation hygiene
- `car-rental` — Better self-drive strategy and handoff logistics
- `food` — Deeper restaurant and cuisine planning
- `english` — Language support for bookings, menus, and practical interactions

## Feedback

- If useful: `clawhub star norway`
- Stay updated: `clawhub sync`
