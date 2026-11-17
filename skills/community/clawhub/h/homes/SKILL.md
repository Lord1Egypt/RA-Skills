---
name: homes
description: Look up real-estate listings, property details, price/tax history, market reports, saved homes, and photo galleries on homes.com via MCP. Triggers on phrases like "find homes on homes.com in", "homes.com property details for", "what does homes.com say about", "homes.com price history for", or any request involving homes.com properties, prices, history, or photos. Requires homes-mcp installed and the ContextMint Bridge extension active (see Setup below).
---

# homes-mcp

MCP server for homes.com — natural-language access to listings, property records, price/tax history, market reports, saved homes/searches, and photo galleries. Routes through your signed-in homes.com tab via the ContextMint Bridge browser extension, so AWS WAF sees a real browser session instead of a Node process.

- **npm:** [npmjs.com/package/homes-mcp](https://www.npmjs.com/package/homes-mcp)
- **Source:** [github.com/chrischall/homes-mcp](https://github.com/chrischall/homes-mcp)

> ⚠️ homes.com does not publish a public consumer API. This server reads the Schema.org JSON-LD blob (and some DOM-side sections) embedded in each SSR page, dispatched through your own signed-in browser tab via the ContextMint Bridge extension. Use at your own discretion.

## Setup

### 1. Install homes-mcp

`.mcp.json` (project) or `~/.claude/mcp.json` (global):

```json
{
  "mcpServers": {
    "homes": {
      "command": "npx",
      "args": ["-y", "homes-mcp"]
    }
  }
}
```

### 2. Install the ContextMint Bridge extension (one-time, shared across all fetchproxy-based MCPs)

The extension is installed separately — it is **not** bundled in this repo. Get it from the [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases):

- **Chrome:** unzip the Chrome zip, then `chrome://extensions` → Developer mode → Load unpacked.
- **Safari:** not available yet (it will ship inside the ContextMint app, which has no public download) — use Chrome for now.

ContextMint Bridge is the renamed fetchproxy extension from the same maintainer ([fetchproxy's README](https://github.com/chrischall/fetchproxy#extension) points to it); its source is public, so build it yourself or verify a release zip with `shasum -a 256 -c <zip>.sha256`.

### 3. Open homes.com and sign in.

That's it. No API keys, no env vars. (Sign-in isn't strictly required for the public-listing tools, but having a real session active helps the page render the way the extractors expect — and saved-homes / saved-searches require it.)

## Tools

Five of these take an optional `view` and answer on the **compact** rung when
you omit it — see [Response shape](#response-shape-view).

### Search & resolve

- **`homes_search_properties`** — Search by free-text location (city, ZIP, neighborhood). Slugifies the input into homes.com's URL routing. Filters by `property_type`, `listing_type`, `sort`, and a `price_min`/`price_max` band (homes.com's `?price-min=`/`?price-max=` query facet). Returns each listing's address, price, beds/baths, sqft, listing agent + brokerage — and, on `view: "full"`, `primary_photo_url` (the default compact rung strips it; see [Response shape](#response-shape-view)). Caps at the ~40-listing SSR page; sets `truncated`/`total_estimated` when the market has more.
- **`homes_get_by_address`** — Resolve a single US street address to its canonical homes.com property URL + opaque property hash. Walks structured smartsearch typeahead → slug routing → city/zip search-fallback, verifying each candidate with a whole-token street + unit match. Returns `matched_via` and degrades gracefully to `{ resolved: false }`.
- **`homes_resolve_addresses`** — Bulk version of `homes_get_by_address` (up to 100 addresses, input order preserved, per-row outcomes). Prefer for any batch ≥ 3.

### Property details

- **`homes_get_property`** — Full record for a property by URL. Parses JSON-LD + DOM-side sections: address, lat/lng, beds/baths, sqft, year built, price, status, listing agent + brokerage, highlights, schools, HOA (raw + normalized monthly), lot size (sqft + derived acres), parking, heating/cooling, MLS id/source, tax, days-on-market, price drops, and server-derived `extracted_features`. Optional inline `price_history` / `tax_history`.
- **`homes_get_property_photos`** — Full photo gallery scraped from `<img>` tags on the detail page (JSON-LD carries only one image). Returns `{ url, position, alt? }` per photo, filtered to the homes.com CDN.
- **`homes_bulk_get`** — Fetch up to 200 properties' structured records in one call (per-row errors captured, input order preserved). Use instead of looping when you just want the records.
- **`homes_compare_properties`** — Side-by-side comparison of 2–8 properties with an aligned summary table. Concurrent fetches, per-row errors.
- **`homes_get_nearby_listings`** — The "Homes for Sale Near This Property" cross-link cards from a detail page (For Sale, optionally Rentals). URL + address only.

### History & market

- **`homes_get_history`** — Combined price + tax history in one fetch: `listing_events`, `ownership_events`, `lien_events`, cross-MCP-normalized `events_normalized`, and `tax_records`. (Preferred over the two split tools below.)
- **`homes_get_property_history`** — *Deprecated* — price/ownership/lien timelines only. Prefer `homes_get_history`.
- **`homes_get_tax_history`** — *Deprecated* — year-by-year tax records only. Prefer `homes_get_history`.
- **`homes_get_market_report`** — Median / average / $-per-sqft for a market, derived from the `sold` search page's JSON-LD.

### Saved (auth-gated)

- **`homes_get_saved_homes`** — The signed-in user's saved (favorited) homes. Requires an authenticated homes.com tab.
- **`homes_get_saved_searches`** — The signed-in user's saved searches. Requires an authenticated homes.com tab.

### Local calculators (no network)

- **`homes_calculate_mortgage`** — Local PITI calculator (price, rate, down payment, taxes, insurance, HOA, PMI → monthly breakdown).
- **`homes_calculate_affordability`** — Local affordability calculator — max purchase price under standard 28/36 DTI.
- **`homes_estimate_rent_vs_buy`** — Local rent-vs-buy model. **You must supply `monthly_rent`** — homes.com publishes no rental estimate to impute it (see Gotchas).

### Diagnostics & sessions

- **`homes_healthcheck`** — Round-trips `/robots.txt` through the fetchproxy bridge; distinguishes "bridge down" vs "extension not connected / pair code pending" (`bridge.session_state`, `error.kind: session_not_ready`) vs "homes.com-side problem."
- **`homes_get_session_context`**, **`homes_register_session`**, **`homes_set_active_session`** — List / register / switch account *labels* for your own bookkeeping. Label only: switching does not change which account requests use; they always go through whichever account the fetchproxy browser tab is signed into.

## Response shape (`view`)

Five tools take `view: "compact" | "full"`, and **`compact` is the default** —
you get the slim shape without asking for it: `homes_search_properties`,
`homes_get_property`, `homes_bulk_get`, `homes_compare_properties`,
`homes_get_market_report`.

**Compact here is media stripping, not a field projection — do not expect a
field list.** It removes image URLs and nothing else. These tools hand back
what the page's JSON-LD said, close to verbatim, and this repo holds no
verified record of which of homes.com's fields matter, so it does not claim to
keep some and drop others: a listing that came back with holes in it would read
exactly like a verified answer. Stripping is subtractive, so it cannot lose a
field nobody knew about. Everything you act on survives — `property_id`, `url`,
`price`, beds/baths/sqft, agent, `matterport_url` (a link to a PAGE you can
open, not an image), the whole `description` byte-for-byte.

**The two fields this actually costs you, both minted by this server:**

- **`primary_photo_url`** — built by the formatter, not a homes.com field. It
  is gone by default on all five, including every row of a `homes_bulk_get` or
  `homes_compare_properties` fan-out and every entry of a market report's
  `sample_sold`.
- **`floorplan_urls`** — scraped out of the detail page's own `<img>` tags by
  `homes_get_property`. Worth knowing that this one is dropped by NAME: it
  holds an ARRAY, and the fleet's URL rule is tested against object values and
  never against array elements, so before the key was named it was not
  "sometimes kept" — it was never stripped at all.

Pass `view: "full"` to get both back, with homes.com's payload otherwise
untouched. There is deliberately **no `raw` rung**: nothing normalises the
payload beyond the formatting these tools already do, so `full` already IS the
untouched result and a third value would silently alias it.

**`homes_get_property_photos` takes no `view`, and that is the important
exclusion.** Its PRODUCT is the image. Compact there would not shrink the
response, it would EMPTY it — `photos` is itself a media key, so the whole
array vanishes while `count: 12` goes on claiming twelve. Never ask for a
compact rung there and never expect one; the tool is tested to keep its URLs
even if a stray `view` is passed.

The other fifteen tools take no `view` because there is nothing in their output
to strip:

- `homes_get_saved_homes` / `homes_get_saved_searches` are card scrapes —
  `{ property_id, url, address, price, beds, baths, sqft, status }` and
  `{ name, url, filters }`, no images.
- `homes_get_nearby_listings` returns URL + address only.
- `homes_get_history`, `homes_get_property_history` and `homes_get_tax_history`
  return event and tax rows.
- `homes_get_by_address` and `homes_resolve_addresses` return a URL and a
  verdict.
- `homes_calculate_mortgage`, `homes_calculate_affordability` and
  `homes_estimate_rent_vs_buy` are local arithmetic — no network, no payload.
- `homes_healthcheck` and the three session tools return status.

Passing `view` to any of them is not an error and not a warning: MCP tool
schemas are non-strict, so the key is dropped and you get that tool's ordinary
output.

## Trigger examples

- "Find me condos for sale in Atlanta under $500k on homes.com" → `homes_search_properties` (with `price_max`)
- "Resolve 3199 Delmar Ln NW, Atlanta GA to a homes.com listing" → `homes_get_by_address`
- "What's the price history for this homes.com listing?" → `homes_get_history` (or `homes_get_property` with `include_price_history`)
- "Show me all photos for this homes.com listing" → `homes_get_property_photos`
- "What's the market report for sold homes in Brooklyn?" → `homes_get_market_report`
- "List my saved homes on homes.com" → `homes_get_saved_homes`
- "Monthly payment on a $500k home, 20% down, 6.5% rate" → `homes_calculate_mortgage`

## In context groups

homes-mcp joins the **home** group (`_meta.mint.domain: "home"`). It has
**no canonical read**: homes.com serves listings, price/tax history, market
reports and the signed-in user's saved homes and searches, none of which is a
dated feed that answers "what's new / due / on", and it has no listable
subjects (children, properties you own, accounts) to name. So the group never
asks homes for a what's-new/due/on answer; every read is a `lookup`, and the
local calculators and session-label writes are `other`.

A compound ask reaches homes only for the lookup part — "is the pool heater on,
and what are 3-bed homes going for in Decatur?" → the home group answers the
pool from its own canonical source and routes the second half to
`homes_search_properties` or `homes_get_market_report`.

homes-mcp is browser-bridged: when no signed-in homes.com tab is attached to
the ContextMint Bridge, the group answers "homes.com needs your browser open"
rather than an empty result.

## Gotchas

- **AWS WAF challenge.** homes.com (CoStar) gates traffic through AWS WAF and occasionally serves a challenge page to fresh sessions. Solving it in the Chrome tab once unblocks subsequent fetches; the client detects the interstitial and throws `SessionNotAuthenticatedError`.
- **No write surface.** All tools are read-only. Saving a home / contact forms are not implemented.
- **Property URL is required for detail tools.** `get_property`, `get_property_photos`, `compare_properties`, history, photos, and nearby all need a full property URL from a search or `get_by_address` result — there's no stable way to construct one from a property id alone.
- **No rental estimate to impute.** homes.com publishes no `rent_zestimate` analogue, so `homes_estimate_rent_vs_buy` requires you to pass `monthly_rent`. For a rent figure to plug in, use a sibling MCP (`zillow_get_property` carries `rent_zestimate`; `redfin_get_comparable_rentals` returns rental comps).
