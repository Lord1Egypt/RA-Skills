# product-price-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**233 endpoints across 36 platform group(s).**

## Amazon (5)

### `amazon_charts`

- **HTTP:** `GET /amazon/charts`
- **What:** Amazon product charts. Returns one page of a ranked Amazon chart (Best Sellers, New Releases, or Most Wished For) for a department or department subcategory on `amazon.com`. Discover valid department/node values with amazon-charts-categories.
- **Params:** `chart` (string, **required**) — Chart type; `department` (string, **required**) — Amazon department slug; `node` (string, optional) — Numeric browse node id; `page` (integer, optional) — 1-based page number

### `amazon_charts_categories`

- **HTTP:** `GET /amazon/charts/categories`
- **What:** Amazon chart categories. Returns the department and subcategory values amazon-charts accepts for a given chart. Omit department to list a chart's top-level departments; pass a department (and optionally a node) to get that category's own name plus its immediate child categories.
- **Params:** `chart` (string, **required**) — Chart type; `department` (string, optional) — Amazon department slug; `node` (string, optional) — Numeric browse node id (requires department)

### `amazon_product`

- **HTTP:** `GET /amazon/product/{asin}`
- **What:** Retrieve Amazon product details. Returns product details for an Amazon ASIN on `amazon.com`, including pricing, availability, overview data, inline review samples, and descriptive content.
- **Params:** `asin` (string, **required**) — Amazon ASIN; `currency` (string, optional) — Amazon currency; `language` (string, optional) — Amazon language

### `amazon_search`

- **HTTP:** `GET /amazon/search`
- **What:** Search Amazon products. Searches `amazon.com` by keyword, with optional sort order and page. Each result card has the ASIN, title, link, image, price and list price, rating and review count, the bought-in-last-month figure, and flags for sponsored placement and free delivery.
- **Params:** `k` (string, **required**) — Search keyword; `page` (integer, optional) — 1-based page number; `s` (string, optional) — Sort order

### `amazon_suggest`

- **HTTP:** `GET /amazon/suggest/{keyword}`
- **What:** Retrieve Amazon search suggestions. Returns Amazon's search-box autocomplete suggestions for a keyword prefix on `amazon.com`, as a plain list of suggested search phrases such as `apple watch bands`.
- **Params:** `keyword` (string, **required**) — Suggestion prefix

## eBay (10)

### `ebay_item`

- **HTTP:** `GET /ebay/item/{item_id}`
- **What:** Get eBay item details. Returns the details of one eBay listing by `item_id`: title, link, images, price and price text, condition, availability, item specifics, description, location and shipping. It also carries the seller's name, store, feedback score, followers and items sold, along with the listing's rating and rating count.
- **Params:** `item_id` (string, **required**) — eBay item ID

### `ebay_live_stream`

- **HTTP:** `GET /ebay/live/streams/{id}`
- **What:** Get an eBay Live stream. Returns one eBay Live stream or event by `id`, taken from the `streams[].id` of the stream list. The response has title, description, state, start and end times, viewer, watch and like counts, tags, channels and the live, preview and replay URLs. Each host carries a 365-day feedback summary and four average ratings. An unknown id returns `404`.
- **Params:** `id` (string, **required**) — eBay Live stream/event id

### `ebay_live_stream_items`

- **HTTP:** `GET /ebay/live/streams/{id}/items`
- **What:** List an eBay Live stream's featured items. Lists the items currently featured in an eBay Live stream, identified by the required event `id`. Each item has its listing id, title, price and currency, bid count, sale type, leader and winner usernames, and `auction_status` (`READY`, `LIVE` or `ENDED`). A stream with no featured items, or an unknown id, returns an empty `items` array.
- **Params:** `id` (string, **required**) — eBay Live stream/event id

### `ebay_live_streams`

- **HTTP:** `GET /ebay/live/streams`
- **What:** List eBay Live streams. Lists live and upcoming eBay Live streams for one category channel, set with `category` (default `explore`; other values are channel ids such as `IPqZx79LNuwFcSVt` for Sports Singles). Each stream has its title, state, start time, watch count, hosts, tags and preview media. Host feedback is not included. Page on with `next_request_number` and `session_id`, passed back as `request_number` and `session_id`.
- **Params:** `category` (string, optional) — eBay Live category channel, defaults to explore; `request_number` (integer, optional) — Pagination cursor from a previous response's next_request_number, defaults to 0; `session_id` (string, optional) — Pagination session id from a previous response's session_id

### `ebay_live_streams_batch`

- **HTTP:** `GET /ebay/live/streams/batch`
- **What:** Get multiple eBay Live streams. Returns summaries for several eBay Live streams in one call. `ids` is required and takes up to 9 stream ids, comma-separated or repeated. Each stream has its title, state, watch count, hosts, tags and preview media, without the per-host feedback summary. Ids that do not resolve are silently omitted, and the order may differ from the request.
- **Params:** `ids` (string, **required**) — One or more eBay Live stream/event ids, up to 9. Comma-separated or repeated query values are both accepted.

### `ebay_search`

- **HTTP:** `POST /ebay/search`
- **What:** Search eBay listings. Searches eBay listings by keyword from a JSON body, with page, page size (60, 120 or 240) and a listing-status filter (`active`, `sold`, `completed` or `sold_completed`). Each result has the item id, title, link, image, price or price range, bid count, seller and rating, location, shipping information, and sold and watcher counts.
- **Params:** `option` (object, **required**) — eBay search payload
- **REST body:** Send the value of the MCP argument `option` directly as the JSON body; do not wrap it in a `option` property.

### `ebay_seller`

- **HTTP:** `GET /ebay/seller/{seller}`
- **What:** Get eBay seller profile. Returns the public profile of an eBay seller by the required `seller` username: display name, store name and URL, profile URL, description, location, member-since date, positive feedback percentage, feedback count, items sold, followers, and detailed seller ratings. Feedback details are included when eBay provides them.
- **Params:** `seller` (string, **required**) — eBay seller username

### `ebay_seller_about`

- **HTTP:** `GET /ebay/seller/{seller}/about`
- **What:** Get eBay seller about details. Returns seller about information from the eBay store about tab, including seller stats, top-rated status, optional location/member-since fields, and cleaned store categories.
- **Params:** `seller` (string, **required**) — eBay seller username

### `ebay_seller_feedback`

- **HTTP:** `GET /ebay/seller/{seller}/feedback`
- **What:** Get eBay seller feedback. Returns the feedback eBay shows for a seller, identified by the required `seller` username. The response has the total feedback count, positive feedback percentage, overall rating summary, detailed seller ratings, and review cards with buyer, comment, rating, period and verified-purchase flag. Page with `page` (default 1) and `per_page` (24, 48 or 72; default 48), using `has_more` and `next_page`.
- **Params:** `page` (integer, optional) — Feedback page number; `per_page` (integer, optional) — Reviews per page; `seller` (string, **required**) — eBay seller username

### `ebay_seller_shop`

- **HTTP:** `GET /ebay/seller/{seller}/shop`
- **What:** Get eBay seller shop listings. Lists the items in an eBay seller's shop, identified by the required `seller` username, one page at a time with `page` (default 1). Each result has its item id, title, link, image, price or price range, shipping note, location, bid count and watcher count. The response gives the `total` and a `has_more` flag.
- **Params:** `page` (integer, optional) — Shop page number; `seller` (string, **required**) — eBay seller username

## Shopify (11)

### `shopify_collection_products`

- **HTTP:** `GET /shopify/collections/{handle}/products`
- **What:** List Shopify collection products. Returns products from a Shopify collection. `sortBy` and dynamic facet-filter query params (e.g. `fit`, `canonicalColour`) only take effect for headless storefronts (`transport_mode: "ssr_embedded"`) and return an invalid-param error if supplied against a classic store, since classic Shopify storefronts have no server-side sort or filter support. `sort_by`, `min_price`, `max_price`, `product_type`, `in_stock_only`, and `option_`-prefixed params (e.g. `option_size=Small,Medium`) drive a separate, independent mechanism -- Shopify's own native Storefront Filtering collection-page feature (`transport_mode: "storefront_filtered"`) -- which works for both classic and headless stores; supplying any of these takes precedence over sortBy/dynamic facet filters.
- **Params:** `handle` (string, **required**) — Collection handle; `in_stock_only` (boolean, optional) — Storefront-filtering transport. true restricts to currently in-stock items only.; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `max_price` (number, optional) — Storefront-filtering transport. Maximum price (inclusive), in the storefront's display currency's major unit.; `min_price` (number, optional) — Storefront-filtering transport. Minimum price (inclusive), in the storefront's display currency's major unit.; `option_size` (string, optional) — Storefront-filtering transport. Example dynamic variant-option filter: comma-separated exact display values for the storefront's own size option (e.g. option_size=Small,Medium). Any variant option name is accepted the same way (option_color, ...) -- see facets in an unfiltered response for the live option names/values per store.; `page` (integer, optional) — 1-based page, defaults to 1; `product_type` (string, optional) — Storefront-filtering transport, comma-separated. Exact product-type display strings from the storefront's own Product Type facet -- see facets.product_type in an unfiltered response for the live value set.; `sortBy` (string, optional) — SSR-fallback transport only (transport_mode ssr_embedded). Allowed values: sortLTH, sortHTL, newest. Omit for the storefront's default relevancy order. Rejected as an invalid param for classic-transport stores.; `sort_by` (string, optional) — Storefront-filtering transport. Allowed values: manual, best-selling, title-ascending, title-descending, price-ascending, price-descending, created-ascending, created-descending. Omit for the collection's own default order.; `url` (string, **required**) — Shopify storefront URL

### `shopify_collections`

- **HTTP:** `GET /shopify/collections`
- **What:** List Shopify collections. Returns collections from a public Shopify storefront. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1; `url` (string, **required**) — Shopify storefront URL

### `shopify_page`

- **HTTP:** `GET /shopify/pages/{handle}`
- **What:** Get Shopify page. Returns one static page from any public Shopify storefront, by path `handle` and the required `url` of the store. The response has the page's title, URL, times and its `content` as plain text. Unknown handles return 404. Localhost, private-network and credentialed URLs are rejected.
- **Params:** `handle` (string, **required**) — Page handle; `url` (string, **required**) — Shopify storefront URL

### `shopify_pages`

- **HTTP:** `GET /shopify/pages`
- **What:** List Shopify pages. Lists static pages from a Shopify storefront given by the required `url`, paged with `page` (from 1) and `limit` (default 50, max 250). Each has `handle`, `title`, `url`, plain-text `content` and dates. If `transport_mode` is `ssr_embedded`, items hold only `handle`, `url` and `updated_at`.
- **Params:** `limit` (integer, optional) — Maximum pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1; `url` (string, **required**) — Shopify storefront URL

### `shopify_product`

- **HTTP:** `GET /shopify/products/{handle}`
- **What:** Get Shopify product. Returns one product from any Shopify storefront, given the store URL and the product handle: title, description, product type, tags, price and compare-at price, availability, options, images, and each variant with its own price, availability and barcode. Prices are in decimal currency units; an unknown handle returns `404`.
- **Params:** `handle` (string, **required**) — Product handle; `url` (string, **required**) — Shopify storefront URL

### `shopify_product_recommendations`

- **HTTP:** `GET /shopify/products/{handle}/recommendations`
- **What:** List Shopify product recommendations. Returns recommended products from Shopify's product recommendations.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20; `url` (string, **required**) — Shopify storefront URL

### `shopify_products`

- **HTTP:** `GET /shopify/products`
- **What:** List Shopify products. Returns products from a public Shopify storefront. Valid empty result pages return `200` with an empty products array. `sortBy` and dynamic facet-filter query params (e.g. `fit`, `canonicalColour`) only take effect for headless storefronts (`transport_mode: "ssr_embedded"`) and return an invalid-param error if supplied against a classic store, since classic Shopify storefronts have no server-side sort or filter support. `sort_by`, `min_price`, `max_price`, `product_type`, `in_stock_only`, and `option_`-prefixed params (e.g. `option_size=Small,Medium`) drive a separate, independent mechanism -- Shopify's own native Storefront Filtering collection-page feature (`transport_mode: "storefront_filtered"`) -- which works for both classic and headless stores; supplying any of these takes precedence over sortBy/dynamic facet filters.
- **Params:** `in_stock_only` (boolean, optional) — Storefront-filtering transport. true restricts to currently in-stock items only.; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `max_price` (number, optional) — Storefront-filtering transport. Maximum price (inclusive), in the storefront's display currency's major unit.; `min_price` (number, optional) — Storefront-filtering transport. Minimum price (inclusive), in the storefront's display currency's major unit.; `option_size` (string, optional) — Storefront-filtering transport. Example dynamic variant-option filter: comma-separated exact display values for the storefront's own size option (e.g. option_size=Small,Medium). Any variant option name is accepted the same way (option_color, ...) -- see facets in an unfiltered response for the live option names/values per store.; `page` (integer, optional) — 1-based page, defaults to 1; `product_type` (string, optional) — Storefront-filtering transport, comma-separated. Exact product-type display strings from the storefront's own Product Type facet -- see facets.product_type in an unfiltered response for the live value set.; `sortBy` (string, optional) — SSR-fallback transport only (transport_mode ssr_embedded). Allowed values: sortLTH, sortHTL, newest. Omit for the storefront's default relevancy order. Rejected as an invalid param for classic-transport stores.; `sort_by` (string, optional) — Storefront-filtering transport. Allowed values: manual, best-selling, title-ascending, title-descending, price-ascending, price-descending, created-ascending, created-descending. Omit for the collection's own default order.; `url` (string, **required**) — Shopify storefront URL

### `shopify_search_suggest`

- **HTTP:** `GET /shopify/search/suggest`
- **What:** Get Shopify search suggestions. Returns predictive search suggestions from any Shopify storefront for a query: matching products, collections and suggested queries. Choose which with `types` (default all three) and cap results per type with `limit` (default 10, max 20). Products carry price, availability, images and options; collections carry title, handle, description and product count.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query; `url` (string, **required**) — Shopify storefront URL

### `shopify_sitemap_urls`

- **HTTP:** `GET /shopify/sitemap/urls`
- **What:** List Shopify sitemap URLs. Lists URL entries from a Shopify storefront's sitemaps, for the required `url`. `type` filters (`all` by default, `products`, `collections`, `pages`, `blogs`, `agentic_discovery`, `other`) and `limit` caps entries (default 50, max 250). Each has `loc`, `type`, `handle`, `lastmod`, `changefreq` and optional `images`.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other; `url` (string, **required**) — Shopify storefront URL

### `shopify_sitemaps`

- **HTTP:** `GET /shopify/sitemaps`
- **What:** List Shopify sitemaps. Lists the child sitemaps in a Shopify storefront's sitemap index, for the required `url`. Each has a `loc` and a `type` (`products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`) inferred from its URL. Localhost, private-network and credentialed URLs are rejected.
- **Params:** `url` (string, **required**) — Shopify storefront URL

### `shopify_store`

- **HTTP:** `GET /shopify/store`
- **What:** Get Shopify store metadata. Resolves a public Shopify storefront and returns its metadata.
- **Params:** `url` (string, **required**) — Shopify storefront URL

## Shop.app (16)

### `shop_app_analysis`

- **HTTP:** `GET /shop-app/analysis`
- **What:** Analyze Shop.app query results. Returns a market snapshot derived from Shop.app search results, including price ranges, currencies, sale counts, discounts, and top shops. Limit defaults to 20 and accepts values up to 50.
- **Params:** `deep_search` (boolean, optional) — Accepted for compatibility; Shop.app no longer offers a separate deep search mode, so results are unchanged; `in_stock` (boolean, optional) — Request in-stock products; `limit` (integer, optional) — Maximum products to analyze, defaults to 20 and supports up to 50; `on_sale` (boolean, optional) — Request sale products; `query` (string, **required**) — Search query

### `shop_app_categories`

- **HTTP:** `GET /shop-app/categories`
- **What:** List Shop.app categories. Returns the Shop.app product category tree, with no parameters. Each category has its `id`, `gid`, `name`, `slug`, `image`, `has_children`, nested `children` and a `path` of ancestors. Ids are taken from Shopify product category GIDs where present.
- **Params:** _none_

### `shop_app_collection_products`

- **HTTP:** `GET /shop-app/shops/{handle}/collections/{collection_id}/products`
- **What:** List Shop.app collection products. Lists products in one collection of a Shop.app merchant, by shop `handle` and `collection_id`. `limit` defaults to 30 (max 60), `sort_by` is `MOST_SALES` (default), `PRICE_LOW_TO_HIGH`, `PRICE_HIGH_TO_LOW` or `RELEVANCE`, and `in_stock` defaults to true. Each card has its title, price, original price, image and URL.
- **Params:** `collection_id` (string, **required**) — Collection id; `handle` (string, **required**) — Shop handle; `in_stock` (boolean, optional) — Request in-stock products; `limit` (integer, optional) — Maximum products, defaults to 30 and supports up to 60; `sort_by` (string, optional) — Sort mode

### `shop_app_product`

- **HTTP:** `GET /shop-app/products/{id}`
- **What:** Get Shop.app product. Returns a Shop.app product by `id`: title, description, price and original price, currency, availability, images, option groups, rating, review count with reviews, related products and the selling shop. Pass `variant_id` to mark a variant as selected. Missing products return an error.
- **Params:** `id` (string, **required**) — Product id; `variant_id` (string, optional) — Variant id

### `shop_app_product_related`

- **HTTP:** `GET /shop-app/products/{id}/related`
- **What:** List Shop.app related products. Lists products related to a Shop.app product, by `id`. `limit` defaults to 20 and is capped at 50. Each card has the product's id, title, price, original price, currency, `on_sale` flag, image, shop name and URL. A product page with no related items returns an error.
- **Params:** `id` (string, **required**) — Product id; `limit` (integer, optional) — Maximum products, defaults to 20 and supports up to 50

### `shop_app_product_reviews`

