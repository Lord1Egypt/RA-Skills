---
name: onehome-fpx
description: >-
  Query OneHome (CoreLogic) — the agent magic-link real-estate portal at
  portal.onehome.com — from a shell with the fpx CLI (@fetchproxy/cli)
  instead of running the onehome-mcp server. Resolve the consumer's group /
  saved-search scope, search shared listings, and read listing detail via
  one-shot GraphQL calls routed through the signed-in browser tab. Use when
  you want OneHome data without the MCP, in a script, or on a machine where
  the MCP isn't installed.
---

# OneHome via fpx (no MCP)

OneHome is a CoreLogic product: buyers reach it through a private
"magic-link" URL their real-estate agent emailed
(`https://portal.onehome.com/en-US/properties/map?token=eyJ...`). It's an
Angular SPA backed by one GraphQL API at `services.onehome.com/graphql`
(plus a couple of REST endpoints), authenticated with
`Authorization: Bearer <sessionToken>`. There's no anti-bot wall on
`services.onehome.com` — the gate is purely the per-user bearer — so `fpx`
is used here to reach the token itself (either by exchanging the magic
link, or by capturing it from a live tab), then to fire the actual GraphQL
calls through the same signed-in tab.

This is the same data the `onehome_*` MCP tools return, reached with CLI
calls instead of a running server. See `src/queries.ts` and `src/auth.ts`
in the repo for the live-verified source of every shape below.

## One-time setup

```sh
npm install -g @fetchproxy/cli                 # provides `fpx`
fpx profile add onehome --domain onehome.com    # covers portal.* and services.*
fpx profile declare onehome \
  --capture-header Authorization@services.onehome.com/graphql  # needed for Path B below
fpx pair -p onehome                             # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** browser extension installed
(from https://github.com/nullnet-app/contextmint-bridge/releases — Chrome:
load the chrome zip unpacked; Safari is not available yet, so use Chrome for now) and paired,
its Chrome **Site access** allowing `onehome.com`, and (for Path B) an open
`portal.onehome.com` tab signed in to the share you want to read.
ContextMint Bridge is the fetchproxy extension renamed, same maintainer (see https://github.com/chrischall/fetchproxy#extension); source at https://github.com/nullnet-app/contextmint-bridge — build it or verify the release zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`.

## Getting a bearer token (two paths)

**Path A — you have the magic-link URL** (from the agent's email). The
`?token=` value is an *email-token*, not a bearer — exchange it once via
the same `checkToken` bootstrap the Angular app runs on load. This also
hands back the consumer's scope (`groupID`, `savedSearchID`, `agentID`,
`contactID`, `mlsID`), so you don't have to guess `group_id` later:

```sh
LINK='https://portal.onehome.com/en-US/properties/map?token=eyJ...'
EMAIL_TOKEN=$(echo "$LINK" | sed -n 's/.*[?&]token=\([^&]*\).*/\1/p')
printf '{"emailToken":"%s"}' "$EMAIL_TOKEN" > /tmp/checktoken-body.json
fpx post-json 'https://services.onehome.com/api/authentication/checkToken' \
  @/tmp/checktoken-body.json -p onehome \
  -H 'Origin: https://portal.onehome.com' -H 'Referer: https://portal.onehome.com/' \
  | tee /tmp/checktoken.json | jq '{groupID,savedSearchID,agentID,contactID,mlsID,email}'
TOKEN="Bearer $(jq -r '.sessionToken' /tmp/checktoken.json)"
```

**Path B — you only have a live signed-in tab** (lost the email, or want
to ride the browser's existing session). This waits for the tab to fire
its next GraphQL request and snapshots the `Authorization` header off it —
scroll the map or click a listing in the tab if it hangs:

```sh
TOKEN=$(fpx session -p onehome | jq -r '.capturedHeaders.Authorization')
```

Path B gives you a bearer only — no session scope, so pass `group_id` /
`saved_search_id` explicitly on every call (or use
`ListingSuggestionsSearch`, which needs neither).

`TOKEN` from either path is already the full `Bearer <jwt>` value.

## Core call

Every operation is a POST of `{"query": "...", "variables": {...}}` to the
GraphQL endpoint, carrying the bearer plus the portal's `Origin`/`Referer`
(upstream checks these). Keep the query text in its own file so you don't
fight shell-quoting on the embedded GraphQL, then assemble the JSON body
with `jq -n --rawfile`:

```sh
cat > /tmp/q.graphql <<'GQL'
query GetSavedSearchBySearchId($searchId: String!) { savedSearch(id: $searchId) { id name listingIds } }
GQL
jq -n --rawfile query /tmp/q.graphql --argjson variables '{"searchId":"REPLACE"}' \
  '{query:$query, variables:$variables}' > /tmp/body.json
fpx post-json 'https://services.onehome.com/graphql' @/tmp/body.json -p onehome \
  -H "Authorization: $TOKEN" -H 'Origin: https://portal.onehome.com' \
  -H 'Referer: https://portal.onehome.com/' \
  | jq '.data'
```

Ready-to-run operation bodies (user/groups, saved search, listing search,
listing detail, photos, and the LocalLogic REST calls) are in
`references/graphql-operations.md`.

## The consumer/agent split

Many fields are **agent-only** and 403 for a consumer-share session:
`user { ... }` (and its nested `groups`), and `savedSearchByGroupId`. The
consumer-readable equivalents are `GetSavedSearchBySearchId(searchId)` →
`listingIds` → `GetSavedListings` (`listingsBySavedSearchId`). Always try
the by-searchId path first; only fall back to the `user`/groups query if
you know the session is an agent's.

## Exit codes (fetch verbs)

- `0` — success (a GraphQL `errors` array can still ride in a `0` body — always check `jq '.errors // empty'`).
- `2` — bridge unavailable: extension not connected or pairing pending → `fpx pair -p onehome`.
- `3` — bot wall (shouldn't happen on `services.onehome.com` — if it does, something upstream changed).
- `4` — upstream non-2xx, most often a stale/expired bearer (401) → get a fresh `TOKEN` via Path A or B above.

## Notes

- The captured/exchanged bearer is a JWT — decode its `exp` if you need to
  know when to refresh. JWTs are base64url, not base64 (they use `-`/`_`
  instead of `+`/`/`), so translate the alphabet before `@base64d`:
  `jq -R 'split(".")[1] | gsub("-";"+") | gsub("_";"/") | @base64d | fromjson | .exp'`
  on the token, ignoring padding errors.
- `fpx health -p onehome` shows bridge connection state when a call fails.
- This project is developed and maintained by AI (Claude).
