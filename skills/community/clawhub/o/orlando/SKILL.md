---
name: Orlando
slug: orlando
version: 1.0.0
homepage: https://clawic.com/skills/orlando
description: Navigate Orlando as visitor, resident, remote worker, or family with theme parks, neighborhoods, transit, costs, and local strategies.
changelog: "Initial release with deep Orlando guidance for theme parks, relocation, family planning, and daily city logistics."
metadata: {"clawdbot":{"emoji":"🎢","requires":{"bins":[],"config":["~/orlando/"]},"os":["linux","darwin","win32"],"configPaths":["~/orlando/"]}}
---

## When to Use

User asks about Orlando for any purpose: theme-park trip, conference, relocation, remote work, family move, school planning, or starting a business in Central Florida. Agent provides practical guidance with current data and metro-specific tradeoffs.

## Architecture

This skill works statelessly for one-off Orlando questions. If the user wants continuity, memory lives in `~/orlando/`. If `~/orlando/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/orlando/
|-- memory.md     # User context, trip style, park priorities, move plans, and open loops
```

## Quick Reference

Load the narrowest file that solves the user's immediate problem. Do not dump the full city when one decision is enough.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| **Visitors** | |
| Best attractions and what to skip | `visitor-attractions.md` |
| 1, 3, and 5 day planning | `visitor-itineraries.md` |
| Hotel zones and resort strategy | `visitor-lodging.md` |
| Practical trip tactics | `visitor-tips.md` |
| Best day trips beyond the parks | `day-trips.md` |
| **Theme Parks** | |
| Park portfolio and audience fit | `theme-parks-overview.md` |
| Disney strategy | `theme-parks-disney.md` |
| Universal strategy | `theme-parks-universal.md` |
| Tickets, Express, Lightning Lane, and logistics | `theme-parks-practical.md` |
| **Neighborhoods** | |
| Metro comparison | `neighborhoods-index.md` |
| Downtown, Thornton Park, Milk District, Ivanhoe | `neighborhoods-downtown.md` |
| Winter Park, Audubon Park, College Park | `neighborhoods-park-avenue.md` |
| Lake Nona, Conway, Baldwin Park, southeast side | `neighborhoods-lake-nona.md` |
| I-Drive, Dr. Phillips, Lake Buena Vista, Celebration | `neighborhoods-tourism.md` |
| Winter Garden, Windermere, Oviedo, Apopka, Clermont | `neighborhoods-suburban.md` |
| How to choose an area | `neighborhoods-choosing.md` |
| **Food** | |
| Dining scene overview | `food-overview.md` |
| Florida and Southern staples | `food-local.md` |
| Global dining and tasting menus | `food-international.md` |
| Best dining districts | `food-areas.md` |
| Reservations, tipping, dietary, kids | `food-practical.md` |
| **Practical** | |
| Moving and settling | `resident.md` |
| Transit, airport, Brightline, rideshare | `transport.md` |
| Cost of living and trip budgeting | `cost.md` |
| Safety, scams, and legal basics | `safety.md` |
| Heat, storms, and seasonality | `climate.md` |
| Utilities, SIMs, errands, and local services | `local.md` |
| **Career** | |
| Tech, simulation, defense, and remote work | `tech.md` |
| Florida business setup and local licenses | `business.md` |
| U.S. immigration context for Orlando moves | `immigration.md` |
| Startups, coworking, and founders | `startup.md` |
| **Lifestyle** | |
| Culture and social norms | `culture.md` |
| Healthcare and insurance navigation | `healthcare.md` |
| Schools, colleges, and family planning | `education.md` |
| Daily life, fitness, and social rhythm | `lifestyle.md` |
| Car ownership and toll-road reality | `driving.md` |

## Core Rules

### 1. Identify the Orlando Mode First
- Classify the user before advising: visitor, conference traveler, relocating resident, current resident, remote worker, student, or family.
- Orlando answers change fast depending on whether the question is about theme parks, airport access, school zones, or commuting across the metro.
- If the user has not named their base area, trip purpose, or timeline, ask for that before recommending hotels or neighborhoods.

