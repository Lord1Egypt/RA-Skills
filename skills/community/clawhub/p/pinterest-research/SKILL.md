---
name: pinterest-research
description: Researches Pinterest profiles, boards, pins, ideas categories, and search results via the Crawlora API, returning clean JSON. Use when the user wants a Pinterest user's profile/boards/pins, a pin's or board's detail, a category feed, or a keyword search on Pinterest — instead of scraping Pinterest directly.
---

# Pinterest research

Look up public Pinterest profiles, boards, and pins, browse the "Ideas"
category taxonomy, and run keyword search — all as normalized JSON from the
Crawlora API, no Pinterest scraping or unofficial client libraries.

## When to use this skill

- "What's <username>'s Pinterest profile / follower count / boards?"
- "Pull the pins from this board / this user's own pins."
- "What's in this pin?" (title, description, image, save count).
- "Search Pinterest for pins about <topic>."
- "What are Pinterest's Ideas categories, and what's trending in <category>?"
- Competitor board audits, content-idea research, or trend scouting on
  Pinterest.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Search** — `/pinterest/search?query=` for pins matching a text query
   (title, description, image, board, pinner per result).
2. **Pin detail** — `/pinterest/pin/{id}` for one pin's full detail: title,
   description, image, board, pinner, comment count, save count, creation
   time.
3. **Board detail** — `/pinterest/board/{username}/{slug}` for a board's
   metadata (name, description, cover image, pin/follower counts, owner)
   plus a page of its pins.
4. **User profile** — `/pinterest/user/{username}` for a user's public
   profile: display name, bio, website, avatar, follower/following/pin/board
   counts.
5. **User's boards / pins** — `/pinterest/user/{username}/boards` and
   `/pinterest/user/{username}/pins` for a page of a user's own boards or
   own pins.
6. **Ideas categories** — `/pinterest/categories` for the top-level "Ideas"
   taxonomy (e.g. "Animals", "Home Decor", "Food And Drink"); each entry's
   `id` feeds `/pinterest/ideas/{id}` for that category's metadata plus a
   page of pins from its feed.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Profile + boards + pins:
scripts/crawlora.sh /pinterest/user/marthastewart | jq '.'
scripts/crawlora.sh /pinterest/user/marthastewart/boards | jq '.'
scripts/crawlora.sh /pinterest/user/marthastewart/pins | jq '.'

# Search + pin detail:
scripts/crawlora.sh /pinterest/search query="minimalist home office" | jq '.'
scripts/crawlora.sh /pinterest/pin/123456789 | jq '.'

# Ideas categories + a category feed:
scripts/crawlora.sh /pinterest/categories | jq '.'
scripts/crawlora.sh /pinterest/ideas/home-decor | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Pinterest
endpoint this skill uses.

## Examples

- **Competitor board audit:** pull a competitor's profile plus
  `/pinterest/user/{username}/boards`, compare board topics, pin counts, and
  follower counts to spot content gaps.
- **Content-idea research:** `/pinterest/categories` to find the relevant
  "Ideas" category, then `/pinterest/ideas/{id}` to see what's currently
  surfacing in that category's feed before planning new pins.
- **Brand-mention / keyword sweep:** `/pinterest/search` for a brand or
  product name, then `/pinterest/pin/{id}` on the top results to check
  save counts and pinner details.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public profiles/boards/pins; no login, no private
  boards. Respect Pinterest's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Board lookups need both `username` and `slug`** — get the slug from the
  board's own `/{username}/{slug}/` URL; there's no board-search-by-name
  endpoint.
- **`/pinterest/ideas/{id}` requires a category id from
  `/pinterest/categories` first** — ids aren't guessable from a category's
  display name.
- List endpoints (`search`, `board`, `user/{username}/boards`,
  `user/{username}/pins`, `ideas/{id}`) return a page of results — check the
  response for a cursor/offset to walk beyond the first page.
