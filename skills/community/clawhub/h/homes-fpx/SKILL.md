---
name: homes-fpx
description: >-
  Query homes.com (US real-estate portal) from a shell with the fpx CLI
  (@fetchproxy/cli) instead of running the homes-mcp server — search
  listings, resolve street addresses, fetch property detail/photos/
  history, and read the signed-in user's saved homes, all through a
  one-shot call over their own signed-in browser tab. Use when you want
  homes.com data without the MCP, in a script, or on a machine where the
  MCP isn't installed.
---

# homes.com via fpx (no MCP)

homes.com is a fully server-rendered site with **no public JSON API**
and gates traffic through **AWS WAF at the session level** — every
request, not just login, needs to ride a real browser session. `fpx`
routes each call through the user's own signed-in `www.homes.com` tab
(the ContextMint Bridge extension), which has already cleared the WAF
challenge, so the same fetch a Node process gets 403'd on succeeds.

This is "Pattern A" (every call rides the bridge) — there's no
bootstrap-once/direct-fetch shortcut like some sibling portals get.

Almost every page is HTML with one embedded Schema.org
`<script type="application/ld+json">` block carrying the structured
data (search results, property detail). One endpoint — the address
typeahead — is a real JSON API. Everything else this skill covers is
DOM scraping over specific, verified sections of the same pages the
`homes_*` MCP tools parse.

## One-time setup

```sh
npm install -g @fetchproxy/cli       # provides `fpx`
fpx profile add homes --domain homes.com
fpx pair -p homes                    # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** browser extension installed
(from its [releases](https://github.com/nullnet-app/contextmint-bridge/releases) — Chrome: load the zip unpacked;
Safari: not available yet (will ship inside the ContextMint app) — use Chrome for now;
it is the renamed fetchproxy extension from the same maintainer — verify a
release zip with `shasum -a 256 -c <zip>.sha256` or build from source), with an
open `www.homes.com` tab (signed in — required for the saved-homes/
saved-searches tools below, and helps every other page render the way
the extractors expect), and its Chrome **Site access** allowing
`homes.com`. Pairing persists after the first approval.

## Core call pattern

Always pass the **full URL** (fpx has no base-URL concept of its own):

```sh
fpx get 'https://www.homes.com/<path>' -p homes
```

Most responses are HTML — pull the JSON-LD block out with `node`, then
project with `jq`. homes.com HTML-entity-encodes the script tag's
`type` attribute (`application/ld&#x2B;json`), so match loosely:

```sh
fpx get 'https://www.homes.com/atlanta-ga/' -p homes > /tmp/page.html
node -e '
  const html = require("fs").readFileSync("/tmp/page.html", "utf8");
  const m = html.match(/<script type="application\/ld(?:\+|&#x2B;)json">([\s\S]*?)<\/script>/);
  if (!m) { console.error("no JSON-LD found"); process.exit(1); }
  process.stdout.write(m[1]);
' > /tmp/jsonld.json
jq '.["@graph"][] | select(.["@type"] == "CollectionPage")' /tmp/jsonld.json
```

The one non-HTML endpoint (address typeahead) is a real JSON POST — no
extraction step, pipe straight to `jq`:

```sh
fpx post-json 'https://www.homes.com/routes/res/consumer/smartsearch/autocomplete/' \
  @/tmp/body.json -p homes | jq '.suggestions.places'
```

Ready-to-run request/extraction recipes for every endpoint — search,
property detail, photos, history/tax, nearby, market report, saved
homes/searches, and the typeahead — are in
`references/homes-requests.md`.

## The one rule: resolve before you fetch detail

If you only have a free-text address (not a `/property/<slug>/<hash>/`
URL), resolve it first — same three-rung order `homes_get_by_address`
uses:

1. **Typeahead** (`POST /routes/res/consumer/smartsearch/autocomplete/`)
   — the primary rung; returns the real detail URL directly.
2. **Slug** (`GET /<address-city-state-zip-slug>/`) — homes.com often
   routes an unambiguous address straight to the detail page.
3. **Search fallback** (`GET /<city-slug>/`, fuzzy-match the street) —
   only when 1 and 2 miss.

See `references/homes-requests.md` for the exact body/path shapes and a
`jq` street-match recipe. Verify whatever candidate you pick against the
address you asked for — homes.com will happily return the "closest"
result, not a confirmed match.

## Auth-gated pages

`homes_get_saved_homes` / `homes_get_saved_searches` need a signed-in
tab. A missing session shows up as either:

- a redirect to `/sign-in`, or
- the AWS WAF challenge interstitial (body contains both `awswaf.com`
  and `challenge.js`, and is under ~80 KB).

If you see either, open `www.homes.com` in the browser tab fpx is
paired to, sign in / clear the challenge, and retry.

## Output & exit codes (fetch verbs)

- `0` — success (still check the body — an empty JSON-LD match or a
  sign-in redirect can ride a `200`).
- `2` — bridge unavailable: extension not connected or pairing pending
  → `fpx pair -p homes`, confirm a `www.homes.com` tab is open.
- `3` — bot wall: the tab hasn't cleared the AWS WAF challenge → open/
  refresh a `www.homes.com` tab and retry.
- `4` — upstream non-2xx from homes.com.
- `fpx health -p homes` shows bridge connection state when a call fails.

## Notes

- No account data beyond the saved-homes/searches pages — everything
  else is public listing data. Stay within homes.com's terms.
- This project is developed and maintained by AI (Claude).