### 2. Treat Orlando as a Multi-Core Metro
- Orlando is not just "the parks." The tourism corridor, Downtown, Winter Park, southeast Lake Nona, and western suburbs solve very different problems.
- Never compare areas only by distance on a map. I-4 traffic, toll roads, and convention or park demand often matter more than mileage.
- Use the neighborhood files before declaring a place "close" or "convenient."

### 3. Theme Parks Operate Like a Second City
- Walt Disney World, Universal Orlando Resort, and SeaWorld shape roads, hotel pricing, staffing, and even meal timing.
- Trip plans that ignore rope drop, mid-day heat, parking, and resort transport waste money and stamina.
- For park-first trips, load `theme-parks-overview.md` and `theme-parks-practical.md` before making itinerary promises.

### 4. Car-First City, With Exceptions
- Most of metro Orlando still works best with a car.
- The exceptions are narrow: Disney hotels with Disney transport, select Universal-area stays, Downtown with LYMMO and SunRail access, and conference trips centered on the convention district.
- If the user wants to avoid a car, verify where they will sleep, which parks or venues they need, and whether they can tolerate rideshare surge pricing.

### 5. Heat, Storms, and Rain Are Operational Constraints
- Summer is not just "warm." Heat index, humidity, and afternoon thunderstorms shape park strategy, outdoor activity, and even driving.
- Hurricane season affects fall travel, insurance, move timing, and power-outage readiness even though Orlando is inland.
- Load `climate.md` whenever the user is planning June through October.

### 6. Cost Reality Is Split in Two
- Orlando can look affordable compared with Miami, New York, or California, but wages are lower and tourism pricing distorts housing, dining, and short-term lodging.
- For residents, housing, car insurance, tolls, and childcare are the real budget drivers.
- For visitors, date-based park tickets, hotel fees, parking, and food inside the parks are the real budget traps.

### 7. Orlando Work Is More Diverse Than the Stereotype
- Hospitality is huge, but Orlando also has simulation and defense work, healthcare, logistics, higher education, sports business, and founder communities.
- Do not reduce Orlando careers to tourism jobs unless the user actually wants that lane.
- Use `tech.md`, `business.md`, and `startup.md` before answering salary or relocation questions with national averages.

### 8. Verify Unstable Rules From Official Sources
- Park perks, Lightning Lane or Express rules, parking prices, toll policy, school boundaries, and immigration requirements change.
- Use official Orlando, Florida, park, airport, and transit sources when the user needs exact current rules.
- If exact verification is blocked, say what is stable versus what must be checked live.

## Current Data (March 2026)

Use this table to calibrate expectations fast, then move into the matching auxiliary file before giving precise recommendations.

| Item | Range |
|------|-------|
| 1BR rent (tourism corridor) | USD 1,500-2,100/month |
| 1BR rent (Downtown or Winter Park) | USD 1,650-2,400/month |
| Median closed home price (metro) | Around USD 380,000-400,000 |
| LYNX local bus fare | USD 2 one way |
| SunRail base fare | USD 2 one way for one zone |
| Disney 1 day ticket | From about USD 119, date based |
| SeaWorld Orlando ticket | From about USD 79.99, date based |
| Orlando hotel ADR | About USD 195 nightly metro average |

## Neighborhood Matching

Start with this table, then verify commute corridor, school fit, and tolerance for toll roads before naming a winner.

| Profile | Best Areas |
|---------|------------|
| First-time park visitor | Lake Buena Vista, Disney Springs area, Universal area |
| Conference traveler | International Drive, Convention Center, nearby Dr. Phillips |
| Young urban professional | Thornton Park, South Eola, Ivanhoe Village, Mills 50 |
| Family with strong schools | Winter Park, Windermere, Winter Garden, Oviedo |
| Airport-heavy traveler | Lake Nona, Conway, southeast Orlando |
| Budget-conscious commuter | Apopka, Clermont, east Orlando, parts of Kissimmee |
| Remote worker wanting polish | Winter Park, Baldwin Park, Lake Nona |

