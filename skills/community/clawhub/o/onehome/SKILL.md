---
name: onehome
description: Search OneHome (CoreLogic) portal listings, get property details, photos, schools, saved searches. Use when the user asks about real estate listings shared by their agent, OneHome links, portal.onehome.com properties, or specific addresses / MLS numbers they want to look up.
---

# OneHome MCP

OneHome is a CoreLogic product. Buyers reach it through a private magic-link URL their real-estate agent emailed (`https://portal.onehome.com/.../?token=...`). It's an Angular SPA backed by a single GraphQL API at `services.onehome.com/graphql`.

This skill drives the `onehome-mcp` tools (`onehome_*`) — all GraphQL-bound except for the local PITI / affordability calculators.

## When to use

- The user mentions OneHome, a portal.onehome.com URL, or a CoreLogic magic-link they got from their agent.
- They ask about listings in a specific "group" their agent set up (Lake Lure, downtown condos, etc.).
- They want to look up a listing by MLS number or address and the other realty MCPs returned nothing.
- They want photos, school info, or to compare two OneHome listings.

If the user asks generally about a property without naming OneHome, prefer one of the public-listing MCPs (zillow / redfin / homes / compass) first.

## Auth modes

The MCP picks one at startup:

1. `ONEHOME_TOKEN` (env): raw bearer JWT.
2. `ONEHOME_MAGIC_LINK` (env): full URL with `?token=`. The token IS the bearer.
3. fetchproxy capture: capture from a signed-in `portal.onehome.com` tab.

Run `onehome_healthcheck` first to confirm auth is wired up — it returns the mode, token expiry (when known), and a one-line hint.

## Workflow

1. **Pick a group.** `onehome_get_groups` → the curated buckets the agent shared with the buyer. Most tools take a `group_id`.
2. **Search inside the group.** `onehome_search_properties { group_id, [saved_search_id] }`. Pass a `saved_search_id` from `onehome_get_saved_search` to apply a saved filter; leave it off for the group default. `onehome_get_saved_search_with_listings` returns the saved search and its inflated listings in one call.
3. **Inflate a listing.** `onehome_get_property { group_id, listing_id }` for the full record. The listing id is an OSK like `EYxOzZSAbCdEf12345`; you can pass a portal URL instead and the MCP will extract it.
4. **Photos / schools / walkability** are separate calls. Use the lat/lng from `onehome_get_property` to drive `onehome_get_schools` and `onehome_get_walk_score`.
5. **Compare** `onehome_compare_properties { group_id, targets: [...], view? }` — 2 to 8 listings, concurrent fetch, per-row error capture. Don't fan out manual `get_property` calls when comparing.
6. **Escape hatch.** `onehome_graphql { operation_name, query, variables?, view? }` lets you send a raw read-only document (mutations and subscriptions are refused) when you need a field the structured tools don't expose. Common operation names: `GetOneHomeUser`, `GetListings`, `GetPins`, `ListingById`, `MediaListingById`, `GetSavedSearches`, `ListingSuggestionsSearch`. (LocalLogic schools / walk-score are REST endpoints, not GraphQL operations — use `onehome_get_schools` / `onehome_get_walk_score` instead.)

## Free-text search

`onehome_search_suggestions { query }` bypasses the group / saved-search structure. Use it when the user knows what they're looking for (MLS number, address, partial street name) but doesn't care which group it lives in.

## Local computation

`onehome_calculate_mortgage` and `onehome_calculate_affordability` are pure local math — no network, no token needed. Use them when the user asks "what would my payment be on this place" or "what can I afford"; identical math to the other realty MCPs.

## Response shape (`view`)

Four tools take `view: "compact" | "full"` — `onehome_get_by_address`,
`onehome_compare_properties`, `onehome_get_user` and `onehome_graphql` — and
**`compact` is the default**. You get the slim shape without asking for it;
an efficiency a caller has to request is one that is usually not requested.

