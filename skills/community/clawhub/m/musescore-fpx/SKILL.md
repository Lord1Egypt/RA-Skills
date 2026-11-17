---
name: musescore-fpx
description: >-
  Query musescore.com (sheet music search, score/license metadata, official
  download links) from a shell with the fpx CLI (@fetchproxy/cli) instead of
  running the musescore-mcp server — one-shot HTTP calls through a signed-in
  browser tab. Use when you want MuseScore data without the MCP, in a script,
  or on a machine where the MCP isn't installed.
---

# MuseScore via fpx (no MCP)

musescore.com has **no public API** (the old one was shut down) and sits
behind a Cloudflare managed challenge ("Just a moment…") that 403s any plain
`curl`/Node request. `fpx` routes the request through the user's own
signed-in browser tab (the ContextMint Bridge extension), which has already cleared
the challenge, so the same page loads that a browser would get. No MuseScore
login is required for search/metadata — just a normal open tab.

This is the same data the `musescore_search` / `musescore_get_score` /
`musescore_download` MCP tools return, reached with one CLI call instead of a
running server.

## One-time setup

```sh
npm install -g @fetchproxy/cli               # provides `fpx`
fpx profile add musescore --domain musescore.com
fpx pair -p musescore                        # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** browser extension installed (from
https://github.com/nullnet-app/contextmint-bridge/releases — Chrome: load the chrome zip
unpacked; Safari not available yet, use Chrome for now —
it is the fetchproxy extension renamed, same maintainer; verify a zip against its
`.sha256` or build from source), with an open
`musescore.com` tab (apex host — no `www`) that has cleared the Cloudflare
challenge, and its Chrome **Site access** allowing `musescore.com`. Pairing
persists — after the first approval every later `fpx` call reuses it.

## Core call — and the JSON-store extraction it needs

Every page is a plain `GET`, HTML in, HTML out:

```sh
fpx get 'https://musescore.com/sheetmusic?text=zelda&recording_type=free-download' -p musescore \
  > /tmp/search.html
```

**The fetched HTML has no result cards** — MuseScore hydrates the DOM
client-side. The real data is an **HTML-entity-encoded JSON store** embedded
in the markup (MuseScore's analogue of a Next.js `__NEXT_DATA__` blob). `jq`
alone can't read it — decode the entities and bracket-match the array/object
you want first. `references/extract-store.mjs` is a small, dependency-free
Node script that does exactly that (mirrors `src/store.ts`'s
`recoverJson`/`findArrayByKey`/`findEnclosingObject`); pipe the saved HTML
through it, then `jq`:

```sh
node references/extract-store.mjs scores < /tmp/search.html | jq '.[] | {id, title, composer_name}'
```

Ready-to-run URL patterns (search, score detail, static render assets) and
their `jq` projections are in `references/endpoints.md`.

## The one rule: search returns ids, detail needs both ids

A score's canonical path is `/user/<userId>/scores/<scoreId>` — search cards
carry `id` (score id) and `user.id` (uploader id), so resolve those from a
search hit before fetching the detail/download page:

```sh
node references/extract-store.mjs scores < /tmp/search.html \
  | jq -r '.[0] | "\(.user.id)\t\(.id)\t\(.title)"'
# 12345   67890   Zelda Theme (arr.)
```

## Downloads: fpx can only RESOLVE the URL, never fetch the bytes

The score-detail store's `type_download_list` array carries the **official**
download link (`musescore.com/score/download/index?score_id=…&type=…&h=…`).
That endpoint is Cloudflare-walled AND 302-redirects **cross-origin** to a
presigned S3 URL. A browser-tab `fetch()` (what `fpx get`/`request` does) hits
the bot wall on that endpoint and, even if it didn't, can't read an opaque
cross-origin redirect. The MCP works around this with a `download` bridge
capability (`chrome.downloads.download`, which issues the request from the
browser's own network stack) — **`fpx` has no equivalent verb**, so from the
shell you can only resolve the URL, not save the file. Print it and open it
yourself in the signed-in tab:

```sh
node references/extract-store.mjs type_download_list < /tmp/score.html \
  | jq -r '.[] | select(.type=="pdf") | .url'
```

Entitlement to check before trusting that link will actually download:
`is_free === true` OR `hasAccess === true` (see `references/endpoints.md`).

## Exit codes (fpx verbs)

- `0` — success.
- `2` — bridge unavailable: extension not connected or pairing pending → run
  `fpx pair -p musescore`, confirm a musescore.com tab is open.
- `3` — bot wall: the tab hasn't cleared Cloudflare → open/refresh a
  `musescore.com` tab and retry.
- `4` — upstream non-2xx from MuseScore.

## Notes

- Anonymous reads only — search, score metadata, and download-URL resolution
  need no MuseScore account. Stay within musescore.com's terms; never
  automate a purchase.
- `fpx health -p musescore` shows bridge connection state when a call fails.
- The rendered page-1 SVG/PNG assets (`musescore.com/static/musescore/scoredata/g/<hash>/score_0.svg|png@0`)
  are session + Referer-gated — they only work fetched via `fpx` (through the
  tab), never a plain `curl`. See `references/endpoints.md`.
- This project is developed and maintained by AI (Claude).