- **HTTP:** `GET /shop-app/products/{id}/reviews`
- **What:** List Shop.app product reviews. Lists customer reviews for a Shop.app product, by `id`, up to `limit` (default 20, max 50). Each review has its rating, title, body, author, date, helpful count and variant label, where present. A product with no reviews returns an error.
- **Params:** `id` (string, **required**) — Product id; `limit` (integer, optional) — Maximum reviews, defaults to 20 and supports up to 50

### `shop_app_product_shop`

- **HTTP:** `GET /shop-app/products/{id}/shop`
- **What:** Get the Shop.app shop for a product. Finds the Shop.app merchant that sells a product, by the product `id`. Returns the shop's handle, name, description, logo, banner, rating, review count, storefront URL, and its collections. Unknown products, or ones with no public shop, return not found.
- **Params:** `id` (string, **required**) — Product id

### `shop_app_product_variant`

- **HTTP:** `GET /shop-app/products/{id}/variant`
- **What:** Get a Shop.app product variant by selected options. Returns the exact public product variant matching selected options. selected_options must be a JSON object when provided. Repeated option filters may also be sent as option.Name=value or option[Name]=value.
- **Params:** `id` (string, **required**) — Product id; `selected_options` (string, optional) — Selected options JSON object

### `shop_app_product_variants`

- **HTTP:** `GET /shop-app/products/{id}/variants`
- **What:** List Shop.app product variants. Returns adjacent variants for a Shop.app product. selected_options must be a JSON object when provided. Repeated option filters may also be sent as option.Name=value or option[Name]=value.
- **Params:** `id` (string, **required**) — Product id; `limit` (integer, optional) — Maximum variants, defaults to 50 and supports up to 100; `selected_options` (string, optional) — Selected options JSON object

### `shop_app_search`

- **HTTP:** `GET /shop-app/search`
- **What:** Search Shop.app products. Searches Shop.app product results. Limit defaults to 20 and accepts values up to 50.
- **Params:** `deep_search` (boolean, optional) — Accepted for compatibility; Shop.app no longer offers a separate deep search mode, so results are unchanged; `in_stock` (boolean, optional) — Request in-stock products; `limit` (integer, optional) — Maximum products, defaults to 20 and supports up to 50; `on_sale` (boolean, optional) — Request sale products; `query` (string, **required**) — Search query

### `shop_app_shop`

- **HTTP:** `GET /shop-app/shops/{handle}`
- **What:** Get Shop.app shop. Returns a Shop.app merchant profile by shop `handle`: name, description, logo, banner, rating, review count, storefront and Shop.app URLs, and collection summaries when the shop page lists them. Unknown handles return an error.
- **Params:** `handle` (string, **required**) — Shop handle

### `shop_app_shop_locations`

- **HTTP:** `GET /shop-app/shops/{handle}/locations`
- **What:** List Shop.app shop locations. Returns the public retail locations of a Shop.app merchant by shop handle, up to `limit` (default 10, max 50). Each location has its id, name, latitude and longitude, and street address; the response also carries the total count and a cursor for the next page. A shop with no public retail locations returns an error.
- **Params:** `handle` (string, **required**) — Shop handle; `limit` (integer, optional) — Maximum locations, defaults to 10 and supports up to 50

### `shop_app_shop_products`

- **HTTP:** `GET /shop-app/shops/{handle}/products`
- **What:** List Shop.app shop products. Lists products from a Shop.app merchant, by shop `handle`. `limit` defaults to 30 (max 60), `sort_by` is `MOST_SALES` (default), `PRICE_LOW_TO_HIGH`, `PRICE_HIGH_TO_LOW` or `RELEVANCE`, and `in_stock` defaults to true. Each card has its id, title, price, original price, image and URL. An invalid `sort_by` is rejected.
- **Params:** `handle` (string, **required**) — Shop handle; `in_stock` (boolean, optional) — Request in-stock products; `limit` (integer, optional) — Maximum products, defaults to 30 and supports up to 60; `sort_by` (string, optional) — Sort mode

### `shop_app_shop_reviews`

- **HTTP:** `GET /shop-app/shops/{handle}/reviews`
- **What:** List Shop.app shop reviews. Lists customer reviews for a Shop.app merchant, by shop `handle`, up to `limit` (default 20, max 50). Each review has its rating, body, author, date, helpful count and the product reviewed. Also returns `total_count` and `next_cursor`. Unknown shops return not found.
- **Params:** `handle` (string, **required**) — Shop handle; `limit` (integer, optional) — Maximum reviews, defaults to 20 and supports up to 50

### `shop_app_shop_typeahead`

- **HTTP:** `GET /shop-app/shops/{handle}/typeahead`
- **What:** Suggest products and collections inside a Shop.app shop. Returns search suggestions inside one Shop.app shop, for the shop `handle` and required `query`. `limit` defaults to 20, which is also the maximum. Suggestions are `type` term, product or collection, with text, position and a product or collection object where relevant. Unknown shops return not found.
- **Params:** `handle` (string, **required**) — Shop handle; `limit` (integer, optional) — Maximum suggestions, defaults to 20 and supports up to 20; `query` (string, **required**) — Typeahead query

### `shop_app_suggestions`

- **HTTP:** `GET /shop-app/suggestions`
- **What:** Suggest Shop.app searches. Returns Shop.app autocomplete suggestions for the required `query`. `limit` defaults to 10 and is capped at 20. Each suggestion is either a search query or a shop, with its `text`, `type`, URL and, for shops, the shop handle, name, rating and image.
- **Params:** `limit` (integer, optional) — Maximum suggestions, defaults to 10 and supports up to 20; `query` (string, **required**) — Search query

## Target (8)

### `target_categories`

- **HTTP:** `GET /target/categories`
- **What:** List all Target categories. Lists Target's top-level category menu in `categories`, plus the grouped shop-all directory in `groups`. Each category has an `id` (the one used by `/target/category-products`), name, canonical URL and, when Target supplies one, an image URL. The response also gives `count` and `group_count`. Takes no parameters.
- **Params:** _none_

### `target_category_products`

- **HTTP:** `GET /target/category-products`
- **What:** Browse Target category products. Returns paginated products for any category id from target-categories. Each response also contains every available dynamic filter group and option. Pass selected option ids through filter_ids as a comma-separated list. The sort enum accepts `relevance`, `featured`, `price-low`, `price-high`, `rating`, `bestselling`, and `newest`.
- **Params:** `category_id` (string, **required**) — Target category id; `filter_ids` (string, optional) — Comma-separated Target filter option ids; `page` (integer, optional) — One-based page (1-50); `sort` (string, optional) — Result order; `store_id` (integer, optional) — Target store id used for pricing

### `target_filter_options`

- **HTTP:** `GET /target/filter-options`
- **What:** List Target filter options. Returns every dynamic filter group and option for either a product query or category. Provide exactly one of q or category_id. Pass currently selected option ids through filter_ids to obtain the remaining context-aware options.
- **Params:** `category_id` (string, optional) — Target category id; mutually exclusive with q; `filter_ids` (string, optional) — Comma-separated selected Target filter option ids; `q` (string, optional) — Product search query; mutually exclusive with category_id; `store_id` (integer, optional) — Target store id used for pricing

### `target_product`

- **HTTP:** `GET /target/product`
- **What:** Get a Target product. Returns product details for one Target item, including product content, images, price, rating, category, and availability flags for the selected store.
- **Params:** `store_id` (integer, optional) — Target store id used for pricing and availability; `tcin` (string, **required**) — Numeric Target item id (TCIN)

### `target_questions`

- **HTTP:** `GET /target/questions`
- **What:** List Target product questions and answers. Lists customer questions for a Target item given by its numeric `tcin`, each with its text, author, submission time, helpful votes and nested answers. `page` is zero-based and `per_page` runs 1 to 25. The response gives `total_pages` and `count` for paging.
- **Params:** `page` (integer, optional) — Zero-based page; `per_page` (integer, optional) — Questions per page; `tcin` (string, **required**) — Numeric Target item id

### `target_reviews`

- **HTTP:** `GET /target/reviews`
- **What:** List Target product reviews. Lists written reviews for a Target item given by its numeric `tcin`. Each review has its rating, title, text, author, submission time, helpful votes, and verified and syndicated flags. `page` is zero-based and stops at 50; `per_page` runs 1 to 25. The response gives `total` and `total_pages`.
- **Params:** `page` (integer, optional) — Zero-based page; `per_page` (integer, optional) — Reviews per page; `tcin` (string, **required**) — Numeric Target item id

### `target_search`

- **HTTP:** `GET /target/search`
- **What:** Search Target products. Searches Target products and returns products plus every filter group and option available for the current result set. Pass option ids back through filter_ids as a comma-separated list. A zero total with an empty products list is a valid no-results response. The sort enum accepts `relevance`, `featured`, `price-low`, `price-high`, `rating`, `bestselling`, and `newest`.
- **Params:** `filter_ids` (string, optional) — Comma-separated Target filter option ids; `page` (integer, optional) — One-based page (1-50); `q` (string, **required**) — Product search query; `sort` (string, optional) — Result order; `store_id` (integer, optional) — Target store id used for pricing

### `target_stores`

- **HTTP:** `GET /target/stores`
- **What:** Find Target stores near a location. Returns Target's physical stores near a ZIP code, a free-text "city, state", or a "latitude,longitude" pair, including each store's store_id, status, distance, phone, address, service list, time zone, and two weeks of daily opening hours. Use the returned store_id values with the store_id parameter on target-search, target-category-products, target-filter-options, and target-product.
- **Params:** `limit` (integer, optional) — Maximum stores to return (1-20); `place` (string, **required**) — ZIP code, city/state, or latitude,longitude; `within` (integer, optional) — Search radius in miles (1-5000)

## Costco (6)

### `costco_categories`

- **HTTP:** `GET /costco/categories`
- **What:** Get Costco category facets. Returns Costco category slugs and product counts relevant to an optional search term, each slug usable directly with GET /costco/search's category filter. Public data sourced from Costco's own search backend.
- **Params:** `query` (string, optional) — Search text to scope the returned categories to, e.g. \

### `costco_product`

- **HTTP:** `GET /costco/product/{id}`
- **What:** Get a Costco product's detail. Returns a Costco product's detail: title, description, manufacturer, image, price, stock status, and rating. Public data sourced from Costco's own product backend.
- **Params:** `id` (string, **required**) — Costco product id, e.g. from a search result's id field or a product page URL's \

### `costco_product_availability`

- **HTTP:** `GET /costco/product/{id}/availability`
- **What:** Get a Costco product's delivery estimate. Returns a Costco product's stock and estimated-delivery status for a delivery destination. Public data sourced from Costco's own fulfillment backend.
- **Params:** `id` (string, **required**) — Costco product id; `postal_code` (string, **required**) — US destination ZIP code; `state` (string, **required**) — US destination two-letter state code

### `costco_product_reviews`

- **HTTP:** `GET /costco/product/{id}/reviews`
- **What:** Get a Costco product's reviews. Returns a page of a Costco product's reviews: title, text, rating, author, and recommendation for each. Public data sourced from Costco's own review platform.
- **Params:** `id` (string, **required**) — Costco product id, e.g. from a search result's id field

### `costco_search`

- **HTTP:** `GET /costco/search`
- **What:** Search Costco products. Returns public Costco products matching a text query and/or a category slug: title, brand, model, image, and rating for each result. Public data sourced from Costco's own search backend.
- **Params:** `category` (string, optional) — Costco category slug, e.g. the last path segment of a category page URL; `query` (string, optional) — Search text

### `costco_warehouses`

- **HTTP:** `GET /costco/warehouses`
- **What:** Find nearby Costco warehouses. Returns Costco warehouses near a latitude/longitude, sorted by distance: name, address, and distance for each. Public data sourced from Costco's own warehouse locator backend.
- **Params:** `latitude` (number, **required**) — Latitude; `longitude` (number, **required**) — Longitude

## Zalando (6)

### `zalando_categories`

- **HTTP:** `GET /zalando/categories`
- **What:** List a Zalando market's top-level category navigation. Returns a Zalando country storefront's live top-level category navigation, department by department. This is the discovery source for zalando-category's category parameter — category slugs are market-specific (each storefront uses its own local-language slug), so there is no fixed value space to hardcode; this endpoint returns the live values instead. market is required (there is no default storefront) and accepts 25 country storefronts — see zalando-markets for the full current list with domains. department optionally restricts the response to one of women, men, or kids; omitting it returns all three. Scope note: only the top-level nav tabs (e.g. Clothing, Shoes, Sports) are returned, not each tab's own hover-revealed mega-menu of sub-categories.
- **Params:** `department` (string, optional) — Restrict to one Zalando shopping department. Omit to return all three.; `market` (string, **required**) — Zalando country storefront

### `zalando_category`

- **HTTP:** `GET /zalando/category`
- **What:** Browse a Zalando category or brand. Browses a Zalando category or brand listing by URL slug (e.g. shoes, womens-dresses, on-running) and returns the same result cards as zalando-search, plus the category's upstream total_count. Category slugs are market-specific (each storefront uses its own local-language slug, e.g. "shoes" on de/gb, "chaussures" on fr, "scarpe" on it) — use zalando-categories to discover a market's live top-level slugs, or take one from a product's url field. market is required (there is no default storefront) and accepts 25 country storefronts — see zalando-markets for the full current list with domains.
- **Params:** `category` (string, **required**) — Zalando category or brand URL slug, in the target market's own language; `market` (string, **required**) — Zalando country storefront

### `zalando_markets`

- **HTTP:** `GET /zalando/markets`
- **What:** List supported Zalando country storefronts. Returns the Zalando country storefronts currently supported by the required market parameter on zalando-search, zalando-category, and zalando-product, with each market's domain. Static metadata.
- **Params:** _none_

### `zalando_product`

- **HTTP:** `GET /zalando/product`
- **What:** Get a Zalando product. Returns product details for one Zalando product, including brand, description, images, and per-size price/availability/GTIN. Pass the sku returned by zalando-search or zalando-category; market is required and must match the storefront the sku was found in (there is no default, and a sku is generally only listed for sale on the market(s) that carry it) — see zalando-markets for the full reference list.
- **Params:** `market` (string, **required**) — Zalando country storefront the sku was found in; `sku` (string, **required**) — Zalando product SKU (article number) from zalando-search or zalando-category

### `zalando_search`

- **HTTP:** `GET /zalando/search`
- **What:** Search Zalando products. Searches a Zalando country storefront by keyword and returns result cards with price, brand, and image. Returns the first page of results plus the upstream total_count; deeper pagination is not yet supported. market is required (there is no default storefront) and accepts 25 country storefronts — see zalando-markets for the full current list with domains.
- **Params:** `market` (string, **required**) — Zalando country storefront; `q` (string, **required**) — Product search keyword

### `zalando_suggest`

- **HTTP:** `GET /zalando/suggest`
- **What:** Autocomplete a Zalando search query. Returns Zalando's own search-box query completions for a partial keyword, e.g. "running sho" -> "running shoes", "running shoes nike". market is required (there is no default storefront) and accepts 25 country storefronts — see zalando-markets for the full current list with domains.
- **Params:** `market` (string, **required**) — Zalando country storefront; `q` (string, **required**) — Partial search text to complete

## Walmart (3)

### `walmart_product`

- **HTTP:** `GET /walmart/product/{item_id}`
- **What:** Get a Walmart product. Returns a Walmart product: price, availability, brand, images, rating, seller, description, highlights, specifications, and variants.
- **Params:** `item_id` (string, **required**) — Walmart item id (the numeric id in a /ip/{id} URL)

### `walmart_product_reviews`

- **HTTP:** `GET /walmart/product/{item_id}/reviews`
- **What:** Get Walmart product reviews. Returns the reviews snapshot embedded in a Walmart product page: average rating, total review count, the per-star rating breakdown, the recommended percentage, the top positive and top negative review, and a sample of recent reviews. This is a single on-page snapshot, not a full paginated feed. A product that exists but has no reviews returns zero counts and an empty reviews list.
- **Params:** `item_id` (string, **required**) — Walmart item id (the numeric id in a /ip/{id} URL)

### `walmart_search`

- **HTTP:** `GET /walmart/search`
- **What:** Search Walmart products. Returns Walmart search results: item id, title, brand, price, image, availability, seller, and rating per product.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `q` (string, **required**) — Search query; `sort` (string, optional) — Sort order

## H&M (7)

### `hm_categories`

- **HTTP:** `GET /hm/categories`
- **What:** Browse H&M's storefront category navigation. Returns H&M's own storefront category navigation, department by department: every direct nav item and subcategory currently shown in the site's own menu, with its display name and storefront URL. Where this build has separately verified the value against hm-listing's own category_id parameter, that id is included too; category_id is omitted for entries not yet verified rather than guessed, since the visible category label is confirmed NOT a reliable way to derive H&M's real listing category ids for every category. department, when given, filters the result to one department.
- **Params:** `department` (string, optional) — Filter to one storefront department

### `hm_listing`

- **HTTP:** `GET /hm/listing`
- **What:** Browse an H&M category's product listing. Returns one H&M category's product listing page: products with pricing, images, colors, and per-size stock. category_id is an H&M category slug (e.g. ladies_newarrivals_all, men_newarrivals_all, ladies_jeans) -- there is no category/nav-tree discovery endpoint, so category_id values come from known H&M storefront paths rather than a lookup call. Pagination is page-based and real: requesting a page beyond the category's real last page returns a normal response with an empty products array rather than an error.
- **Params:** `category_id` (string, **required**) — H&M category slug; `is_new` (boolean, optional) — Optional filter for newly added items only; `page` (integer, optional) — Page number, one-based, defaults to 1; `page_size` (integer, optional) — Results per page, 1 to 72, defaults to 36; `sort` (string, optional) — Sort order, defaults to RELEVANCE

### `hm_product`

- **HTTP:** `GET /hm/product/{product_id}`
- **What:** Get an H&M product's full detail. Returns one H&M product's full detail: every purchasable color grouped with its own per-size price and live availability, plus an aggregate rating and real customer reviews (author label, date, body, rating, and any fit-feedback tags the reviewer left, such as "True to Size") when the product has any. This data is not available from hm-listing or hm-search, which only carry one representative price and a per-color stock count. product_id is the numeric id from a listing/search result's id field or its url field's productpage.<id>.html segment. An unrecognized product_id returns 404.
- **Params:** `product_id` (string, **required**) — Numeric H&M product id, from a listing/search result's id field

