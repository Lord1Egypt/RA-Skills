---
name: Paraguay
slug: paraguay
version: 1.0.0
homepage: https://clawic.com/skills/paraguay
changelog: "Initial release with Paraguay city playbooks, border logistics, river escapes, and practical trip planning."
description: Plan Paraguay trips with border-savvy routing, river-city priorities, and practical guidance for Asuncion, Encarnacion, Ciudad del Este, and the Chaco.
metadata: {"clawdbot":{"emoji":"🇵🇾","requires":{"bins":[],"config":["~/paraguay/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/paraguay/` does not exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a Paraguay trip and needs more than generic inspiration: how to split time between Asuncion, the south, the border, and the Chaco, plus food, payments, heat, and day-to-day logistics.

## Architecture

Memory lives in `~/paraguay/`. See `memory-template.md` for structure.

```
~/paraguay/
└── memory.md     # Trip context and evolving preferences
```

## Quick Reference

Use this map to load the module that changes the next travel decision.

| Topic | File |
|-------|------|
| **Cities and Bases** | |
| Asuncion city strategy | `asuncion.md` |
| Encarnacion waterfront and mission base | `encarnacion.md` |
| Ciudad del Este border and shopping logic | `ciudad-del-este.md` |
| Chaco and north planning | `chaco-and-north.md` |
| **Planning Backbone** | |
| Sample routes and trip shapes | `itineraries.md` |
| Where to stay by trip type | `accommodation.md` |
| Money, cash, cards, and exchange logic | `money-and-payments.md` |
| Border crossings and shopping strategy | `border-shopping.md` |
| Useful apps and workflow helpers | `apps.md` |
| **Food and Lifestyle** | |
| Core dishes and where they matter | `food-guide.md` |
| Terere, cocido, and drink culture | `yerba-and-drinks.md` |
| Nightlife by city and season | `nightlife.md` |
| **Experiences and Nature** | |
| Best experiences by trip style | `experiences.md` |
| River beaches and waterfront escapes | `beaches-and-waterfronts.md` |
| Parks, hikes, and nature days | `hiking-and-nature.md` |
| **Reference and Practical** | |
| Macro-regions and what each is for | `regions.md` |
| Etiquette, timing, and social norms | `culture.md` |
| Family travel guidance | `with-kids.md` |
| Flights, buses, driving, and transfers | `transport.md` |
| SIMs, coverage, plugs, and Wi-Fi | `telecoms.md` |
| Emergencies and safety basics | `emergencies.md` |

## Core Rules

### 1. Pick the Trip Shape First
Decide whether the trip is a city break, a river-and-missions route, a border-shopping run, or a Chaco nature trip before recommending stops. Paraguay looks compact on a map but the experience changes a lot by corridor.

### 2. Treat Border Cities as Operational Places
Ciudad del Este and Encarnacion are not just attractions. They are border systems with bridge timing, shopping logic, and day-flow constraints. Use `border-shopping.md` before promising easy same-day combinations.

### 3. Heat and Seasonality Change Everything
Ask for the month early. Summer heat, afternoon storms, and winter cool spells change whether waterfront time, long walks, or Chaco days are sensible.

### 4. Use Asuncion as a Decision Hub
Asuncion is often the easiest arrival base for food, museums, and logistics, but not always the emotional highlight of the trip. Recommend it for structure, then decide whether to add south, east, or Chaco.

### 5. Give Payment Guidance With the Route
Paraguay trips work better when cash, cards, ATMs, and border pricing are handled up front. Pair itinerary advice with `money-and-payments.md`.

### 6. Prefer Specific Recommendations
Do not say "visit the Jesuit missions" or "go to the lake." Say which mission pair, which waterfront, which neighborhood, and when each works best.

### 7. Deliver Execution, Not Just Ideas
Output should include:
- best base or base pair
- day-by-day flow with transfer buffers
- weather or heat caveats
- payment and safety notes
- what is not worth squeezing in

## Common Traps

- Trying to combine Asuncion, Encarnacion, Ciudad del Este, and the Chaco in one short trip.
- Assuming a border hop is a 20-minute formality instead of a half-day variable.
- Underestimating afternoon heat and planning long exposed walks in mid-summer.
- Treating Ciudad del Este as a relaxed city break instead of a shopping-and-logistics environment.
- Adding lake or river beach time without checking the season and local conditions.
- Staying only in transit zones and missing Paraguay's stronger food and cultural experiences.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/paraguay/`

**This skill does NOT:** Access files outside `~/paraguay/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` - General trip planning and itinerary structure
- `booking` - Reservation workflows and confirmation hygiene
- `food` - Deeper restaurant and cuisine planning
- `spanish` - Language support for bookings and practical interactions
- `argentina` - Better regional planning for cross-border combinations

## Feedback

- If useful: `clawhub star paraguay`
- Stay updated: `clawhub sync`
