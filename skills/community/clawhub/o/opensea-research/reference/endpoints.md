# opensea-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**36 endpoints across 1 platform group(s).**

## OpenSea (36)

### `opensea_activity`

- **HTTP:** `GET /opensea/activity`
- **What:** List marketplace-wide OpenSea activity. Returns the live cross-collection activity feed — every sale, listing, offer, transfer, and mint OpenSea indexes, newest first, with the collection each event belongs to. Filter with `event_types` for a marketplace-wide trade tape.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `event_types` (string, optional) — Comma-separated event types; `limit` (integer, optional) — Events per page, 1-100

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

### `opensea_collection_best_deals`

- **HTTP:** `GET /opensea/collection/{slug}/best-deals`
- **What:** List an OpenSea collection's best-value listings. Returns the listed items OpenSea surfaces as the best value in a collection, judged against each item's rarity and the collection floor. This is the curated "best deals" shelf from the collection page, not a generic price sort.
- **Params:** `slug` (string, **required**) — OpenSea collection slug

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

### `opensea_collection_items`

- **HTTP:** `GET /opensea/collection/{slug}/items`
- **What:** List items in an OpenSea collection. Returns a cursor-paginated page of NFTs in a collection with their traits, rarity rank, current owner, best standing listing, and last sale price. Pass `cursor` from `next_page_cursor` to page forward. Narrow the result set with `listed_only`, `traits`, a `min_price`/`max_price` band, or a `min_rarity`/`max_rarity` rank band — the filters combine, so `traits=Fur:Solid Gold&listed_only=true` returns only buyable Solid Gold apes.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `limit` (integer, optional) — Items per page, 1-100; `listed_only` (boolean, optional) — Only return items with a standing listing; `max_price` (number, optional) — Maximum listing price in the collection's native token; `max_rarity` (integer, optional) — Maximum rarity rank; `min_price` (number, optional) — Minimum listing price in the collection's native token; `min_rarity` (integer, optional) — Minimum rarity rank (1 is rarest); `slug` (string, **required**) — OpenSea collection slug; `sort_by` (string, optional) — Sort field; `sort_direction` (string, optional) — Sort direction; `traits` (string, optional) — Comma-separated trait_type:value pairs

### `opensea_collection_offers`

- **HTTP:** `GET /opensea/collection/{slug}/offers`
- **What:** List an OpenSea collection's offer book. Returns the collection-wide offer book as price levels: how many standing offers sit at each price per item, plus the aggregate offer count and total value across the whole collection. Offers are sorted by price.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `limit` (integer, optional) — Price levels per page, 1-100; `slug` (string, **required**) — OpenSea collection slug; `sort_direction` (string, optional) — Sort direction by offer price

### `opensea_collection_rarest_items`

- **HTTP:** `GET /opensea/collection/{slug}/rarest-items`
- **What:** List an OpenSea collection's rarest listed items. Returns the rarest items in a collection that currently have a standing listing, each with its rarity rank, traits, and asking price. Unlike the trait endpoints, this shelf is scoped to what is actually buyable right now.
- **Params:** `slug` (string, **required**) — OpenSea collection slug

### `opensea_collection_search_items`

- **HTTP:** `GET /opensea/collection/{slug}/search-items`
- **What:** Search items inside an OpenSea collection. Runs a keyword search scoped to one collection — matching on item name and trait values — and returns the hits with rarity rank and best standing listing. Narrower than `/opensea/collection/{slug}/items`, which lists everything.
- **Params:** `limit` (integer, optional) — Results per page, 1-100; `query` (string, **required**) — Search keyword; `slug` (string, **required**) — OpenSea collection slug

### `opensea_collection_social_proof`

- **HTTP:** `GET /opensea/collection/{slug}/social-proof`
- **What:** Get an OpenSea collection's social following. Returns how many accounts follow or watch a collection, plus the notable collectors OpenSea highlights for it. Useful as a demand signal alongside the trading stats.
- **Params:** `slug` (string, **required**) — OpenSea collection slug

