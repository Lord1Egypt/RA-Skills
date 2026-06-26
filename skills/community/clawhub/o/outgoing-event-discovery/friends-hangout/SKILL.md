---
name: friends-hangout
description: >-
  Find casual group outings — fun bars, breweries, games and activities, lively
  happy hours, and group-friendly spots — via natural-language search. Use when
  the user is going out with friends ("fun bars for a group Saturday night",
  "where to hang with friends", "something fun for 6 of us", "good happy hour").
  Powered by Outgoing, which works in cities worldwide.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🍻"
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

# Friends hangout — powered by Outgoing

Find fun, casual spots for a group of friends.

## When to use

The user is going out with friends. Triggers: "with friends", "group hangout",
"fun bars", "happy hour", "something for a group of 6", "lively night out",
"games and drinks".

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
  --data-urlencode "prompt=fun, lively bars for a group of six on Saturday night" \
  --data-urlencode "city=chicago"
```

- `city` — the city to search, lowercase with underscores (e.g. `paris`,
  `new_york`, `tokyo`, `mexico_city`). Defaults to `new_york`. Outgoing is
  global — pass whatever city the user names.
- Returns `{ message, activities[] }`; each activity has `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search on a neighborhood.

## Shape the prompt

Lead with the group frame and capture size, vibe (chill vs. rowdy), and whether
they want an activity (games, bowling, karaoke) or just drinks/food.

- "lively bars with space for a group of 8 to stand and talk"
- "fun activity for friends — think arcade, bowling, or karaoke"
- "laid-back brewery or beer garden for a Sunday afternoon hang"

## Present & book

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price `label`
when `is_bookable`. Render `picture_url` where supported. Only report what the
API returns — never invent venues, prices, or availability. To buy tickets, use
the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific plans — see the **outgoing** skill for the full list.
