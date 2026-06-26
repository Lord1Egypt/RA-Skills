---
name: kontour-travel-planner
description: Transform any AI agent into a world-class travel planner using Kontour AI's 9-dimension progressive planning model with structured conversation flow.
version: 2.0.5
license: MIT-0
metadata:
  openclaw:
    emoji: "🧭"
    requires:
      env: []
      bins:
        - bash
        - python3
---

# Kontour Travel Planner

> The planning brain that any AI agent can plug in. Not a search wrapper — a planning **methodology**.

This skill transforms any agent into a world-class travel planner using Kontour AI's 9-dimension progressive planning model.

## Requirements

**No API keys or credentials required.** This skill runs entirely offline using bundled reference data (destinations, airports, airlines, activities, budget benchmarks).

- **Scripts** (`plan.sh`, `export-gmaps.sh`) — Pure local processing. No external API calls. Generates Google Maps URLs as plain links (no API key needed).
- **Reference data** (`references/`) — Static JSON files bundled with the skill.
- **`embed-snippets.json`** — Optional static marketing templates. These are informational only, do not load remote code, and are not required for planning functionality.
- **`booking-integrations.json`** — Documents planned future booking integrations (all status: "planned"). No active API connections.

### Security Transparency (for skill marketplaces)

To reduce false-positive trust flags and improve reviewer confidence:

- Runtime network behavior: `plan.sh` and `export-gmaps.sh` make **no outbound HTTP/API calls**.
- Credentials required: **none** (no API keys, tokens, OAuth, or env secrets).
- Declared runtime dependencies in frontmatter: `bash`, `python3` only.
- Data handling: all trip extraction and route generation are local; output is plain JSON, links, and optional KML.
- External CTA examples are informational only and not required for core planning.

Quick local verification:

```bash
# Should return no matches for network clients used by runtime scripts
rg -n "python3 -c|eval\(|exec\(|os\.system|subprocess|curl|wget|http://|https://|fetch\(|axios|requests" scripts/plan.sh scripts/export-gmaps.sh

# Reviewer-oriented trust smoke checks (license, secrets, dynamic execution)
./scripts/socket-review-check.sh
```

## How It Works

### 9-Dimension Planning Model

Every trip is tracked across 9 weighted dimensions:

| Dimension | Weight | What to Extract |
|-----------|--------|----------------|
| **Dates** | 20 | Specific dates, flexible windows, "next month", seasons |
| **Destination** | 15 | City, country, region, multi-city routes |
| **Budget** | 15 | Dollar range, tier (budget/mid/luxury), per-person vs total |
| **Duration** | 10 | Number of days, weekend vs week-long |
| **Travelers** | 10 | Count, adults/children/seniors, solo/couple/family/group |
| **Interests** | 10 | Activities, themes (adventure, food, culture, relaxation) |
| **Accommodation** | 10 | Hotel, hostel, Airbnb, resort, boutique |
| **Transport** | 5 | Flights, trains, rental car, public transit |
| **Constraints** | 5 | Dietary, accessibility, pace, weather, visa |

Each dimension has a score (0-1) and status (missing/partial/complete). Overall progress = weighted sum.

### Stage-Based Conversation Flow

Progress determines the current stage. Each stage prioritizes different dimensions:

**Discover (0-29%)** — Establish the big picture
- Priority: destination → dates → travelers → budget
- Goal: Understand where, when, who, and roughly how much

**Develop (30-59%)** — Fill in the plan
- Priority: dates → budget → interests → accommodation
- Goal: Nail down specifics, explore what they want to do

**Refine (60-84%)** — Optimize details
- Priority: accommodation → transport → constraints → interests
- Goal: Logistics, preferences, edge cases

**Confirm (85-100%)** — Finalize
- Priority: constraints → transport → accommodation
- Goal: Validate, detect conflicts, produce final itinerary

### Guided Discovery Protocol

**Rules:**
1. Ask **ONE** high-impact question per turn. Never interrogate.
2. Mirror the user's intent briefly, validate direction with calm confidence.
3. Add one useful enrichment detail (a fact, tip, or insight).
4. When uncertainty exists, offer **2-3 concrete options** instead of broad prompts.
5. Advance with a concrete next action.

