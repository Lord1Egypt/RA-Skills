---
name: pet-friendly
description: >-
  Find dog- and pet-friendly outings — patios, cafés, parks, breweries, and
  trails that welcome pets — via natural-language search. Use when the user
  wants to bring their pet along ("dog-friendly cafés", "where can I bring my
  dog", "pet-friendly patios", "places that allow dogs this weekend"). Powered
  by Outgoing, which works in cities worldwide.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🐾"
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

# Pet-friendly outings — powered by Outgoing

Find places that welcome dogs and other pets.

## When to use

The user wants to bring a pet. Triggers: "dog-friendly", "pet-friendly", "can I
bring my dog", "patio that allows dogs", "dog park", "somewhere with my pet".

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
  --data-urlencode "prompt=dog-friendly cafés and patios where I can bring my dog this weekend" \
  --data-urlencode "city=london"
```

- `city` — the city to search, lowercase with underscores (e.g. `paris`,
  `new_york`, `tokyo`, `mexico_city`). Defaults to `new_york`. Outgoing is
  global — pass whatever city the user names.
- Returns `{ message, activities[] }`; each activity has `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search on a neighborhood.

## Shape the prompt

Always state the pet need explicitly in the `prompt` so results actually allow
pets. Add the type of outing (café, patio, park, trail) and the pet's size/needs
when relevant.

- "dog-friendly patios for brunch where a large dog is welcome"
- "off-leash dog parks and pet-friendly trails nearby"
- "breweries or cafés that allow dogs inside"

## Present & book

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price `label`
when `is_bookable`. Render `picture_url` where supported. Only report what the
API returns — never invent venues, prices, availability, or pet policies. To buy
tickets, use the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific plans — see the **outgoing** skill for the full list.
