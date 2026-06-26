---
name: enjoy-nature
description: >-
  Find outdoor and nature outings — parks, gardens, scenic walks, easy hikes,
  waterfronts, and green escapes — via natural-language search. Use when the
  user wants fresh air or the outdoors ("nature spots near me", "scenic walk
  this weekend", "easy hikes", "a park or garden to relax in"). Powered by
  Outgoing, which works in cities worldwide.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🌳"
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

# Enjoy nature — powered by Outgoing

Find parks, gardens, trails, and scenic outdoor escapes.

## When to use

The user wants the outdoors and fresh air. Triggers: "nature", "outdoors",
"park", "garden", "hike", "scenic walk", "waterfront", "somewhere green to
unwind".

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
  --data-urlencode "prompt=scenic outdoor walks and gardens to relax this weekend" \
  --data-urlencode "city=barcelona"
```

- `city` — the city to search, lowercase with underscores (e.g. `paris`,
  `new_york`, `tokyo`, `mexico_city`). Defaults to `new_york`. Outgoing is
  global — pass whatever city the user names.
- Returns `{ message, activities[] }`; each activity has `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search near the user or a trailhead.

## Shape the prompt

Lead with the outdoor frame and capture effort level (gentle stroll vs. real
hike), scenery, and how far they'll travel. Note the weather/season when known.

- "easy, flat scenic walks good for a relaxed afternoon"
- "a real half-day hike with views, not too crowded"
- "botanical gardens and green spaces to unwind with a book"

## Present & book

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price `label`
when `is_bookable`. Render `picture_url` where supported. Only report what the
API returns — never invent venues, prices, or availability. To buy tickets, use
the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific plans — see the **outgoing** skill for the full list.
