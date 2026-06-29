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
5. **Compare** `onehome_compare_properties { group_id, targets: [...] }` — 2 to 8 listings, concurrent fetch, per-row error capture. Don't fan out manual `get_property` calls when comparing.
6. **Escape hatch.** `onehome_graphql` lets you send a raw document with variables when you need a field the structured tools don't expose. Common operation names: `GetOneHomeUser`, `GetListings`, `GetPins`, `ListingById`, `MediaListingById`, `GetSavedSearches`, `ListingSuggestionsSearch`. (LocalLogic schools / walk-score are REST endpoints, not GraphQL operations — use `onehome_get_schools` / `onehome_get_walk_score` instead.)

## Free-text search

`onehome_search_suggestions { query }` bypasses the group / saved-search structure. Use it when the user knows what they're looking for (MLS number, address, partial street name) but doesn't care which group it lives in.

## Local computation

`onehome_calculate_mortgage` and `onehome_calculate_affordability` are pure local math — no network, no token needed. Use them when the user asks "what would my payment be on this place" or "what can I afford"; identical math to the other realty MCPs.

## Common pitfalls

- **Forgetting `group_id` on listing detail / photos.** Every listing surface is scoped to a group. If you have a listing id from `onehome_search_suggestions`, you still need a group id to inflate it. Pick the group most likely to contain it (usually the user's primary one).
- **Stale token.** OneHome JWTs expire. `onehome_healthcheck` shows `seconds_until_expiry`. Refresh the env var if it's close to zero.
- **fetchproxy capture mode + no interaction.** In capture mode, the MCP can't read the bearer until the user's tab fires a GraphQL request. If a call hangs there, ask the user to scroll the map / click a listing / refresh the portal page.
