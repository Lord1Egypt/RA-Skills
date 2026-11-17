---
name: koopje-search
description: Search koopje.ai for Belgian second-hand deals and auctions.
version: 1.0.23
author: Lukas, koopje.ai
license: MIT
metadata:
  openclaw:
    requires:
      env:
        - KOOPJE_API_KEY
  hermes:
    tags: [koopje, search, second-hand, belgium, api]
---

# koopje.ai search API

Search ~155k Belgian second-hand listings and live auctions via the
koopje.ai REST API. The index aggregates 2dehands.be, auction houses,
Troc.com, Think Twice, De Striep Promo, Marktplaats, Zoekertjes.be and Belgian car dealers, plus user ads:

| source | what it is |
|---|---|
| `2dehands` | private sellers on 2dehands.be (Belgium's largest marketplace) |
| `trader` | professional occasion sellers on 2dehands.be |
| `troc` | Troc.com second-hand store inventory (Belgian stores) |
| `thinktwice` | Think Twice vintage chain webshop Think2.eu (fixed price, kringloop) |
| `strieppromo` | De Striep Promo Belgian strip shop, second-hand wall (fixed price, tweedehands) |
| `marktplaats` | Belgian listings on Marktplaats.nl |
| `zoekertjes` | free classifieds on Zoekertjes.be |
| `kringwinkel` | Kringwinkel.be thrift webshop (fixed price) + veilingsite (auction lots); one source, `listing_type` splits them |
| `user` | user-submitted own ads (live at `https://koopje.ai/<category>/<slug>-<id>`, 30-day expiry) |
| car-dealer domains | Belgian cars carry their dealer/platform as source: `autoscout24.be`, `gocar.be`, `mazdastock.be`, `vroom.be`, `autohero.com`, `irisautocenter.be`, `autocadre.com` (resolved from listings, never the aggregator) |
| auction-house slugs | auction lots carry their house as source: `alleveilingen`, `vavato`, `troostwijk`, `auctelia`, `belga-veilingen`, `vlavem`, `auctionport`, `openbare-verkopen`, `bopa`, `hammertime`, `veilbalie`, `komerco`, `lussis`, `bell-auction`, `industrial-auctions`, `appelboom`, `auctim` (house name also in `seller_name`) |

Every result also carries `listing_type`: `veiling` (any auction house),
`kringloop` (Troc.com + Kringwinkel shop) or `tweedehands` (everything
else) — repeatable for multiselect, independent of source.

## When to use

Use this skill **only** when the user asks for Belgian second-hand
listings or auction lots — e.g. "find a used bike in Gent", "wat kost
een tweedehands espresso-machine?", "similar to <listing url>", "zoek
een veilingkavel". Do not use it for generic shopping, price or product
questions that are not about a Belgian second-hand/auction listing. If
the intent is ambiguous, ask the user before calling the API.

## Prerequisites

- `KOOPJE_API_KEY` env var, a `kk_...` key from koopje.ai (account →
  "API keys"; shown once at creation).

## How to call

All endpoints: `https://koopje.ai`, auth header on every request:
`Authorization: Bearer $KOOPJE_API_KEY`. JSON responses, CORS enabled.

### POST-free quickstart — GET /v1/search

```
curl -s "https://koopje.ai/v1/search?q=vintage+stoel&price_max=200&limit=5" \
  -H "Authorization: Bearer $KOOPJE_API_KEY"
```

Key parameters (full list in `references/api.md`):

| param | notes |
|---|---|
| `q` | required, natural language or keywords (Dutch works best) |
| `source` | exact origin: `2dehands`, `troc`, `thinktwice`, `strieppromo`, `marktplaats`, `zoekertjes`, `kringwinkel`, a car-dealer domain (`autoscout24.be`, `gocar.be`, …), or an auction-house slug (`vavato`, `troostwijk`, …). Legacy aliases still work: `2dehands` → all tweedehands, `veiling` → all auctions. Default: all sources |
| `listing_type` | `tweedehands` (all second-hand), `veiling` (all auction lots) or `kringloop` (thrift stores) — repeat for multiselect, independent of source |
| `category` | one of the 27 slugs (`computers`, `fietsen`, `boeken`, `verzamelen`, …). Ambiguous queries get an automatic prior (`kaart` → maps/postcards/GPUs by phrase); `resolvedCategory` in the response shows the choice. Pass `category` to override |
| `type` | `auto` (default), `neural` (semantic), `keyword` |
| `price_min` / `price_max` | euros |
| `no_price` | `0` hides listings without a price |
| `limit` | default 24; max 100 (`keyword`) or 50 (`neural`/`auto`) |

### Other endpoints

- `GET /v1/similar?url=<listing-url>&limit=12` — visually/semantically
  similar listings; url must be a listing already in the index.
- `POST /v1/agent` — the website agent as an API: JSON body
  `{"message": "...", "conversation": [...], "source": "..."}`,
  streams the answer as Server-Sent Events (multi-step: it runs its own
  searches). Limits (Gratis): 10/min + 10/day per key — higher tiers
  via Abonnement (/profiel#abonnement).
- `GET /v1/contents?urls=<url1,url2,...>` — full details per listing URL
  (max 20 urls). Use after search when the user wants depth.
- `GET /v1/stats` — per-source listing counts; good connectivity check.
- MCP (Claude/Cursor/ChatGPT): hosted endpoint `https://koopje.ai/mcp`
  (Streamable HTTP, JSON-RPC 2.0) with your Bearer key — tools
  `search_listings`, `find_similar`, `get_listing`, `corpus_stats`,
  `list_reminders`, `create_reminder`, `update_reminder`,
  `delete_reminder`, same params and limits as above. The reminder tools
  require a key (they appear in the MCP tool list only when the key is
  sent) and manage the user's herinneringen (watchlist alerts).
  `search_listings` also returns a `price_context` block (n, median,
  p25, p75 over comparable asking prices — quote it as asking prices of
  similar ads, never as an appraised market value). Full setup:
  https://koopje.ai/api#mcp.
- Herinneringen (watchlist alerts; need the user's key):
  `GET /v1/alerts` (newest first), `POST /v1/alerts` with `query_text`
  (free-form description, max 400 chars) or `listing_id`, plus optional
  `price_max` and `frequency` (`daily`/`weekly`, default weekly);
  `POST /v1/alerts/update` with `{id, query_text?, frequency?, paused?}`;
  `POST /v1/alerts/remove` with `{id}`. Creation is idempotent per
  description/listing and capped at 3/hour per account. These send
  recurring email — only create one when the user explicitly asks.
- Saved listings (need the user's key; login-gated like everything else):
  `GET /v1/saved` (newest first), `POST /v1/saved` with
  `{"url": ..., "title": ..., "price_value": ..., "price_text": ...,
  "thumbnail_url": ..., "source": ..., "location": ...}` (idempotent),
  `POST /v1/saved/remove` with `{"url": ...}`.
- Own listings (need the user's key): `POST /v1/listings` with
  `{title, location, own: true}` plus `description, price_value,
  category, source_url, images[]` (base64, max 5) → `{id, url}`;
  `POST /v1/listings/fetch-url` to prefill from an ad link;
  `POST /v1/listings/draft` with `{url, own: true}` for an unindexed
  draft → `POST /v1/listings/publish` with `{id, ...overrides}`;
  `GET /v1/listings/mine`, `POST /v1/listings/remove|renew`.
  Full fields in `references/api.md`.

## Safety

This skill is **read-only by default**. The saved-listing and
herinnering endpoints change the user's account (a reminder sends
recurring email); call them **only** when the user explicitly asks for
that action, and ask for confirmation before creating or deleting a
reminder. The own-listing endpoints publish/remove public ads: ask for
confirmation before `POST /v1/listings/publish`,
`.../remove`, `.../renew` or `POST /v1/saved/remove`. Never publish,
renew or remove a listing on your own initiative.

## Reading results

`results[]` items carry: `url`, `title`, `description` (short snippet),
`price_value` + `price_text` (null when bidding/no price), `location`
(city), `source` (actual origin: `2dehands`, `trader`, `troc`,
`thinktwice`, `strieppromo`, `marktplaats`, `zoekertjes`, `user` (own ads at `koopje.ai/<category>/…`), a car-dealer domain (`autoscout24.be`,
`gocar.be`, …), or an auction-house slug — `alleveilingen`,
`vavato`, `troostwijk`, `auctelia`, `belga-veilingen`, `vlavem`, `auctionport`,
`openbare-verkopen`, `bopa`, `hammertime`, `veilbalie`, `komerco`,
`lussis`, `bell-auction`, `industrial-auctions`, `appelboom`, `auctim`), `listing_type`
(`tweedehands` or `veiling`), `thumbnail_url`, `_score` (similarity).

Always follow the user's language and locale; use Dutch when the user
writes in Dutch (or asks for it). Always include price, location and the
actual source: name the site or auction house
explicitly (2dehands, Troc.com, Marktplaats.nl, or for auctions the
auction house from `seller_name` — e.g. Vavato, Troostwijk,
Belga-Veilingen); link the `url`. Auction items
(`source: "veiling"`) have no fixed price — say so instead of quoting
`price_text` as a sale price.

## Pitfalls

- `limit` caps at 100 (`keyword`) or 50 (`neural`/`auto`) — page with `offset` while `hasMore` is true.
- `source` is a bucket alias (`2dehands` = all tweedehands, `veiling` = all auctions, `kringloop`/`troc`/`thinktwice` = thrift stores); the fine-grained site is
  only visible per-result in the `source` field of the response.
- 401 → key missing/revoked; 429 → rate limited (Gratis:
  search/similar/contents/stats: 60/min + 100/day per key; agent:
  10/min + 10/day — higher tiers via Plannen), back off and retry
  once. Other failures (400/403/404/500) come
  as `{"error": "..."}` — report the message, don't guess.
- Agent docs: `GET https://koopje.ai/llms.txt` lists every agent-readable
  page; `Accept: text/markdown` on `/`, `/docs`, `/api`, `/koppelen`
  returns Markdown instead of HTML. n8n users: ready-made agent template
  at https://koopje.ai/koppelen (n8n tab).
- Empty `results` ≠ error: rephrase the query broader (Dutch nouns help)
  before giving up.
- Never invent listings; only report what the API returned.

## Verification

`GET /v1/stats` returns `{"total": ..., "2dehands": ..., "veiling": ...}`
— if that fails, the key or connectivity is broken; tell the user instead
of guessing.
