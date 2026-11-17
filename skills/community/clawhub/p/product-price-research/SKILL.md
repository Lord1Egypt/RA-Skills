---
name: product-price-research
description: Researches products, prices, sellers, and reviews across major online marketplaces and big-box/specialty retailers (Amazon, eBay, Shopify stores, Shop.app, Target, Costco, Walmart, Nike, Zara, Adidas, Best Buy, Home Depot, Sephora, SHEIN, IKEA, Chewy, and more) using the Crawlora API, returning clean JSON. Use when the user asks to find a product, compare prices or sellers, track listings, or pull marketplace/retailer reviews — instead of scraping store pages.
---

# Product & price research

Look up and compare products, prices, sellers, and reviews across Amazon,
eBay, Shopify storefronts, Shop.app, Target, Costco, Zalando, Walmart, H&M,
Kohl's, Lululemon, Macy's, Nike, Old Navy (plus Gap, Banana Republic, and
Athleta under the same endpoints), Sam's Club, Ulta Beauty, Wayfair, Wish,
Zappos, Zara, Adidas, Best Buy, Home Depot, Sephora, SHEIN, IKEA, and
Chewy — all as normalized JSON from the Crawlora API, with no HTML
scraping. Walgreens is store-locator only (no product catalog).

## When to use this skill

- "What does X cost on Amazon / eBay / Target / Walmart?" or "compare prices
  for X across sellers/retailers."
- "Find listings for X" / "search this Shopify store" / "what's in this collection?"
- "Pull reviews / ratings for this product or seller."
- "Track this product's price / variants / availability."
- Competitive pricing, catalog, or marketplace-review research.
- "Browse category X on Wayfair / Kohl's / Sam's Club" when the retailer has
  no keyword search of its own.
- Apparel/beauty catalog lookups spanning Nike, Zara, H&M, Old Navy/Gap/Banana
  Republic/Athleta, Lululemon, Ulta Beauty, Adidas, or Sephora.
- Home-goods/electronics/pet lookups spanning Home Depot, Best Buy, IKEA, or Chewy.
- "Find the nearest Walgreens" (store locator only — no product catalog).

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

Pick the marketplace, then the job:

1. **Search / discover** — `/amazon/search`, `/ebay/search`, `/shopify/products`,
   `/shop-app/search`, `/target/search`, `/costco/search`, `/walmart/search`,
   `/hm/search`, `/nike/search`, `/oldnavy/search` (covers Old Navy, Gap,
   Banana Republic, and Athleta via `brand=on|gap|br|at`, defaults to `on`),
   `/ulta/search`, `/wish/search`, `/zappos/search`, `/zara/search` (**requires
   `section`**, a department like `WOMAN`/`MAN`), and `/zalando/search` (this
   one **requires `market`** — a Zalando country storefront code like `de`,
   `fr`, `com`; list them via `/zalando/markets`) to find candidate products by
   keyword. **Kohl's, Lululemon, Macy's, Sam's Club, and Wayfair have no
   keyword-search endpoint** — browse a category instead:
   `/kohls/category` (facets give follow-up category strings),
   `/lululemon/categories` → `/lululemon/category`, `/samsclub/departments` →
   `/samsclub/category`, and `/wayfair/categories` → `/wayfair/category`.
   Macy's has neither search nor category browse at all — only direct
   `productId` lookup (below) plus `/macys/suggest` typeahead.
   `/adidas/search` (`query` or `category`, exactly one required),
   `/bestbuy/search` (`q`), `/homedepot/search` (`q`), `/sephora/search`
   (`query`, plus `brand`/`filter`/`price_min`+`price_max`
   as a matched pair/`rating_min`/`is_new` facets), `/ikea/search`
   (`q`, or an IKEA item number resolves directly), and `/chewy/search`
   (`q` — a strong category match like "dog food" transparently redirects
   to that category listing) round out search. **Walgreens has no product
   catalog at all** — `/walgreens/stores` (lat/lon or zip) is its only
   endpoint, for store lookup.