### `opensea_collection_top_sales`

- **HTTP:** `GET /opensea/collection/{slug}/top-sales`
- **What:** List an OpenSea collection's highest-value sales. Returns the highest-value sales ever recorded for a collection, with the buyer, seller, price, and transaction hash for each. Unlike `/opensea/collection/{slug}/activity?event_types=SALE`, which is a reverse-chronological feed, this is ranked by sale price.
- **Params:** `slug` (string, **required**) — OpenSea collection slug

### `opensea_collection_trait_offers`

- **HTTP:** `GET /opensea/collection/{slug}/trait-offers`
- **What:** List an OpenSea collection's trait offer book. Returns standing offers scoped to a specific trait value rather than the whole collection, as price levels with the trait type and value attached. Useful for pricing rare-trait items against the collection floor.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `limit` (integer, optional) — Price levels per page, 1-100; `slug` (string, **required**) — OpenSea collection slug; `sort_direction` (string, optional) — Sort direction by offer price

### `opensea_collection_traits`

- **HTTP:** `GET /opensea/collection/{slug}/traits`
- **What:** List an OpenSea collection's traits. Returns a cursor-paginated page of the collection's trait types and the values each takes, with per-value item counts where OpenSea publishes them. Numeric traits carry a comparison operator.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `limit` (integer, optional) — Trait types per page, 1-100; `slug` (string, **required**) — OpenSea collection slug

### `opensea_collections`

- **HTTP:** `GET /opensea/collections`
- **What:** Look up several OpenSea collections at once. Resolves up to 50 collections in a single call from a comma-separated `slugs` list, returning each one's floor price, verification flag, headline stats, and per-marketplace listed-item counts. Use this instead of calling `/opensea/collection/{slug}` in a loop — it costs one upstream request regardless of how many slugs you pass. The `markets` array shows how many items are listed on OpenSea versus other marketplaces for the same collection.
- **Params:** `slugs` (string, **required**) — Comma-separated collection slugs, at most 50

### `opensea_drops`

- **HTTP:** `GET /opensea/drops`
- **What:** List the OpenSea drop calendar. Returns the NFT drop calendar — either upcoming mints or recently minted drops — with each drop's contract, chain, and parent collection. Use `type=UPCOMING` to watch for launches and `type=RECENTLY_MINTED` for ones that just went live.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `limit` (integer, optional) — Drops per page, 1-100; `type` (string, optional) — Calendar window

### `opensea_item`

- **HTTP:** `GET /opensea/item/{chain}/{contract_address}/{token_id}`
- **What:** Get a single OpenSea NFT. Returns one NFT addressed by chain, contract address, and token id, including its traits, rarity rank, current owner, parent collection, best standing listing, and best standing offer. Call `/opensea/chains` for the accepted `chain` values.
- **Params:** `chain` (string, **required**) — Chain identifier from /opensea/chains; `contract_address` (string, **required**) — NFT contract address; `token_id` (string, **required**) — Token id within the contract

### `opensea_item_activity`

