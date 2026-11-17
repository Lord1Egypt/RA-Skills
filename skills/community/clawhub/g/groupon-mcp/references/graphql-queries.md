# Groupon curl recipes

All hit `POST https://www.groupon.com/mobilenextapi/graphql` with headers
`content-type: application/json` and `apollographql-client-name: mobilenextapi`.
The `sha256Hash` values are public persisted-query fingerprints (verified
2026-07-24); if one returns `PersistedQueryNotFound`, re-capture it (see SKILL.md).

A reusable shell function:

```bash
gp() {  # gp '<json-array-body>'  ->  raw JSON array on stdout
  curl -s -H 'content-type: application/json' \
       -H 'apollographql-client-name: mobilenextapi' \
       -X POST --data "$1" \
       'https://www.groupon.com/mobilenextapi/graphql'
}
```

## 1. Search / browse deals — `BrowseDealFeed`

Hash: `b035b25dceb8a84a64c618345cc21a14897b7328506a39b2e27fc7ca4ec2f429`

```bash
# Search "massage" in New York (drop the filters[] entry for a plain city browse)
grpn '[{"operationName":"BrowseDealFeed","variables":{
  "dealFeedParams":{"limit":24,"division":"new-york","locationFromUrl":false,
    "filters":[{"key":"query","subKey":null,"value":{"static":"massage"}}],
    "offset":0,"feedToken":null,"includeLocationsCount":true},
  "browseParams":{"pathName":"/search","isFetchMore":false},"allLocations":false},
  "extensions":{"persistedQuery":{"version":1,
    "sha256Hash":"b035b25dceb8a84a64c618345cc21a14897b7328506a39b2e27fc7ca4ec2f429"}}}]' \
| jq -r '.[0].data.browseDealFeed.cards[]
    | "\(.title)\n  \(.merchant.name // "-")  ★\(.rating.value // "-") (\(.rating.count // 0))  -\(.discountPercentage // 0)%\n  $\((.prices.price.amount // 0)/100)  \(.url)\n"'
```

- Paginate with `offset` (multiples of `limit`); total via `.[0].data.browseDealFeed.pagination`.
- Available filters (categories, price, sort) are in `.[0].data.browseDealFeed.facets`.
- Price is integer cents: `.prices.price.amount` (e.g. 3700 = $37.00); `.prices.strikeThroughPrice.amount` is the list price.

## 2. Deal detail — `getDeal`

Hash: `d60360371251da4c5ce1f753d3e55a77e80d538c6c57fd4fc20dc894cd121236`

```bash
# dealId = last path segment of a card .url (e.g. from https://www.groupon.com/deals/pat-s-pizza-1)
grpn '[{"operationName":"getDeal","variables":{
  "dealId":"pat-s-pizza-1","optionId":null,"adSafe":false,
  "includeGeoBreadcrumbs":true,"useFinePrintV3":true},
  "extensions":{"persistedQuery":{"version":1,
    "sha256Hash":"d60360371251da4c5ce1f753d3e55a77e80d538c6c57fd4fc20dc894cd121236"}}}]' \
| jq '.[0].data.getDeal | {title, subtitle, merchant: .merchant.name, division,
    rating: .representativeReview, options: [.options[]? | {title, id, price: .price}]}'
```

`getDeal` also carries `aiReviewSummary`, `images`, `videos`, `status`,
`showQuantitySelector`, fine print, and per-option pricing.

## 3. Category taxonomy — `GetMainNavigation`

Hash: `da722d6e5ae1b4e336bbda8d2d07f31925aa709acf9843c67c5a65d0827aeb01`

```bash
grpn '[{"operationName":"GetMainNavigation","variables":{"includeChildren":true,"maxDepthLevel":3},
  "extensions":{"persistedQuery":{"version":1,
    "sha256Hash":"da722d6e5ae1b4e336bbda8d2d07f31925aa709acf9843c67c5a65d0827aeb01"}}}]' \
| jq '.[0].data'
```

## Notes

- Deal reads are **public**; no account, key, or cookie is involved. (Purchasing a
  Groupon needs an authenticated session — that lives in the full `groupon-mcp`
  server, not this skill.)
- The full `groupon-mcp` MCP server wraps these same ops as typed tools
  (`groupon_search_deals`, `groupon_get_deal`, `groupon_list_categories`) with
  compact projections and drift-tolerant parsing — prefer it when running inside
  an MCP host.
