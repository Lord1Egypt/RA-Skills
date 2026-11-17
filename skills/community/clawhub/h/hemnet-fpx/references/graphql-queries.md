# Hemnet GraphQL queries for fpx

Ready-to-run bodies for `fpx post-json 'https://www.hemnet.se/graphql' @file -p hemnet`.
Each block is the full POST body (`{"query","variables"}`). All field names
and input shapes are live-verified; the exhaustive field selections live in
the repo at `src/graphql.ts` (these are compact subsets).

Endpoint: `https://www.hemnet.se/graphql` · Method: POST · anonymous.

Write the body to a file (heredoc avoids shell-quoting the GraphQL string),
then send it:

```sh
cat > /tmp/hq.json <<'JSON'
{ "query": "…", "variables": { … } }
JSON
fpx post-json 'https://www.hemnet.se/graphql' @/tmp/hq.json -p hemnet | jq '.data'
```

Always check for GraphQL errors: `jq '.errors // empty'` (an errors array can
ride in an HTTP-200 body).

---

## 1. Resolve a location → locationId (do this first)

`variables.query` is free text; `limit` is required (`Int!`).

```json
{
  "query": "query Autocomplete($query: String!, $limit: Int!) { autocompleteLocations(query: $query, limit: $limit) { hits { locationId fullName parentFullName } } }",
  "variables": { "query": "Höllviken", "limit": 5 }
}
```

```sh
jq -r '.data.autocompleteLocations.hits[] | "\(.locationId)\t\(.fullName) — \(.parentFullName)"'
```

## 2. Search for-sale listings

`search.locationIds` is an array of strings (from step 1). Optional filters:
`priceMin`/`priceMax` (SEK), `roomsMin`/`roomsMax`, `livingAreaMin`/`livingAreaMax`
(m²), `keywords` (string), `housingFormGroups` (array of `HOUSES`, `APARTMENTS`,
`ROW_HOUSES`, `VACATION_HOMES`, `PLOTS`, `OTHERS`). `limit` is required; `sort`
is `NEWEST` or `OLDEST`.

```json
{
  "query": "query Search($search: ListingSearchForSaleInput!, $limit: Int!, $sort: ListingSearchForSaleSorting) { searchForSaleListings(search: $search, limit: $limit, sort: $sort) { total listings { id streetAddress area numberOfRooms livingArea listingHemnetUrl askingPrice { amount formatted } fee { formatted } squareMeterPrice { formatted } } } }",
  "variables": {
    "search": { "locationIds": ["898675"], "housingFormGroups": ["HOUSES"], "priceMax": 10000000 },
    "limit": 10,
    "sort": "NEWEST"
  }
}
```

```sh
jq -r '.data.searchForSaleListings | "total=\(.total)", (.listings[] | "\(.id)\t\(.askingPrice.formatted)\t\(.streetAddress)")'
```

## 3. Listing detail by id

`id` from a search card (`ID!`); `photoLimit` required (`Int!`). `listing`
returns the `PropertyListing` interface — the detail fields sit behind the
`... on ActivePropertyListing` fragment. A non-active id yields
`__typename` ≠ `ActivePropertyListing` (use the sold query in §5 instead).

```json
{
  "query": "query GetListing($id: ID!, $photoLimit: Int!) { listing(id: $id) { __typename ... on ActivePropertyListing { streetAddress area numberOfRooms livingArea legacyConstructionYear description listingHemnetUrl askingPrice { formatted } fee { formatted } runningCosts { formatted } squareMeterPrice { formatted } tenure { name } energyClassification { classification } broker { name } brokerAgency { name } coordinates { lat long } images(limit: $photoLimit) { total images { url(format: ITEMGALLERY_L) } } } } }",
  "variables": { "id": "21625405", "photoLimit": 5 }
}
```

```sh
jq '.data.listing | {addr: .streetAddress, price: .askingPrice.formatted, rooms: .numberOfRooms, m2: .livingArea, photos: [.images.images[].url]}'
```

## 4. Search sold listings (slutpriser — the comps)

Same filter shape as §2 but the input type is `SaleSearchInput!`, the result
is `searchSales { total cards }`, and money fields are pre-formatted **strings**
(not `Money` objects). `sort` is `SaleSearchSorting` (`NEWEST`/`OLDEST`).

```json
{
  "query": "query Sold($search: SaleSearchInput!, $limit: Int!, $sort: SaleSearchSorting) { searchSales(search: $search, limit: $limit, sort: $sort) { total cards { id streetAddress finalPrice askingPrice priceChange soldAtLabel livingArea rooms squareMeterPrice } } }",
  "variables": { "search": { "locationIds": ["898675"] }, "limit": 25, "sort": "NEWEST" }
}
```

```sh
# Median final price across the sold cards (strip "kr" and spaces):
jq -r '[.data.searchSales.cards[].finalPrice | gsub("[^0-9]";"") | tonumber] | sort | .[length/2|floor]'
```

## 5. Sold listing detail by id

`soldListing` returns `SoldPropertyListing` — note the renamed fields
(`sellingPrice`, `squareMeterSellingPrice`, `hemnetUrl`; no `region`).

```json
{
  "query": "query GetSold($id: ID!) { soldListing(id: $id) { __typename ... on SoldPropertyListing { streetAddress area numberOfRooms livingArea soldAt hemnetUrl sellingPrice { formatted } askingPrice { formatted } squareMeterSellingPrice { formatted } tenure { name } broker { name } } } }",
  "variables": { "id": "REPLACE_WITH_SOLD_ID" }
}
```

---

## Market stats

Hemnet has no market-stats query — the `hemnet_get_market_stats` tool derives
median/average final price and price-per-m² locally from a `searchSales` page
(§4). Reproduce with `jq` over the `cards` as shown above; check the card
count before trusting a thin median.
