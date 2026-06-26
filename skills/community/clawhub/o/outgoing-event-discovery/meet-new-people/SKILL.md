---
name: meet-new-people
description: >-
  Find social events to meet new people — mixers, meetups, classes, workshops,
  community events, and solo-friendly outings — via natural-language search. Use
  when the user is new in town or wants to expand their circle ("ways to meet
  people", "social events this week", "beginner classes to meet others", "I'm
  new here, what should I do"). Powered by Outgoing, which works in cities
  worldwide.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🫂"
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

# Meet new people — powered by Outgoing

Find social, welcoming events where it's easy to meet others.

## When to use

The user wants to meet people or is new in town. Triggers: "meet new people",
"make friends", "social events", "mixers", "meetups", "classes/workshops to
meet others", "new in the city", "solo but social".

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
  --data-urlencode "prompt=social events and beginner classes to meet new people this week" \
  --data-urlencode "city=berlin"
```

- `city` — the city to search, lowercase with underscores (e.g. `paris`,
  `new_york`, `tokyo`, `mexico_city`). Defaults to `new_york`. Outgoing is
  global — pass whatever city the user names.
- Returns `{ message, activities[] }`; each activity has `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search on a neighborhood.

## Shape the prompt

Lead with the social-connection frame and favor group, interactive formats
(classes, workshops, mixers, clubs) over passive ones. Note any interests to
match like-minded people.

- "welcoming social events this week where it's easy to talk to strangers"
- "beginner-friendly group classes or workshops to meet people"
- "community meetups around hiking, board games, or language exchange"

## Present & book

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price `label`
when `is_bookable`. Render `picture_url` where supported. Only report what the
API returns — never invent venues, prices, or availability. To buy tickets, use
the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific plans — see the **outgoing** skill for the full list.