- **HTTP:** `GET /opensea/item/{chain}/{contract_address}/{token_id}/activity`
- **What:** List one OpenSea NFT's event history. Returns the marketplace event history for a single NFT — sales, listings, offers, transfers, and mints — with counterparties, price, and transaction hash. Filter with `event_types`, for example `event_types=SALE,TRANSFER` for an ownership trail.
- **Params:** `chain` (string, **required**) — Chain identifier from /opensea/chains; `contract_address` (string, **required**) — NFT contract address; `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `event_types` (string, optional) — Comma-separated event types; `limit` (integer, optional) — Events per page, 1-100; `token_id` (string, **required**) — Token id within the contract

### `opensea_item_chart`

- **HTTP:** `GET /opensea/item/{chain}/{contract_address}/{token_id}/chart`
- **What:** Get an OpenSea NFT's sale-price history. Returns every indexed sale of one NFT with its timestamp and price, in both the settlement token and USD — the price history behind the chart on an item page. An item that has never sold returns an empty `points` list. For collection-level sale history use `/opensea/collection/{slug}/activity?event_types=SALE`.
- **Params:** `chain` (string, **required**) — Chain identifier from /opensea/chains; `contract_address` (string, **required**) — NFT contract address; `token_id` (string, **required**) — Token id within the contract

### `opensea_item_depth`

- **HTTP:** `GET /opensea/item/{chain}/{contract_address}/{token_id}/depth`
- **What:** Get an OpenSea NFT's order book. Returns the bid/ask ladder for a single NFT: resting listings and offers grouped into price levels with the quantity at each. Useful for ERC-1155 items where many units trade at different prices.
- **Params:** `chain` (string, **required**) — Chain identifier from /opensea/chains; `contract_address` (string, **required**) — NFT contract address; `token_id` (string, **required**) — Token id within the contract

### `opensea_item_listings`

- **HTTP:** `GET /opensea/item/{chain}/{contract_address}/{token_id}/listings`
- **What:** List standing listings for an OpenSea NFT. Returns every standing sell order for one NFT, with price, quantity, validity window, marketplace, and the maker's wallet. An item with no active listings returns an empty list rather than a 404.
- **Params:** `chain` (string, **required**) — Chain identifier from /opensea/chains; `contract_address` (string, **required**) — NFT contract address; `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `limit` (integer, optional) — Listings per page, 1-100; `sort_direction` (string, optional) — Sort direction by price; `token_id` (string, **required**) — Token id within the contract

### `opensea_item_offers`

- **HTTP:** `GET /opensea/item/{chain}/{contract_address}/{token_id}/offers`
- **What:** List standing offers for an OpenSea NFT. Returns every standing bid on one NFT, with price, quantity, validity window, marketplace, and the maker's wallet. An item with no active offers returns an empty list rather than a 404.
- **Params:** `chain` (string, **required**) — Chain identifier from /opensea/chains; `contract_address` (string, **required**) — NFT contract address; `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `limit` (integer, optional) — Offers per page, 1-100; `token_id` (string, **required**) — Token id within the contract

### `opensea_item_owners`

- **HTTP:** `GET /opensea/item/{chain}/{contract_address}/{token_id}/owners`
- **What:** List the owners of an OpenSea NFT. Returns the wallets holding one NFT plus the total owner count. ERC-721 items resolve to a single owner; ERC-1155 items can have many, each with the quantity held.
- **Params:** `chain` (string, **required**) — Chain identifier from /opensea/chains; `contract_address` (string, **required**) — NFT contract address; `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `limit` (integer, optional) — Owners per page, 1-100; `token_id` (string, **required**) — Token id within the contract

### `opensea_most_watched`

- **HTTP:** `GET /opensea/most-watched`
- **What:** List the most watchlisted OpenSea collections. Returns the collections most added to watchlists on OpenSea, with their current floor price and headline stats. A demand signal that leads trading volume, since watchlisting precedes buying.
- **Params:** `limit` (integer, optional) — Collections to return, 1-100

### `opensea_profile`

- **HTTP:** `GET /opensea/profile/{identifier}`
- **What:** Get a public OpenSea profile. Returns the public profile for a wallet, resolved from a wallet address, an ENS name, or an OpenSea username: display name, avatar and banner imagery, verification flag, and linked social handles. Wallet balances, portfolio value, and profit/loss are deliberately not exposed.
- **Params:** `identifier` (string, **required**) — Wallet address, ENS name, or OpenSea username

### `opensea_profile_activity`

