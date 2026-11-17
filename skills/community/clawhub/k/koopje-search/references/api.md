# koopje.ai /v1 API reference

Base: `https://koopje.ai` — all requests need `Authorization: Bearer kk_...`.
All responses JSON; `/v1/*` sends `Access-Control-Allow-Origin: *`.

Errors: 401 missing/invalid key · 401 revoked key · 400 invalid params ·
429 rate limited.

## GET /v1/search

Semantic + keyword search over the unified index.

| param | type | required | description |
|---|---|---|---|
| `q` | string | yes | natural language or keywords (Dutch works best) |
| `type` | string | no | `auto` (default) · `neural` · `keyword` |
| `source` | string | no | exact origin: `2dehands` (2dehands.be platform incl. traders) · `troc` · `thinktwice` (Think Twice vintage) · `marktplaats` · `zoekertjes` · `kringwinkel` (thrift webshop + veilingsite, split by `listing_type`) · car-dealer domain (`autoscout24.be`, `gocar.be`, `mazdastock.be`, `vroom.be`, `autohero.com`, `irisautocenter.be`, `autocadre.com`) · auction house slug (`vavato`, `troostwijk`, `auctelia`, `belga-veilingen`, `vlavem`, `auctionport`, `openbare-verkopen`, `bopa`, `hammertime`, `veilbalie`, `komerco`, `lussis`, `bell-auction`, `industrial-auctions`, `appelboom`, `auctim`) · legacy bucket aliases: `2dehands`/`trader` → all tweedehands, `veiling` → all auctions |
| `listing_type` | string | no | `tweedehands` (all second-hand) · `veiling` (all auction lots, every auction house) · `kringloop` (thrift stores) — repeatable for multiselect |
| `category` | string | no | one of the 27 slugs (`computers`, `fietsen`, `boeken`, `verzamelen`, …). For ambiguous queries (`kaart`, `bank`, …) the server applies a category prior automatically; `resolvedCategory` / `resolvedCategorySource` in the response show whether it was `user` or `auto`. Pass `category` to override |
| `price_min` | number | no | minimum price in euro |
| `price_max` | number | no | maximum price in euro |
| `no_price` | bool | no | `0` hides listings without a price (default `1` shows them) |
| `limit` | number | no | default 24; max 100 (`keyword`) or 50 (`neural`/`auto`) |
| `offset` | number | no | skip N results ("toon meer" pagination) |
| `postcode` | string | no | 4-digit Belgian postcode ("2000") — anchors distance and annotates `_distance_km`; add `max_km` to actually filter. A postcode alone does **not** limit the radius |
| `lat` / `lng` | number | no | raw user coordinates (alternative to `postcode`). Privacy: these are sent to koopje.ai — prefer `postcode` when that is precise enough, and only send coordinates the user shared for distance filtering |
| `max_km` | number | no | radius in km around the user location (omit = no limit). Listings without any locatable city/coords are excluded when a location filter is active |

Location privacy: `postcode` / `lat` / `lng` / `max_km` leave the machine
and are sent to koopje.ai to filter by distance. Prefer a postcode; do
not send precise coordinates unless the user asked for distance
filtering.

`hasMore` is exact (server gathers limit+1 survivors past availability /
title-dedup filters) — page with `offset` while it is true.

Response:

```json
{
  "requestId": "…",
  "resolvedSearchType": "auto",
  "hasMore": true,
  "results": [
    {
      "url": "https://www.2dehands.be/v/…",
      "title": "…",
      "description": "short snippet",
      "price_value": 60.0,
      "price_text": "60 EUR",
      "location": "Borgerhout",
      "source": "2dehands",
      "thumbnail_url": "…",
      "_score": 0.83
    }
  ]
}
```

`source` values in results: `2dehands` (private sellers on 2dehands.be),
`trader` (professional occasion sellers on 2dehands.be), `troc` (Troc.com
store inventory), `thinktwice` (Think Twice vintage webshop), `strieppromo` (De Striep Promo second-hand strips), `marktplaats` (Belgian listings on Marktplaats.nl),
`zoekertjes` (Zoekertjes.be free classifieds), and auction-house slugs for
auction lots (`vavato`, `troostwijk`, `auctelia`, `belga-veilingen`,
`vlavem`, `auctionport`, `openbare-verkopen`, `bopa`, `hammertime`,
`veilbalie`, `komerco`, `lussis`, `bell-auction`, `industrial-auctions`,
`appelboom`, `auctim`; `alleveilingen` when the house is unknown), and car-dealer
domains for Belgian cars (`autoscout24.be`, `gocar.be`, `mazdastock.be`,
`vroom.be`, `autohero.com`, `irisautocenter.be`, `autocadre.com`). Every result also
carries `listing_type`: `veiling` for auction lots, `kringloop` for
thrift stores, `tweedehands` for everything else. Auction lots have no fixed price.