### `hm_product_related`

- **HTTP:** `GET /hm/product/{product_id}/related`
- **What:** Get an H&M product's related items. Returns every product-detail recommendation list H&M's own app shows for one product (which lists are present genuinely varies by product -- for example "more from series" and "style with" appear only when the product has one, while "alternatives" and "upsell" are more consistently present). An unrecognized product_id returns a well-formed empty result rather than an error.
- **Params:** `product_id` (string, **required**) — Numeric H&M product id, from a listing/search result's id field

### `hm_search`

- **HTTP:** `GET /hm/search`
- **What:** Search H&M product listings by free-text keyword. Runs a free-text keyword search on H&M and returns products with pricing, images, colors, and per-size stock, plus search-quality metadata (a spelling-correction suggestion, related searches, and a content-filter flag). Unlike category browsing, an obscure or nonsense keyword returns a genuine empty result (zero products) rather than a fallback set. Pagination is page-based and real: requesting a page beyond the real last page returns a normal response with an empty products array rather than an error.
- **Params:** `page` (integer, optional) — Page number, one-based, defaults to 1; `page_size` (integer, optional) — Results per page, 1 to 72, defaults to 36; `query` (string, **required**) — Free-text search keyword

### `hm_search_suggestions`

- **HTTP:** `GET /hm/search/suggestions`
- **What:** Get H&M search-box suggestions. Returns H&M's own search-box typeahead suggestions. When query is given, returns spelling-complete phrase suggestions and merchandised content results. When query is omitted or empty, instead returns trending searches and popular-search shortcuts (phrase/content suggestions are both empty in that mode). search_history is not session-scoped -- it returns the identical list for every request, so treat it as fixed default content rather than a real per-caller history.
- **Params:** `query` (string, optional) — Free-text search-box input; omit or leave empty for trending/popular searches instead

### `hm_stores`

- **HTTP:** `GET /hm/stores`
- **What:** Find nearby H&M physical stores. Returns H&M physical retail store locations near a point: name, phone, full address, and coordinates. Either search, or both lat and lng, is required. search is a free-text zip code or place name that is first resolved to coordinates; if it does not resolve to any location, a well-formed empty result is returned rather than an error. lat and lng, when given directly, skip that resolution step. radius_meters is optional (1000 to 50000, defaults to 10000). A location with no stores within the radius returns a well-formed empty result rather than an error.
- **Params:** `lat` (number, optional) — Latitude, requires lng; `lng` (number, optional) — Longitude, requires lat; `radius_meters` (integer, optional) — Search radius in meters, 1000 to 50000, defaults to 10000; `search` (string, optional) — Free-text zip code or place name to resolve to coordinates

## Kohl's (4)

### `kohls_category`

- **HTTP:** `GET /kohls/category`
- **What:** Browse a Kohl's category or curated campaign page. Returns a Kohl's category or curated campaign page's product grid (page 1 only), with products (title, image, colors, pricing, rating, availability) and facets for discovering further category values. category is Kohl's own catalog taxonomy string, e.g. "Room:Dorm" or "Department:Kitchen & Dining" -- combine multiple dimensions with a literal "+", percent-encoded as "%2B" so it survives as "+" rather than being decoded to a space (e.g. "Room%3ADorm%2BDepartment%3ABedding"). Every facets[].options[].category value in a response is a ready-to-use category string for a follow-up call, so a caller can discover the full taxonomy by starting from a known category (e.g. "Room:Dorm") and following facets. A category value Kohl's does not recognize returns a 404 rather than an unfiltered listing; a recognized dimension with no matching products returns a genuine zero-result response instead.
- **Params:** `category` (string, **required**) — Kohl's catalog taxonomy string, e.g. \

### `kohls_product_reviews`

- **HTTP:** `GET /kohls/product/reviews`
- **What:** Browse a Kohl's product's customer reviews. Returns one page of a Kohl's product's customer reviews (title, text, rating, secondary ratings such as quality/durability/value/style, reviewer name and location, submission date, and photo URLs). web_id is the same identifier a GET /kohls/category response's products[].web_id field carries. A web_id with zero reviews returns a genuine zero-result response rather than an error.
- **Params:** `page` (integer, optional) — Page number, 10 reviews per page (default 1); `web_id` (string, **required**) — Kohl's product web id, e.g. from a GET /kohls/category response's products[].web_id

### `kohls_stores`

- **HTTP:** `GET /kohls/stores`
- **What:** Find nearby Kohl's store locations. Returns physical Kohl's store locations near a free-text location (city/state, zip code, or address): address, phone, weekly hours, distance, and store badges/services. A search with no results returns a genuine empty list rather than an error.
- **Params:** `search` (string, **required**) — Free-text location: city/state, zip code, or address

### `kohls_suggest`

- **HTTP:** `GET /kohls/suggest`
- **What:** Kohl's search-box typeahead suggestions. Returns Kohl's own search-box typeahead result for a partial query: a flat list of suggested search phrases (no product data). A nonsense query returns a genuine, well-formed empty list rather than an error.
- **Params:** `query` (string, **required**) — Partial search text, e.g. \

## Lululemon (5)

### `lululemon_categories`