- **HTTP:** `GET /opensea/profile/{identifier}/activity`
- **What:** List a wallet's NFT marketplace activity. Returns a cursor-paginated feed of a wallet's NFT marketplace events — sales, listings, offers, transfers, and mints — with the counterparty, price, and collection for each. Accepts a wallet address, ENS name, or OpenSea username. Scoped to NFT events only; token transfers and swaps are not returned.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `event_types` (string, optional) — Comma-separated event types; `identifier` (string, **required**) — Wallet address, ENS name, or OpenSea username; `limit` (integer, optional) — Events per page, 1-100

### `opensea_profile_collections`

- **HTTP:** `GET /opensea/profile/{identifier}/collections`
- **What:** List the collections a wallet holds. Returns the collections a wallet holds items in, with how many items it holds in each and that collection's current floor price. Useful for valuing a wallet's holdings collection by collection.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `identifier` (string, **required**) — Wallet address, ENS name, or OpenSea username; `limit` (integer, optional) — Collections per page, 1-100

### `opensea_profile_created`

- **HTTP:** `GET /opensea/profile/{identifier}/created`
- **What:** List the collections a wallet created. Returns the collections a wallet created, as opposed to the ones it holds, each with its floor price and trading statistics. Use this to find a creator's full body of work from any one of their collections' contract deployer address.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `identifier` (string, **required**) — Wallet address, ENS name, or OpenSea username; `limit` (integer, optional) — Collections per page, 1-100; `sort_by` (string, optional) — Sort field; `sort_direction` (string, optional) — Sort direction

### `opensea_profile_items`

- **HTTP:** `GET /opensea/profile/{identifier}/items`
- **What:** List the NFTs a wallet holds. Returns a cursor-paginated page of the NFTs held by a wallet, with each item's collection, rarity rank, and best standing listing. Accepts a wallet address, ENS name, or OpenSea username; a non-address identifier costs one extra resolution lookup.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `identifier` (string, **required**) — Wallet address, ENS name, or OpenSea username; `limit` (integer, optional) — Items per page, 1-100; `sort_direction` (string, optional) — Sort direction by received date

### `opensea_profile_search_items`

- **HTTP:** `GET /opensea/profile/{identifier}/search-items`
- **What:** Search the NFTs a wallet holds. Runs a keyword search across a wallet's holdings, matching on item and collection name, and returns the hits with rarity rank and best standing listing. Narrower than `/opensea/profile/{identifier}/items`, which lists everything the wallet holds.
- **Params:** `identifier` (string, **required**) — Wallet address, ENS name, or OpenSea username; `limit` (integer, optional) — Results per page, 1-100; `query` (string, **required**) — Search keyword

### `opensea_rankings`

- **HTTP:** `GET /opensea/rankings`
- **What:** List ranked OpenSea collections. Returns the collections on one of OpenSea's ranking boards for a given window, each with its ranking score, floor price, and rolling stats. `TRENDING` ranks by recent momentum, `TOP` by absolute volume, and `NEW` surfaces recently launched collections.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous next_page_cursor; `limit` (integer, optional) — Collections per page, 1-100; `ranking` (string, optional) — Ranking board; `timeframe` (string, optional) — Ranking window

### `opensea_search_collections`

- **HTTP:** `GET /opensea/search/collections`
- **What:** Search OpenSea collections by keyword. Runs a keyword search across OpenSea collections and returns the matches with floor price, verification flag, and headline stats. Use this to resolve a human-readable name to the `slug` the other collection endpoints take.
- **Params:** `limit` (integer, optional) — Results per page, 1-100; `query` (string, **required**) — Search keyword

### `opensea_top_movers`

- **HTTP:** `GET /opensea/top-movers`
- **What:** List the biggest movers on OpenSea. Returns the collections with the largest recent floor-price and volume moves, each with its current floor and rolling one-hour and one-day stats. Complements `/opensea/rankings`, which ranks by score rather than by change.
- **Params:** `limit` (integer, optional) — Collections to return, 1-100