2. **Detail** — fetch a specific product (`/amazon/product`, `/ebay/item`,
   `/shopify/products/{handle}`, `/shop-app/products/{id}`,
   `/target/product` (`tcin`), `/costco/product/{id}`, `/walmart/product/{item_id}`,
   `/zalando/product` (`sku`+`market`), `/hm/product/{product_id}`,
   `/nike/product` (`slug`+`style_color`), `/oldnavy/product` (`pid`+`brand`),
   `/lululemon/product/{product_id}`, `/macys/product/{productId}`,
   `/samsclub/product/{id}`, `/ulta/product/{productId}`, `/wayfair/product/{id}`,
   `/wish/product/{id}`, `/zappos/product/{productId}`, `/zara/product/{productId}`,
   `/adidas/product` (`product_id`), `/bestbuy/product` (`sku`),
   `/homedepot/product/{id}`, `/sephora/product` (`product_id` — the full
   product-page slug like `lip-sleeping-mask-P420652`, not just the SKU),
   `/shein/products/detail` (`goods_id`+`goods_sn`), `/ikea/product`
   (`item_no`), `/chewy/product` (`id`))
   for price, variants, specs. **Kohl's has no standalone product-detail
   endpoint** — product cards (including `web_id`, needed for reviews below)
   only come back embedded in `/kohls/category`'s listing.
3. **Sellers** — for eBay/Shop.app, resolve the seller/shop (`/ebay/seller/...`,
   `/shop-app/shops/{handle}`) to compare offers.
4. **Reviews** — pull product/seller reviews where available
   (`/shop-app/products/{id}/reviews`, `/ebay/seller/.../feedback`,
   `/target/reviews`, `/costco/product/{id}/reviews`, `/walmart/product/{item_id}/reviews`,
   `/kohls/product/reviews` (`web_id`), `/macys/product/reviews` (`product_id`),
   `/nike/product/reviews` (`slug`+`style_color`), `/oldnavy/product/reviews`
   (`pid`+`brand`), `/ulta/product/reviews` (`product_id`), `/wish/product/{id}/reviews`).
   H&M, Lululemon, Sam's Club, and Zappos surface reviews (when present)
   embedded in their own product-detail call instead of a separate endpoint;
   Wayfair and Zara expose no reviews at all — Wayfair's product detail only
   has an aggregate rating. `/bestbuy/product/reviews` (`sku`),
   `/sephora/product/reviews` (`product_id`), and `/ikea/reviews`
   (`item_no`) cover those three separately; Home Depot and Chewy surface
   reviews embedded in their own product-detail call instead. Adidas reviews and rating summaries are available at
   `/adidas/product/reviews`, using the search result's `model_number` (not its
   SKU). Discover per-model review topics via `/adidas/product/review-topics`;
   locale controls review language and can yield an empty review sample. SHEIN
   exposes no review endpoint in this catalog.
5. **Compare** the JSON fields (price, currency, rating, seller) and answer.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search a marketplace (GET, key=value params):
scripts/crawlora.sh /amazon/search k="standing desk" | jq '.'
scripts/crawlora.sh -X POST /ebay/search '{"keyword":"mechanical keyboard"}' | jq '.'
scripts/crawlora.sh /shop-app/search query="running shoes" | jq '.'
scripts/crawlora.sh /target/search q="standing desk" | jq '.'
scripts/crawlora.sh /walmart/search q="standing desk" | jq '.'
scripts/crawlora.sh /zalando/search q="running shoes" market=de | jq '.'
scripts/crawlora.sh /nike/search keyword="running shoes" | jq '.'
scripts/crawlora.sh /ulta/search query="retinol serum" | jq '.'
scripts/crawlora.sh /bestbuy/search q="laptop" | jq '.'
scripts/crawlora.sh /sephora/search query="retinol serum" | jq '.'
scripts/crawlora.sh /chewy/search q="salmon dog food" | jq '.'

