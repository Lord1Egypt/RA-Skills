---
name: opentable-fpx
description: >-
  Query and manage OpenTable (opentable.com) restaurant reservations from a
  shell with the fpx CLI (@fetchproxy/cli) instead of running the
  opentable-mcp server — search restaurants, check slot availability, list
  reservations/favorites, and book/modify/cancel a table via one-shot
  GraphQL + REST calls through a signed-in browser tab. Use when you want
  OpenTable data or actions without the MCP, in a script, or on a machine
  where the MCP isn't installed.
---

# OpenTable via fpx (no MCP)

OpenTable fronts `www.opentable.com` with Akamai bot protection, and every
booking/cancel action rides the user's own signed-in session (their
loyalty account, saved cards) — there's no API key and no server-side
login. `fpx` routes requests through the user's own signed-in browser tab
(the ContextMint Bridge extension), which already carries a cleared session, so
the same requests the opentable.com web app makes succeed.

This is the same data/actions the `opentable_*` MCP tools expose, reached
with one-shot CLI calls instead of a running server. Every body/header/hash
below is transcribed verbatim from opentable-mcp's `src/client.ts` and
`src/tools/*.ts` — not guessed.

## One-time setup

```sh
npm install -g @fetchproxy/cli            # provides `fpx`
fpx profile add opentable --domain opentable.com
fpx pair -p opentable                     # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** browser extension installed
(https://github.com/nullnet-app/contextmint-bridge/releases; Chrome: load the zip unpacked; Safari isn't available yet, so use Chrome for now), an open
`www.opentable.com` tab **signed in**, and its Chrome **Site access**
allowing `opentable.com`. Pairing persists — after the first approval every
later `fpx` call reuses it.
ContextMint Bridge is the fetchproxy extension renamed, same maintainer (https://github.com/chrischall/fetchproxy#extension); source at https://github.com/nullnet-app/contextmint-bridge — build it or verify a release zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`.

## Core call pattern

Two response families:

- **SSR HTML** (`/s`, `/r/{slug}`, `/user/dining-dashboard`,
  `/user/favorites`, `/booking/details`) embeds the page's data as a
  `window.__INITIAL_STATE__ = {...}` (or `"__INITIAL_STATE__":{...}`) JSON
  blob inside the HTML — extract it with `references/extract-initial-state.mjs`
  before `jq`.
- **`/dapi/...` JSON/GraphQL** returns plain JSON on stdout — pipe straight
  to `jq`.

```sh
fpx get 'https://www.opentable.com/r/state-of-confusion-charlotte' -p opentable \
  | node references/extract-initial-state.mjs \
  | jq '.restaurantProfile.restaurant | {id: .restaurantId, name, bookable: (.type != "Listing")}'
```

Most GraphQL calls here are **Apollo persisted queries** — you send an
operation name + a pre-registered `sha256Hash`, never GraphQL text. Write
the body to a file first (a heredoc avoids shell-quoting the nested JSON),
then `fpx post-json <url> @file -p opentable`.

## The one rule: resolve `dining_area_id` before you book

The numeric `dining_area_id` needed to lock a slot and make a reservation
is **not** in the search or find-slots responses — it only appears on the
`/booking/details` SSR page's `timeSlot.diningAreasBySeating[]`. Always
fetch that page first and take `diningAreasBySeating[0].diningAreaId` (or
match `.tableCategory` to the seating you want) before locking or booking.
That page is also where you learn whether the slot is CC-required, has a
cancellation-fee policy, or requires picking an Experience — read it before
committing to a booking, same as the MCP's `opentable_book_preview`.

## Full request catalogue

Ready-to-run bodies for every read + write (search, restaurant detail,
find-slots, reservations/profile/favorites, book preview→commit, modify,
cancel) with `jq` recipes and the persisted-query hashes are in
`references/opentable-fpx-requests.md`.

## Sign-in detection

A response is the sign-in interstitial, not real data, when the fetched
URL contains `/authenticate/` or the HTML body contains
`continue-with-email-button` / `header-sign-in-button`. Sign into
opentable.com in the bridged tab and retry.

## Exit codes (fetch verbs)

- `0` — success. A GraphQL response can still carry a top-level `errors`
  array in a `0`-exit body — check `jq '.errors // empty'`.
- `2` — bridge unavailable: extension not connected / pairing pending →
  `fpx pair -p opentable`, confirm an opentable.com tab is open.
- `3` — bot wall: the tab hasn't cleared Akamai → open/refresh a
  `www.opentable.com` tab and retry.
- `4` — upstream non-2xx from OpenTable — the body usually names the
  invalid/missing field.

## Notes

- **Booking, modifying, and cancelling are real actions with no
  confirm-gate here.** The MCP's `opentable_book`/`opentable_modify`/
  `opentable_cancel` tools ask the user to confirm first (a prompt, or a
  preview + single-use `confirmToken`) plus a mandatory preview step; raw
  `fpx` calls have none of that — a `make-reservation` POST
  commits immediately. Fetch `/booking/details` and read the cancellation
  policy first (§5 of the reference) before calling it.
- Same-day double-booking, CC-required slots, 3-D Secure, Experience-
  mandatory slots, and non-NA `databaseRegion` shards are all real
  OpenTable constraints — see `references/opentable-fpx-requests.md` and
  this repo's `CLAUDE.md` → "Hot spots / gotchas" for the full detail.
- `fpx health -p opentable` shows bridge connection state when a call
  fails.
- This project is developed and maintained by AI (Claude).