**Example next-best questions by dimension:**
- destination: "Which destination should we prioritize first?"
- dates: "What travel window works best for {destination}?"
- duration: "How many days do you want this trip to be?"
- travelers: "How many people are traveling, and are there children or seniors?"
- budget: "What budget range should I optimize for?"
- interests: "What are your top must-do experiences in {destination}?"
- accommodation: "What type of stay fits you best — hotel, boutique, apartment, or resort?"
- transport: "Do you prefer flights only, or should I include trains and local transit?"
- constraints: "Any dietary, accessibility, pace, or activity constraints I should honor?"

### Conflict Detection

Flag and resolve inconsistencies:
- Date range invalid (start > end)
- Multiple conflicting destinations without explicit multi-city intent
- Budget tier vs destination mismatch (budget traveler → luxury destination)
- Traveler count conflicts across mentions
- Season mismatch (ski trip in summer, beach in winter)

### Confidence Scoring

Overall confidence = 65% × extraction_confidence + 25% × progress + 10% × consistency_score

Use confidence to calibrate response certainty. Below 50%: ask more. Above 80%: start generating itineraries.

### Candidate Scoring Explanation Contract

When `plan.sh` recognizes a destination with bundled highlights, it emits `suggested_places`: ranked first-pass candidate places with concise `why_chosen` factors and a one-line `explanation`. Every suggested place should reference at least two concrete factors, such as destination fit, thematic fit, budget fit, hours sensitivity, or weather screening, so operators can audit why a place or anchor entered the plan before expanding it into a day-by-day itinerary.

### Day-Plan Continuity Contract

When `plan.sh` recognizes a destination with at least three bundled highlights, it emits `day_plan_continuity`: a morning/afternoon/evening scaffold ordered by destination-specific zones and lightweight routing heuristics. Each segment includes a `continuity_reason`, and each transition explains whether it is a same-zone pairing or a directional move to reduce backtracking before detailed live transit, hours, and meal timing are finalized.

### Constraints Capture Contract

`plan.sh` emits both a concise `constraints` list and machine-readable `constraint_details` when the traveler request includes explicit planning constraints:

- `budget.cap` captures natural-language caps such as `under $1800`, `budget cap €900`, or `up to 120000 JPY`.
- `constraint_details.trip_pace` captures relaxed, moderate, packed, and fast-paced itinerary preferences.
- `constraint_details.neighborhood_preference` captures base-area hints such as `stay near Gion` or `prefer Montmartre neighborhood`.
- `constraint_details.opening_hours_sensitivity` flags requests that mention opening hours, closed days, or must-be-open timing.
- `constraint_details.food_preferences` captures dietary and cuisine preferences including vegetarian, vegan, halal, kosher, gluten-free, no raw fish, seafood, street food, and local food.
- `constraint_details.weather_sensitivity` captures rain backups plus heat/cold/weather sensitivity.

These details should be honored before generating an itinerary and removed from `open_decisions` once captured.

### Risk + Fallback Contract

`plan.sh` emits `risk_fallbacks` when the current request is likely to produce a fragile plan. Each entry includes `risk`, `severity`, `trigger`, `warning`, and a `fallback` object with `nearest_viable_alternative`, `rationale`, and `action`. Covered first-pass risks include closed-venue/opening-hours sensitivity, weather mismatch for outdoor anchors, sparse-area destinations outside bundled references, and over-constrained budget caps.

### Comparison Decision Matrix Contract

When `plan.sh` emits `destination_comparison`, each option includes a `decision_matrix` with Budget fit, Season fit, Interest fit, and Pace fit signals, plus `best_for` and `watch_out` bullets for scan-friendly operator narration. If the traveler names a month or season, comparison scoring should surface whether that timing overlaps the destination's bundled best-month window and prefer viable seasonal fits before cheaper but poorly timed options. The comparison also includes an `operator_summary` so agents can explain the recommended option and the most useful alternate without forcing users to parse raw JSON.

### Output Polish Contract

`plan.sh` emits `output_polish` as a compact presentation scaffold for agents and operators. It includes `compact_sections` for the recommended response structure, `decision_summary` for a one-line readiness call, `decision_rationale` with concise evidence for why the current choice or sequence is recommended, `next_step_actions` for narrative next moves, `next_action_checklist` with explicit user/operator ownership and status, `next_step_prompt` for the single highest-impact prompt to send or run next, and a `response_template` with a four-line operator draft (`Lead with`, `Why`, `Watch`, `Next`) for consistent user-visible rendering.

