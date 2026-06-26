---
name: stay-active
description: >-
  Find active and sporty things to do — fitness classes, climbing, cycling,
  watersports, drop-in sports, and active outdoor outings — via natural-language
  search. Use when the user wants to move and stay active ("active things to do
  this weekend", "drop-in fitness class", "climbing or cycling", "something
  sporty"). Powered by Outgoing, which works in cities worldwide.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🏃"
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

# Stay active — powered by Outgoing

Find sporty, energetic things to do.

## When to use

The user wants physical activity. Triggers: "active", "sporty", "fitness
class", "climbing", "cycling", "yoga", "watersports", "drop-in sports",
"something to get moving".

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
  --data-urlencode "prompt=active things to do this weekend — climbing, cycling, or a drop-in class" \
  --data-urlencode "city=sydney"
```

- `city` — the city to search, lowercase with underscores (e.g. `paris`,
  `new_york`, `tokyo`, `mexico_city`). Defaults to `new_york`. Outgoing is
  global — pass whatever city the user names.
- Returns `{ message, activities[] }`; each activity has `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search on a neighborhood.

## Shape the prompt

Lead with the active frame and capture the sport/activity type, intensity, skill
level, and whether they want drop-in (no commitment) vs. a course.

- "drop-in fitness or HIIT class I can join this evening, no membership"
- "beginner-friendly bouldering or rock climbing"
- "kayaking, paddleboarding, or cycling routes for the weekend"

## Present & book

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price `label`
when `is_bookable`. Render `picture_url` where supported. Only report what the
API returns — never invent venues, prices, or availability. To buy tickets, use
the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific plans — see the **outgoing** skill for the full list.
