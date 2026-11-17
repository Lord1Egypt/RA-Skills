---
name: hellofresh-fpx
description: "Read HelloFresh (US) meal-kit data from a shell — the subscription (box size, delivery slot, frequency), upcoming delivery weeks with cutoffs and skip status, a week's menu with the current meal picks and premium upcharges, HelloFresh's own price for a week's box, the box sizes on offer, and the customer plan — with curl and jq, using the session token from the user's signed-in hellofresh.com tab (read once with the fpx CLI). Use when asked about HelloFresh boxes, deliveries, cutoffs, menus or picks without the hellofresh-mcp server."
---

# HelloFresh access (fpx + curl)

The hellofresh.com web app keeps its session in the cookie **`apiV2Auth`** on
`www.hellofresh.com`: a URL-encoded JSON token set whose `access_token` (a
30-minute JWT) is sent as `Authorization: Bearer` to
`https://www.hellofresh.com/gw/...`. With a bearer the API answers plain `curl`
(no Cloudflare wall), so `fpx` is used for three things only:
- reading that cookie from the signed-in tab;
- after a shell-side refresh, writing the rotated token set back so the
  browser stays signed in;
- the one call Cloudflare walls even with a bearer: HelloFresh's price
  calculator, sent through the tab.

**Read-only.** For changes (meal picks, skips, box size, delivery day), use the
hellofresh-mcp tools: they are confirmation-gated and verify every write. The
request shapes here are the ones that server uses (`docs/HELLOFRESH-API.md` in
the repo, captured from the live web app). US market only.

## One-time setup

```sh
npm install -g @fetchproxy/cli            # provides `fpx`
fpx profile add hellofresh --domain hellofresh.com
fpx profile declare hellofresh --cookie apiV2Auth --allow-cookie-write
fpx pair -p hellofresh --subdomain www    # approve the pair code in ContextMint Bridge
```

Declare the cookie AND `--allow-cookie-write` **before** pairing — a later
`profile declare` can't widen an existing grant (you would have to
`fpx profile remove hellofresh` and start again).

Needs **ContextMint Bridge** in Chrome and a tab signed in at
`https://www.hellofresh.com/`. If the bridge runs in **more than one browser**,
each one dials the same port: a `pair code` on stderr on every call, while the
command still succeeds, is the second browser being turned away. Don't approve
those codes. Pinned the wrong browser? `fpx trust clear fpx-hellofresh`, then
pair in the browser that holds the HelloFresh session.

## Core pattern

The token goes **into a file, never to stdout** (and never onto a command
line): `scripts/hf-token.mjs` decodes the cookie into `auth.json` and a one-line
`auth.header` that curl reads with `-H @file`. All files are mode 600 in the
skill's own state dir.

```sh
S=~/.hellofresh-fpx; mkdir -p -m 700 "$S"
T=~/.claude/skills/hellofresh-fpx/scripts/hf-token.mjs   # or <repo>/skills/hellofresh-fpx/scripts/hf-token.mjs
(umask 077; fpx cookies apiV2Auth -p hellofresh --storage-subdomain www > "$S/cookie.json") && node "$T" load "$S"
hf() { curl -sS --fail-with-body -H @"$S/auth.header" -H 'accept: application/json' "https://www.hellofresh.com/gw$1"; }
hf '/api/customers/me/subscriptions?country=US&locale=en-US' | jq '.items[0] | {id, sku: .product.sku, nextDeliveryWeek, nextCutoffDate}'
```

`hf-token.mjs load` prints (to stderr) how many minutes the token has left. The
access token lives 30 minutes. When it has expired: **reload the hellofresh.com
tab** (the web app refreshes itself) and run the two lines above again. Only if
that doesn't help, refresh from the shell and write the new set back — the
refresh token ROTATES on every refresh, so skipping the write-back signs the
browser out. Recipe: `references/requests.md` § Refresh.

Every read and its `jq` projection is in `references/requests.md`. The records
carry the account holder's name, email, addresses and payment details — the
recipes project them away; keep it that way when writing new ones.

## Errors

- `401` — token expired or revoked: reload the tab, `load` again.
- `400 {"error":"invalid_grant"}` on refresh — the refresh token is spent:
  sign in again at hellofresh.com in the paired browser.
- A `Just a moment…` HTML page — the request went out without a bearer.
- `403` with an "Attention Required" HTML page on `/gw/calculate` — it was
  sent from curl; it only works through the tab (`fpx post-json`, see
  `references/requests.md` § Real box price).
- The menu call answers `400` unless it carries `servings` + `product-sku`.
- `hf-token.mjs` exits `4` when the cookie holds no session (signed out) or a
  refresh was refused, `64` on bad usage.
- `fpx` exits `2` when the bridge is down or the tab/pairing is missing.

Never paste token values into chat, commits or issues. `rm ~/.hellofresh-fpx/{cookie.json,auth.json,auth.header,refreshed.json,cookie.txt,calc-*.json}` clears them.

Every recipe here was run live in both bash and zsh on 2026-11-12.
