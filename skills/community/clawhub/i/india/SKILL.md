---
name: India
slug: india
version: 1.0.0
homepage: https://clawic.com/skills/india
changelog: Added country-level routing, city guides, and practical travel advice for first-time and repeat India trips.
description: Plan India trips with specific neighborhoods, regional food calls, route choices, and grounded advice that avoids common travel mistakes.
metadata: {"clawdbot":{"emoji":"🇮🇳","requires":{"bins":[],"config":["~/india/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/india/` does not exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a trip to India or wants local guidance on cities, routes, food, safety, timing, and how to avoid tourist-default recommendations.

## Architecture

Memory lives in `~/india/`. See `memory-template.md` for structure.

```
~/india/
└── memory.md     # Trip context, pacing, preferences, and warnings already given
```

## Quick Reference

Load only the files that fit the current route, city, or friction point. India trips get better when the advice narrows fast.

| Topic | File |
|-------|------|
| **Cities** | |
| Delhi complete guide | `delhi.md` |
| Mumbai complete guide | `mumbai.md` |
| Jaipur complete guide | `jaipur.md` |
| Goa complete guide | `goa.md` |
| **Planning** | |
| Sample itineraries | `itineraries.md` |
| Where to stay by trip type | `accommodation.md` |
| Useful apps | `apps.md` |
| **Food** | |
| Regional dishes and what to order where | `food-guide.md` |
| **Experiences** | |
| Markets, classes, safaris, and high-signal activities | `experiences.md` |
| Best beaches by vibe | `beaches.md` |
| Best hiking and mountain bases | `hiking.md` |
| Nightlife by city and style | `nightlife.md` |
| **Reference** | |
| Regions, seasons, and what each area is best at | `regions.md` |
| Etiquette, bargaining, temple rules, and social context | `culture.md` |
| Traveling with children | `with-kids.md` |
| **Practical** | |
| Flights, trains, cars, and ride apps | `transport.md` |
| SIMs, eSIMs, OTPs, and connectivity | `telecoms.md` |
| Emergencies, hospitals, and common safety issues | `emergencies.md` |

## Core Rules

### 1. Match India to the Traveler
Do not default every first trip to "do everything". Separate:
- First-timer who needs a smooth entry to India
- Repeat visitor who wants depth
- Family, luxury, backpacker, food-led, or wellness-led traveler

### 2. Specific Over Generic
Do not say "visit Old Delhi" or "try local food". Say where to base, what street or market is worth it, what is overrated, and what order makes sense in a real day.

### 3. Regional Differences Matter

| Area | What changes |
|------|--------------|
| Delhi + North plains | Mughlai food, winter fog, intense traffic |
| Rajasthan | Heritage hotels, dry heat, best done by car + train |
| Mumbai + West coast | Fast pace, sea humidity, strong nightlife |
| Goa | Beach split matters more than town names |
| Himalayas | Weather and road conditions decide the plan |
| Kerala + South India | Slower pace, backwaters, spice and coconut-heavy food |

### 4. Timing is Infrastructure
- April-June: brutal heat in much of North India
- July-September: monsoon changes Goa, Kerala, and mountain roads
- October-March: easiest first-trip window for most routes
- Festival periods are amazing, but they change pricing, crowds, and transport availability

### 5. Reduce Friction Early
Call out the things that derail trips:
- Overpacked itineraries with too many one-night stops
- Long road transfers treated like short hops
- Blind trust in "top rated" tourist restaurants
- Assuming cards, UPI, and foreign numbers will work everywhere

### 6. Match Trip Style

| Traveler | Start with |
|----------|------------|
| First trip | `itineraries.md`, `delhi.md`, `jaipur.md` |
| Food-led | `food-guide.md`, `delhi.md`, `mumbai.md` |
| Beach + nightlife | `goa.md`, `beaches.md`, `nightlife.md` |
| Family | `with-kids.md`, `accommodation.md` |
| Nature | `hiking.md`, `regions.md`, `experiences.md` |
| Practical/logistics | `transport.md`, `telecoms.md`, `emergencies.md` |

## Common Traps

- Trying Delhi, Agra, Jaipur, Varanasi, Mumbai, and Goa in one week
- Treating a "5 hour drive" as predictable in India
- Landing in peak heat or monsoon without adapting the route
- Booking the cheapest hotel instead of the best-located one
- Eating at empty tourist-facing restaurants instead of busy local spots
- Assuming every foreign card, eSIM flow, or payment app will work on day one
- Forgetting temple and mosque dress rules, shoe rules, and photo etiquette

## Security & Privacy

**Data that stays local:** Trip preferences in `~/india/`

**This skill does NOT:**
- Access files outside `~/india/`
- Make network requests
- Store payment or passport details unless the user explicitly asks to track them in `~/india/`

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General travel planning
- `food` — Food recommendations and dining guidance
- `hindi` — Hindi language help for signs, menus, and quick phrases

## Feedback

- If useful: `clawhub star india`
- Stay updated: `clawhub sync`
