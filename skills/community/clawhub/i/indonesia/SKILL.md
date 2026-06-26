---
name: Indonesia
slug: indonesia
version: 1.0.0
homepage: https://clawic.com/skills/indonesia
changelog: "Initial release with Indonesia entry guidance, island-routing playbooks, and practical travel logistics."
description: Plan Indonesia trips with island-routing logic, verified entry guidance, weather-aware logistics, and practical local execution.
metadata: {"clawdbot":{"emoji":"🇮🇩","requires":{"bins":[],"config":["~/indonesia/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/indonesia/` does not exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning an Indonesia trip and needs practical guidance beyond generic highlights: visa pathway, island choice, route design, surf and weather fit, transport tradeoffs, and on-the-ground execution across a large archipelago.

## Architecture

Memory lives in `~/indonesia/`. See `setup.md` for first activation flow and `memory-template.md` for the file structure.

```text
~/indonesia/
└── memory.md     # Trip context and evolving constraints
```

## Quick Reference

Use this map to load only the Indonesia subtopic that changes the decision in front of you.

| Topic | File |
|-------|------|
| **Entry and Arrival** | |
| Visa, VOA, onward proof, stay limits | `entry-and-documents.md` |
| Customs, e-CD, airport arrival, first-hour logic | `customs-and-arrival.md` |
| **Planning Backbone** | |
| Island choice and route strategy | `regions.md` |
| Sample itineraries | `itineraries.md` |
| Where to stay by route style | `accommodation.md` |
| Budget planning | `budget-and-costs.md` |
| Cards, cash, and payment norms | `payments-and-money.md` |
| **Transport** | |
| Flights, trains, ferries, boats, and city transit | `transport-domestic.md` |
| Driving and scooter risk | `road-trips-and-driving.md` |
| **Destination Playbooks** | |
| Bali, Uluwatu, Ubud, Canggu, Nusa islands | `bali-and-nusa-islands.md` |
| Jakarta, Bandung, and West Java gateways | `jakarta-and-west-java.md` |
| Yogyakarta, Borobudur, and Prambanan | `yogyakarta-and-central-java.md` |
| East Java, Bromo, and Ijen | `east-java-and-bromo-ijen.md` |
| Lombok, Gilis, and quieter beach routes | `lombok-and-gili-islands.md` |
| Komodo, Flores, and Labuan Bajo | `komodo-and-flores.md` |
| Sumatra and orangutan or volcano routes | `sumatra-and-bukit-lawang.md` |
| **Lifestyle and Execution** | |
| Food by island and meal style | `food-guide.md` |
| Nightlife by destination type | `nightlife.md` |
| Traveling with children or older relatives | `family-travel.md` |
| Accessibility and low-mobility strategy | `accessibility.md` |
| **Safety and Conditions** | |
| Emergencies, health, scams, volcano and sea risk | `safety-and-emergencies.md` |
| Climate, monsoon timing, and seasonality | `weather-and-seasonality.md` |
| **Tools** | |
| Connectivity and useful apps | `telecoms-and-apps.md` |
| Official source map | `sources.md` |

## Core Rules

### 1. Route by Islands and Transfer Friction, Not by Postcard Count
Indonesia punishes over-routing. For most users, keep one main island cluster per week:
- Bali plus Nusa or Bali plus Lombok
- Java backbone with Yogyakarta and East Java
- Flores and Komodo
- Sumatra wildlife and volcanoes

### 2. Clear Entry Path First
Use `entry-and-documents.md` before recommending non-refundable flights. Visa-free, VOA, onward-proof expectations, passport validity, and Bali levy assumptions can change how safe the booking path is.

### 3. Match the Island to the User, Not the Hype
Always identify the user's real objective:
- First trip and easy logistics
- Surf and beach time
- Diving and boats
- Culture and temples
- Volcanoes and hiking
- Family pacing
- Low-friction luxury or remote nature

### 4. Make Every Plan Season-Aware
Use `weather-and-seasonality.md` before locking islands, boat days, dive trips, volcano starts, or beach-heavy routes. Indonesia weather is not one national answer, and sea conditions matter as much as rain.

### 5. Treat Boats, Scooters, and Mountain Sun as Real Risk
Do not romanticize fast boats, scooters, or volcano starts:
- Tight same-day boat plus flight chains are fragile
- Beginner scooter recommendations are often bad advice
- Heat, dehydration, altitude, rough roads, and poor clinic access change destination fit

### 6. Budget With Real Archipelago Math
Price the whole route, not the villa headline:
- Domestic flight baggage
- Boat tickets and harbor transfers
- Driver days and airport friction
- Tourist levy, visa fees, park fees, and guide costs
- Cash-only moments outside major hubs

### 7. Deliver Operational Plans
Every output should include:
- Base logic and what to skip
- Day-by-day flow with realistic transfer windows
- What must be booked early
- Weather or sea-condition fallback
- Safety, payment, and mobility notes for the chosen route

## Common Traps

- Treating Indonesia as "Bali and maybe something else" instead of an archipelago with very different operating conditions.
- Trying Bali, Yogyakarta, Komodo, Gilis, and Sumatra in one short trip.
- Assuming cards, ATMs, data, sidewalks, and English work equally well everywhere.
- Booking fast boats and flights on the same day with no buffer.
- Sending families or older travelers to Nusa Penida, Bromo, or Komodo without discussing stairs, roads, ladders, heat, or medical backup.
- Giving one monsoon answer for the whole country.
- Recommending scooters by default to users who are tired, inexperienced, or traveling in rain season.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/indonesia/`

**This skill does NOT:** Access files outside `~/indonesia/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `booking` — Reservation workflows and confirmation hygiene
- `food` — Deeper restaurant and cuisine planning
- `esim` — Better mobile-data setup before arrival
- `indonesian` — Language support for bookings, transport, and daily interactions

## Feedback

- If useful: `clawhub star indonesia`
- Stay updated: `clawhub sync`