Each result also carries `_price_kind` (`fixed`, `bid`, `auction`,
`free`, `none`) and `category_slug`: the site's fine-grained
`category`/`subcategory` names mapped onto one of 27 canonical Dutch
facets (`fietsen`, `autos`, …, `overig` when unmappable) — use the facet
for grouping/filtering, the originals for detail. Chat answers show it as
`Categorie: <original> [<facet>]`. When a location filter was given — `_distance_km`
(+ `_distance_approx` when derived from a city centroid). The envelope
echoes `userLocation` (`label`, `lat`, `lng`, `maxKm`, `approx`) and
`distance` (`maxKm`, `hidden`: rows dropped for lack of location).

## GET /v1/similar

| param | type | required | description |
|---|---|---|---|
| `url` | string | yes | URL of a listing in the index (2dehands, troc, thinktwice, strieppromo, marktplaats, zoekertjes, kringwinkel, veiling urls work) |
| `limit` | number | no | default 24; keyword max 100, neural/auto max 50 |

Same response shape as search.

If the seed URL is gone (sold/delisted), `similar` falls back to live
lookalikes derived from the URL slug instead of a bare 404: the response
carries `"seed_gone": true` alongside `results`. Only a hintless/empty
fallback still 404s (`{"error": "listing not found"}`).

## GET /v1/contents

| param | type | required | description |
|---|---|---|---|
| `urls` | string | yes | comma-separated listing URLs, max 20 |
| `similar` | int | no | attach N similar listings per result (max 12, default 0) |

Full listing details (description, attributes, seller, images) for the
given URLs — use to deepen search results before reporting.

## POST /v1/agent

The website agent as an API (streaming Server-Sent Events — read until
connection close). JSON body:

| param | type | required | description |
|---|---|---|---|
| `message` | string | yes | the question in natural language |
| `conversation` | array | no | earlier [{role, content}] messages for follow-ups |
| `source` | string | no | source filter, same values as search |

Limits (Gratis): 10/min + 10/day per key — higher tiers via Plannen.
Use for multi-step tasks (it runs its
own searches); use `/v1/search` + `/v1/contents` for single questions.

## GET /v1/stats

No parameters. Returns `{"total": N, "2dehands": N, "veiling": N,
"trader": N, "troc": N, "thinktwice": N, "strieppromo": N, "marktplaats": N, "zoekertjes": N, "kringwinkel": N}` — per-source listing counts.

## Saved listings (login-gated)

- `GET /v1/saved` → `{"saved": [{url, title, price_value, price_text,
  thumbnail_url, source, location, saved_at}]}` newest first.
- `POST /v1/saved` with `{"url": ...}` plus the snapshot fields above
  (idempotent upsert — re-saving refreshes the snapshot).
- `POST /v1/saved/remove` with `{"url": ...}`.

## Herinneringen (login-gated)

A herinnering is a recurring email with new listings that match a
description (the watchlist feature on the site).

- `GET /v1/alerts` → `{"alerts": [{id, seed_title, seed_price,
  category, created_at, query_text, confirmed_at, confirm_expires,
  paused, frequency}]}` newest first.
- `POST /v1/alerts` with `{"query_text": "...", "price_max": 300,
  "frequency": "weekly"}` for a free-form reminder, or
  `{"listing_id": "...", "query_text": "...", "frequency": "daily"}`
  to seed from an existing listing. `query_text` is required without a
  listing and max 400 chars; idempotent per description/listing;
  max 3/hour per account.
- `POST /v1/alerts/update` with `{"id": 12}` plus one or more of
  `query_text`, `frequency` (`daily`/`weekly`) and `paused` (boolean).
- `POST /v1/alerts/remove` with `{"id": 12}`.

## Own listings (login-gated, own ads only)

Users can publish their own ads (link import or from scratch); rows
carry `source: "user"`, live at `https://koopje.ai/<category>/<slug>-<id>`, expire
after 30 days (renewable). They appear in search like any row.

- `POST /v1/listings/fetch-url` with `{"url": ...}` (known ad platform)
  → `{title, description, price_value?, images?}` prefill, writes nothing.
- `POST /v1/listings` with `{title, location, own: true}` plus
  `description, price_value, price_text, category, source_url,
  origin ("manual"|"link"), images[]` (base64 data URLs, max 5, 5MB each)
  → `{ok, id, url, expires_at}`. `own: true` (ownership declaration)
  is required. Max 10 active listings per account.
- `GET /v1/listings/mine` → `{"listings": [...]}` newest first.
- `POST /v1/listings/remove` / `POST /v1/listings/renew` with `{"id": ...}`.
- `POST /v1/listings/draft` with `{url, own: true}` reads an ad link
  into an unindexed, non-public draft → `{ok, id, draft: true, ...}`.
- `POST /v1/listings/publish` with `{id}` plus optional field
  overrides (title, description, price_value, price_text, location,
  category, images[]) validates, indexes and publishes at
  `https://koopje.ai/<category>/<slug>-<id>`, 30 days. (`/l/<id>` redirects there.)

## Getting a key

Log in at koopje.ai → menu (top right) → *API keys* → create. Keys
are `kk_` + 32 chars and shown exactly once. Store as `KOOPJE_API_KEY`.
