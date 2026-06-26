---
name: Macau
slug: macau
version: 1.0.0
homepage: https://clawic.com/skills/macau
description: Navigate Macau as visitor, resident, worker, student, or founder with districts, transport, costs, borders, culture, and practical local context.
changelog: "Initial release with district guides, border planning, cost ranges, and practical Macau travel and relocation coverage."
metadata: {"clawdbot":{"emoji":"MO","requires":{"bins":[],"config":["~/macau/"]},"os":["linux","darwin","win32"]}}
---

## When to Use

User asks about Macau for any purpose: visiting, relocating, working in hospitality or gaming-adjacent roles, studying, or setting up cross-border plans with Hong Kong or Zhuhai.

## Architecture

Memory lives in `~/macau/`. If `~/macau/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/macau/
`-- memory.md     # User context for trip, relocation, work, and border logistics
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| **Visitors** | |
| Attractions and what matters | `visitor-attractions.md` |
| 1, 2, and 3 day routes | `visitor-itineraries.md` |
| Where to stay by trip style | `visitor-lodging.md` |
| Border, money, and practical tips | `visitor-tips.md` |
| **Districts** | |
| Quick comparison | `neighborhoods-index.md` |
| Historic peninsula districts | `neighborhoods-historic.md` |
| NAPE, Outer Harbour, east peninsula | `neighborhoods-central.md` |
| Taipa village and central Taipa | `neighborhoods-taipa.md` |
| Cotai and integrated resorts | `neighborhoods-cotai.md` |
| Coloane village and south side | `neighborhoods-coloane.md` |
| Choosing guide | `neighborhoods-choosing.md` |
| **Food** | |
| Dining scene overview | `food-overview.md` |
| Macanese, Cantonese, and local staples | `food-local.md` |
| International and hotel dining | `food-international.md` |
| Best food areas | `food-areas.md` |
| Reservations, tipping, and practical rules | `food-practical.md` |
| **Practical** | |
| Moving and settling | `resident.md` |
| Buses, LRT, ferries, walking, taxis | `transport.md` |
| Cost of living | `cost.md` |
| Safety and legal realities | `safety.md` |
| Weather and typhoon planning | `climate.md` |
| Banking, SIM, payments, and utilities | `local.md` |
| **Career** | |
| Tech and digital work reality | `tech.md` |
| Company setup and taxes | `business.md` |
| Entry and residency paths | `visas.md` |
| Startup and diversification landscape | `startup.md` |
| **Lifestyle** | |
| Culture and etiquette | `culture.md` |
| Healthcare and hospitals | `healthcare.md` |
| Schools and universities | `education.md` |
| Expat and local lifestyle | `lifestyle.md` |
| Driving, parking, and scooter logic | `driving.md` |

## Core Rules

### 1. Identify the User's Macau First
- Clarify whether the user means old-town sightseeing, casino resort time, family relocation, cross-border commuting, or a Greater Bay Area business base.
- Macau is tiny, but user needs differ sharply between Peninsula, Taipa, Cotai, and Coloane.

### 2. Treat Borders as a Core Planning Layer
- Most friction comes from entry rules, ferry or bridge timing, and day-trip or commute assumptions.
- Always ask where the person is arriving from: Hong Kong, Zhuhai, mainland China, or direct flight.
- Re-check current entry rules in `visas.md` before claiming certainty.

### 3. Macau Is Not Just Casinos
- Gaming and tourism dominate the economy, but useful guidance also means heritage streets, Portuguese legacy, food, family logistics, universities, and GBA positioning.
- Avoid giving casino-only itineraries unless the user explicitly wants that.

### 4. Small Geography Does Not Mean Zero Logistics
- The peninsula is walkable in parts, but heat, humidity, crowds, and bridge bottlenecks change the real experience.
- Cotai resorts look close on the map yet still require planned walking or shuttles.
- Load `transport.md` and the relevant district file before estimating travel times.

### 5. Current Data Snapshot (March 2026)

| Item | Range |
|------|-------|
| 1BR rent, peninsula | MOP 8,000-14,000/month |
| 1BR rent, Taipa/Cotai | MOP 12,000-20,000/month |
| Median monthly employment earnings | Around MOP 17,000 |
| Bus fare | MOP 6 per ride |
| LRT fare | MOP 6-12 |
| Taxi flag drop | MOP 21 |
| Casual meal | MOP 60-120 |

### 6. Cash, Currency, and Payment Reality
- Macau pataca (MOP) is the official currency.
- Hong Kong dollars are widely accepted in tourist areas, often at 1:1, which is convenient but not favorable.
- Smaller shops, bakeries, taxis, and some old-town spots still work better with cash or local e-wallets than with foreign cards.

### 7. Match the District to the User

| Profile | Best Areas |
|---------|------------|
| First-time tourist | Senado / St. Paul's / Barra or Taipa |
| Resort-focused weekend | Cotai |
| Heritage + food traveler | Historic peninsula + Taipa Village |
| Family relocation | Taipa or selected south peninsula pockets |
| Budget-conscious stay | Inner peninsula and simple Taipa hotels |
| Quiet escape | Coloane |

## Macau-Specific Traps

- Assuming Macau and Hong Kong share the same entry rules or money behavior.
- Staying only in Cotai, then claiming "Macau has no local character."
- Treating a casino resort as a normal urban neighborhood.
- Assuming all vendors take cards and all prices are quoted in HKD.
- Underestimating weekend or holiday queues at ports and the bridge.
- Planning heavy outdoor walking in July or August afternoons.
- Forgetting that many good local restaurants close between lunch and dinner.
- Thinking Portuguese heritage means Portugal-style pace; Macau often runs faster and denser.

## Legal Awareness

- Gambling is legal only in licensed venues.
- Drugs are a serious offense; do not improvise.
- Photography is generally fine in streets, but gaming floors and some museums or temples restrict it.
- Public order, smoking, and customs rules tighten around ports, casinos, and transport areas.
- Do not give immigration certainty without checking the latest official notices in `visas.md`.

## Greater Bay Area Context

Macau works best when framed correctly inside the Greater Bay Area:
- Tourism and hospitality hub with deep China-facing visitor flows
- Strong links to Hong Kong for flights and finance
- Practical land connection to Zhuhai for cost relief and mainland access
- Much weaker as a pure tech base than Shenzhen or Hong Kong

## Security & Privacy

**Data that stays local:** Trip, relocation, and district preferences in `~/macau/`

**This skill does NOT:**
- Access files outside `~/macau/`
- Make network requests
- Claim border, visa, or residency certainty without telling the user to re-check official sources

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` - General trip planning and itinerary structure
- `money` - Budgeting, exchange-rate thinking, and cost trade-offs
- `traditional-chinese` - Traditional Chinese context useful across Macau and nearby regions
- `taiwan` - Another Chinese-language destination with practical travel depth
- `dubai` - Another compact, tourism-heavy city benchmark with relocation depth

## Feedback

- If useful: `clawhub star macau`
- Stay updated: `clawhub sync`
