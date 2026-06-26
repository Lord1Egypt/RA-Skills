---
name: outgoing
description: >-
  Find and book real-world things to do — restaurants, bars, concerts, comedy,
  museums, events, and activities — via natural-language search. The general
  entry point to Outgoing; use it for any "what should we do / where should we
  eat / what's on near me" request, or route to a narrower companion skill when
  the occasion is specific (date-night, kids-weekend, trip-planning, work-meetup,
  enjoy-nature, friends-hangout, meet-new-people, pet-friendly, stay-active,
  accessible-outings) or the user wants to buy tickets (book-tickets). Works in
  cities worldwide.
version: 0.1.7
metadata:
  openclaw:
    emoji: "🧭"
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

# Outgoing — things to do

Outgoing is an AI concierge for the real world: turn any "what should we do?"
into a short, ranked list of real places and events, and automatically book tickets
or make reservations when you're ready.

Use this general skill for everyday "what's on / where should we eat" requests at home, as
well as detailed planning when you and your family are traveling.

We offer many skills specifically tuned to get you better results for common scenarios:

| Skill | Helps you… |
|-------|-----------|
| `date-night` | plan a romantic night out for two |
| `kids-weekend` | find family- and kid-friendly fun |
| `trip-planning` | make the most of a visit to a new city |
| `work-meetup` | pick the right spot for a client dinner or meeting |
| `enjoy-nature` | get outside to parks, gardens, scenic walks, hikes |
| `friends-hangout` | round up a fun night with a group |
| `meet-new-people` | find welcoming social events to meet people |
| `pet-friendly` | bring your dog or pet along |
| `stay-active` | do something sporty and active |
| `accessible-outings` | find low-mobility, accessible places |
| `book-tickets` | buy tickets for a bookable activity |

## How it works

Calls the **Outgoing API** (`GET /partner/v1/search`) — one
natural-language search returns ranked, personalized, high-quality events and activities. Full
reference (auth, every parameter, booking, schemas) as plain Markdown:
<https://www.outgoing.world/llms.txt> and <https://www.outgoing.world/llms-full.txt>.

### Setup

You can authenticate with either an Outgoing API key or an AAuth key —
AAuth keys are auto-provisioned by OpenClaw (see
<https://www.npmjs.com/package/@aauth/mcp-openclaw>). If you're not using AAuth,
request an API key with the partner scope and store it in an env var:

```bash
export OUTGOING_API_KEY="og_api_…"   # partner scope — get one at https://outgoing.world
```

For Claw, usually your agent will act on behalf of a single user account, but you can provision 
additional users (e.g. for a partner or family member) and pass that id as `X-External-User-Id`.

### Search

```bash
curl -sS -G https://api.outgoing.world/partner/v1/search \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  -H "X-External-User-Id: user-123" \
  --data-urlencode "prompt=live jazz and a late dinner tonight" \
  --data-urlencode "city=paris"
```

- `city` — an optional hint to ground the search, if the query doesn't specify enough. Overridden
by the contents of the query (e.g. `live jazz in Soho`)
- Returns `{ message, activities[] }`; each activity has `name`,
  `short_description`, `semantic_location`, `is_bookable`, `ticket_price`, ….

## Shape the prompt

Pass the user's intent verbatim and fold in timeframe, vibe, group, and any
landmark. One rich `prompt` beats several thin ones.

- "what's on tonight in SoMa — drinks and live music"
- "low-key things to do this rainy Sunday afternoon"
- "best outdoor music near the Eiffel Tower next weekend"

## Present & book

Lead with the `message`, then list picks: **name**, one-line
`short_description`, neighborhood (`semantic_location`), and the price `label`
when `is_bookable`. Render `picture_url` where supported. Only report what the
API returns — never invent venues, prices, or availability. To buy tickets, use
the **book-tickets** skill (`POST /partner/v1/bookings`).
