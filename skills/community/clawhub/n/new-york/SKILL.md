---
name: New York (State)
slug: new-york
version: 1.0.1
homepage: https://clawic.com/skills/new-york
description: Navigate New York State for living, moving, working, and visiting with region fit, taxes, winter risk, and daily logistics.
changelog: "Expanded the skill into statewide New York guidance with regional tradeoffs, resident workflows, and practical travel planning."
metadata: {"clawdbot":{"emoji":"🍎","requires":{"bins":[],"config":["~/new-york/"]},"os":["linux","darwin","win32"],"configPaths":["~/new-york/"]}}
---

## When to Use

User needs New York State guidance that generic U.S. advice usually gets wrong: choosing a region, moving, licensing, taxes, housing, weather readiness, healthcare, school planning, business setup, or statewide trip design.

This skill should activate for four modes: visiting New York State, moving to New York, living in New York, and operating a New York-based business.

## Architecture

This skill works statelessly for one-off New York questions. If the user wants continuity across sessions, memory lives in `~/new-york/`. If `~/new-york/` does not exist, read `setup.md`, explain planned local storage in plain language, and ask for confirmation before creating files. See `memory-template.md` for structure.

```text
~/new-york/
└── memory.md     # User context, region, timelines, constraints, and open loops
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Regions, metros, and corridor tradeoffs | `regions.md` |
| Move-in sequence and relocation checklist | `moving-and-settling.md` |
| Driver license, registration, inspections, and vehicles | `new-york-dmv-and-vehicles.md` |
| Renting, buying, insurance pressure, and property fit | `housing-and-insurance.md` |
| Electricity, heating, internet, and recurring bills | `utilities-and-bills.md` |
| Taxes, tolls, salaries, and cost reality | `costs-and-taxes.md` |
| Winter storms, floods, heat, and emergency readiness | `weather-and-preparedness.md` |
| Laws, scams, and practical safety | `laws-and-safety.md` |
| Schools, childcare, and family-location logic | `family-and-schools.md` |
| Health insurance, care access, and coverage choices | `healthcare-and-coverage.md` |
| Work, startups, permits, and business tradeoffs | `work-and-business.md` |
| Transit, driving, and commute design | `transit-and-commutes.md` |
| Road trips, parks, and visiting strategy | `road-trips-and-visiting.md` |
| Official sources map | `sources.md` |

## Core Rules

### 1. Classify the User Before Giving Advice
- Decide which New York mode applies first: visitor, future resident, current resident, or business operator.
- Then anchor the answer to the user's region, metro, county, ZIP, and school district when those variables change the recommendation.
- If that context is missing, ask for it before pretending New York is one market.

### 2. Separate State Rules from Local New York Reality
- Statewide rules are only the first layer. NYC, Long Island, Hudson Valley, Capital Region, Western New York, Central New York, the Finger Lakes, and the North Country do not solve the same problem.
- Always label which parts are statewide and which parts must be verified by county, school district, utility, transit agency, or municipality.
- For address-specific questions, prefer official portals over generic summaries.

### 3. Region Choice Changes the Real Answer
- A good New York answer usually depends on commute shape, winter exposure, housing stock, school district, car dependence, and tax pressure together.
- Never compare NYC, Buffalo, Saratoga, Rochester, Syracuse, and the Adirondacks as if only rent changes.
- Use `regions.md` before recommending a "best place" in New York.

### 4. Total Cost Beats Headline Rent or Salary
- Include state income tax, local property tax, tolls, heating cost, parking, insurance, and commute cost.
- For homeowners and renters, mention flood exposure, snow removal reality, and older-building maintenance risk when relevant.
- Use `costs-and-taxes.md` before saying a region is "cheap" or "worth it."

### 5. Winter and Infrastructure Risk Change Good Advice
- Snow, ice, lake effect storms, flooding, summer humidity, and outage risk are not side notes.
- Adjust moving plans, road trips, home choice, and school or work routines around actual weather and utility exposure.
- When weather matters, lead with readiness and fallback plans, not scenery.

### 6. Deliver Sequence, Not Brochure Copy
- New York users often need deadlines, documents, portals, and tradeoffs.
- For administrative topics, answer in the form "do this today / this week / later" whenever possible.
- For relocation and regional questions, show why one corridor or metro fits better than another.
- Before creating or changing local files in `~/new-york/`, explain the planned write and ask for confirmation.

### 7. Use Official Sources for Unstable Rules
- DMV steps, tax credits, school boundaries, health-plan options, and utility rules can change.
- Verify current information from the official state or local source before giving precise compliance steps.
- If current verification is blocked, say so plainly and avoid false precision.

## Common Traps

- Treating New York like NYC plus "upstate" instead of multiple different housing, weather, and tax environments.
- Recommending a suburb or city without checking commute corridor, school district, winter driving, and property-tax reality.
- Comparing salaries without subtracting state tax, heating cost, tolls, parking, and insurance pressure.
- Ignoring floodplain, shoreline, or snow-belt exposure until after housing is narrowed.
- Mixing up DMV, Department of Taxation and Finance, NY State of Health, DFS, local assessors, school districts, and county clerks.
- Planning statewide travel by map distance instead of snow timing, thruway tolls, holiday traffic, and seasonal park access.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.ny.gov | Page requests only unless user explicitly wants form guidance | State services and resident tasks |
| https://dmv.ny.gov | Page requests only unless user explicitly provides case details | Driver license, REAL ID, registration, title, and inspection workflows |
| https://www.tax.ny.gov | Page requests only unless user explicitly wants tax-specific guidance | State income tax, sales tax, property-tax benefits, and filing references |
| https://nystateofhealth.ny.gov | County or ZIP if the user asks for marketplace coverage help | Health insurance marketplace and plan lookup |
| https://www.dfs.ny.gov | ZIP, county, or region references if the user asks about insurance or financial protection | Insurance, consumer protections, and complaint pathways |
| https://www.nysed.gov | ZIP, city, district, or school references if the user asks for school matching | Education and school district framework |
| https://www.businessexpress.ny.gov | Page requests only unless user explicitly wants permit or filing help | Business licensing, permits, and startup workflows |
| https://www.dhses.ny.gov | County or region references if the user asks for emergency guidance | Preparedness and hazard planning |

No other data is sent externally.

## Security & Privacy

**Data that may leave your machine:**
- Public page requests to official New York state or local-government websites
- ZIP, county, district, or region data only when the user asks for location-specific guidance

**Data that stays local:**
- Region preference, move timeline, family constraints, vehicle notes, and open tasks in `~/new-york/`

**This skill does NOT:**
- Submit government forms on the user's behalf without explicit instruction
- Store credentials, SSNs, or payment information in local memory
- Assume local rules when the answer depends on a city, county, district, or utility territory

## Trust

By using this skill, location details such as ZIP, county, or district may be checked against official New York or local-government websites when the user asks for precise guidance.

Only install if you trust those public services with that lookup context.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General itinerary design and travel planning structure
- `booking` — Reservation workflows for flights, hotels, and schedule holds
- `business` — Broader business operations guidance beyond New York-specific rules
- `health-insurance` — More detailed plan comparison and terminology support
- `home-buying` — Deeper purchase workflow support after region and housing fit are narrowed

## Feedback

- If useful: `clawhub star new-york`
- Stay updated: `clawhub sync`
