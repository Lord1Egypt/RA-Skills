---
name: work-meetup
description: >-
  Find professional venues — restaurants for client dinners, quiet cafés for
  meetings, bars for after-work drinks, and spaces for team offsites — via
  natural-language search. Use when the user is planning something work-related
  ("restaurant for a client dinner", "quiet café to meet a colleague", "venue
  for a small team offsite", "networking spots"). Powered by Outgoing, which
  works in cities worldwide.
version: 1.0.0
metadata:
  openclaw:
    emoji: "💼"
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

# Work & networking — powered by Outgoing

Find venues that work for business: client dinners, meetings, after-work drinks,
and team offsites.

## When to use

The user is planning something professional. Triggers: "client dinner",
"business lunch", "meeting spot", "after-work drinks", "team offsite",
"networking", "somewhere quiet to talk shop".

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
  --data-urlencode "prompt=upscale but quiet restaurant for a client dinner downtown" \
  --data-urlencode "city=new_york"
```

- `city` — the city to search, lowercase with underscores (e.g. `paris`,
  `new_york`, `tokyo`, `mexico_city`). Defaults to `new_york`. Outgoing is
  global — pass whatever city the user names.
- Returns `{ message, activities[] }`; each activity has `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….
- Optional `lat`/`lng` center the search near the office or a landmark.

## Shape the prompt

Lead with the professional context, then add the must-haves: noise level
(quiet enough to talk), group size, formality, and budget/expense-friendliness.

- "quiet, upscale restaurant for a 4-person client dinner — easy to talk"
- "café with good wifi and tables for an informal 1:1 meeting"
- "lively but not loud bar for after-work drinks with the team"

## Present & book

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price `label`
when `is_bookable`. Render `picture_url` where supported. Only report what the
API returns — never invent venues, prices, or availability. To buy tickets, use
the **book-tickets** skill (`POST /partner/v1/bookings`).

> Outgoing has more skills for specific plans — see the **outgoing** skill for the full list.