- **HTTP:** `GET /lululemon/categories`
- **What:** Browse lululemon's storefront category navigation. Returns lululemon's own storefront category navigation, flattened out of the site's shared header nav: every navigable category with its display name, breadcrumb path, and the exact category/cdp_hash pair lululemon-category's own parameters expect (read directly from the nav's own URL, not guessed from the display label). section, when given, filters the result to one top-level nav section.
- **Params:** `section` (string, optional) — Filter to one top-level storefront nav section

### `lululemon_category`

- **HTTP:** `GET /lululemon/category`
- **What:** Browse a lululemon category's product listing. Returns one lululemon category's product listing page: products with pricing, sale detection, sizes, colors, and style numbers. category and cdp_hash are the two path segments of a lululemon category URL (https://shop.lululemon.com/c/{category}/{cdp_hash}), e.g. women-new-styles and n14f1wz6o10 -- both are also available from lululemon-categories's own category and cdp_hash fields. Pagination is page-based and real: requesting a page beyond the category's real last page returns a normal response with an empty products array rather than an error. An unrecognized category/cdp_hash pair returns 404.
- **Params:** `category` (string, **required**) — lululemon category slug, from a category URL's first path segment; `cdp_hash` (string, **required**) — lululemon category id, from a category URL's second path segment; `page` (integer, optional) — Page number, one-based, defaults to 1; `page_size` (integer, optional) — Results per page, 1 to 100, defaults to 24

### `lululemon_outfit`

- **HTTP:** `GET /lululemon/outfit`
- **What:** Get lululemon's outfit/style recommendations for a product color. Returns lululemon's own curated outfit/style recommendations for one product color: every complementary item in each styled look, plus the anchor product itself. unified_id and color_code are lululemon-product's own unified_id response field and a color's code field (from lululemon-product's colors[] or lululemon-category's style_numbers-paired colors[]) -- not lululemon-product's own product_id, which is a different id space. Recommended items' own id is a separate, third-party catalog id (not lululemon-product's product_id) -- use each item's url to reach its product page. An unrecognized unified_id/color_code pair returns 404.
- **Params:** `color_code` (string, **required**) — lululemon color code, from a lululemon-product result's colors[].code field; `unified_id` (string, **required**) — lululemon product unified id, from a lululemon-product result's unified_id field

### `lululemon_product`

- **HTTP:** `GET /lululemon/product/{product_id}`
- **What:** Get a lululemon product's full detail. Returns one lululemon product's full detail: every purchasable color/size SKU with its own price, sale status, and live availability, plus an aggregate rating and real customer reviews when the product has any -- none of which lululemon-category exposes (it only carries one representative color/price per product). product_id is the id from a lululemon-category result's id field or a lululemon product URL's trailing path segment (https://shop.lululemon.com/p/{slug}/{product_id}) -- the slug itself is not needed. An unrecognized product_id returns 404.
- **Params:** `product_id` (string, **required**) — lululemon product id, from a lululemon-category result's id field

### `lululemon_stores`

- **HTTP:** `GET /lululemon/stores`
- **What:** Browse lululemon's physical store directory. Returns lululemon's own complete physical store directory (480 US and 86 Canada locations), including regular weekly hours and in-store amenities. All filters are optional and applied to the full directory. country and state are free-text equality filters against the values this directory actually carries (2-letter codes, e.g. US/CA, NY/CA), not an enforced enum. lat and lng (both required together) filter to stores within radius_miles (1 to 500, defaults to 50), sorted nearest-first.
- **Params:** `country` (string, optional) — Filter to one country by its 2-letter code; `lat` (number, optional) — Latitude, requires lng; `lng` (number, optional) — Longitude, requires lat; `radius_miles` (number, optional) — Search radius in miles, 1 to 500, defaults to 50; `state` (string, optional) — Filter to one state/province by its 2-letter code

## Macy's (3)

### `macys_product`

- **HTTP:** `GET /macys/product/{productId}`
- **What:** Get a Macy's product's full detail. Returns one Macy's product's full detail: name, brand, description, department/division, category breadcrumb, pricing (with sale detection), availability, images, aggregate rating, and every purchasable color variant with its own price. productId is a numeric id, taken from a Macy's product page's ?ID= query parameter.
- **Params:** `productId` (string, **required**) — Numeric Macy's product id, from a product page's ?ID= query parameter

### `macys_product_reviews`

- **HTTP:** `GET /macys/product/reviews`
- **What:** Get a Macy's product's customer reviews. Returns one page of a Macy's product's customer reviews, plus a site-wide rating summary (rating count, average rating, recommended ratio, rating histogram) for the product. product_id is a numeric id, the same one used by GET /macys/product/{productId}. A product with zero reviews, or a well-formed but unrecognized product_id, returns a normal, empty result rather than an error.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `product_id` (string, **required**) — Numeric Macy's product id, from a product page's ?ID= query parameter

### `macys_suggest`

- **HTTP:** `GET /macys/suggest`
- **What:** Get Macy's search-box suggestions. Returns Macy's own search-box suggestions (typeahead) for a partial query: a flat list of suggested search phrases, no product data. A partial query with no real matches returns a normal, empty result rather than an error.
- **Params:** `query` (string, **required**) — Partial search query

## Nike (9)

### `nike_categories`

- **HTTP:** `GET /nike/categories`
- **What:** List Nike's category and subcategory taxonomy. Returns Nike's full Men/Women/Kids/Jordan category and subcategory taxonomy tree, sourced directly from Nike.com's own nav mega-menu. Each top-level entry (Men, Women, Kids, Jordan) breaks down into named groups (e.g. Shoes, Clothing, Accessories, Shop By Sport -- Women additionally carries a Shop by Color group, and Jordan is organized by Men/Women/Kids instead of by product type), each with its own subcategory entries. Every subcategory (and most groups) carries a slug usable as a future category-browse endpoint's path/slug input, and is directly browsable today at https://www.nike.com/w/<slug>. This mirrors the live nav exactly, including its seasonal/promotional groups (e.g. Limited Time, New & Featured) alongside the stable structural ones -- Nike's own markup does not distinguish the two.
- **Params:** _none_

### `nike_product`

- **HTTP:** `GET /nike/product`
- **What:** Get a Nike product. Returns product-detail data for one color variant: title, description, pricing, images, every offered size, and every other available color. slug and style_color together reproduce Nike's own product page URL (nike.com/t/<slug>/<style_color>) and are both returned by nike-search's product colors[].slug and colors[].style_color fields.
- **Params:** `slug` (string, **required**) — Product-detail URL slug, from a search result's colors[].slug field; `style_color` (string, **required**) — Style-color id, from a search result's colors[].style_color field

### `nike_product_availability`

- **HTTP:** `GET /nike/product/availability`
- **What:** Get Nike product size availability. Returns per-size shipping availability for one product, sourced from the same anonymous mobile backend Nike's own app uses. group_key is the product's rollup key (from a search result's products[].group_key field). Each size carries its label, localized label, the color variant it belongs to, a GTIN, an available flag, Nike's own shipping-availability level (HIGH/LOW/MEDIUM/OOS), and the width grouping (Regular/Wide). Per-store pickup availability is not included -- this reflects online shipping availability.
- **Params:** `group_key` (string, **required**) — Product rollup key, from a search result's products[].group_key field

### `nike_product_details`

- **HTTP:** `GET /nike/product/details`
- **What:** Get full Nike product details. Returns full product-group detail for one product's rollup key, sourced from the same anonymous mobile backend Nike's own app uses: shared product copy plus every purchasable color variant (across width groupings), each with its own pricing, sizes, and images. group_key is the product's rollup key, the same value nike-search returns as a products[].group_key field. Unlike nike-product (which returns one color variant by slug/style_color), this returns every color of the product in one response.
- **Params:** `group_key` (string, **required**) — Product rollup key, from a search result's products[].group_key field

### `nike_product_recommendations`

- **HTTP:** `GET /nike/product/recommendations`
- **What:** Get Nike product recommendations. Returns Nike's own related-product ("Shop Similar") recommendations for one product, sourced from the same anonymous mobile backend Nike's own app uses. style_color is the anchor product's style-color id (from a search result's colors[].style_color field). Each recommendation carries the product's style-color, rank, title/subtitle, image, PDP URL, and current pricing. Recommendations are Nike's own ranking, not a guaranteed keyword match: an unrecognized style_color returns Nike's fallback recommendations rather than an empty list or an error.
- **Params:** `style_color` (string, **required**) — Anchor product's style-color id, from a search result's colors[].style_color field

### `nike_product_reviews`

- **HTTP:** `GET /nike/product/reviews`
- **What:** Get Nike product reviews. Returns one page of a Nike product's customer reviews, plus an aggregate rating summary (average rating and a per-star rating breakdown) that Nike's own product-detail endpoint does not otherwise expose. slug and style_color are the same values nike-product accepts (from a search result's colors[].slug/colors[].style_color fields). A product with no reviews yet returns a well-formed empty result rather than an error. Requesting a page beyond the available result pages returns a not-found error.
- **Params:** `page` (integer, optional) — One-based page number, defaults to 1; `slug` (string, **required**) — Product-detail URL slug, from a search result's colors[].slug field; `style_color` (string, **required**) — Style-color id, from a search result's colors[].style_color field

### `nike_search`

- **HTTP:** `GET /nike/search`
- **What:** Search or browse Nike products. Searches Nike.com product listings by keyword, or browses a category/subcategory listing by slug, with real pagination. Exactly one of keyword or category is required. Returns product groups with pricing, colorway images, and every purchasable color variant, plus filter and subcategory navigation data (facet_nav) already present on the same response -- both keyword search and a category listing's first page include filter groups (Gender, Color, Price, Size, and similar); only a category listing includes a breadcrumb trail and subcategory drill-down options, and only its first page (a category listing's later pages do not repeat navigation data). Keyword search is best-effort relevance, not a guaranteed keyword match: for an obscure or nonsense keyword, Nike's own search index falls back to its own recommended results instead of returning an empty list, and there is currently no reliable signal in the response to distinguish a true keyword match from that fallback behavior. A keyword Nike's own search router treats as structurally empty (for example a punctuation-only query) does return a genuine empty result. Category values come from nike-categories' own slug field, or from a prior response's own facet_nav navigation paths (with the leading /w/ stripped). Requesting a page beyond the available result pages returns a not-found error.
- **Params:** `category` (string, optional) — Category/subcategory browse slug, from nike-categories' own slug field or a prior response's facet_nav navigation. Exactly one of keyword or category is required.; `keyword` (string, optional) — Search keyword. Exactly one of keyword or category is required.; `page` (integer, optional) — One-based page number, defaults to 1

### `nike_stores`

- **HTTP:** `GET /nike/stores`
- **What:** Find nearby Nike stores. Searches Nike's physical retail store locator by coordinates and radius. Returns each nearby store's name, address, phone, coordinates, distance, and store page URL. A location with no nearby stores within the given radius returns a well-formed empty result.
- **Params:** `lat` (number, **required**) — Latitude, -90 to 90; `lng` (number, **required**) — Longitude, -180 to 180; `page` (integer, optional) — One-based page number, defaults to 1; `radius_miles` (integer, optional) — Search radius in miles, defaults to 50

### `nike_suggest`

- **HTTP:** `GET /nike/suggest`
- **What:** Get Nike search-box suggestions. Returns Nike's own search-box suggestions (typeahead) for a partial query, the same "Top Suggestions" list shown while typing into Nike's search box: a flat list of suggested search phrases, no product data.
- **Params:** `query` (string, **required**) — Partial search query

## Old Navy (7)

### `oldnavy_categories`

- **HTTP:** `GET /oldnavy/categories`
- **What:** List Old Navy storefront categories. Lists Old Navy's own storefront navigation as name/cid pairs, resolving the cid-discovery gap oldnavy-search, oldnavy-product, and oldnavy-category all document. Omit cid to list Old Navy's top-level divisions (e.g. Women, Men, Boys, Toddler). Pass a cid (a division's own, or any deeper category's) to list the related categories for that part of the storefront instead, in the same order the live storefront menu shows them -- this is section-level, not necessarily unique per leaf category. Currently only available for brand=on (Old Navy).
- **Params:** `brand` (string, optional) — Storefront to list -- only on (Old Navy) is currently supported; `cid` (string, optional) — Category id to list related categories for; omit to list the top-level divisions

### `oldnavy_category`

- **HTTP:** `GET /oldnavy/category`
- **What:** Browse an Old Navy, Gap, Banana Republic, or Athleta category. Returns a category/browse listing for one storefront category id (cid). cid is an opaque Gap Inc category id assigned by the storefront's own navigation -- neither oldnavy-search nor oldnavy-category currently surface a category-id list, so find one from the storefront's own category page URLs (the cid query parameter on a /browse/... page) for now. Select the storefront with the brand parameter (`on` for Old Navy, `gap` for Gap, `br` for Banana Republic, `at` for Athleta; defaults to `on`) -- it must match the brand the cid was found under. Returns the category's subcategory breakdown, product summaries with per-color inventory data, and available search facets with live counts.
- **Params:** `brand` (string, optional) — Storefront to browse; `cid` (string, **required**) — Category id, from a storefront category page's own cid query parameter; `page` (integer, optional) — One-based page

### `oldnavy_product`

- **HTTP:** `GET /oldnavy/product`
- **What:** Get an Old Navy, Gap, Banana Republic, or Athleta product. Returns product-detail data for one color variant: name, description, images, aggregate rating, and every size offered in that color as a separate priced offer. pid is a color-specific product id, as returned by oldnavy-search's product colors[].id field (not the bare base product id). Select the storefront with the brand parameter (`on` for Old Navy, `gap` for Gap, `br` for Banana Republic, `at` for Athleta; defaults to `on`) -- it must match the brand the pid was found under.
- **Params:** `brand` (string, optional) — Storefront the pid belongs to; `pid` (string, **required**) — Color-specific product id, from a search result's colors[].id field

### `oldnavy_product_availability`

- **HTTP:** `GET /oldnavy/product/availability`
- **What:** Check in-store pickup stock for an Old Navy, Gap, Banana Republic, or Athleta product. Checks per-size, in-store pickup stock status for one color (pid) at one or more physical stores. pid matches oldnavy-product's own color-level id. Give store location either directly with store_id (one or more comma-separated store ids, e.g. from a prior call to this endpoint or a value you already have) or with zip or both lat and lng, which resolves the nearest stores automatically. Select the storefront with the brand parameter (`on` for Old Navy, `gap` for Gap, `br` for Banana Republic, `at` for Athleta; defaults to `on`). Each returned store lists every offered size's stock status: `in_stock`, `out_of_stock`, or `low_stock`.
- **Params:** `brand` (string, optional) — Storefront to check; `lat` (number, optional) — Latitude to resolve the nearest stores from (must be given together with lng); `lng` (number, optional) — Longitude to resolve the nearest stores from (must be given together with lat); `pid` (string, **required**) — Color-level Old Navy/Gap/Banana Republic/Athleta product id; `store_id` (string, optional) — One or more comma-separated numeric store ids; `zip` (string, optional) — Zip code to resolve the nearest stores from

### `oldnavy_product_reviews`

- **HTTP:** `GET /oldnavy/product/reviews`
- **What:** Get reviews for an Old Navy, Gap, Banana Republic, or Athleta product. Returns one page of a product's customer reviews (author, date, rating, headline, body, and verified-purchase flag), plus the product's overall rating summary (average rating, rating count, per-star histogram, and recommended ratio). pid is a color-specific product id, as returned by oldnavy-search's product colors[].id field (not the bare base product id) -- the same pid oldnavy-product accepts. Select the storefront with the brand parameter (`on` for Old Navy, `gap` for Gap, `br` for Banana Republic, `at` for Athleta; defaults to `on`) -- it must match the brand the pid was found under. A product with no reviews yet returns a well-formed empty result, not an error.
- **Params:** `brand` (string, optional) — Storefront the pid belongs to; `page` (integer, optional) — One-based page, 10 reviews per page; `pid` (string, **required**) — Color-specific product id, from a search result's colors[].id field

### `oldnavy_search`

- **HTTP:** `GET /oldnavy/search`
- **What:** Search Old Navy, Gap, Banana Republic, or Athleta products. Searches product listings across Old Navy, Gap, Banana Republic, and Athleta -- select the storefront with the brand parameter (`on` for Old Navy, `gap` for Gap, `br` for Banana Republic, `at` for Athleta; defaults to `on`). Returns product summaries with pricing, review scores, and every purchasable color variant. This search is best-effort relevance, not a guaranteed keyword match: for an obscure or nonsense keyword the upstream search index falls back to its own recommended results instead of returning an empty list, and there is currently no reliable signal in the response to distinguish a true keyword match from that fallback behavior.
- **Params:** `brand` (string, optional) — Storefront to search; `keyword` (string, **required**) — Search keyword; `page` (integer, optional) — One-based page

### `oldnavy_stores`

- **HTTP:** `GET /oldnavy/stores`
- **What:** Find Old Navy, Gap, Banana Republic, or Athleta store locations. Searches physical store locations for one storefront by free-text search (zip code or city) and/or coordinates. Provide search, or both lat and lng. Select the storefront with the brand parameter (`on` for Old Navy, `gap` for Gap, `br` for Banana Republic, `at` for Athleta; defaults to `on`). Returns each nearby store's name, full address, phone number, coordinates, distance, and specialties (e.g. "In-Store Shopping", "Outlet"). This is location search only -- it does not report per-item, per-store stock levels; use oldnavy-product-availability for that.
- **Params:** `brand` (string, optional) — Storefront to search; `lat` (number, optional) — Latitude (must be given together with lng); `lng` (number, optional) — Longitude (must be given together with lat); `search` (string, optional) — Zip code or city to search near

## Sam's Club (5)

### `samsclub_category`

- **HTTP:** `GET /samsclub/category`
- **What:** Browse a Sam's Club category or collection. Returns a Sam's Club category or collection page's product grid, with real page-based pagination. id accepts a bare numeric category id (from a nav link's /browse/{id} URL) or a full /browse/{slug}/{id} URL copied from samsclub.com -- only the trailing id is used. Returns products with name, brand, pricing, availability, rating, and image. An id samsclub.com does not recognize returns a genuine zero-result response rather than an error.
- **Params:** `id` (string, **required**) — Sam's Club category id, or a /browse/{slug}/{id} URL; `page` (integer, optional) — Result page, 1-based, defaults to 1

### `samsclub_content`

- **HTTP:** `GET /samsclub/content/{id}`
- **What:** Get a Sam's Club curated content or landing page. Returns one Sam's Club curated content/landing page (e.g. a seasonal savings hub or a "New Arrivals" page) -- distinct data from GET /samsclub/category's flat, paginated product grid. id accepts a bare numeric content page id (from a nav link's /cp/{id} URL) or a full /cp/{slug}/{id} URL copied from samsclub.com -- only the trailing id is used. Returns a title, breadcrumb, named curated product shelves, and a category-navigation tile grid. There is no pagination -- a content page's shelves are a fixed, hand-curated set. An id samsclub.com does not recognize returns a 404, unlike GET /samsclub/category's zero-result response for the same situation.
- **Params:** `id` (string, **required**) — Numeric Sam's Club content page id, from a /cp/{slug}/{id} URL

### `samsclub_departments`

- **HTTP:** `GET /samsclub/departments`
- **What:** List Sam's Club departments and categories. Returns Sam's Club's full department/category taxonomy, as shown on its own "All Departments" page: every top-level department with its own subcategory list. Each link's type is "browse" (pairs directly with GET /samsclub/category), "cp" (a content/landing page that does not reliably carry a product grid), or empty (an unrecognized link shape).
- **Params:** _none_

### `samsclub_product`

- **HTTP:** `GET /samsclub/product/{id}`
- **What:** Get a Sam's Club product's full detail. Returns one Sam's Club product's full detail: name, brand, description, category breadcrumb, pricing, availability, images, aggregate rating and review count, and the club's own item number. id is the numeric product id from a Sam's Club product page's /ip/ URL.
- **Params:** `id` (string, **required**) — Numeric Sam's Club product id, from a product page's /ip/{slug}/{id} URL

### `samsclub_product_related`

- **HTTP:** `GET /samsclub/product/{id}/related`
- **What:** Get a Sam's Club product's related items. Returns the related-item carousels shown on a Sam's Club product page, each a named shelf (e.g. "Members also considered", "Items you may like") of products with pricing, rating, and image. id is the numeric product id from a Sam's Club product page's /ip/ URL. An unrecognized id is not distinguished from a known one -- it still returns generic fallback shelves rather than an error.
- **Params:** `id` (string, **required**) — Numeric Sam's Club product id, from a product page's /ip/{slug}/{id} URL

## Ulta Beauty (8)

### `ulta_categories`

- **HTTP:** `GET /ulta/categories`
- **What:** List Ulta Beauty storefront categories. Lists Ulta Beauty's own storefront category navigation: department, group, name, and a URL usable directly as GET /ulta/category's own category parameter. Closes the discovery gap of not already knowing a category path. department, if set, filters to just that department's entries. group is empty for a department's own top-level link or a group's own heading link, and set to that group's name for the leaf categories nested under it. The exact same real category can legitimately appear more than once under a different department/group when the site's own navigation cross-lists it.
- **Params:** `department` (string, optional) — Filter to one department

### `ulta_category`

- **HTTP:** `GET /ulta/category`
- **What:** Browse an Ulta Beauty category page. Browses an Ulta Beauty category page's product grid, with real page-based pagination and the category's own guided-navigation refinement options. category accepts a category path or full URL copied from Ulta's own site navigation (e.g. shop/makeup/eyes/mascara). filter narrows results using Ulta's own guided-navigation facet-code shape (e.g. BENEFIT--WATERPROOF, or a comma-joined combination of codes) -- discover valid codes for a category from that category's own response facets field, whose value is ready to use directly as this parameter. An unrecognized category returns 404.
- **Params:** `category` (string, **required**) — Ulta category path or URL; `filter` (string, optional) — Guided-navigation facet code(s), comma-joined for multiple; `page` (integer, optional) — Result page, 1-based, defaults to 1

### `ulta_product`

- **HTTP:** `GET /ulta/product/{productId}`
- **What:** Get an Ulta Beauty product's full detail. Returns one Ulta Beauty product's full detail: name, brand, description, category, pricing, rating, review count, images, and every purchasable color/shade variant. productId is taken from a search result's product_id field or a product page's URL (e.g. pimprod2020260). sku is optional and selects a specific color/shade variant; an omitted or invalid sku still resolves the base product using its own default variant. An unrecognized productId returns 404.
- **Params:** `productId` (string, **required**) — Ulta product id, from a search result's product_id field; `sku` (string, optional) — Numeric Ulta sku id selecting a specific color/shade variant

### `ulta_product_questions`

- **HTTP:** `GET /ulta/product/questions`
- **What:** Get an Ulta Beauty product's customer questions and answers. Returns one page of an Ulta Beauty product's customer questions, each with every answer it received. product_id is taken from a search result's product_id field or a product page's URL. A product with zero questions, or a well-formed but unrecognized product_id, returns a normal, empty result rather than an error.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `product_id` (string, **required**) — Ulta product id, from a search result's product_id field

### `ulta_product_reviews`

- **HTTP:** `GET /ulta/product/reviews`
- **What:** Get an Ulta Beauty product's customer reviews. Returns one page of an Ulta Beauty product's customer reviews, plus the retailer's own site-wide rating summary (rating count, average rating, recommended ratio, rating histogram) for the product. product_id is taken from a search result's product_id field or a product page's URL. A product with zero reviews, or a well-formed but unrecognized product_id, returns a normal, empty result rather than an error.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `product_id` (string, **required**) — Ulta product id, from a search result's product_id field

### `ulta_search`

- **HTTP:** `GET /ulta/search`
- **What:** Search Ulta Beauty products. Searches Ulta Beauty's product catalog by keyword, with real page-based pagination. Returns products with brand, pricing, rating, and review count. An unrecognized/nonsense keyword returns a genuine empty result rather than a fallback set. Requesting a page beyond the available results returns a normal, empty result rather than an error.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `query` (string, **required**) — Search keyword

### `ulta_stores`

- **HTTP:** `GET /ulta/stores`
- **What:** Find nearby Ulta Beauty physical stores. Returns Ulta Beauty physical retail store locations near a point: name, phone, full address, hours, services, and coordinates. Either search, or both lat and lng, is required. search is a free-text zip code, city, or address that is first resolved to coordinates; if it does not resolve to any location, a well-formed empty result is returned rather than an error. lat and lng, when given directly, skip that resolution step. radius_meters is optional (1000 to 50000, defaults to 25000). A location with no stores within the radius returns a well-formed empty result rather than an error.
- **Params:** `lat` (number, optional) — Latitude, requires lng; `lng` (number, optional) — Longitude, requires lat; `radius_meters` (integer, optional) — Search radius in meters, 1000 to 50000, defaults to 25000; `search` (string, optional) — Free-text zip code, city, or address to resolve to coordinates

### `ulta_suggest`

- **HTTP:** `GET /ulta/suggest`
- **What:** Get Ulta Beauty search suggestions. Returns Ulta Beauty's own search-suggestion (typeahead) result for a partial search term: suggested search terms, each with its own top product matches, plus a featured top result matching what a real user sees at the top of the dropdown. A partial term with no matches returns a normal, empty result rather than an error.
- **Params:** `query` (string, **required**) — Partial search term

## Wayfair (3)

### `wayfair_categories`

- **HTTP:** `GET /wayfair/categories`
- **What:** List Wayfair categories. Returns a page of Wayfair categories discovered from Wayfair's own published sitemap, closing the discovery gap where a category id otherwise has to be found elsewhere. Pair a returned id with GET /wayfair/category to browse that category's product grid. name is derived from the category's own URL slug (title-cased), not an authoritative site-provided label. q, if set, case-insensitively filters to categories whose derived name or department contains it.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `page_size` (integer, optional) — Results per page, defaults to 100, max 1000; `q` (string, optional) — Case-insensitive substring filter on name or department

### `wayfair_category`

- **HTTP:** `GET /wayfair/category`
- **What:** Browse a Wayfair category. Returns a Wayfair category page's product grid, with real page-based pagination. category accepts a bare Wayfair category id ("478390"), a "c"-prefixed id ("c478390"), a category slug ("office-chairs-c478390"), or a full category URL copied from wayfair.com. Returns products with name, brand, pricing, and image.
- **Params:** `category` (string, **required**) — Wayfair category id, slug, or URL; `page` (integer, optional) — Result page, 1-based, defaults to 1

### `wayfair_product`

- **HTTP:** `GET /wayfair/product/{id}`
- **What:** Get a Wayfair product's full detail. Returns one Wayfair product's full detail: name, brand, price, stock status, aggregate rating with a 1-5 star breakdown, images, every selectable variant option (e.g. color, finish), and site-selected feature highlights. id is the product's own "W"-prefixed id (e.g. W100794312), taken from a category result's product_id field or a product page's URL. An unrecognized id returns 404.
- **Params:** `id` (string, **required**) — Wayfair product id, starting with W

## Wish (6)

### `wish_categories`

- **HTTP:** `GET /wish/categories`
- **What:** Get Wish's category and filter navigation tree. Returns Wish's own top navigation/category tree (e.g. "Popular", "Deals Hub", "Fashion", "Gadgets") plus each category's nested filter groups (e.g. Color, Rating) where present. This is a static, site-wide taxonomy -- it takes no input and its result does not vary by search term or category.
- **Params:** _none_

### `wish_product`

- **HTTP:** `GET /wish/product/{id}`
- **What:** Get a Wish product's full detail. Returns one Wish product's full detail: name, description, sold-out state, aggregate rating, image URLs, and every purchasable variation with its own price, currency, inventory, and merchant. id is taken from a search result's product_id field or a product page's URL. An unrecognized id returns 404.
- **Params:** `id` (string, **required**) — Wish product id, a 24-character hex id from a search result's product_id field

### `wish_product_related`

- **HTTP:** `GET /wish/product/{id}/related`
- **What:** Get a Wish product's related items. Returns a Wish product's related-item rails: shelves of similar products, grouped by rail (e.g. general similar items, a faster-shipping-eligible subset). id is taken from a search result's product_id field or a product page's URL. A faster-shipping rail with no eligible items, or a nonexistent id, returns a normal, empty result rather than an error.
- **Params:** `count` (integer, optional) — Number of items to return per rail, 1 to 70, defaults to 10; `id` (string, **required**) — Wish product id, a 24-character hex id from a search result's product_id field

### `wish_product_reviews`

- **HTTP:** `GET /wish/product/{id}/reviews`
- **What:** Get a Wish product's customer reviews. Returns a Wish product's customer reviews. id is taken from a search result's product_id field or a product page's URL. A product with zero reviews returns a normal, empty result rather than an error. A caller wanting more reviews should re-request with a larger count -- this endpoint does not support an offset/cursor parameter.
- **Params:** `count` (integer, optional) — Number of reviews to return, 1 to 200, defaults to 10; `id` (string, **required**) — Wish product id, a 24-character hex id from a search result's product_id field

### `wish_search`

- **HTTP:** `GET /wish/search`
- **What:** Search Wish products. Searches Wish's product catalog by keyword, with real offset-based pagination. Returns products with price, currency, rating, review count, and merchant id. A query with no matches returns a normal, empty result rather than an error.
- **Params:** `count` (integer, optional) — Number of results per page, 1 to 70, defaults to 30; `offset` (integer, optional) — Result offset, 0-based, defaults to 0, must be an exact multiple of count up to 3 * count; `query` (string, **required**) — Search keyword

### `wish_suggest`

- **HTTP:** `GET /wish/suggest`
- **What:** Get Wish search suggestions. Returns Wish's own search-suggestion (typeahead) result for a partial search term: a flat list of suggested search terms, no product data. A partial term with no matches returns a normal, empty result rather than an error.
- **Params:** `query` (string, **required**) — Partial search term

## Zappos (5)

### `zappos_brand`

- **HTTP:** `GET /zappos/brand`
- **What:** Browse a Zappos brand. Returns a Zappos brand page's product grid, with real page-based pagination and per-field filter facets. brand accepts a full brand URL copied from zappos.com, the "slug/id.zso" path from that URL, or just the opaque id from a GET /zappos/brands result's own id field. An unrecognized brand returns 404.
- **Params:** `brand` (string, **required**) — Zappos brand URL, slug/id.zso path, or opaque id; `page` (integer, optional) — Result page, 1-based, defaults to 1

### `zappos_brands`

- **HTTP:** `GET /zappos/brands`
- **What:** List Zappos brands. Returns a page of Zappos brands discovered from Zappos's own published sitemap, closing the discovery gap where a brand id otherwise has to be found elsewhere. Pair a returned id or url with GET /zappos/brand to browse that brand's product grid. name is derived from the brand's own URL slug (title-cased), not an authoritative site-provided label. q, if set, case-insensitively filters to brands whose derived name or slug contains it.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `page_size` (integer, optional) — Results per page, defaults to 100, max 1000; `q` (string, optional) — Case-insensitive substring filter on name or slug

### `zappos_product`

- **HTTP:** `GET /zappos/product/{productId}`
- **What:** Get a Zappos product's full detail. Returns one Zappos product's full detail: name, brand, description, category, breadcrumbs, pricing, images, aggregate rating with a 1-5 star breakdown, up to two featured customer reviews with real author/date/body/rating, reviewer-submitted fit feedback for size/width/arch (each response option's own share of respondents plus the most common answer), and every sibling color variant with its own price. productId is taken from a search result's product_id field or a product page's URL. colorId is optional and selects a specific color variant; an omitted or invalid colorId still resolves the base product using a real color variant rather than failing. An unrecognized productId returns 404.
- **Params:** `colorId` (string, optional) — Zappos color id selecting a specific color variant; `productId` (string, **required**) — Zappos product id, from a search result's product_id field

### `zappos_search`

- **HTTP:** `GET /zappos/search`
- **What:** Search Zappos products. Searches Zappos's product catalog by keyword, with real page-based pagination. Returns products with brand, pricing, sale status, rating, and review count, plus filterable facets (gender, department, shoe size, and more) each with a live result count and its own drill-down URL. Requesting a page beyond the available results returns a normal, empty result rather than an error.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `term` (string, **required**) — Search keyword

### `zappos_suggest`

- **HTTP:** `GET /zappos/suggest`
- **What:** Get Zappos search-box suggestions. Returns Zappos's own search-box suggestions (typeahead) for a partial query: a flat list of suggested search phrases, no product data. A partial query with no real matches returns a normal, empty result rather than an error.
- **Params:** `query` (string, **required**) — Partial search query

## Zara (6)

### `zara_categories`

- **HTTP:** `GET /zara/categories`
- **What:** List Zara's category and subcategory taxonomy. Returns Zara's full category and subcategory navigation tree for the US storefront (WOMAN, MAN, KID, and other top-level sections), sourced directly from Zara's own category navigation data. Each entry's id is the value to pass as categoryId to zara-category-products. Takes no query parameters.
- **Params:** _none_

### `zara_category_products`

- **HTTP:** `GET /zara/category/{categoryId}/products`
- **What:** Browse a Zara category's product listing. Returns a Zara category's full product listing: products with pricing, images, and availability. categoryId is a numeric id from zara-categories. Zara does not paginate this data -- the response always contains the category's complete listing in one call, not one page of it. Each entry represents one purchasable color variant rather than a color-grouped product family.
- **Params:** `categoryId` (string, **required**) — Numeric Zara category id, from zara-categories' id field

### `zara_product`

- **HTTP:** `GET /zara/product/{productId}`
- **What:** Get a Zara product's full detail. Returns one Zara product's full detail: every purchasable color variant with its real marketing description, per-size stock, and full image gallery -- richer than the per-product summaries returned by zara-category-products and zara-search. productId is a numeric id, taken from a search/category result's url field (the digits after "-p" in the product-detail URL). An unrecognized productId returns 404.
- **Params:** `productId` (string, **required**) — Numeric Zara product id, from a search/category result's url field

### `zara_search`

- **HTTP:** `GET /zara/search`
- **What:** Search Zara products. Searches Zara product listings by keyword within one department section, with real offset-based pagination. Returns products with pricing, images, availability, and every purchasable color variant, plus the search facets. This search is best-effort relevance, not a guaranteed keyword match: for an obscure or nonsense keyword, Zara's own search falls back to a broader recommended result set instead of returning an empty list, and there is no reliable field in the response to distinguish a true keyword match from that fallback behavior. Requesting an offset beyond the available results returns a normal, empty result with is_last_page true rather than an error.
- **Params:** `limit` (integer, optional) — Results per request, 1 to 100, defaults to 24; `offset` (integer, optional) — Zero-based result offset, defaults to 0; `query` (string, **required**) — Search keyword; `section` (string, **required**) — Department section to search

### `zara_stores`

- **HTTP:** `GET /zara/stores`
- **What:** Find nearby Zara physical stores. Returns Zara physical retail stores near a location: name, full address, phone, coordinates, opening hours status, pickup/donation eligibility, and a canonical store page URL. lat and lng are both required -- this endpoint does not accept a free-text zip/city search. A location with no stores within the radius returns a normal response with an empty stores array rather than an error.
- **Params:** `donation_only` (boolean, optional) — Only return stores that accept clothing donations; `lat` (number, **required**) — Latitude; `lng` (number, **required**) — Longitude; `pickup_only` (boolean, optional) — Only return stores that support in-store pickup; `radius` (integer, optional) — Search radius in miles, 1 to 500, defaults to 30

### `zara_suggest`

- **HTTP:** `GET /zara/suggest`
- **What:** Get Zara search-box suggestions for a partial keyword. Returns Zara's own search-suggestion (typeahead) results for a partial keyword, the same suggestions shown while typing into Zara's search box. A nonsense query returns a normal response with an empty suggestions array rather than a fallback/recommended set.
- **Params:** `query` (string, **required**) — Partial search keyword

## Adidas (7)

### `adidas_product`

- **HTTP:** `GET /adidas/product`
- **What:** Get an Adidas product. Returns product-detail data for one Adidas SKU: name, brand, category, description, pricing (current/standard/sale), images, and every purchasable size variant. product_id is the Adidas SKU (e.g. JI0397), taken from a search result's products[].id field or the trailing segment of an Adidas product page URL. An unknown product_id returns a not-found error.
- **Params:** `product_id` (string, **required**) — Adidas SKU/product id, from a search result's products[].id field

### `adidas_product_review_topics`

- **HTTP:** `GET /adidas/product/review-topics`
- **What:** Get Adidas review topics for a product. Returns the topics an Adidas product model's customer reviews can be filtered by -- the "filter by topic" chips the product page shows, commonly satisfaction, comfort, color, purchase, fit, appearance, quality and style. Feed a topics[].topic value back to /adidas/product/reviews as its topic parameter to return only reviews about that aspect. The topic vocabulary is per model, not a fixed list: a shoe exposes fit and comfort topics that an accessory does not, so read it per model rather than hard-coding it. model_number is the Adidas model number (e.g. SAMBAU2312) -- NOT the SKU: take it from an adidas_search result's products[].model_number field. A model with no reviews, including a well-formed but unrecognized model_number, returns an empty topics list rather than an error. Note the label field is a display form of topic, not translated text: Adidas returns the same English values for every locale on this route.
- **Params:** `locale` (string, optional) — Locale accepted for consistency with the reviews endpoint. Allowed values: cs_CZ, da_DK, de_AT, de_CH, de_DE, el_GR, en_AE, en_AU, en_CA, en_GB, en_IE, en_IL, en_IN, en_NZ, en_PH, en_SG, en_US, en_ZA, es_AR, es_CL, es_CO, es_ES, es_MX, es_PE, fr_BE, fr_CA, fr_CH, fr_FR, id_ID, it_CH, it_IT, ja_JP, ko_KR, nl_BE, nl_NL, pl_PL, pt_BR, pt_PT, ru_RU, sk_SK, sv_SE, th_TH, tr_TR, zh_HK, zh_TW. Defaults to en_US. Note Adidas returns the same English topic labels regardless of this value.; `model_number` (string, **required**) — Adidas model number, from an adidas_search result's products[].model_number field

### `adidas_product_reviews`

- **HTTP:** `GET /adidas/product/reviews`
- **What:** Get Adidas product reviews. Returns one page of customer reviews for an Adidas product model, plus the model's rating summary: overall rating, star histogram, percentage of reviewers who recommend it, per-attribute averages (Size, Width, Comfort, Quality with their own scale labels), and Adidas's AI-generated review digest when one exists. Each review carries the rating, headline, body, author nickname, purchased colorway, helpful/not-helpful vote counts, badges, customer photos, and submission time. model_number is the Adidas model number (e.g. SAMBAU2312) -- NOT the SKU: take it from an adidas_search result's products[].model_number field, which is a different value from products[].id. Reviews are returned 10 per page. Reviews are scoped to review text written in the requested locale's language, and most of the US catalog's reviews are English, so a non-English locale commonly returns rating statistics and a localized summary with an empty reviews list. A model with no reviews -- including a well-formed but unrecognized model_number -- returns an empty reviews list rather than an error, because Adidas answers 200 with a zero count rather than 404.
- **Params:** `locale` (string, optional) — Locale for the review-summary language, the secondary-rating scale labels, and the language of the reviews returned. Allowed values: cs_CZ, da_DK, de_AT, de_CH, de_DE, el_GR, en_AE, en_AU, en_CA, en_GB, en_IE, en_IL, en_IN, en_NZ, en_PH, en_SG, en_US, en_ZA, es_AR, es_CL, es_CO, es_ES, es_MX, es_PE, fr_BE, fr_CA, fr_CH, fr_FR, id_ID, it_CH, it_IT, ja_JP, ko_KR, nl_BE, nl_NL, pl_PL, pt_BR, pt_PT, ru_RU, sk_SK, sv_SE, th_TH, tr_TR, zh_HK, zh_TW. Defaults to en_US.; `model_number` (string, **required**) — Adidas model number, from an adidas_search result's products[].model_number field; `page` (integer, optional) — One-based page number, 10 reviews per page, defaults to 1; `rating` (integer, optional) — Return only reviews with this star rating. Allowed values: 1, 2, 3, 4, 5. Omitted returns every rating.; `topic` (string, optional) — Return only reviews about one topic. Valid values are per-model -- read them from /adidas/product/review-topics for the same model_number (commonly satisfaction, comfort, color, purchase, fit, appearance, quality, style). An unrecognized topic returns a 400 listing the model's own topics.

### `adidas_search`

- **HTTP:** `GET /adidas/search`
- **What:** Search or browse Adidas products. Searches Adidas.com product listings by keyword, or browses a category listing by taxonomy slug, with real pagination and sort options. Exactly one of query or category is required. Returns product summaries (title, price, rating, images, color variants) plus facet filter groups, sort options, and (for category browse) a breadcrumb trail. Keyword search is best-effort relevance, not a guaranteed match: an obscure keyword returns whatever Adidas's own search index surfaces. A genuinely empty keyword search returns an empty product list, and requesting a page beyond the available result pages (or an unknown category) returns a not-found error. Category values are the path segment after /us/ in an Adidas category URL (e.g. women-athletic_sneakers); they can also be read from the url fields of a search/category response's own filters and breadcrumbs. Facets are applied by composing them into the category slug rather than by a separate parameter: each filters[].values[].slug is a token you splice into the category value (e.g. category=women-black-athletic_sneakers applies the Color=Black facet, and category=women-athletic_sneakers-prime applies Shipping=PRIME). Use filters[].key (the facet's stable name, e.g. searchcolor) rather than filters[].id, which is an opaque per-deployment UUID that cannot be used to build a request. Note the token's position within the slug varies by facet, so compose from a slug you have seen rather than assuming a fixed order.
- **Params:** `category` (string, optional) — Category/taxonomy slug, the path segment after /us/ in an Adidas category URL. Exactly one of query or category is required.; `page` (integer, optional) — One-based page number, defaults to 1; `query` (string, optional) — Search keyword. Exactly one of query or category is required.; `sort` (string, optional) — Sort order. Allowed values: price-low-to-high, newest-to-oldest, top-sellers, price-high-to-low. Omitted means relevance.

### `adidas_store`

- **HTTP:** `GET /adidas/store`
- **What:** Get an Adidas store. Returns detail for one Adidas retail store: name, status, phone, description, full address, coordinates, opening hours, and in-store services (e.g. Click and Collect, Free Wi-Fi). store_id is the numeric Adidas store id, taken from an adidas-stores response's stores[].id field. An unknown store_id returns a not-found error.
- **Params:** `store_id` (string, **required**) — Adidas store id, from a stores response's stores[].id field

### `adidas_stores`

- **HTTP:** `GET /adidas/stores`
- **What:** Find nearby Adidas stores. Returns Adidas physical retail stores nearest to a coordinate, sourced from Adidas's own store-finder API: name, address, phone, coordinates, distance in miles, opening hours, and in-store feature flags. lat and lng are both required. Adidas's upstream ignores a caller-supplied radius and returns the nearest ~20 stores ordered by distance. A location with no stores returns an empty list rather than an error.
- **Params:** `lat` (number, **required**) — Latitude, -90 to 90; `lng` (number, **required**) — Longitude, -180 to 180; `page` (integer, optional) — Accepted only as 0. Adidas's store finder returns every nearby store (up to 20) in a single page, so any higher value is always empty and is rejected as an invalid parameter.

### `adidas_suggest`

- **HTTP:** `GET /adidas/suggest`
- **What:** Get Adidas search suggestions. Returns the top matching products for a partial query, the same search-as-you-type preview Adidas's own search box shows. Adidas has no separate term-autocomplete index, so each suggestion is a matching product (id, title, url, image, price) rather than a completed search phrase. Best-effort relevance: an obscure query returns whatever Adidas's own search surfaces.
- **Params:** `query` (string, **required**) — Partial search query

## Best Buy (11)

### `bestbuy_brands`

- **HTTP:** `GET /bestbuy/brands`
- **What:** Get Best Buy's full brand directory. Returns Best Buy's full brand directory (name, category id, url), sourced from the site's own "Name Brands" page. Each id is directly usable as bestbuy_category's category_id input.
- **Params:** _none_

### `bestbuy_categories`

- **HTTP:** `GET /bestbuy/categories`
- **What:** Get Best Buy's top-level shopping departments. Returns Best Buy's current top-level Shop departments (name, category id, url). Each id is directly usable as bestbuy_category's category_id input; this is not the full category tree.
- **Params:** _none_

### `bestbuy_categories_trending`

- **HTTP:** `GET /bestbuy/categories/trending`
- **What:** Get Best Buy's fine-grained trending product-type categories. Returns Best Buy's fine-grained, often deeply-nested product-type categories (e.g. "Windows Laptops", "55-Inch TVs (55 - 64 in)", "PS5 Consoles") sourced from the homepage's own "Best Selling" section -- much more specific than bestbuy_categories' 21 current top-level departments. Each id is directly usable as bestbuy_category's category_id input.
- **Params:** _none_

### `bestbuy_category`

- **HTTP:** `GET /bestbuy/category`
- **What:** Get a Best Buy category's product listing. Returns one page (up to 24) of one Best Buy category's product listing (sku, title, url, image, price, rating, review count). category_id is a Best Buy category id, e.g. pcmcat138500050001, found in a category page URL's trailing <id>.c?id=<id> segment. page is the optional 1-indexed page number (defaults to 1); requesting a page past the last one returns an empty products list, not an error.
- **Params:** `category_id` (string, **required**) — Best Buy category id; `page` (integer, optional) — 1-indexed page number, defaults to 1

### `bestbuy_category_subcategories`

- **HTTP:** `GET /bestbuy/category/subcategories`
- **What:** Get a Best Buy category's own sibling/child categories. Returns a Best Buy category's own sibling/child category set (name, category id, url), sourced from that category page's own "Category" filter facet. Each id is directly usable as bestbuy_category's category_id input. category_id is a Best Buy category id, e.g. pcmcat138500050001, found in a category page URL's trailing <id>.c?id=<id> segment. A leaf category with no siblings returns an empty list, not an error.
- **Params:** `category_id` (string, **required**) — Best Buy category id

### `bestbuy_product`

- **HTTP:** `GET /bestbuy/product`
- **What:** Get a Best Buy product's detail. Returns one Best Buy product's detail (name, brand, model, color, price, availability, rating, images, breadcrumbs). sku is the numeric Best Buy SKU shown on bestbuy.com product pages and URLs.
- **Params:** `sku` (string, **required**) — Numeric Best Buy SKU

### `bestbuy_product_questions`

- **HTTP:** `GET /bestbuy/product/questions`
- **What:** Get a Best Buy product's customer questions and answers. Returns the customer questions (with answers, when present) Best Buy embeds directly on a product's page: question text, answer text, who answered, and when. sku is the numeric Best Buy SKU shown on bestbuy.com product pages and URLs. A product with no questions asked yet returns an empty list, not an error.
- **Params:** `sku` (string, **required**) — Numeric Best Buy SKU

### `bestbuy_product_related`

- **HTTP:** `GET /bestbuy/product/related`
- **What:** Get a Best Buy product's related products. Returns the organic (non-sponsored) related products Best Buy embeds in a product page's own comparison table (sku, name, url, image, price). sku is the numeric Best Buy SKU shown on bestbuy.com product pages and URLs. A product page with no comparison table returns an empty list, not an error.
- **Params:** `sku` (string, **required**) — Numeric Best Buy SKU

### `bestbuy_product_reviews`

- **HTTP:** `GET /bestbuy/product/reviews`
- **What:** Get a Best Buy product's customer reviews. Returns page 1 (up to 20) of one Best Buy product's customer reviews (rating, title, text, author, posted date, tags such as Verified Purchaser, recommended flag, helpful/unhelpful counts). sku is the numeric Best Buy SKU shown on bestbuy.com product pages and URLs.
- **Params:** `sku` (string, **required**) — Numeric Best Buy SKU

### `bestbuy_search`

- **HTTP:** `GET /bestbuy/search`
- **What:** Search Best Buy's product catalog. Returns one page (up to 24) of one Best Buy keyword search's product listing (sku, title, url, image, price, rating, review count). q is free-text search keywords, e.g. "laptop". page is the optional 1-indexed page number (defaults to 1); requesting a page past the last one returns an empty products list, not an error.
- **Params:** `page` (integer, optional) — 1-indexed page number, defaults to 1; `q` (string, **required**) — Search keywords

### `bestbuy_stores`

- **HTTP:** `GET /bestbuy/stores`
- **What:** Get Best Buy's physical stores in one city. Returns Best Buy's physical store locations in one city (name, address, phone, coordinates, rating, hours), sourced from Best Buy's own SEO store directory. state is one of the 50 US state codes plus dc and pr: `al`, `ak`, `az`, `ar`, `ca`, `co`, `ct`, `de`, `dc`, `fl`, `ga`, `hi`, `id`, `il`, `in`, `ia`, `ks`, `ky`, `la`, `me`, `md`, `ma`, `mi`, `mn`, `ms`, `mo`, `mt`, `ne`, `nv`, `nh`, `nj`, `nm`, `ny`, `nc`, `nd`, `oh`, `ok`, `or`, `pa`, `pr`, `ri`, `sc`, `sd`, `tn`, `tx`, `ut`, `vt`, `va`, `wa`, `wv`, `wi`, `wy`. city is free text matched case-insensitively against that state's own directory (e.g. "Chicago").
- **Params:** `city` (string, **required**) — City name; `state` (string, **required**) — Two-letter state/territory code

## Home Depot (6)

### `homedepot_categories`

- **HTTP:** `GET /homedepot/categories`
- **What:** Home Depot department taxonomy. Returns Home Depot's top-level department taxonomy (name, path, url) from the homepage's own "All Departments" navigation. Each department's path is directly usable as GET /homedepot/category's path parameter.
- **Params:** _none_

### `homedepot_category`

- **HTTP:** `GET /homedepot/category`
- **What:** Browse a Home Depot category or brand page. Returns one page of a Home Depot category or brand browse page's product grid: products with title, image, model, current/original price, and rating/review count, plus the category's total result count and the refinement facets the page offers. path is the segment of a /b/ URL after "/b/", e.g. "Tools-Power-Tools-Drills-Impact-Drivers/N-5yc1vZc29x"; a full https://www.homedepot.com/b/... URL or a "/b/..." path is also accepted. sort selects the result ordering and is one of best_match, top_sellers, top_rated, price_low_to_high, price_high_to_low, most_popular, delivery_date; omit it to keep the site's default ordering. page is a 1-indexed page number (default 1, maximum 42), 24 products per page. Each returned facet's path is directly usable as this endpoint's own path parameter to drill down. An unrecognized or blocked path returns an upstream error rather than an empty result.
- **Params:** `page` (integer, optional) — 1-indexed page number, default 1, maximum 42 (12 products per page); `path` (string, **required**) — Home Depot category/brand browse path, e.g. \; `sort` (string, optional) — Result ordering. One of: best_match, top_sellers, top_rated, price_low_to_high, price_high_to_low, most_popular, delivery_date. Omit for the site's default ordering

### `homedepot_product`

- **HTTP:** `GET /homedepot/product/{id}`
- **What:** Home Depot product detail. Returns one Home Depot product's full detail: name, description, brand, model, store SKU, GTIN, price, images, aggregate rating and review count, and the featured customer reviews embedded on the product page. id is the numeric product/internet id (the trailing number of a /p/{slug}/{id} URL). The product page does not distinguish an unknown id from a known one in a consistent way, so an unrecognized id may return an upstream error rather than a not-found.
- **Params:** `id` (string, **required**) — Home Depot product/internet id, e.g. 320326875

### `homedepot_product_questions`

- **HTTP:** `GET /homedepot/product/{id}/questions`
- **What:** Home Depot product questions and answers. Returns the first page (8 questions) of a Home Depot product's customer questions and answers, plus the product's total Q&A count. id is the numeric product/internet id. A product with no Q&A returns a genuine zero-result response rather than an error.
- **Params:** `id` (string, **required**) — Home Depot product/internet id, e.g. 328425526

### `homedepot_search`

- **HTTP:** `GET /homedepot/search`
- **What:** Home Depot keyword search. Returns one page of a Home Depot keyword search's product listing: products with title, image, model, current/original price, and rating/review count, plus the search's total result count. A page carries up to 24 products, or up to 12 when Home Depot answers the query with a category page. q is free-text search keywords, e.g. "impact driver". page is a 1-indexed page number (default 1). An unrecognized/blocked query returns an upstream error rather than an empty result.
- **Params:** `page` (integer, optional) — 1-indexed page number, default 1; `q` (string, **required**) — Free-text search keywords, e.g. \

### `homedepot_suggest`

- **HTTP:** `GET /homedepot/suggest`
- **What:** Home Depot search suggestions. Returns Home Depot's own search-box typeahead suggestions for a partial query, in the site's own ranking order. term is the partial search text, e.g. "drill". Each suggestion's term is directly usable as GET /homedepot/search's q parameter. A term that matches nothing returns an empty suggestion list rather than an error.
- **Params:** `term` (string, **required**) — Partial search text, e.g. \

## Sephora (9)

### `sephora_brands`

- **HTTP:** `GET /sephora/brands`
- **What:** Sephora brand directory. Returns Sephora's full brand directory (373 brands at time of writing), sourced from the site's own A-Z brand list page. Each brand's `name` is the exact string GET /sephora/search and GET /sephora/category's repeatable `brand` filter parameter expect.
- **Params:** _none_

### `sephora_categories`

- **HTTP:** `GET /sephora/categories`
- **What:** Sephora storefront categories. Returns Sephora's own live storefront category navigation (department, group, name, and slug for each), sourced from the site's own "Shop" mega-nav. Each entry's slug is directly usable as GET /sephora/category's own `slug` query parameter.
- **Params:** `department` (string, optional) — Filter to one storefront department

### `sephora_category`

- **HTTP:** `GET /sephora/category`
- **What:** Sephora category browse. Returns one page of a Sephora category/browse listing (e.g. Makeup, Skincare), with the same sort and facet filters as /sephora/search. slug is the path segment after sephora.com/shop/, e.g. makeup-cosmetics. The response uses Sephora's public catalog search to keep browse listings available when the category page's legacy embedded data is absent.
- **Params:** `brand` (array, optional) — One or more exact brand names to filter to (OR'd together); repeat the param for multiple values; `filter` (array, optional) — Additional facet:value filters, repeat the param for multiple; facet must be one of: benefits, ingredientpreferences, colorfamily, formulation, size, shoppingpreferences, agerange, skintype, finish, skinconcerns, coverage, hairtype, hairconcerns, hairtexture; `is_new` (boolean, optional) — When true, filters to products flagged New; `page` (integer, optional) — Result page, 1-based, defaults to 1; `price_max` (integer, optional) — Maximum price in whole dollars; must be set together with price_min; `price_min` (integer, optional) — Minimum price in whole dollars; must be set together with price_max; `rating_min` (integer, optional) — Minimum star rating, 1 to 4; `slug` (string, **required**) — Category-page slug; `sort_by` (string, optional) — Sort order, defaults to featured

### `sephora_product`

- **HTTP:** `GET /sephora/product`
- **What:** Sephora product detail. Returns one Sephora product's full detail (every color/shade variant with its own price and availability, rating, review count, and a sample of recent reviews). `product_id` is the full product-page slug, e.g. `lip-sleeping-mask-P420652` -- copy it from the path segment after sephora.com/product/ on any product page; unlike some other retailers, an arbitrary or partial slug does not resolve.
- **Params:** `product_id` (string, **required**) — Full Sephora product-page slug

### `sephora_product_questions`

- **HTTP:** `GET /sephora/product/questions`
- **What:** Sephora product questions and answers. Returns one page of a Sephora product's customer Q&A: each question plus every answer it received (text, author, whether it's a brand answer, helpful votes). product_id is the Sephora productGroupID, e.g. P420652 -- the same value /sephora/product returns as product_group_id.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `product_id` (string, **required**) — Sephora productGroupID

### `sephora_product_reviews`

- **HTTP:** `GET /sephora/product/reviews`
- **What:** Sephora product reviews. Returns one page of a Sephora product's full customer reviews (title, body, rating, author, helpful votes, secondary ratings, photos), plus the product's site-wide rating rollup (average rating, recommended ratio, star-count histogram). product_id is the Sephora productGroupID, e.g. P420652 -- the same value /sephora/product returns as product_group_id.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `product_id` (string, **required**) — Sephora productGroupID

### `sephora_search`

- **HTTP:** `GET /sephora/search`
- **What:** Sephora product search. Searches Sephora's product catalog by keyword, with real page-based pagination. Returns products with brand, pricing, rating, and review count. Sephora's own search never returns a genuine zero-result state for a nonempty keyword -- an unrecognized/nonsense keyword still returns a full, unrelated fallback result set rather than an empty one. price_min/price_max must be provided together (whole dollars) -- upstream silently ignores a one-sided price range rather than filtering or erroring, so this endpoint rejects a one-sided range as invalid instead of passing it through. brand and filter each accept multiple values (OR'd together within the same facet); brand/rating_min/is_new/filter/price_min/price_max can all be combined with each other (AND'd together across different facets).
- **Params:** `brand` (array, optional) — One or more exact brand names to filter to (OR'd together); repeat the param for multiple values; `filter` (array, optional) — Additional facet:value filters, repeat the param for multiple; facet must be one of: benefits, ingredientpreferences, colorfamily, formulation, size, shoppingpreferences, agerange, skintype, finish, skinconcerns, coverage, hairtype, hairconcerns, hairtexture; `is_new` (boolean, optional) — When true, filters to products flagged New; `page` (integer, optional) — Result page, 1-based, defaults to 1; `page_size` (integer, optional) — Results per page, 1 to 100, defaults to 60; `price_max` (integer, optional) — Maximum price in whole dollars; must be set together with price_min; `price_min` (integer, optional) — Minimum price in whole dollars; must be set together with price_max; `query` (string, **required**) — Search keyword; `rating_min` (integer, optional) — Minimum star rating, 1 to 4; `sort_by` (string, optional) — Sort order, defaults to featured

### `sephora_stores`

- **HTTP:** `GET /sephora/stores`
- **What:** Sephora store locator. Returns Sephora physical store locations near a coordinate (address, hours, BOPIS/curbside/same-day flags). Renders through a JS-executing browser backend, unlike every other Sephora endpoint -- the store-locator data call itself is plain HTTP, but it requires a per-visit access token minted by an endpoint gated behind a bot-management JS challenge, so responses may take longer.
- **Params:** `latitude` (number, **required**) — Latitude, -90 to 90; `limit` (integer, optional) — Max stores to return, 1 to 50, defaults to 10; `longitude` (number, **required**) — Longitude, -180 to 180; `radius` (integer, optional) — Search radius in miles, 1 to 500, defaults to 50

### `sephora_suggest`

- **HTTP:** `GET /sephora/suggest`
- **What:** Sephora search suggestions. Returns Sephora's own search-box type-ahead suggestions for a partial keyword: keyword-completion terms, matching products, and trending/related categories. Sephora's own upstream never returns a genuine zero-result state for a nonempty query -- a deliberately nonsense query still returns unrelated product suggestions.
- **Params:** `query` (string, **required**) — Partial search keywords

## SHEIN (8)

### `shein_category_filters`

- **HTTP:** `GET /shein/category/filters`
- **What:** SHEIN category filter facets. Returns the filter facets for a SHEIN category by the required numeric `cat_id`, such as sizes, colours and composition. Each group has a `node_id`, `node_name` and a list of options with their own ids and names. Also returns `min_price`, `max_price` and the `currency`.
- **Params:** `cat_id` (string, **required**) — Numeric SHEIN category id

### `shein_category_goods`

- **HTTP:** `GET /shein/category/goods`
- **What:** SHEIN category product listing. Lists products in a SHEIN category, by the required numeric `cat_id`. `page` starts at 1 and `page_size` defaults to 20; `sort` is a non-negative integer, `0` by default. Each product has its id, name, images, sale, retail and USD prices, rating, review count, and `on_sale` and `sold_out` flags. `total` is the category's listing count.
- **Params:** `cat_id` (string, **required**) — Numeric SHEIN category id; `page` (integer, optional) — 1-based page number; `page_size` (integer, optional) — Results per page; `sort` (string, optional) — SHEIN sort code: a non-negative integer. `0` is the default (recommended). Other codes are accepted and forwarded as-is; the full code-to-meaning mapping has not been live-verified yet (see the endpoint markdown), so callers relying on a specific ordering should confirm behavior empirically.

### `shein_category_nav`

- **HTTP:** `GET /shein/category/nav`
- **What:** SHEIN category nav tabs. Returns the subcategory navigation tabs for a SHEIN category, by the required numeric `cat_id`. Each tab has its `nav_id`, `nav_name`, `nav_type`, `nav_img` and the `goods_id` of a representative product.
- **Params:** `cat_id` (string, **required**) — Numeric SHEIN category id

### `shein_products_aggregation_filters`

- **HTTP:** `POST /shein/products/aggregation-filters`
- **What:** SHEIN search aggregation filters. Returns the filter facets for a SHEIN search, given the required `keyword` and an optional `cat_id` that narrows them. The response has filter groups (id, name, options), a recursive `category` drill-down with `children`, and the `min_price` and `max_price` for the query.
- **Params:** `cat_id` (string, optional) — Numeric SHEIN category id, narrows the facets; `keyword` (string, **required**) — Free-text search query

### `shein_products_detail`

- **HTTP:** `GET /shein/products/detail`
- **What:** SHEIN product detail. Returns a SHEIN product by the required numeric `goods_id`; `goods_sn` is optional and narrows the lookup. The response has the name, description, category, brand code, sale, retail and USD prices, images, video URL, size options, per-SKU stock and prices, and colour variants.
- **Params:** `goods_id` (string, **required**) — Numeric SHEIN goods id (from a search result's goods_id); `goods_sn` (string, optional) — SHEIN goods serial number, narrows the lookup

### `shein_products_search`

- **HTTP:** `POST /shein/products/search`
- **What:** SHEIN product search. Searches SHEIN products for the required `keyword`. `page` starts at 1, `page_size` defaults to 20 and `sort` is a non-negative integer, `0` by default. Each product card has its id, name, images, prices, rating, review count and stock flags. Also returns `total` and spelling suggestions in `suggest_words`.
- **Params:** `keyword` (string, **required**) — Free-text search query; `page` (integer, optional) — 1-based page number; `page_size` (integer, optional) — Results per page; `sort` (string, optional) — SHEIN sort code: a non-negative integer. `0` is the default (recommended). Other codes are accepted and forwarded as-is; the full code-to-meaning mapping has not been live-verified yet (see the endpoint markdown), so callers relying on a specific ordering should confirm behavior empirically.

### `shein_search_autocomplete`

- **HTTP:** `POST /shein/search/autocomplete`
- **What:** SHEIN search autocomplete. Returns SHEIN search suggestions for a partial query in the required `word`. Each suggestion has its `word`, `word_id` and `type`. A word with no matching phrase returns an empty list, not an error.
- **Params:** `word` (string, **required**) — Partial search query

### `shein_search_keywords`

- **HTTP:** `POST /shein/search/keywords`
- **What:** SHEIN trending search keywords. Returns the trending search keywords SHEIN shows in its search box. `scene` defaults to `trendStoreChannel` and `word_type` to `1`. Each keyword has its `word`, `word_id`, `type` and `from`.
- **Params:** `scene` (string, optional) — Keyword scene (trendStoreChannel); `word_type` (string, optional) — Keyword type (1)

## Walgreens (1)

### `walgreens_stores`

- **HTTP:** `GET /walgreens/stores`
- **What:** Find nearby Walgreens stores. Returns Walgreens stores near a latitude/longitude or a zip code, nearest first: name, address, phone, hours, and in-store services (pharmacy, clinic, photo, and more) for each. Public data sourced from Walgreens' own store locator.
- **Params:** `latitude` (number, optional) — Latitude; provide with longitude, or provide zip instead; `longitude` (number, optional) — Longitude; provide with latitude, or provide zip instead; `zip` (string, optional) — US ZIP code; used when latitude/longitude are omitted

## IKEA (9)

### `ikea_availability`

- **HTTP:** `GET /ikea/availability`
- **What:** Get an IKEA item's real-time stock availability. Returns one IKEA item's real-time home-delivery and click-and-collect stock signal for the requested country. item_no is IKEA's own item number.
- **Params:** `country` (string, optional) — Lowercase 2-letter IKEA site country code; `item_no` (string, **required**) — IKEA item number

### `ikea_categories`

- **HTTP:** `GET /ikea/categories`
- **What:** Discover IKEA category keys. Returns a page of IKEA's full category taxonomy, sourced from IKEA's own site navigation data: every top-level department and nested subcategory, with the key each one uses as ikea_category's own category input. key is IKEA's own category key (numeric, e.g. 20649, or a short alphanumeric department code, e.g. st001). parent_key is the immediate parent category's own key (empty for a top-level department); level is depth in the taxonomy tree, starting at 1. q optionally filters by a case-insensitive substring of name.
- **Params:** `country` (string, optional) — Lowercase 2-letter IKEA site country code; `language` (string, optional) — Lowercase 2-letter IKEA site language code; `page` (integer, optional) — 1-based page number; `page_size` (integer, optional) — Result count per page (1-1000); `q` (string, optional) — Case-insensitive substring filter on category name

### `ikea_category`

- **HTTP:** `GET /ikea/category`
- **What:** Browse an IKEA category. Returns one page of an IKEA category's product listing, with real offset/size pagination and sort. category is IKEA's own category key (e.g. 20649), taken from a category URL's trailing -{key}/ segment, a product's own category_path field, or GET /ikea/categories, which discovers every valid category value.
- **Params:** `category` (string, **required**) — IKEA category key; `country` (string, optional) — Lowercase 2-letter IKEA site country code; `language` (string, optional) — Lowercase 2-letter IKEA site language code; `offset` (integer, optional) — Zero-based result offset; `size` (integer, optional) — Result count (1-100); `sort` (string, optional) — Result order

### `ikea_product`

- **HTTP:** `GET /ikea/product`
- **What:** Get an IKEA product's detail. Returns one IKEA item's full detail: name, price, rating, every product image, quick facts, and category breadcrumb path. item_no is IKEA's own item number (8 digits, optionally prefixed with "s" for a combination/set article), taken from a search result's item_no field or an ikea.com product page's own URL.
- **Params:** `country` (string, optional) — Lowercase 2-letter IKEA site country code; `item_no` (string, **required**) — IKEA item number; `language` (string, optional) — Lowercase 2-letter IKEA site language code

### `ikea_reviews`

- **HTTP:** `GET /ikea/reviews`
- **What:** Get an IKEA item's highlighted customer reviews. Returns one IKEA item's own highlighted customer reviews (title, rating, text, author) plus its aggregate rating, sourced from the product page's own curated reviews carousel. This is a small, representative set of reviews (a handful per item), not the full paginated review list.
- **Params:** `country` (string, optional) — Lowercase 2-letter IKEA site country code; `item_no` (string, **required**) — IKEA item number; `language` (string, optional) — Lowercase 2-letter IKEA site language code

### `ikea_search`

- **HTTP:** `GET /ikea/search`
- **What:** Search IKEA products. Searches IKEA products and returns name, price, rating, images, colors, and variant data. q is a free-text query; an IKEA item number also resolves as its own single result. country and language select IKEA's per-country site (default us/en). A zero total with an empty products list is a valid no-results response.
- **Params:** `country` (string, optional) — Lowercase 2-letter IKEA site country code; `language` (string, optional) — Lowercase 2-letter IKEA site language code; `q` (string, **required**) — Free-text product search query; `size` (integer, optional) — Result count (1-100)

### `ikea_store`

- **HTTP:** `GET /ikea/store`
- **What:** Get an IKEA store's detail. Returns one IKEA physical location's full detail: address, geo coordinates, opening hours, and price range. slug is IKEA's own store URL slug, taken from an ikea_stores result's own slug field. Geo, hours, and price range are only present for full/small stores; order points and pick-up-only points return address only.
- **Params:** `country` (string, optional) — Lowercase 2-letter IKEA site country code; `language` (string, optional) — Lowercase 2-letter IKEA site language code; `slug` (string, **required**) — IKEA store URL slug

### `ikea_stores`

- **HTTP:** `GET /ikea/stores`
- **What:** List IKEA physical store locations. Returns IKEA's own directory of physical locations for the requested country: name, URL slug, region grouping, and location type (Store, Small store, Plan & order point with pick-up, etc). Each slug is usable directly as ikea_store's own slug input.
- **Params:** `country` (string, optional) — Lowercase 2-letter IKEA site country code; `language` (string, optional) — Lowercase 2-letter IKEA site language code

### `ikea_suggest`

- **HTTP:** `GET /ikea/suggest`
- **What:** Get IKEA search-box typeahead suggestions. Returns IKEA's own search-box typeahead result for a partial or full query: suggested query completions with their own match counts, plus a small number of top matching products. A query with no matches returns a clean empty response.
- **Params:** `country` (string, optional) — Lowercase 2-letter IKEA site country code; `language` (string, optional) — Lowercase 2-letter IKEA site language code; `q` (string, **required**) — Partial or full search term; `size` (integer, optional) — Top-product count (1-20)

## Chewy (14)

### `chewy_brands`

- **HTTP:** `GET /chewy/brands`
- **What:** List Chewy's brand directory. Returns one page of Chewy's full brand directory -- roughly 7,600 brands -- with each brand's id, name, Chewy's own written description, image, parent-catalog group, and its child brands where a brand umbrellas others (Purina lists 27). This is the whole catalog of brands, unlike chewy_facets, which only reports the brands present in one category's listing. Pass name to look up a single brand by exact name, case-insensitive; it is an exact match upstream, not a search, so "Purina" matches while "purina pro" does not. To filter products by a brand, pass the brand's NAME to chewy_category or chewy_search as filter=brand_facet:<name> -- facet_id is the join key onto chewy_facets' own option ids and is not accepted by the filter parameter.
- **Params:** `limit` (integer, optional) — Brands per page, 1 to 500 (default 100).; `name` (string, optional) — Return only the brand with this exact name, case-insensitive. Exact match, not a search.; `page` (integer, optional) — Page number, 1-based (default 1).

### `chewy_categories`

- **HTTP:** `GET /chewy/categories`
- **What:** Browse Chewy's category taxonomy tree. Returns Chewy's category taxonomy tree: how to discover group_id values for chewy_category, not the products within a category. Omitting group_id returns all top-level departments (Dog, Cat, Horse, Bird, Fish, Reptile, Small Pet, Farm and Livestock Supplies, Wild Bird and Wildlife Supplies, Pharmacy, Pet Parents); a group_id expands that specific group's own subtree instead. depth controls how many levels of subcategories are expanded in one call.
- **Params:** `depth` (integer, optional) — How many levels of subcategories to expand, 1 to 3 (default 2); `group_id` (string, optional) — Chewy category group id to expand, e.g. 332 for Dog Food. Omit for the full top-level department tree.

### `chewy_category`

- **HTTP:** `GET /chewy/category`
- **What:** Browse a Chewy category listing. Returns one page (36 products) of a Chewy category/browse listing's product grid (price, autoship price/discount, stock, rating, images), plus embedded facets and breadcrumbs. group_id is Chewy's own numeric category id -- the trailing id segment of a chewy.com/b/<slug>-<id> browse URL, e.g. 294 for /b/dry-food-294. Every breadcrumbs[].group_id and facets[].options[].value in a response is a ready-to-use group_id for a follow-up call, so a caller can discover the full category taxonomy starting from a known category. A group_id Chewy does not recognize returns a 404 rather than an unfiltered listing. sort and filter narrow/reorder the listing; every facets[].value paired with one of that facet's options[].value from any prior response is a valid filter key:value pair (e.g. brand, breed size, flavor, price range, customer rating -- whichever facets that category exposes). Set include_content to also return the category's curated editorial content -- Chewy's own FAQ question/answer pairs, the rich category description, and the SEO page title and meta description; it costs no extra upstream call and is omitted entirely when not requested. A keyword search carries none of this content, so it is a category-only addition.
- **Params:** `filter` (array, optional) — Repeatable, up to 10. Each value is \; `group_id` (string, **required**) — Chewy's numeric category id, e.g. \; `include_content` (boolean, optional) — Also return the category's curated editorial content -- Chewy's own FAQ question/answer pairs, the rich category description, and the SEO page title/meta description. Costs no extra upstream call. Omitted entirely when false (the default).; `page` (integer, optional) — Page number, 36 products per page (default 1); `sort` (string, optional) — Sort order. One of byRelevance, byNewest, byPopularity, byLowestPrice, byHighestPrice, byRating, byRatingCount. Defaults to Chewy's own relevance ordering when omitted.

### `chewy_facets`

- **HTTP:** `GET /chewy/facets`
- **What:** List a Chewy category or search's refinement options. Returns the full set of refinement options (facets) a Chewy category or keyword search can be narrowed by -- brand, sub-category, lifestage, food form, breed size, special diet, health feature, flavor, ingredient, packaging type, price band, customer rating, and whichever other dimensions that listing exposes -- with each option's product count. No products are returned, so this is a much smaller call than chewy_category/chewy_search when only the option set is wanted. The Brand dimension is effectively Chewy's brand directory for the requested listing: each brand option carries its product count and, where Chewy publishes one, its own chewy.com/brands/<slug>-<id> landing-page slug in seo_hvf_slug. Exactly one of group_id or q is required. Every facets[].value paired with one of that facet's options[].value is a ready-to-use filter key:value pair for this endpoint, chewy_category, and chewy_search alike; passing filter here narrows the listing first, so the returned counts describe the already-narrowed result set. A group_id Chewy does not recognize returns a 404 rather than an empty option set.
- **Params:** `filter` (array, optional) — Repeatable, up to 10. Each value is \; `group_id` (string, optional) — Chewy's numeric category id, e.g. \; `q` (string, optional) — Free-text search keywords to return refinement options for, e.g. \

### `chewy_gtin_lookup`

- **HTTP:** `GET /chewy/gtin-lookup`
- **What:** Resolve Chewy GTIN/UPC barcodes to part numbers. Resolves a batch of up to 20 GTIN/UPC barcodes to their Chewy part numbers in one call. gtins is a comma-separated list of barcodes, e.g. "192268541316". A barcode Chewy does not recognize is omitted from part_numbers and listed in not_found rather than causing the whole call to fail. The resolved part_numbers values feed directly into chewy_product/chewy_products.
- **Params:** `gtins` (string, **required**) — Comma-separated GTIN/UPC barcodes, up to 20

### `chewy_inventory`

- **HTTP:** `GET /chewy/inventory`
- **What:** Look up live warehouse inventory for a batch of Chewy products. Returns Chewy's live warehouse inventory position for up to 20 products in one call, keyed by part number: the availability status, total units on hand, units inbound/in progress, units already reserved against unshipped orders, and the quantity actually available to the storefront. This is the only Chewy surface that carries real quantities -- every other endpoint in this family reports stock as a single boolean, so "36 units left" and "84,386 units left" are indistinguishable there. Quantities are live and move between calls. Part numbers Chewy does not return inventory for are reported in not_found; if none resolve the response is a 404.
- **Params:** `part_numbers` (string, **required**) — Comma-separated Chewy part numbers, up to 20 per request, e.g. \

### `chewy_item_attributes`

- **HTTP:** `GET /chewy/item-attributes`
- **What:** Look up a batch of Chewy products' structured attributes and handling flags. Returns Chewy's own specification table for up to 20 products in one call, keyed by part number -- the structured attribute list (lifestage, pet type, product type, material, made-in country, packaging type, flavor, defining size, plus long-form key-benefits and cautions copy), together with the handling and compliance flags that govern how an item ships (pharmaceutical, prescription vet-diet, frozen, refrigerated, single-tablet, gift card), its bundle structure and component SKUs, its autoship eligibility/discount and preset reorder cadence, its merchandising classification path, and the numeric category group ids it belongs to (each usable directly as chewy_category's group_id). This complements rather than repeats chewy_products and chewy_product: price, rating, images, reviews, and descriptions stay on those endpoints, and the attribute table is not available from either. Use the group parameter to return a single attribute group. Part numbers Chewy does not recognize are reported in not_found; if none of them resolve the response is a 404.
- **Params:** `group` (string, optional) — Return only attributes in one group. One of DEFINING, STANDARD, EXTENDED, HIDDEN. Omit for every group.; `part_numbers` (string, **required**) — Comma-separated Chewy part numbers, up to 20 per request, e.g. \

### `chewy_product`

- **HTTP:** `GET /chewy/product`
- **What:** Get a Chewy product's detail. Returns one Chewy product's full detail: name, brand, description, images, price, stock, rating and its star-count breakdown, category breadcrumbs, customer questions and answers, and customer reviews. id is the numeric id from a chewy.com PDP URL, e.g. 185468 from https://www.chewy.com/frisco-lion-mane-dog-cat-costume/dp/185468 -- also the same value a chewy_category response's products[].part_number field carries for that product's own default variant. The response also carries the item's shipping weight and package dimensions as Chewy states them, its per-order purchase limit, and any promotions currently attached to it (each with a type such as "Spend $X" or "BOGO", plus short and long descriptions).
- **Params:** `id` (string, **required**) — Numeric id from a chewy.com PDP URL

### `chewy_product_questions`

- **HTTP:** `GET /chewy/product-questions`
- **What:** List a Chewy product's customer questions and answers, paginated. Returns one page of a Chewy product's customer questions, each with its answers (text, author, date, staff flag, helpful count). chewy_product embeds only the first 20 questions with no way to page past them; this endpoint reaches the whole set. id is the numeric id from any chewy.com PDP URL, and questions are shared across a product's variants, so any variant's id returns the same set. Each question reports answers_total alongside its answers array, so a caller can tell when answers were truncated by answer_limit. Chewy offers no sort or filter on questions, so this endpoint deliberately exposes paging only.
- **Params:** `answer_limit` (integer, optional) — Answers to return per question, 1 to 20 (default 10). Each question also reports answers_total.; `id` (string, **required**) — The numeric id from a chewy.com PDP URL, e.g. \; `limit` (integer, optional) — Questions per page, 1 to 50 (default 20).; `page` (integer, optional) — Page number, 1-based (default 1).

### `chewy_product_reviews`

- **HTTP:** `GET /chewy/product-reviews`
- **What:** List a Chewy product's customer reviews, paginated. Returns one page of a Chewy product's customer reviews -- rating, title, body, author, submission date, helpful count, incentivized flag, and contributor badge -- with sorting and positive/negative filtering. chewy_product embeds only the first 20 reviews with no way to page past them; this endpoint reaches the whole set (products routinely carry thousands). id is the numeric id from any chewy.com PDP URL, and reviews are shared across a product's variants, so any variant's id returns the same set. total is the count for the current filter, so it drops when filter is applied, while rating_count stays the product's overall rating tally.
- **Params:** `filter` (string, optional) — Restrict to POSITIVE (4-5 star) or NEGATIVE (1-3 star) reviews. Omit for all.; `id` (string, **required**) — The numeric id from a chewy.com PDP URL, e.g. \; `limit` (integer, optional) — Reviews per page, 1 to 50 (default 20).; `page` (integer, optional) — Page number, 1-based (default 1).; `sort` (string, optional) — Sort order. One of MOST_RELEVANT, NEWEST, OLDEST, HIGHEST_RATING, LOWEST_RATING, PHOTOS. Defaults to Chewy's own ordering when omitted.

### `chewy_products`

- **HTTP:** `GET /chewy/products`
- **What:** Get a batch of Chewy products' lightweight summaries. Returns a batch of up to 20 Chewy products' lightweight summaries (price, rating, stock, images) in one call. part_numbers is a comma-separated list of Chewy part numbers, e.g. "52448,767758" -- the same value chewy_product returns as part_number/parent_part_number, and chewy_category/chewy_search return as products[].part_number. A part number Chewy does not recognize is omitted from products and listed in not_found rather than causing the whole call to fail.
- **Params:** `part_numbers` (string, **required**) — Comma-separated Chewy part numbers, up to 20

### `chewy_search`

- **HTTP:** `GET /chewy/search`
- **What:** Search Chewy by keyword. Returns one page of a Chewy keyword search's product listing (price, autoship price/discount, stock, rating, images), plus embedded facets. q is free-text search keywords, e.g. "salmon dog food". A generic query that strongly matches one of Chewy's own categories (e.g. "dog food", "cat litter", "leash") is transparently redirected to that category's listing, the same real results a chewy.com visitor would see -- source_url reflects the actual listing fetched. sort and filter narrow/reorder the listing; every facets[].value paired with one of that facet's options[].value from any prior response is a valid filter key:value pair.
- **Params:** `filter` (array, optional) — Repeatable, up to 10. Each value is \; `page` (integer, optional) — Page number, 36 products per page (default 1); `q` (string, **required**) — Free-text search keywords; `sort` (string, optional) — Sort order. One of byRelevance, byNewest, byPopularity, byLowestPrice, byHighestPrice, byRating, byRatingCount. Defaults to Chewy's own relevance ordering when omitted.

### `chewy_suggest`

- **HTTP:** `GET /chewy/suggest`
- **What:** Chewy search-box typeahead suggestions. Returns Chewy's own search-box typeahead result for a partial query term: search-term suggestions (some resolving directly to a category/brand browse URL via their own url field) plus a handful of educational-content article suggestions. term is a partial query, e.g. "salmon dog" or "blue buff". Omit term entirely to get what Chewy shows on an empty search box instead: its current Popular Searches (each resolving to a category or brand listing) and Popular Articles.
- **Params:** `term` (string, optional) — Partial search text, e.g. \

### `chewy_variants`

- **HTTP:** `GET /chewy/variants`
- **What:** List every size/flavor variant of a Chewy product. Returns the full roster of purchasable variants for the product a given item belongs to -- every size, flavor, or color Chewy sells it in -- with each variant's own part number, price, Autoship price, stock, images, and the defining option that distinguishes it (e.g. Size = Medium). id is the numeric id from any chewy.com PDP URL; passing any one variant's id returns that variant's whole family, and the variant you asked for is flagged with is_requested. This answers a question chewy_product cannot: chewy_product describes only the single variant it was given and names its parent, but never lists the siblings or their prices. Only the defining option is returned, not the full attribute table -- use chewy_item_attributes for that.
- **Params:** `id` (string, **required**) — The numeric id from a chewy.com PDP URL, e.g. \

## BigCommerce (3)

### `bigcommerce_category`

- **HTTP:** `GET /bigcommerce/category`
- **What:** Browse a BigCommerce storefront category. Returns one product-listing page from a public BigCommerce storefront category page. url must be the full public category-page URL. page is 1-indexed and defaults to 1.
- **Params:** `page` (integer, optional) — 1-indexed category page, defaults to 1; `url` (string, **required**) — Full public BigCommerce category page URL

### `bigcommerce_product`

- **HTTP:** `GET /bigcommerce/product`
- **What:** Get a BigCommerce storefront product. Returns product detail from a public BigCommerce storefront product page. url must be the full public product-page URL for a BigCommerce Stencil storefront.
- **Params:** `url` (string, **required**) — Full public BigCommerce product page URL

### `bigcommerce_search`

- **HTTP:** `GET /bigcommerce/search`
- **What:** Search a BigCommerce storefront. Returns one product-search page from a public BigCommerce storefront. url must be the public storefront origin; an optional caller path or query is ignored. q is required search text. page is 1-indexed and defaults to 1.
- **Params:** `page` (integer, optional) — 1-indexed search page, defaults to 1; `q` (string, **required**) — Search text; `url` (string, **required**) — Public BigCommerce storefront origin

## Boots (2)

### `boots_search`

- **HTTP:** `GET /boots/search`
- **What:** Search Boots UK products and categories. Returns one page of Boots UK's public product catalog, including product cards and live facets. Supply `q`, one or more hierarchical `category` keys, or both. Use repeatable `filter=facet_key:option_key` values from that response's dynamic facets, plus the dedicated price and stock controls. `sort` accepts `relevance`, `price_low_to_high`, `price_high_to_low`, `top_rated`, `best_seller`, or `newest`.
- **Params:** `category` (array, optional) — Repeat the exact category hierarchy keys from root through the desired leaf; required unless q is supplied; `filter` (array, optional) — Repeat a dynamic facet filter as facet_key:option_key, using key/option values returned in facets; category, currentPrice, and inStock use their dedicated parameters; `in_stock` (boolean, optional) — true hides out-of-stock items; false leaves stock unfiltered; `page` (integer, optional) — Page from 1 through 1000; `page_size` (integer, optional) — Results per page from 1 through 48; `price_max` (number, optional) — Inclusive maximum GBP price; may be combined with price_min; `price_min` (number, optional) — Inclusive minimum GBP price; may be combined with price_max; `q` (string, optional) — Free-text product query; required unless category is supplied; `sort` (string, optional) — Sort: relevance, price_low_to_high, price_high_to_low, top_rated, best_seller, or newest

### `boots_suggest`

- **HTTP:** `GET /boots/suggest`
- **What:** Get Boots UK search-box suggestions. Returns Boots UK's own public typeahead phrases for a partial product query. The suggestions are search terms only; pass one to boots-search's q parameter for product cards and live facets.
- **Params:** `q` (string, **required**) — Partial product query

## CVS (7)

### `cvs_brands`

- **HTTP:** `GET /cvs/brands`
- **What:** CVS brand directory. Returns CVS.com's full brand directory (name and path). Each brand's path is directly usable as GET /cvs/category's path parameter to browse that brand's products.
- **Params:** _none_

### `cvs_categories`

- **HTTP:** `GET /cvs/categories`
- **What:** CVS category taxonomy. Returns CVS.com's full category/subcategory navigation taxonomy (name and path, nested to whatever depth the upstream carries). Each node's path is directly usable as GET /cvs/category's path parameter.
- **Params:** _none_

### `cvs_category`

- **HTTP:** `GET /cvs/category`
- **What:** Browse a CVS OTC category page. Returns one page of a CVS.com OTC (over-the-counter) retail category, subcategory, or brand page's product grid: products with title, brand, image, current/original price, and sponsored/featured/new-product flags; the total result count; and the facets (brand, color, size, price range, and other category-specific attributes, each with its selectable values and result counts) available to filter the page further. Covers the non-prescription retail catalog only. path is the segment of a page URL after "/shop/", e.g. "beauty" (top-level category), "health-medicine/allergy-sinus" (subcategory), or "brand-shop/s/safe-home" (brand page); a full https://www.cvs.com/shop/... URL or a "/shop/..." path is also accepted. Any of these can also carry an optional facet-filter suffix in the site's own URL shape, e.g. "beauty/makeup/eyes/q/CoverGirl/Black/brpc" to filter to brand CoverGirl and color Black -- see the response's facets field for which values/type codes a given category supports; filter values are case-sensitive exactly as the site renders them. page is a 1-indexed page number (default 1). sort is an optional result order matching the site's own Sort By control. CVS.com is only available from US and US-territory locations; a request served from an unsupported region returns an upstream error rather than an empty result.
- **Params:** `page` (integer, optional) — 1-indexed page number, default 1; `path` (string, **required**) — CVS category, subcategory, or brand-page URL path, optionally with a /q/{value}/{typeCode} facet-filter suffix, e.g. \; `sort` (string, optional) — Result sort order, default the site's own relevance order. One of pa (Price Low to High), pd (Price High to Low), tr (Top Rated), rc (Most Reviewed), az (Name A-Z), za (Name Z-A)

### `cvs_product`

- **HTTP:** `GET /cvs/product/{slug}`
- **What:** CVS OTC product detail. Returns one CVS.com OTC (over-the-counter) retail product's detail: name, description, brand, category, price, currency, online availability, image gallery, and aggregate rating. Covers the non-prescription retail catalog only -- this does not cover prescription items, pharmacy ordering, or any patient-specific data. slug is the segment of a product page URL after "/shop/", e.g. "safe-home-premium-radon-test-kit-prodid-945948"; a full https://www.cvs.com/shop/... URL is also accepted. CVS.com is only available from US/US-territory egress; a request from an unsupported region returns an upstream error rather than an empty result.
- **Params:** `slug` (string, **required**) — CVS product page URL slug, e.g. \

### `cvs_product_ingredients`

- **HTTP:** `GET /cvs/product-ingredients/{slug}`
- **What:** CVS OTC product ingredients. Returns one CVS.com OTC (over-the-counter) retail product's ingredient/label statement: active ingredients, inactive ingredients, and the vendor's full free-text ingredient paragraph (which, for OTC drug products, frequently also carries a Drug Facts-style purpose note). This is sourced from the product's own dedicated ingredients page, a separate page from the main product detail endpoint. Covers the non-prescription retail catalog only -- this does not cover prescription items, pharmacy ordering, or any patient-specific data. slug is the segment of a product page URL after "/shop/", e.g. "e-l-f-16hr-camo-concealer-prodid-2370023"; a full https://www.cvs.com/shop/... URL is also accepted. Some products (particularly non-consumable goods) may return empty ingredient fields -- this reflects upstream having no label data for that product, not an error. CVS.com is only available from US/US-territory egress; a request from an unsupported region returns an upstream error rather than an empty result.
- **Params:** `slug` (string, **required**) — CVS product page URL slug, e.g. \

### `cvs_search`

- **HTTP:** `GET /cvs/search`
- **What:** Search CVS OTC products by keyword. Performs a keyword search across CVS.com's non-prescription retail/OTC catalog and returns one page of results: products with title, brand, image, current/original price, and sponsored/featured/new-product flags; the total result count; and the facets (brand, color, size, price range, and other attributes, each with its selectable values and result counts) available to filter the results further. Covers the non-prescription retail catalog only. q is the search keyword or phrase, required. page is a 1-indexed page number (default 1). sort is an optional result order matching cvs-category's own Sort By values. CVS.com is only available from US and US-territory locations; a request served from an unsupported region returns an upstream error rather than an empty result.
- **Params:** `page` (integer, optional) — 1-indexed page number, default 1; `q` (string, **required**) — Search keyword or phrase; `sort` (string, optional) — Result sort order, default relevance. One of pa (Price Low to High), pd (Price High to Low), tr (Top Rated), rc (Most Reviewed), az (Name A-Z), za (Name Z-A)

### `cvs_store_locator`

- **HTTP:** `GET /cvs/store-locator`
- **What:** CVS store locator. Returns nearby CVS store locations for a ZIP code, a free-text address/city/state, or a latitude/longitude pair: address, phone, fax, distance, and retail store hours, plus a has_pharmacy existence flag and a list of general service indicators (e.g. photo, ATM, same-day delivery). Covers general store info only -- this does not return pharmacy hours, pharmacy phone, prescription data, or any patient-specific information. zip is a 5-digit US ZIP code; alternatively supply address (a free-text location such as a city, state, or street address) or latitude and longitude together. When more than one is supplied, zip wins, then address, then latitude/longitude. Optionally narrow results to stores carrying one specific service via the service param (the same code vocabulary the response's services field uses); only one service value is accepted per request. CVS.com is only available from US/US-territory egress; a request from an unsupported region returns an upstream error rather than an empty result.
- **Params:** `address` (string, optional) — Free-text location -- a city, state, or street address, e.g. \; `latitude` (number, optional) — Latitude, used together with longitude when zip and address are not supplied; `longitude` (number, optional) — Longitude, used together with latitude when zip and address are not supplied; `service` (string, optional) — Narrow results to stores carrying one specific service; `zip` (string, optional) — 5-digit US ZIP code, e.g. \

## Lazada (5)

### `lazada_categories`

- **HTTP:** `GET /lazada/categories`
- **What:** Get a Lazada country storefront's category directory. Returns one Lazada country storefront's public category directory from the server-rendered LazMall navigation menu. The response includes top-level groups, categories, and subcategory links; it does not include product listings.
- **Params:** `country` (string, optional) — Lazada country storefront. Defaults to id.

### `lazada_category_products`

- **HTTP:** `GET /lazada/category-products`
- **What:** Get a Lazada country storefront's product listing for one category. Returns one Lazada country storefront's product listing for one category, optionally filtered to one brand within it. Product cards include item ids, canonical product URLs, images, prices, ratings, and review counts, with pagination and sort. The category (and optional brand) value is the raw Lazada path slug, not a display name -- use the categories endpoint's own returned URLs to discover a category's slug.
- **Params:** `brand` (string, optional) — Optional brand path slug to filter within the category.; `category` (string, **required**) — Lazada category path slug, e.g. \; `country` (string, optional) — Lazada country storefront. Defaults to id.; `page` (integer, optional) — Result page, 1-indexed. Defaults to 1.; `sort` (string, optional) — Sort order. Defaults to popularity.

### `lazada_home`

- **HTTP:** `GET /lazada/home`
- **What:** Get a Lazada country storefront's homepage feed. Returns one Lazada country storefront's anonymous homepage feed: current flash-sale product cards, featured category links, and (where shown) an official-stores carousel. Product-detail and free-text catalog pages are not included because Lazada's stateless routes currently return an anti-bot challenge on every country domain.
- **Params:** `country` (string, optional) — Lazada country storefront. Defaults to id.

### `lazada_product`

- **HTTP:** `GET /lazada/product`
- **What:** Get a Lazada country storefront's product-detail page. Returns one Lazada country storefront's product-detail page: title, brand, full description, image gallery, category breadcrumb, and selectable variant properties. item_id (and, for a specific variant, sku_id) are the same ids the search, category-products, and home endpoints already return as item_id. Price is best-effort, read from the page's own display-tracking data rather than a dedicated pricing field; rating and review count are not available on this endpoint because Lazada fetches them client-side after the initial page load.
- **Params:** `country` (string, optional) — Lazada country storefront. Defaults to id.; `item_id` (integer, **required**) — Lazada item id.; `sku_id` (integer, optional) — Optional Lazada sku id, for a specific variant.

### `lazada_search`

- **HTTP:** `GET /lazada/search`
- **What:** Search a Lazada country storefront's catalog by keyword. Returns one Lazada country storefront's free-text catalog search results: product cards with item ids, canonical product URLs, images, prices in the storefront's own currency, ratings, and review counts, with pagination and sort. Lazada's own search always substitutes generic or trending items rather than returning a genuinely empty result set, so an empty items list or a low total_results is not by itself a reliable "no matches" signal.
- **Params:** `country` (string, optional) — Lazada country storefront. Defaults to id.; `page` (integer, optional) — Result page, 1-indexed. Defaults to 1.; `q` (string, **required**) — Free-text search query.; `sort` (string, optional) — Sort order. Defaults to popularity.

## Otto (3)

### `otto_categories`

- **HTTP:** `GET /otto/categories`
- **What:** Get Otto.de's top-level categories. Lists the top-level categories shown in Otto.de's homepage navigation, each with its name and its canonical browse URL. The response also gives the `count` of categories and a `fetched_at` time. It takes no parameters.
- **Params:** _none_

### `otto_product`

- **HTTP:** `GET /otto/product`
- **What:** Get an Otto.de product. Returns a product's public detail, images, selectable colors and sizes. This endpoint uses a browser renderer because Otto.de product pages require JavaScript rendering.
- **Params:** `url` (string, **required**) — Canonical Otto.de product URL returned by otto-search

### `otto_search`

- **HTTP:** `GET /otto/search`
- **What:** Search Otto.de products. Searches Otto.de's public catalogue and returns the server-rendered product cards. offset advances by Otto's fixed 109-card page size; valid values are 0, 109, 218, and so on.
- **Params:** `offset` (integer, optional) — Result offset; non-negative multiple of 109; `q` (string, **required**) — Product search keyword

## Tokopedia (8)

### `tokopedia_autocomplete`

- **HTTP:** `GET /tokopedia/autocomplete`
- **What:** Autocomplete Tokopedia product searches. Returns current public Tokopedia search suggestions for a partial keyword. Suggestions include canonical product-search URLs and are not product-search results.
- **Params:** `q` (string, **required**) — Partial product keyword, up to 100 characters

### `tokopedia_category`

- **HTTP:** `GET /tokopedia/category`
- **What:** Browse a Tokopedia category. Returns public product cards from a canonical Tokopedia category path. `path` must begin with `/p/`; use the category page path, not a product or search URL.
- **Params:** `path` (string, **required**) — Canonical Tokopedia category path beginning with /p/

### `tokopedia_home`

- **HTTP:** `GET /tokopedia/home`
- **What:** Get Tokopedia home recommendations. Returns public product-card recommendations for a current Tokopedia home tab. Omit `tab_id` for the first available tab; discover other tabs through `/tokopedia/home/tabs`.
- **Params:** `page` (integer, optional) — Recommendation page from 1 through 5; `tab_id` (string, optional) — Current ID from /tokopedia/home/tabs

### `tokopedia_home_tabs`

- **HTTP:** `GET /tokopedia/home/tabs`
- **What:** List Tokopedia home recommendation tabs. Lists the current Tokopedia home recommendation tabs, each with its `id`, `name` and an optional image URL, plus a `fetched_at` timestamp. It takes no parameters. Pass a returned `id` as `tab_id` to `/tokopedia/home` to load that tab.
- **Params:** _none_

### `tokopedia_product`

- **HTTP:** `GET /tokopedia/product`
- **What:** Get a Tokopedia product's public detail. Returns public product detail from a canonical Tokopedia shop domain and product key. This endpoint does not accept arbitrary URLs; numeric product IDs are returned when the product page exposes them but cannot be used as lookup input.
- **Params:** `product_key` (string, **required**) — Canonical Tokopedia product key; `shop_domain` (string, **required**) — Canonical Tokopedia shop domain

### `tokopedia_product_review_filters`

- **HTTP:** `GET /tokopedia/product/review-filters`
- **What:** Get Tokopedia product review-filter metadata. Returns which public review media, rating, and topic filters are available for a numeric product ID. It does not return review text, review media, or a review archive.
- **Params:** `product_id` (string, **required**) — Numeric Tokopedia product ID

### `tokopedia_search`

- **HTTP:** `GET /tokopedia/search`
- **What:** Search Tokopedia products. Returns public Tokopedia product cards for a keyword from Tokopedia's public product-search operation. `sort` accepts `3` (lowest price), `4` (highest price), `5` (most reviewed), `9` (newest), or `23` (most relevant). Repeat `filter` as `key:value` using values from `/tokopedia/search/filters`.
- **Params:** `filter` (array, optional) — Repeat live key:value filter selections from /tokopedia/search/filters; `page` (integer, optional) — Search page from 1 through 5; `q` (string, **required**) — Product keyword; `sort` (integer, optional) — Sort: 3 lowest price, 4 highest price, 5 most reviewed, 9 newest, 23 most relevant

### `tokopedia_search_filters`

- **HTTP:** `GET /tokopedia/search/filters`
- **What:** Get Tokopedia search filters and sorts. Returns the live filter tree and supported sort choices for a Tokopedia product search. The response includes categories when the current query exposes them, store type, delivery location, price, rating, offer, condition, recency, shipping, and stock options as applicable.
- **Params:** `q` (string, **required**) — Product keyword

## SparkFun (4)

### `sparkfun_categories`

- **HTTP:** `GET /sparkfun/categories`
- **What:** List SparkFun categories. Lists SparkFun's top-level browse categories. Each has an id, name, `url_key` and `url_path`. Pass a category's `url_key` to `sparkfun-category` to browse it. Takes no parameters, and the set follows the live storefront catalogue.
- **Params:** _none_

### `sparkfun_category`

- **HTTP:** `GET /sparkfun/category`
- **What:** Browse a SparkFun category. Returns paginated public products and dynamic facet filters for a SparkFun category URL key. Each filter must be `attribute:value`; use values from the response's filters array.
- **Params:** `filter` (array, optional) — Repeatable dynamic facet in attribute:value form; `page` (integer, optional) — One-based result page (1-100); `per_page` (integer, optional) — Products per page (1-24); `url_key` (string, **required**) — SparkFun category URL key

### `sparkfun_product`

- **HTTP:** `GET /sparkfun/product`
- **What:** Get a SparkFun product. Returns one SparkFun product by `sku`, for example `DEV-18158`: name, URL, stock status, current minimum price and currency, main image and media gallery, categories, and a cleaned short description. `recommendations` lists related, upsell or crosssell products when available. An unknown SKU returns 404.
- **Params:** `sku` (string, **required**) — SparkFun product SKU

### `sparkfun_search`

- **HTTP:** `GET /sparkfun/search`
- **What:** Search SparkFun products. Searches public SparkFun product data with pagination and dynamic facet filters. Each filter must be `attribute:value`; use values from the response's filters array.
- **Params:** `filter` (array, optional) — Repeatable dynamic facet in attribute:value form; `page` (integer, optional) — One-based result page (1-100); `per_page` (integer, optional) — Products per page (1-24); `q` (string, **required**) — Product search query

## AliExpress (3)

### `aliexpress_reviews`

- **HTTP:** `GET /aliexpress/reviews`
- **What:** Get AliExpress product reviews. Returns one page of public reviews and rating statistics for a numeric AliExpress product id. AliExpress currently returns up to 20 review records per page.
- **Params:** `page` (integer, optional) — 1-indexed review page (1-50), defaults to 1; `product_id` (string, **required**) — Numeric AliExpress product id

### `aliexpress_search`

- **HTTP:** `GET /aliexpress/search`
- **What:** Search AliExpress products. Returns one page (up to 60 products) of public keyword search results with product ids, titles, links, images, prices, ratings, sold text, discount, SKU id, ship-from country, and store name when AliExpress lists them. Results can be sorted and filtered by price, free shipping, the Choice program, and product attributes; list the attribute values for a keyword with the search-filters endpoint. The search uses the anonymous US English/USD locale. Product-detail pages are currently unavailable through the supported HTTP profiles.
- **Params:** `attr` (string, optional) — Attribute filter <attributeId>-<valueId>, from the search-filters endpoint for the same q; comma-separate up to 5 values, one per attribute group; `choice` (boolean, optional) — Only products in AliExpress's Choice program; `free_shipping` (boolean, optional) — Only free-shipping products; `max_price` (number, optional) — Maximum price in USD (0-1000000), not below min_price; `min_price` (number, optional) — Minimum price in USD (0-1000000); `page` (integer, optional) — 1-indexed result page (1-200), defaults to 1; `q` (string, **required**) — Free-text search keywords; `sort` (string, optional) — Sort order. Allowed values: best_match (default), orders, price_asc, price_desc

### `aliexpress_search_filters`

- **HTTP:** `GET /aliexpress/search-filters`
- **What:** List AliExpress search filters. Returns every sort value and boolean filter the search endpoint accepts, plus the product-attribute filters (brand, color, style, and so on) AliExpress offers for the keyword, as ready-to-use attr values. Attribute filters differ per keyword, so call this with the same q as the search.
- **Params:** `q` (string, **required**) — Free-text search keywords
