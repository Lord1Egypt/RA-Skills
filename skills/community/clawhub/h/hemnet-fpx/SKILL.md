---
name: hemnet-fpx
description: >-
  Query hemnet.se (Swedish property portal) from a shell with the fpx CLI
  (@fetchproxy/cli) instead of running the hemnet-mcp server — resolve
  locations, search for-sale and sold listings, and read listing detail via
  one-shot GraphQL calls through a signed-in browser tab. Use when you want
  Hemnet data without the MCP, in a script, or on a machine where the MCP
  isn't installed.
---

# Hemnet via fpx (no MCP)

Hemnet fronts `www.hemnet.se` — including `/graphql` — with a Cloudflare
managed challenge that 403s any plain `curl`/Node request. `fpx` routes the
request through the user's own signed-in browser tab (the ContextMint Bridge
extension), which has already cleared the challenge, so the same anonymous
GraphQL query succeeds. No Hemnet login is needed — just a normal open tab.

This is the same data the `hemnet_*` MCP tools return (money in **SEK**
strings, areas in **m²**), reached with one CLI call instead of a running
server.

## One-time setup

```sh
npm install -g @fetchproxy/cli            # provides `fpx`
fpx profile add hemnet --domain hemnet.se # only the fetch capability is needed
fpx pair -p hemnet                        # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** browser extension installed (from
[its releases](https://github.com/nullnet-app/contextmint-bridge/releases) —
Chrome: load the chrome zip unpacked; Safari isn't available yet, so use
Chrome for now), with an open
`www.hemnet.se` tab, and its Chrome **Site access** allowing `hemnet.se`.
Pairing persists — after the first approval every later `fpx` call reuses it.
ContextMint Bridge is the renamed fetchproxy extension (same maintainer; source at https://github.com/nullnet-app/contextmint-bridge — verify a release zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`).

## Core call

Every query is a POST of `{"query": "...", "variables": {...}}` to the
GraphQL endpoint. Send the body raw (no `--json`) so stdout is the GraphQL
JSON, ready for `jq`:

```sh
fpx post-json 'https://www.hemnet.se/graphql' @query.json -p hemnet \
  | jq '.data'
```

`@file` reads the body from a file; a literal `'{...}'` string works too but
shell-quoting the embedded query is fiddly — prefer a heredoc into a file.

Ready-to-run query bodies (autocomplete, for-sale search, listing detail,
sold search) with jq recipes are in `references/graphql-queries.md`. Exhaustive
field lists live in the repo at `src/graphql.ts` — the operations here are
compact, live-verified subsets.

## The one rule: resolve the location first

Hemnet searches take numeric **location ids**, never place names. Always
autocomplete first, take the `locationId`, then search:

```sh
printf '{"query":"query($q:String!,$l:Int!){autocompleteLocations(query:$q,limit:$l){hits{locationId fullName parentFullName}}}","variables":{"q":"Höllviken","l":3}}' > /tmp/q.json
fpx post-json 'https://www.hemnet.se/graphql' @/tmp/q.json -p hemnet \
  | jq -r '.data.autocompleteLocations.hits[] | "\(.locationId)\t\(.fullName)"'
# 898675  Höllviken tätort
```

## Exit codes (fetch verbs)

- `0` — success (a GraphQL `errors` array can still ride in a `0` body; check it).
- `2` — bridge unavailable: extension not connected or pairing pending → run `fpx pair -p hemnet`, confirm a hemnet tab is open.
- `3` — bot wall: the tab hasn't cleared Cloudflare → open/refresh a `www.hemnet.se` tab and retry.
- `4` — upstream non-2xx from Hemnet.

## Notes

- Anonymous reads only — this touches the same public GraphQL surface as the
  MCP; no account data. Stay within hemnet.se's terms.
- `fpx health -p hemnet` shows bridge connection state when a call fails.
- This project is developed and maintained by AI (Claude).