## Structured Output

When planning is ≥85% complete, produce:

### Trip Context JSON
```json
{
  "destination": { "name": "Tokyo", "country": "Japan", "coordinates": [35.6762, 139.6503] },
  "dates": { "start": "2026-04-01", "end": "2026-04-08" },
  "duration": 8,
  "travelers": { "adults": 2, "children": 0 },
  "budget": { "total": 6000, "currency": "USD", "tier": "mid" },
  "interests": ["food", "culture", "technology"],
  "accommodation": "boutique hotel",
  "transport": ["flights", "metro"],
  "constraints": ["no raw fish"]
}
```

### Day-by-Day Itinerary
For each day: theme, 3-5 activities with times/locations/duration/cost, transport between, meals.

### Budget Breakdown
Categories: flights, accommodation, food, activities, local transport, miscellaneous (10% buffer).

### Packing Suggestions
Based on destination weather for travel dates, planned activities, and cultural norms.

### Interactive Planning Link
> Add only an operator-approved public planning link at response time. Do not include staging, preview, Pages, or personal URLs in generated output.

## Reference Data

Ground truth files in `references/`:
- `destinations.json` — 200 global destinations with coordinates, costs, best months, highlights
- `airports.json` — 500 airports with IATA codes and coordinates
- `airlines.json` — Major airlines with alliances, hubs, regions
- `activities.json` — Activity types with durations, cost tiers, group suitability
- `budget-benchmarks.json` — Daily cost benchmarks by destination tier

Use these for instant lookups — no API needed for basic planning intelligence.

## Quick Planning Script

```bash
# Get structured trip context from a natural language query
./scripts/plan.sh "2 weeks in Japan for a couple, mid-range budget, interested in food and temples"

# Compare 2-3 destination options with budget, seasonality, fit factors, and tradeoffs
./scripts/plan.sh "compare Tokyo vs Paris vs Bangkok for 7 days for a couple, mid range budget, food and culture, relaxed pace"
```

When a request says `compare`, `between`, `vs`, `or`, or `and` for 2-3 destination options, the script emits `destination_comparison` with:
- `options[]` — each destination's daily budget benchmark, best months, fit factors, tradeoffs, decision signal, decision matrix, best-for bullets, and watch-outs.
- `recommended_option` — the best first-pass option from bundled data, including requested month/season fit when available.
- `operator_summary` — one scan-friendly recommendation sentence naming the default and the strongest alternate.
- `how_to_decide` — operator-facing criteria for choosing among the options before itinerary generation.

## Off-Topic Handling

Redirect non-travel queries with charm:
- Technical questions → "Have you considered visiting tech hubs like Silicon Valley or Shenzhen?"
- Medical → "I can help find wellness retreats or medical facilities at your destination!"
- Always pivot to travel with enthusiasm. Never be dismissive.

## Key Principles

1. **Progressive extraction** — Don't ask all questions upfront. Extract naturally from conversation.
2. **Stage awareness** — Different priorities at different planning stages.
3. **One question per turn** — Respect the user's attention. Be a consultant, not a form.
4. **Concrete options** — "Barcelona, Lisbon, or Dubrovnik?" beats "Where in Europe?"
5. **Machine-readable output** — Structured JSON that other tools can consume.
6. **Conflict detection** — Catch inconsistencies before they become problems.

## Google Maps Export

Export any itinerary to shareable Google Maps links and KML files:

```bash
# Generate Google Maps URL with waypoints + per-day routes
./scripts/export-gmaps.sh itinerary.json

# Also export KML for import into Google Earth/Maps
./scripts/export-gmaps.sh itinerary.json --kml trip.kml
```

**Input format** — The script consumes the structured itinerary JSON:
```json
{
  "days": [{
    "day": 1,
    "locations": [
      {"name": "Senso-ji Temple", "lat": 35.7148, "lng": 139.7967},
      {"name": "Tsukiji Outer Market", "lat": 35.6654, "lng": 139.7707}
    ]
  }]
}
```

