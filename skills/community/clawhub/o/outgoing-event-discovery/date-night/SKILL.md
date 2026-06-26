---
name: date-night
description: >-
  Plan a romantic date — restaurants, wine bars, cocktail lounges, live music,
  and intimate experiences for couples — via natural-language search. Use when
  the user wants date ideas, a first-date spot, an anniversary outing, or a
  romantic night out ("plan a date night", "romantic dinner this Friday", "where
  to take a date in Paris"). Powered by Outgoing, which works in cities
  worldwide.
version: 1.0.0
metadata:
  openclaw:
    emoji: "💞"
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

# Date night — powered by Outgoing

Find romantic spots and date-worthy experiences for two.

## When to use

The user is planning something for a couple: a first date, an anniversary, a
surprise, or just a romantic night out. Triggers: "date night", "romantic
dinner", "first-date spot", "cocktails for two", "anniversary ideas".

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
  --data-urlencode "prompt=romantic first-date dinner this Friday" \
  --data-urlencode "city=paris"
```

- `city` — the city to search, lowercase with underscores (e.g. `paris`,
  `new_york`, `tokyo`, `mexico_city`). Defaults to `new_york`. Outgoing is
  global — pass whatever city the user names.
- Returns `{ message, activities[] }`; each activity has `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search on a landmark or neighborhood.

## Shape the prompt

Lead with the romantic frame, then add the user's specifics — vibe (cozy,
upscale, lively), timing, budget, neighborhood, and whether it's a first date
vs. a long-time couple.

- "intimate, candle-lit dinner for a first date Saturday night"
- "romantic rooftop cocktails with a view, dressy but not stuffy"
- "cozy wine bar + live jazz for our anniversary near the Marais"

## Present & book

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price `label`
when `is_bookable`. Render `picture_url` where supported. Only report what the
API returns — never invent venues, prices, or availability. To buy tickets, use
the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific plans — see the **outgoing** skill for the full list.
