---
name: Ibiza
slug: ibiza
version: 1.0.0
changelog: "Initial release with complete Ibiza guidance for visitors, residents, remote workers, seasonal workers, and entrepreneurs."
homepage: https://clawic.com/skills/ibiza
description: Navigate Ibiza as visitor, resident, remote worker, or founder with neighborhoods, transport, costs, visas, and local operational guidance.
metadata: {"clawdbot":{"emoji":"🏝️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

User asks about Ibiza for holidays, relocation, seasonal work, remote work, or business setup. Agent gives practical, current guidance with zone-level detail and legal context.

## Quick Reference

| Topic | File |
|-------|------|
| **Visitors** | |
| Beaches and coves strategy | `visitor-beaches.md` |
| Nightlife planning and club logistics | `visitor-nightlife.md` |
| Itineraries (3, 5, 7 days) | `visitor-itineraries.md` |
| Where to stay by profile | `visitor-lodging.md` |
| Day activities and alternatives | `visitor-activities.md` |
| **Zones** | |
| Island quick comparison | `zones-index.md` |
| Ibiza Town and Marina zones | `zones-ibiza-town.md` |
| Sant Antoni and west coast | `zones-san-antonio.md` |
| Santa Eularia and east coast | `zones-santa-eulalia.md` |
| North and quieter areas | `zones-north.md` |
| Zone selection framework | `zones-choosing.md` |
| **Food and Going Out** | |
| Dining scene overview | `food-overview.md` |
| Local Ibizan food | `food-local.md` |
| Fine dining and premium tables | `food-fine-dining.md` |
| Beach clubs and day parties | `food-beach-clubs.md` |
| Budget food strategy | `food-budget.md` |
| **Practical** | |
| Arrival by air and sea | `transport-arrival.md` |
| Local mobility and day movement | `transport-local.md` |
| Cost of living and trip budgets | `cost.md` |
| Housing and rental risks | `housing.md` |
| Safety and legal basics | `safety.md` |
| Seasons and weather decisions | `seasons.md` |
| Local admin and services | `local.md` |
| **Residency and Work** | |
| Short and long stay visa logic | `visas.md` |
| Remote work and nomad setup | `nomad.md` |
| Seasonal jobs and contracts | `seasonal-work.md` |
| **Lifestyle** | |
| Culture, etiquette, and local rhythm | `culture.md` |
| Healthcare and coverage | `healthcare.md` |
| Wellness and recovery lifestyle | `wellness.md` |
| **Research** | |
| Source map and official links | `sources.md` |

## Core Rules

### 1. Identify User Profile First
- Role: tourist, relocating resident, remote worker, seasonal worker, founder.
- Time horizon: weekend, one summer, multi-month, year-round plan.
- Budget and transport tolerance determine 80% of good decisions.

### 2. Ibiza Is Multi-Zone, Not One Destination
Ibiza Town, Sant Antoni, Santa Eularia, and the North have different price levels, sleep quality, mobility stress, and social rhythm. Never give lodging advice without zone matching.

### 3. Seasonality Controls Everything
- High season drives peak prices, club demand, and road pressure.
- Shoulder season is often best value-quality trade-off.
- Winter has lower intensity and different business hours.
Use `seasons.md` before making schedule promises.

### 4. Current Data Snapshot (March 2026)

| Item | Current Reference |
|------|-------------------|
| Ibiza Airport passengers in 2025 | 9,138,224 (AENA) |
| Ibiza Airport flights in 2025 | 85,086 (AENA) |
| Eivissa rent level | 29.0 EUR/m2 (Feb 2026, idealista) |
| Eivissa rent level prior month | 26.9 EUR/m2 (Jan 2026, idealista) |
| Numbeo 1BR city-center benchmark | ~2,000 EUR/month |
| Numbeo meal benchmark | ~17.5 EUR inexpensive restaurant |

### 5. Mobility Is the Main Operational Bottleneck
Road congestion can break naive itineraries. Formentera access and beach-club timing need preplanning. Use clustered daily plans, not island-wide zigzags.

### 6. Entry and Visa Context Must Be Explicit
- Schengen short stays follow 90/180 logic for visa-exempt nationals.
- ETIAS is not active yet; EU states start in late 2026 according to official EU notice.
- Longer stays need national visa or residence route.
Use `visas.md` with exact assumptions.

### 7. Tax and Fee Awareness
Balearic Sustainable Tourism Tax (ITS) applies to overnight tourist stays with category-based rates and legal reductions by season and stay length. Mention this upfront in budget answers.

### 8. Safety Priority: Transport + Party Context
Most avoidable incidents involve transport behavior, intoxication risk, and unmanaged party logistics. Include harm-reduction recommendations by default.

### 9. Source-Critical Guidance
Rules and prices change. For legal, visa, and tax advice, cite official sources and date-stamp guidance before the user spends money.

## Ibiza-Specific Traps

- Booking far from planned nightlife and underestimating 02:00-06:00 transport friction.
- Assuming every beach and club is easy walk-in during peak season.
- Ignoring legal tourist tax and extra accommodation charges.
- Treating Ibiza as cheap because flights were cheap.
- Planning cross-island schedules with zero traffic buffers.
- Renting vehicles or housing without compliance and deposit clarity.
- Using unlicensed transfers or party offers.
- Assuming all businesses run full schedule in off-season.
- Mixing seasonal-job assumptions with wrong visa status.
- Underinsuring for emergency medical scenarios.

## Legal Awareness

- Spain and Balearic local regulations apply; municipality rules can differ.
- Entry conditions for non-EU nationals depend on nationality, visa status, and 90/180 limits.
- Traffic controls and vehicle-cap measures are active in peak season.
- Drug offenses and public-order breaches carry severe legal consequences.
- Use only licensed transport and legal accommodation channels.

See `visas.md`, `safety.md`, and `transport-local.md` for operational detail.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` - trip planning and logistics optimization
- `expat` - relocation and adaptation workflows
- `food` - dining research and personalization
- `startup` - founder operations and execution systems

## Feedback

- If useful: `clawhub star ibiza`
- Stay updated: `clawhub sync`
