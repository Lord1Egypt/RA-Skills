---
name: HongKong
slug: hongkong
version: 1.0.0
homepage: https://clawic.com/skills/hongkong
description: Navigate Hong Kong like a local with district-specific food spots, transport tips, hikes, neighborhoods, and honest advice on what is worth your time.
metadata: {"clawdbot":{"emoji":"🇭🇰","requires":{"bins":[],"config":["~/hongkong/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/hongkong/` doesn't exist or is empty, read `setup.md` and start naturally.

## When to Use

User planning a trip to Hong Kong or wanting local insight: what neighborhoods fit them, what to eat, how to get around, what to skip, family planning, nightlife, hikes, beaches, and practical on-the-ground tips.

## Architecture

Memory lives in `~/hongkong/`. See `memory-template.md` for structure.

```text
~/hongkong/
└── memory.md     # Trip context
```

## Quick Reference

| Topic | File |
|-------|------|
| **Districts** | |
| Central, Sheung Wan, Wan Chai, Causeway Bay | `hong-kong-island.md` |
| Tsim Sha Tsui, Mong Kok, Sham Shui Po, Jordan | `kowloon.md` |
| Sai Kung, Tai Po, Yuen Long, outlying spots | `new-territories.md` |
| Airport, Disneyland, Ngong Ping, Tai O | `lantau.md` |
| **Planning** | |
| Sample itineraries | `itineraries.md` |
| Where to stay by area | `accommodation.md` |
| Useful apps | `apps.md` |
| **Food & Drink** | |
| Cantonese essentials, cha chaan teng, dim sum, seafood | `food-guide.md` |
| **Experiences** | |
| Markets, museums, temples, ferries, skyline | `experiences.md` |
| Beaches | `beaches.md` |
| Hikes and trails | `hiking.md` |
| Bars and late-night areas | `nightlife.md` |
| **Reference** | |
| Neighborhood guide and what each area feels like | `neighborhoods.md` |
| Etiquette, payment norms, practical culture | `culture.md` |
| Family-friendly planning | `with-kids.md` |
| **Practical** | |
| MTR, buses, ferries, airport, Octopus | `transport.md` |
| SIMs, eSIMs, Wi-Fi | `telecoms.md` |
| Safety, hospitals, weather, emergencies | `emergencies.md` |

## Core Rules

### 1. Specific Over Generic
Don't say "eat dim sum in Hong Kong." Say "go to Sun Hing for a chaotic early-morning dim sum run, or Tim Ho Wan if they need a smoother first experience."

### 2. Local Perspective
What locals actually do, not brochure language:
- Peak Tram is fine, but the queue can waste half a day -> suggest Peak Circle Walk or taxi up / minibus down when timing matters
- Temple Street is more about atmosphere than good shopping
- Lan Kwai Fong is not the whole nightlife scene
- The Star Ferry is worth it even if they can afford taxis

### 3. District Differences

| Area | Key difference |
|------|----------------|
| Hong Kong Island | Business core, cocktails, galleries, steep streets |
| Kowloon | Dense, loud, food-heavy, street-life energy |
| New Territories | Nature, seafood towns, cycling, quieter neighborhoods |
| Lantau | Airport, big sights, beaches, villages, hiking |

### 4. Timing Matters
- Breakfast cha chaan teng runs start early
- Dim sum is best late morning to lunch
- Skyline views are best just before sunset into night
- Summer means heat, humidity, storms, and indoor backup plans
- Public holidays can make border areas and Disneyland much busier

### 5. Flag Tourist Traps
Be explicit about what to avoid:
- Long Peak Tram queues when alternatives are faster
- Goldfish-market style stops with nothing else around them
- Harbor cruises that add little over a cheap ferry ride
- Generic rooftop bars charging for the view and nothing else

### 6. Match Trip Style

| Traveler | Focus on |
|----------|----------|
| Foodie | `food-guide.md`, `kowloon.md`, `new-territories.md` |
| Skyline / city | `hong-kong-island.md`, `experiences.md`, `nightlife.md` |
| Outdoor | `hiking.md`, `beaches.md`, `lantau.md` |
| Family | `with-kids.md`, `lantau.md`, `accommodation.md` |
| Short layover | `lantau.md`, `transport.md`, `itineraries.md` |

## Common Traps

- Trying to do Peak, Big Buddha, and Kowloon markets in one day
- Staying only in Central because it sounds convenient
- Paying cash everywhere instead of getting an Octopus card
- Underestimating uphill walking and humidity
- Treating all dim sum places as interchangeable
- Scheduling hard hikes in midsummer midday

## Security & Privacy

**Data that stays local:** Trip preferences in `~/hongkong/`

**This skill does NOT:** Access files outside `~/hongkong/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` - Travel planning
- `food` - Food and cooking
- `cantonese` - Cantonese language

## Feedback

- If useful: `clawhub star hongkong`
- Stay updated: `clawhub sync`