# Product detail:
scripts/crawlora.sh /amazon/product/B0XXXXXXX | jq '.data'
scripts/crawlora.sh /ikea/product item_no=00263850 | jq '.'

# Category browse (no keyword search on this platform):
scripts/crawlora.sh /wayfair/category category=478390 | jq '.'
scripts/crawlora.sh /zara/category/2420463/products | jq '.'

# Store locator only (no product catalog):
scripts/crawlora.sh /walgreens/stores zip=10001 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every endpoint
this skill uses, including its method, path, parameters, and platform coverage.

## Examples

- **Cross-marketplace price compare:** search `/amazon/search` and `/ebay/search`
  for the same query, collect `price` from each, and present the spread.
- **Seller due diligence:** `/ebay/seller/{seller}` + `/ebay/seller/{seller}/feedback`
  to summarize a seller's rating and recent feedback before buying.
- **Shopify catalog audit:** `/shopify/products` (paginate) to list a store's
  catalog with prices, then flag items above/below a threshold.
- **No-search retailer browse:** for a retailer with no keyword search
  (Kohl's, Wayfair, Sam's Club), call the category/department-discovery
  endpoint first (`/kohls/category`'s facets, `/wayfair/categories`,
  `/samsclub/departments`) to find a category id, then browse it directly
  instead of trying to search by keyword.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public product/listing pages; respect each marketplace's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- Results are paginated — pass `page` (and `count` where supported) to walk listings.
- **Zalando always needs `market`** (no default storefront) — resolve valid
  codes via `/zalando/markets` if unsure.
- **Macy's has no search or category browse** — only `/macys/product/{productId}`
  (needs a known `productId`) and `/macys/suggest` typeahead.
- **Wayfair has no search and no reviews endpoint** — only
  `/wayfair/categories` → `/wayfair/category` and `/wayfair/product/{id}`
  (which carries an aggregate rating, but no review text).
- **Kohl's has no search or standalone product-detail endpoint** — browse
  `/kohls/category` (its `category` param takes a `+`-joined taxonomy string,
  percent-encode the `+` as `%2B`) and read product cards from the listing;
  `/kohls/product/reviews` needs the `web_id` from that listing.
- **Sam's Club has no keyword-search endpoint** — start from
  `/samsclub/departments` or `/samsclub/category`; there's also no dedicated
  reviews endpoint (rating/review count only comes from `/samsclub/product/{id}`).
- **Lululemon has no keyword-search endpoint** — browse via
  `/lululemon/categories` → `/lululemon/category`; reviews are embedded in
  `/lululemon/product/{product_id}`, not a separate call.
- **Zara's `/zara/search` requires `section`** (a department like `WOMAN`),
  and Zara exposes no reviews endpoint at all.
- **Old Navy's endpoints are shared across four storefronts** — pass
  `brand=on|gap|br|at` (Old Navy/Gap/Banana Republic/Athleta; defaults to
  `on`); a `cid`/`pid` found under one brand only works with that same brand.

## AliExpress product and attribute comparisons

Discover `aliexpress_search_filters` for the exact query before applying its
attribute IDs and value IDs to search. Attribute pairs are query-specific, with
at most one value per group and up to five pairs; do not reuse another search's
facet identifiers. Preserve listing variant, currency (search price filters use
USD), seller/condition evidence, shipping basis, and returned source identifiers.
Review samples do not authenticate a seller or establish typical delivery times.
Choice/free-shipping flags are source labels; quoted shipping and total cost can
still depend on destination and checkout conditions. Compare observed offers,
not guaranteed landed costs or transaction volume inferred from sort order.

```sh
scripts/crawlora.sh /aliexpress/search-filters q="usb c hub"
scripts/crawlora.sh /aliexpress/search q="usb c hub" page=1 sort=best_match
```
