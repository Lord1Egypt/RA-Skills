---
name: trip-planning
description: >-
  Plan what to do on a trip — must-see sights, local gems, neighborhoods to
  explore, and half-day itineraries for visitors — via natural-language search.
  Use when the user is visiting a city or planning a trip ("what to do on my
  first visit to Paris", "things to see this weekend as a tourist", "plan my
  afternoon near the Eiffel Tower"). Powered by Outgoing, which works in cities
  worldwide.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🧳"
    homepage: https://www.outgoing.world/developers
    primaryEnv: OUTGOING_API_KEY
    requires:
      env:
        - OUTGOING_API_KEY
      anyBins:
        - curl
    envVars:
      - name: OUTGOING_API_KEY
        required: true
        description: >-
          Outgoing API key with the partner scope (og_api_…). Request one at https://outgoing.world.
---

# Trip planning — powered by Outgoing

Help a visitor make the most of a city.

## When to use

The user is a tourist or trip-planner: a first visit, a few days in town, or
building an itinerary. Triggers: "visiting", "in town for the weekend", "first
time in", "what should I see", "itinerary", "things to do near my hotel".

## How it works

Calls the **Outgoing API** (`GET /partner/v1/search`) — one
natural-language search returns up to 20 ranked, real venues/events. The same
API powers every Outgoing skill; full reference (auth, every parameter, booking,
schemas) as plain Markdown: <https://www.outgoing.world/llms.txt> and
<https://www.outgoing.world/llms-full.txt>.

### Setup

```bash
export OUTGOING_API_KEY="og_api_…"   # partner scope — get one at https://outgoing.world
```

Provision each end user once (`POST /partner/v1/users` with their
`external_user_id`), then pass that id as `X-External-User-Id` on every call. A
`404` means provision them first (details in llms.txt).

### Search

```bash
curl -sS -G https://api.outgoing.world/partner/v1/search \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  -H "X-External-User-Id: user-123" \
  --data-urlencode "prompt=must-see things to do for a first visit, plus a few local gems" \
  --data-urlencode "city=tokyo"
```

- `city` — the city to search, lowercase with underscores (e.g. `paris`,
  `new_york`, `tokyo`, `mexico_city`). Defaults to `new_york`. Outgoing is
  global — pass whatever city the user names.
- Returns `{ message, activities[] }`; each activity has `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Use `lat`/`lng` to anchor the search near the traveler's hotel or a landmark.

## Shape the prompt

Capture trip length, interests, and pace; mix iconic sights with local gems.
Anchor on where they're staying when known (pass `lat`/`lng`).

- "a half-day of must-see sights plus one neighborhood worth wandering"
- "local, non-touristy food and culture near my hotel in Shibuya"
- "what to do with one free evening — something memorable and walkable"

## Present & book

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price `label`
when `is_bookable`. Render `picture_url` where supported. Only report what the
API returns — never invent venues, prices, or availability. To buy tickets, use
the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific plans — see the **outgoing** skill for the full list.
