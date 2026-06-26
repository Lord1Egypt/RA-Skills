---
name: accessible-outings
description: >-
  Find step-free, wheelchair-accessible things to do — accessible restaurants,
  museums, venues, and outings — via natural-language search. Use when the user
  needs accessibility ("wheelchair-accessible restaurants", "step-free things to
  do", "accessible museums", "outings for a wheelchair user"). Powered by
  Outgoing, which works in cities worldwide.
version: 1.0.0
metadata:
  openclaw:
    emoji: "♿"
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

# Accessible outings — powered by Outgoing

Find step-free, wheelchair-accessible places to go.

## When to use

The user needs accessible venues. Triggers: "wheelchair accessible", "step-
free", "accessible", "no stairs", "mobility-friendly", "outing for someone with
limited mobility".

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
  --data-urlencode "prompt=wheelchair-accessible, step-free restaurants and museums this weekend" \
  --data-urlencode "city=paris"
```

- `city` — the city to search, lowercase with underscores (e.g. `paris`,
  `new_york`, `tokyo`, `mexico_city`). Defaults to `new_york`. Outgoing is
  global — pass whatever city the user names.
- Returns `{ message, activities[] }`; each activity has `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search on a neighborhood.

## Shape the prompt

Always state the accessibility requirement explicitly in the `prompt`, and add
specifics when known (step-free entrance, accessible restroom, elevator). Be
honest that the user should confirm details with the venue.

- "wheelchair-accessible restaurants with step-free entry and accessible restrooms"
- "museums and galleries with elevators and ramps, no stairs to enter"
- "accessible outdoor spots with paved, level paths"

## Present & book

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price `label`
when `is_bookable`. Render `picture_url` where supported. Only report what the
API returns — never invent venues, prices, or accessibility details; suggest the
user confirm specific access needs with the venue. To buy tickets, use the
**book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific plans — see the **outgoing** skill for the full list.
