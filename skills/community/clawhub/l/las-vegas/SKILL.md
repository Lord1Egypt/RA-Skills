---
name: Las Vegas
slug: las-vegas
version: 1.0.0
homepage: https://clawic.com/skills/las-vegas
description: Navigate Las Vegas as visitor, resident, remote worker, or entrepreneur with neighborhoods, entertainment, costs, and desert-living insights.
changelog: Launches a full Las Vegas city guide for visitors, residents, remote workers, and founders.
metadata: {"clawdbot":{"emoji":"🎰","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

User asks about Las Vegas for any purpose: visiting, moving, working remotely, starting a business, or relocating for tax benefits. Agent provides practical guidance with current data.

## Architecture

Memory lives in `~/las-vegas/`. If `~/las-vegas/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```
~/las-vegas/
├── memory.md     # User context, preferences, and ongoing notes
└── notes/        # Trip-specific or move-specific working notes
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| **Visitors** | |
| Attractions (must-see vs skip) | `visitor-attractions.md` |
| Itineraries (weekend/week) | `visitor-itineraries.md` |
| Where to stay | `visitor-lodging.md` |
| Tips & day trips | `visitor-tips.md` |
| Shows & entertainment | `visitor-shows.md` |
| **Neighborhoods** | |
| Quick comparison | `neighborhoods-index.md` |
| The Strip & Paradise | `neighborhoods-strip.md` |
| Downtown & Arts District | `neighborhoods-downtown.md` |
| Summerlin | `neighborhoods-summerlin.md` |
| Henderson | `neighborhoods-henderson.md` |
| Affordable areas | `neighborhoods-affordable.md` |
| Choosing guide | `neighborhoods-choosing.md` |
| **Food** | |
| Overview & dining scene | `food-overview.md` |
| Celebrity chef restaurants | `food-celebrity.md` |
| Local favorites & hidden gems | `food-local.md` |
| Best areas for dining | `food-areas.md` |
| Buffets, steak, dietary | `food-practical.md` |
| **Practical** | |
| Moving & settling | `resident.md` |
| Transport (car-centric reality) | `transport.md` |
| Cost of living | `cost.md` |
| Safety & laws | `safety.md` |
| Weather & desert survival | `climate.md` |
| Local services (utilities, DMV) | `local.md` |
| **Career** | |
| Tech industry & gaming | `tech.md` |
| Business setup & licensing | `business.md` |
| Remote work & tax benefits | `remote-work.md` |
| Startups & funding | `startup.md` |
| Hospitality careers | `hospitality.md` |
| **Lifestyle** | |
| Culture & local identity | `culture.md` |
| Healthcare & insurance | `healthcare.md` |
| Schools & education | `education.md` |
| Entertainment beyond casinos | `lifestyle.md` |
| Outdoor activities | `outdoors.md` |
| Driving & car ownership | `driving.md` |

## Core Rules

### 1. Identify User Context First
- **Role**: Tourist, resident, remote worker, tech professional, hospitality worker, retiree
- **Timeline**: Weekend trip, extended visit, considering relocation, already there
- Load relevant auxiliary file for details

### 2. Tax Haven Reality
Nevada has NO state income tax. This is a primary draw for:
- Remote workers from high-tax states (CA, NY, etc.)
- Entrepreneurs and business owners
- Retirees protecting retirement income
- High earners maximizing take-home pay

**What this means**:
- Significant savings vs California (~10-13% state tax)
- Nevada LLC formation popular for businesses
- You need real Nevada ties: primary home, driver's license, voter registration, vehicle registration, daily-life footprint
- There is no magic single-number shortcut for a former-state audit; verify high-stakes tax moves with a CPA
See `remote-work.md` and `resident.md` for residency strategy details.

### 3. Desert Climate Reality
- **Summer (May-Sep)**: 40-45°C (105-115°F). Brutal. Outdoor activities limited to early morning or evening.
- **Monsoon (Jul-Aug)**: Flash floods possible. Desert washes flood instantly.
- **Winter (Nov-Feb)**: 10-18°C (50-65°F). Best weather. Peak tourist season after holidays.
- **Spring/Fall**: Brief but pleasant. Ideal for outdoor activities.
See `climate.md` for survival strategies.

### 4. Current Planning Ranges (early 2026)

| Item | Range |
|------|-------|
| 1BR rent (Summerlin) | $1,500-1,900/month |
| 1BR rent (Henderson) | $1,350-1,800/month |
| 1BR rent (North LV) | $1,000-1,400/month |
| Median home price (metro) | ~$440,000-480,000 |
| Tech salary (senior) | $120,000-180,000 |
| Hospitality (dealer) | $60,000-100,000 (w/ tips) |
| Electricity (summer) | $200-400/month |
| Strip transit pass (RTC, 24h) | $8 |

### 5. Car-Centric Reality
Unlike walkable cities, Las Vegas REQUIRES a car:
- **Strip**: Walkable but brutal in summer heat
- **Everywhere else**: Driving distances, limited transit
- **RTC bus**: Exists but slow, limited coverage
- **Monorail**: Strip-only, not practical for residents
- **Uber/Lyft**: Expensive for daily use

**Budget for car**: Lease/payment + insurance (~$500-700/month total) + gas
See `transport.md` and `driving.md` for details.

### 6. The Strip vs Real Las Vegas
Most tourists only see The Strip. Actual Las Vegas is a sprawling suburban metro of 2.3M people.

| What tourists see | What residents experience |
|------------------|---------------------------|
| Casinos, shows, nightlife | Master-planned communities, malls |
| Expensive restaurants | Normal suburban chains + local gems |
| Walking the Strip | Driving everywhere |
| 24/7 action | Surprisingly quiet neighborhoods |
| Slot machines | Normal grocery stores without gaming |

### 7. Neighborhood Matching

| Profile | Best Areas |
|---------|------------|
| Families | Summerlin, Henderson, Green Valley |
| Young professionals | Southwest, Enterprise, Downtown |
| Remote workers | Summerlin, Henderson (quiet, good internet) |
| Budget-conscious | North Las Vegas, Sunrise Manor |
| Retirees | Sun City, Henderson, Boulder City |
| Tech workers | Summerlin, Southwest (near tech corridor) |
| Nightlife lovers | Downtown, Paradise (near Strip) |

### 8. Entertainment Capital
Las Vegas reinvents itself constantly:
- **Residencies**: Headliners rotate through venues like Sphere, Caesars, Park MGM, Resorts World, and Fontainebleau
- **Cirque du Soleil**: Multiple permanent shows
- **Sports**: Raiders (NFL), Golden Knights (NHL), Aces (WNBA), F1 Grand Prix
- **Conventions**: CES, SEMA, thousands annually at LVCC
- **Pool parties**: Seasonal dayclubs at major hotels
- **Free attractions**: Fountains, Fremont Experience, conservatories, and casino spectacle

See `visitor-shows.md` for venue logic, live-show categories, and booking strategies.

## Vegas Economy Reality

The economy has diversified beyond gaming:

| Sector | Share | Notes |
|--------|-------|-------|
| Tourism/Hospitality | 30%+ | Still dominant, includes conventions |
| Healthcare | Growing | Major hospital systems expanding |
| Tech | Emerging | Zappos HQ, gaming tech, data centers |
| Logistics | Growing | Amazon, Switch data centers |
| Construction | Cyclical | Always building something |
| Sports/Entertainment | New | Raiders stadium, F1, NHL |

**Gaming industry jobs**:
- Dealers: $60,000-100,000 with tips
- Hosts/VIP: $50,000-150,000+
- Management: Competitive corporate salaries
- Security, IT, marketing: Normal corporate roles

See `hospitality.md` for career paths.

## The Remote Work Migration

Post-2020, Las Vegas saw massive influx from California and other high-tax states:
- **Why**: No state income tax, lower cost of living, sunshine
- **Who**: Tech workers, entrepreneurs, content creators, retirees
- **Impact**: Housing prices up 50%+ since 2020, gentrification of some areas
- **Reality check**: Infrastructure hasn't kept pace, water concerns, crowding

## Las Vegas-Specific Traps

- **Summer heat underestimation** — 45°C (115°F) is dangerous. People die hiking. Hydrate or die, literally.
- **The "just 5 more minutes" Strip walk** — Distances deceive. Casinos are HUGE. What looks close is a 30-min walk.
- **Gambling budget creep** — Casinos are designed to make you lose track. Set hard limits.
- **Timeshare presentations** — "Free show tickets" usually means 4-hour high-pressure sales pitch.
- **Resort fees** — Not included in advertised rates. Add $40-60/night at Strip hotels.
- **Parking fees** — Most Strip resorts charge $15-25/day for parking.
- **Dehydration** — You sweat faster than you realize. Drink water constantly, even if not thirsty.
- **"Extended stay" vs residency** — Living in a hotel doesn't establish tax residency. Need actual address.
- **Buying first, researching later** — Housing market volatile. Research neighborhoods extensively first.
- **Ignoring HOA rules** — Summerlin, Henderson HOAs are strict. Read CC&Rs before buying.
- **Flash flood zones** — Some cheap houses are in flood zones. Check FEMA maps.
- **Assuming Vegas is just The Strip** — Miss the actual city, nature, community.

## Water & Sustainability

Las Vegas faces real water challenges:
- **Lake Mead**: Primary water source, historically low levels
- **Conservation**: Strict watering rules, grass removal incentives ($3/sq ft rebate)
- **Reality check**: Single-family pools still common, but new grass banned in many areas
- **Future**: Desalination, recycling, Colorado River negotiations ongoing

This affects:
- Landscaping choices (desert-friendly required in new builds)
- Pool ownership (still legal, but water bills matter)
- Long-term property values (water-secure areas premium)

## Legal Awareness

Key laws visitors/residents must know:
- **Gambling**: Legal at 21+. Casinos can ban you for any reason.
- **Marijuana**: Legal recreationally 21+. Cannot consume in public or casinos.
- **Open container**: Legal on The Strip and Fremont. NOT in vehicles.
- **Prostitution**: ILLEGAL in Clark County (Vegas). Legal in some rural counties.
- **Gun laws**: Permissive. Concealed carry with permit. Open carry legal.
- **Squatter rights**: Nevada has some of the toughest anti-squatter laws.
- **Driving**: 0.08 BAC limit. DUI heavily enforced, especially near Strip.

See `safety.md` for comprehensive legal guidance.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — Trip planning and logistics
- `dubai` — Another world-class destination guide
- `business` — Business strategy and planning
- `money` — Budgeting and personal finance for relocation decisions

## Feedback

- If useful: `clawhub star las-vegas`
- Stay updated: `clawhub sync`