**What compact does here is strip image and avatar URLs, and nothing else.**
There is no field projection, and none is claimed: this server hands OneHome's
payload back close to verbatim and holds no verified record of which of its
fields matter, so nothing here could honestly name a keep-list. Stripping media
is *subtractive* — it names what to remove, never what to keep — so it cannot
lose a field nobody anticipated. Every non-media field, at every depth,
survives compact untouched.

**The surprise is `onehome_graphql`.** Compact keeps every envelope key
(`data`, `errors`, `status`, `url`), but the strip reaches *inside* `data` —
and `MediaListingById`, one of the operation names this skill recommends, is
all media. OneHome nests its variants under an `Image` key, so at the default
rung each photo comes back as `{ Order, LongDescription }` with `Thumbnail`,
`Medium` and `Large` all gone: the call succeeds and returns nothing you asked
for. Pass `view: "full"` for any media query — and for any call you are making
*because* a payload was not what you expected, so a missing field is never this
server's doing.

`view: "full"` returns what the tool built with nothing removed. There is
deliberately **no `raw` rung**, for two different reasons: on `onehome_graphql`
`full` already *is* the unprojected upstream envelope, so a third value would
silently alias the second; and the other three assemble their record from a
query result plus derived fields, so there is no single upstream payload left
to hand back.

**One tool takes a different `view`:** `onehome_get_saved_search_with_listings`
takes `view: "full" | "brief"` — `full` (the default) is its usual record;
`brief` is one line per listing for context groups (below). It has no
`compact` rung.

**The other sixteen tools take no `view` at all.** That is scope — a partial
rollout, not an oversight — but for two of them it is also correct on the
merits:

- `onehome_get_property_photos` exists to return exactly the URLs compact
  strips. Its product *is* the image; stripping there would not shrink the
  response, it would empty it. Never media-strip a tool whose name is the test.
- `onehome_calculate_mortgage` and `onehome_calculate_affordability` are local
  math returning a handful of numbers — already narrower than any projection.

## In context groups

This server is in the **home** group (`_meta.mint.domain: "home"`); every tool
but `onehome_healthcheck` carries a hint.

- **Canonical read:** `onehome_get_saved_search_with_listings` answers
  *what's new* — the saved search's listings, newest change first, as one
  `view: "brief"` line each (`address · price — date of its last change —
  status, change`, e.g. a new listing or a price decrease), inside the
  untrusted-data envelope as `data: string[]` because listing text comes from
  the MLS feed. An empty search answers `-- none`; a page holding fewer
  listings than the search adds `-- N of M shown`. It takes no date
  range and declares no subject: saved searches are not listable at start (a
  consumer share sees only the one in its session context), so the host calls
  it once and it answers from the session's own saved search.
- Nothing here answers *what's due* or *what's on*; every other read is a
  `lookup`. `onehome_set_active_session` is a `change`; `onehome_set_auth` is
  `other`.
- **A compound ask** looks like "anything new on the house hunt, and is the
  pool heater on?" — the home group fans out to this server's saved search and
  to the other home members in one call.
- In fetchproxy-capture mode (no `ONEHOME_TOKEN` / `ONEHOME_MAGIC_LINK`) the
  bearer comes from a signed-in `portal.onehome.com` tab; with no tab open the
  group answers that OneHome **needs your browser open**.

## Common pitfalls

- **Forgetting `group_id` on listing detail / photos.** Every listing surface is scoped to a group. If you have a listing id from `onehome_search_suggestions`, you still need a group id to inflate it. Pick the group most likely to contain it (usually the user's primary one).
- **Stale token.** OneHome JWTs expire. `onehome_healthcheck` shows `seconds_until_expiry`. Refresh the env var if it's close to zero.
- **fetchproxy capture mode + no interaction.** In capture mode, the MCP can't read the bearer until the user's tab fires a GraphQL request. If a call hangs there, ask the user to scroll the map / click a listing / refresh the portal page.
