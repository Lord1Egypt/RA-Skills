---
name: New York City
slug: new-york-city
version: 1.0.0
homepage: https://clawic.com/skills/new-york-city
description: Navigate New York City for visits, moves, neighborhoods, transit, housing, food, work, and daily street-level decisions.
changelog: "Initial release with borough-aware guidance for visits, moves, transit, neighborhoods, and daily city logistics."
metadata: {"clawdbot":{"emoji":"🗽","requires":{"bins":[],"config":["~/new-york-city/"]},"os":["linux","darwin","win32"],"configPaths":["~/new-york-city/"]}}
---

## When to Use

User needs New York City guidance that generic travel or relocation advice usually gets wrong: choosing a borough or neighborhood, planning a visit, moving into the city, handling transit, avoiding tourist traps, or making housing and commute decisions that only work in NYC.

This skill should activate for four modes: visiting New York City, moving to New York City, living in New York City, and working or studying in New York City.

## Architecture

This skill works statelessly for one-off New York City questions. If the user wants continuity across sessions, memory lives in `~/new-york-city/`. If `~/new-york-city/` does not exist, read `setup.md`, explain planned local storage in plain language, and ask for confirmation before creating files. See `memory-template.md` for structure.

```text
~/new-york-city/
└── memory.md     # User context, borough, timelines, constraints, and open loops
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Boroughs, neighborhoods, and where to base yourself | `neighborhoods-and-bases.md` |
| Moving, renting, and settling in | `moving-and-housing.md` |
| Subway, buses, ferries, airports, and commute design | `transit-and-airports.md` |
| Eating well without falling into tourist traps | `food-and-dining.md` |
| Street safety, weather, and city reality checks | `safety-and-weather.md` |
| Work, study, startups, and local professional fit | `work-study-and-startups.md` |
| Visiting strategy, itineraries, and booking logic | `visiting-and-itineraries.md` |
| Official sources map | `sources.md` |

## Core Rules

### 1. Classify the User Before Giving Advice
- Decide whether the user is a visitor, a future resident, a current resident, or someone optimizing work or study life in the city.
- Then anchor the answer to borough, neighborhood, budget, and commute pattern.
- If that context is missing, ask for it before pretending all of NYC works the same way.

### 2. Borough and Commute Beat Landmark Thinking
- The right New York City answer usually depends on where the user must go every week, not what they saw on social media.
- Manhattan, Brooklyn, Queens, the Bronx, and Staten Island do not solve the same problem.
- Use `neighborhoods-and-bases.md` before naming a place to stay or live.

### 3. Time Beats Distance
- In NYC, one mile is not the decision-maker. Transfers, stairs, platform heat, late-night service, airport access, and last-mile walking usually matter more.
- Use `transit-and-airports.md` before saying something is "easy."

### 4. Deliver Practical Tradeoffs, Not City Mythology
- New York users usually need the honest tradeoff: quieter but slower, cheaper but farther, fun but exhausting, convenient but tiny.
- Frame choices by daily routine, not by hype.

### 5. Use Official Sources for Unstable Rules
- Transit fares, museum policies, airport access details, short-term rental rules, and city service workflows can change.
- Verify current information from official city or transit sources before giving precise operational steps.
- If current verification is blocked, say so plainly and avoid false precision.

## Common Traps

- Treating "New York" as Manhattan only.
- Recommending a neighborhood without mapping the actual commute and late-night return path.
- Sending visitors to Times Square restaurants, fake speakeasies, and generic "top 10" stops without filtering for value.
- Assuming car ownership, airport transfers, or grocery routines work the same in every borough.
- Giving rent, fare, or hotel numbers with false precision instead of ranges and verification guidance.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.nyc.gov | Page requests only unless user explicitly wants city-service workflow help | City services, housing rules, and local guidance |
| https://new.mta.info | Page requests only unless user explicitly wants route-specific help | Subway, bus, commuter rail, and service guidance |
| https://omny.info | Page requests only | Fare payment and contactless transit guidance |
| https://www.nyc.gov/311 | Page requests only unless user explicitly wants local issue reporting guidance | City issue reporting and service lookup |
| https://www.panynj.gov | Page requests only unless user explicitly wants airport workflow details | JFK, LaGuardia, bus terminal, and regional travel infrastructure |

No other data is sent externally.

## Security & Privacy

**Data that may leave your machine:**
- Public page requests to official New York City or transit websites
- Borough, ZIP, or station context only when the user asks for location-specific guidance

**Data that stays local:**
- Neighborhood preference, move timeline, budget notes, commute constraints, and open tasks in `~/new-york-city/`

**This skill does NOT:**
- Book or submit anything on the user's behalf without explicit instruction
- Store credentials, payment information, or passport details in local memory
- Assume borough-level advice applies to a specific block or building

## Trust

By using this skill, location details such as borough, ZIP, station, or airport may be checked against official New York City or transit websites when the user asks for precise guidance.

Only install if you trust those public services with that lookup context.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General itinerary design and travel planning structure
- `booking` — Reservation workflows for hotels, flights, and schedules
- `business` — Broader business operations guidance beyond city-specific tradeoffs
- `car-rental` — Rental-car decisions for airport pickups and day trips
- `health-insurance` — More detailed plan and coverage comparison support

## Feedback

- If useful: `clawhub star new-york-city`
- Stay updated: `clawhub sync`