## Orlando-Specific Traps

- Staying "close to Disney" and assuming Universal or Downtown will also be easy. They are not.
- Booking a cheap off-site hotel without checking parking fees, shuttle quality, resort fees, and drive times.
- Underestimating afternoon storms and trying to do full outdoor park days without a weather plan.
- Assuming International Drive is a local neighborhood. It is mostly a tourism corridor.
- Planning without tolls, especially for airport runs, western suburbs, and Disney-area driving.
- Treating Kissimmee, Celebration, Lake Buena Vista, and southwest Orange County as the same market.
- Forgetting that Epic Universe changed Universal-area traffic and hotel demand after opening on May 22, 2025.
- Calling Orlando "walkable" because one district or resort feels walkable. Most errands still need a car.
- Recommending public transit for families with strollers or late park exits without explaining the tradeoff.
- Using national salary benchmarks without adjusting for Orlando wages and Florida insurance costs.

## Legal Awareness

Key Florida and Orlando basics users should know:
- Recreational cannabis remains illegal in Florida.
- Open containers in vehicles are not allowed.
- School-zone and work-zone driving enforcement can be aggressive.
- Short-term rentals are heavily location-specific. HOA and city rules matter.
- Heat, lightning, and pool safety are real liability issues for families.
- Theme-park tickets, reservations, and add-ons are date-based and often nonrefundable or partially restricted.

See `safety.md` for scams, laws, and practical risk reduction.

## External Endpoints

Use these only when the user needs live verification for prices, transit, filing rules, or date-based park details.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.visitorlando.com | Page requests only unless user asks for booking-style help | Official destination updates, attractions, and seasonal events |
| https://www.orlando.gov | Page requests only unless the user asks for permit or address-specific guidance | City services, neighborhoods, utilities, and local rules |
| https://www.golynx.com | Route, stop, or fare context if the user asks for transit planning | Orlando bus network, LYMMO, and fare guidance |
| https://sunrail.com | Station, schedule, or fare context if the user asks for commuter rail help | SunRail service and pricing |
| https://disneyworld.disney.go.com | Date and park context only if the user asks for exact ticket or park-planning help | Official Disney rules, prices, and hours |
| https://www.universalorlando.com | Date and park context only if the user asks for exact ticket or Express guidance | Official Universal rules, prices, and hours |
| https://seaworld.com/orlando | Date context only if the user asks for exact ticket or event guidance | Official SeaWorld rules and ticketing |
| https://www.sunbiz.org | Filing type only if the user asks for exact Florida entity setup steps | Official Florida business registration and annual-report rules |
| https://www.ucf.edu | Program or tuition context if the user asks for education specifics | University of Central Florida references |

No other data is sent externally.

## Security & Privacy

**Data that may leave your machine:**
- Public page requests to official Orlando, Florida, park, transit, airport, and university websites
- Travel dates, route context, ZIP, district, or filing type only when the user asks for location-specific or date-specific guidance

**Data that stays local:**
- Trip goals, neighborhood shortlist, commute constraints, school needs, and open loops in `~/orlando/`

**This skill does NOT:**
- Buy tickets, submit forms, or create reservations without explicit instruction
- Store passport numbers, payment data, or health-insurance identifiers in local memory
- Pretend the tourism corridor and the residential city are the same thing

## Trust

By using this skill, limited travel, location, or filing context may be checked against official Orlando, Florida, park, transit, and university websites when the user asks for precise guidance.

Only install if you trust those public services with that lookup context.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` - General trip planning and itinerary design
- `florida` - Statewide weather, insurance, and moving context beyond Orlando
- `united-states` - National baseline for immigration, healthcare, and relocation questions
- `car-rental` - Airport pickup, toll roads, and rental-car decision support
- `money` - Budgeting support for trips, housing, and family cost planning

## Feedback

- If useful: `clawhub star orlando`
- Stay updated: `clawhub sync`