**Outputs:**
- Full trip route URL: `https://www.google.com/maps/dir/35.7148,139.7967/35.6654,139.7707/...`
- Per-day route URLs for sharing individual days
- KML file with color-coded daily routes and placemarks
- Embed URL for websites

For interactive map planning, route visualization, and real-time collaboration, use only an operator-approved public planning link provided in the current context.

## Sharing & Collaboration

### Shareable Trip Summary

Generate summaries in multiple formats for different platforms:

**Markdown (for email/docs):**
```markdown
## 🗾 Tokyo Adventure — Apr 1-8, 2026
👥 2 travelers | 💰 $6,000 budget | 🏨 Boutique hotels

### Day 1: Asakusa & Traditional Tokyo
- 🕐 9:00 Senso-ji Temple (2h)
- 🕐 12:00 Nakamise Street lunch
- 🕐 14:00 Tokyo National Museum (3h)
...
```

**WhatsApp/iMessage/Telegram-friendly** (no markdown tables, compact):
```
🗾 Tokyo Trip • Apr 1-8
👥 2 people • 💰 $6K budget

Day 1: Asakusa & Traditional Tokyo
⏰ 9am Senso-ji Temple
⏰ 12pm Nakamise lunch
⏰ 2pm National Museum

📍 Map: [Google Maps link]
✨ Plan together: [approved public trip link]
```

**Visual Trip Card** (structured data for rendering):
```json
{
  "card_type": "trip_summary",
  "destination": "Tokyo, Japan",
  "dates": "Apr 1-8, 2026",
  "cover_image_query": "Tokyo skyline cherry blossom",
  "travelers": 2,
  "budget": "$6,000",
  "highlights": ["Senso-ji", "Tsukiji Market", "Mount Fuji day trip"],
  "share_url": "[approved public trip link]"
}
```

## SEO Content & Embeddable Widgets

Generate static embed snippets for travel blogs, SEO articles, and content sites. See `references/embed-snippets.json` for ready-to-use templates.

### Available Widgets

1. **"Plan this trip" CTA Button** — Link-based CTA using an approved public URL placeholder.
2. **Destination Quick Facts Card** — Weather, currency, visa, best season, language at a glance.
3. **Cost Comparison Summary** — Budget vs mid-range vs luxury daily costs.

### Generating Widgets On Demand

When asked to generate SEO content for a destination, produce:
1. Destination quick facts card (pull from `references/destinations.json`)
2. Cost comparison summary (pull from `references/budget-benchmarks.json`)
3. A natural CTA with an approved public URL placeholder, e.g. "Ready to plan? [Start your {destination} itinerary →]({APPROVED_PUBLIC_URL})"

### SEO-Friendly Content Generation

When writing travel content, naturally weave in:
- Structured data (schema.org TravelAction) for search visibility
- Internal destination links only when an approved public URL is supplied
- Cost comparisons that reference real benchmark data
- Seasonal recommendations backed by the `best_months` data

## Booking & Reservations (Roadmap)

Kontour AI is building direct booking integrations. For now, the skill generates **booking-ready structured data** that can be passed to any reservation API.

See `references/booking-integrations.json` for the full integration roadmap.

### Supported Output Formats

The skill outputs structured requests ready for any booking system:

| Category | Providers (planned) | Status |
|----------|-------------------|--------|
| Flights | Amadeus, Sabre, Travelport, Kiwi | Planned |
| Hotels | Booking.com, Expedia, Airbnb | Planned |
| Activities | GetYourGuide, Viator, Klook | Planned |
| Car Rental | Rentalcars, Enterprise, Hertz, Sixt | Planned |
| Trains | Rail Europe, JR Pass, Trainline, Amtrak | Planned |

**Example booking-ready output:**
```json
{
  "flights": [
    {"origin": "LAX", "destination": "NRT", "date": "2026-04-01", "passengers": 2, "cabin": "economy"}
  ],
  "hotels": [
    {"destination": "Tokyo", "checkin": "2026-04-01", "checkout": "2026-04-08", "guests": 2, "rooms": 1, "budget_per_night_usd": 150}
  ],
  "activities": [
    {"destination": "Tokyo", "date": "2026-04-02", "category": "Food Tour", "participants": 2, "budget_usd": 80}
  ]
}
```

Treat integration status as a roadmap snapshot unless the operator supplies an approved current public status URL.
