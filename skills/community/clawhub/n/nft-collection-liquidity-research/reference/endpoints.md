# nft-collection-liquidity-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**11 endpoints across 1 platform group(s).**

## OpenSea (11)

### `opensea_categories`

- **HTTP:** `GET /opensea/categories`
- **What:** List OpenSea's browse categories. Returns OpenSea's category taxonomy as top-level groups and their child categories, with display names. The child slugs are the canonical category identifiers used across the marketplace.
- **Params:** _none_

### `opensea_chains`

- **HTTP:** `GET /opensea/chains`
- **What:** List the chains OpenSea indexes. Returns every blockchain OpenSea indexes, with its identifier, display name, and architecture. The identifiers are the accepted values for the `chain` path parameter on the item endpoints.
- **Params:** _none_

### `opensea_collection`

- **HTTP:** `GET /opensea/collection/{slug}`
- **What:** Get an OpenSea collection. Returns public marketplace metadata and trading statistics for one NFT collection: name, description, imagery, verification flag, contract address and chain, social links, current floor price and top collection offer, plus lifetime and rolling one-hour/one-day/seven-day/thirty-day sales, volume, and floor-price change. Delisted and blacklisted collections return 404 rather than an empty payload.
- **Params:** `slug` (string, **required**) — OpenSea collection slug

### `opensea_collection_activity`

- **HTTP:** `GET /opensea/collection/{slug}/activity`
- **What:** List an OpenSea collection's marketplace activity. Returns a cursor-paginated feed of marketplace events for a collection — sales, listings, offers, transfers, mints, and collection/trait offers — with the counterparties, price, marketplace, and transaction hash. Filter with `event_types` to narrow the feed, for example `event_types=SALE` for a sales-only history.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `event_types` (string, optional) — Comma-separated event types; `limit` (integer, optional) — Events per page, 1-100; `slug` (string, **required**) — OpenSea collection slug

### `opensea_collection_chart`

- **HTTP:** `GET /opensea/collection/{slug}/chart`
- **What:** Get an OpenSea collection's price or volume history. Returns a time series for a collection — either its floor price or its traded volume — over the requested window, with each sample in both the settlement token and USD. Use `metric=floor_price` for the floor line and `metric=volume` for the volume bars.
- **Params:** `metric` (string, optional) — Series to return; `slug` (string, **required**) — OpenSea collection slug; `timeframe` (string, optional) — Window

### `opensea_collection_depth`

- **HTTP:** `GET /opensea/collection/{slug}/depth`
- **What:** Get an OpenSea collection's order book. Returns the full bid/ask ladder for a collection: resting listings and offers grouped into price levels with the quantity available at each. This is the depth chart behind OpenSea's own collection page, and it is the fastest way to see how thin or deep the book is above the floor.
- **Params:** `slug` (string, **required**) — OpenSea collection slug

### `opensea_collection_holders`

- **HTTP:** `GET /opensea/collection/{slug}/holders`
- **What:** List an OpenSea collection's holders. Returns a cursor-paginated leaderboard of wallets holding items in the collection, ranked by quantity held, with each holder's address and display name where OpenSea publishes one.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `limit` (integer, optional) — Holders per page, 1-100; `slug` (string, **required**) — OpenSea collection slug; `sort_direction` (string, optional) — Sort direction by quantity held

### `opensea_collection_offers`

- **HTTP:** `GET /opensea/collection/{slug}/offers`
- **What:** List an OpenSea collection's offer book. Returns the collection-wide offer book as price levels: how many standing offers sit at each price per item, plus the aggregate offer count and total value across the whole collection. Offers are sorted by price.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `limit` (integer, optional) — Price levels per page, 1-100; `slug` (string, **required**) — OpenSea collection slug; `sort_direction` (string, optional) — Sort direction by offer price

### `opensea_collection_top_sales`

- **HTTP:** `GET /opensea/collection/{slug}/top-sales`
- **What:** List an OpenSea collection's highest-value sales. Returns the highest-value sales ever recorded for a collection, with the buyer, seller, price, and transaction hash for each. Unlike `/opensea/collection/{slug}/activity?event_types=SALE`, which is a reverse-chronological feed, this is ranked by sale price.
- **Params:** `slug` (string, **required**) — OpenSea collection slug

### `opensea_collection_traits`

- **HTTP:** `GET /opensea/collection/{slug}/traits`
- **What:** List an OpenSea collection's traits. Returns a cursor-paginated page of the collection's trait types and the values each takes, with per-value item counts where OpenSea publishes them. Numeric traits carry a comparison operator.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `limit` (integer, optional) — Trait types per page, 1-100; `slug` (string, **required**) — OpenSea collection slug

### `opensea_search_collections`

- **HTTP:** `GET /opensea/search/collections`
- **What:** Search OpenSea collections by keyword. Runs a keyword search across OpenSea collections and returns the matches with floor price, verification flag, and headline stats. Use this to resolve a human-readable name to the `slug` the other collection endpoints take.
- **Params:** `limit` (integer, optional) — Results per page, 1-100; `query` (string, **required**) — Search keyword
