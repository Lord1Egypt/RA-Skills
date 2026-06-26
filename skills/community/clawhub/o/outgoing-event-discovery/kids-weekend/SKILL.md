---
name: kids-weekend
description: >-
  Find family-friendly things to do with kids — interactive museums, parks,
  workshops, shows, and rainy-day activities — via natural-language search. Use
  when the user wants ideas for children or the whole family ("things to do with
  the kids this weekend", "indoor activities for a toddler", "family fun
  Saturday"). Powered by Outgoing, which works in cities worldwide.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🧸"
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

# Kids & family — powered by Outgoing

Find things to do with children and the whole family.

## When to use

The user is planning for kids or a family outing. Triggers: "with the kids",
"family-friendly", "toddler", "rainy-day activities", "something for a
4-year-old", "school holiday plans".

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
  --data-urlencode "prompt=family-friendly things to do with two young kids this Saturday" \
  --data-urlencode "city=san_francisco"
```

- `city` — the city to search, lowercase with underscores (e.g. `paris`,
  `new_york`, `tokyo`, `mexico_city`). Defaults to `new_york`. Outgoing is
  global — pass whatever city the user names.
- Returns `{ message, activities[] }`; each activity has `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search on a landmark or neighborhood.

## Shape the prompt

Lead with the family frame and capture the kids' ages, indoor vs. outdoor,
weather, and timing — these dramatically change good picks.

- "interactive, hands-on activities for a curious 4- and 7-year-old Saturday morning"
- "indoor rainy-day ideas for toddlers — somewhere they can run around"
- "something artistic to do with my kids this weekend"

## Present & book

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price `label`
when `is_bookable`. Render `picture_url` where supported. Only report what the
API returns — never invent venues, prices, or availability. To buy tickets, use
the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific plans — see the **outgoing** skill for the full list.
