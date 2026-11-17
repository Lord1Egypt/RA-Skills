# luxury-resale-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**162 endpoints across 21 platform group(s).**

## 1stDibs (4)

### `firstdibs_categories`

- **HTTP:** `GET /1stdibs/categories`
- **What:** List 1stDibs categories and filters. Returns the live handbags category directory, sort keys, price presets, and filter values discovered from 1stDibs. Returned category slugs are valid for firstdibs-search.
- **Params:** _none_

### `firstdibs_designers`

- **HTTP:** `GET /1stdibs/designers`
- **What:** List 1stDibs designers. Lists the designer filter values found on a 1stDibs category page, with a `count` and, for each designer, its `name`, `slug` and `url`. `category` is optional and comes from `firstdibs-categories`. Each `slug` can be used as the designer filter in `firstdibs-search`.
- **Params:** `category` (string, optional) — Category slug from firstdibs-categories

### `firstdibs_product`

- **HTTP:** `GET /1stdibs/product`
- **What:** Get a 1stDibs product. Returns the details of one 1stDibs product, identified by its product `url`: `name`, `brand`, `category`, `description`, `images`, `price` with `currency`, and the `in_stock` flag. The price is in USD and is present only when 1stDibs shows one.
- **Params:** `url` (string, **required**) — 1stDibs product URL

### `firstdibs_search`

- **HTTP:** `GET /1stdibs/search`
- **What:** Search 1stDibs listings. Searches or browses 1stDibs handbags and purses with category, designer, price, sale, color, period, location, gender, origin, seller, and sort filters.
- **Params:** `category` (string, optional) — Category slug from firstdibs-categories; `color` (string, optional) — Color value; `designer` (string, optional) — Designer slug from firstdibs-designers; `gender` (string, optional) — Gender value; `location` (string, optional) — Item location; `measurements` (boolean, optional) — Listings with measurements; `on_sale` (boolean, optional) — On-sale listings only; `origin` (string, optional) — Place-of-origin value; `page` (integer, optional) — 1-based page; `per_page` (integer, optional) — Results per page; `period` (string, optional) — Period value; `price` (string, optional) — Price preset; `price_max` (number, optional) — Maximum price; `price_min` (number, optional) — Minimum price; `q` (string, optional) — Free-text search; `recognized_seller` (boolean, optional) — Recognized seller listings only; `returnable` (boolean, optional) — Returnable items only; `sort` (string, optional) — Sort; `this_week` (boolean, optional) — Listings added this week; `top_seller` (boolean, optional) — Top seller listings only

## Balenciaga (7)

### `balenciaga_categories`

- **HTTP:** `GET /balenciaga/categories`
- **What:** List Balenciaga categories. Lists Balenciaga's storefront categories with `count`, and for each its `id`, `name`, `department`, `path` and `url`. Each `path` is the value `balenciaga-category` accepts. The response reports `country` (`ZW`) and `language` (`en`).
- **Params:** _none_

### `balenciaga_category`

- **HTTP:** `GET /balenciaga/category`
- **What:** Browse a Balenciaga category. Returns one Balenciaga category listing from the site's own Search-ShowAjax fragment. path comes from balenciaga-categories. sort accepts latest, price_ascending, or price_descending. filters is a comma-separated list of exact field:value pairs from the response's live facets; repeat a field to OR multiple values within that facet; omit it for an unfiltered listing.
- **Params:** `filters` (string, optional) — Comma-separated exact facet filters; repeat a field for OR values, for example akeneo_macroColor:BLACK,akeneo_macroColor:WHITE; `limit` (integer, optional) — Products per page, defaults to 16, maximum 48; `page` (integer, optional) — One-based page number, defaults to 1; `path` (string, **required**) — Category path from balenciaga-categories; `sort` (string, optional) — Sort order

### `balenciaga_product`

- **HTTP:** `GET /balenciaga/product`
- **What:** Get a Balenciaga product. Returns structured product detail from Balenciaga's product page, including schema.org name/SKU/price/availability, images, color variants, and visible product details. url must be a product URL returned by balenciaga-category or balenciaga-search.
- **Params:** `url` (string, **required**) — Product URL from a Balenciaga listing

### `balenciaga_product_variants`

- **HTTP:** `GET /balenciaga/product/variants`
- **What:** Get Balenciaga product variations. Returns Balenciaga's live color/size variation matrix for a product, including variation ids, selection/sellability flags, care text, availability, and related product ids. url may be a product URL or a Product-Variation URL from balenciaga-product's colors[].url.
- **Params:** `url` (string, **required**) — Balenciaga product URL or Product-Variation URL

### `balenciaga_search`

- **HTTP:** `GET /balenciaga/search`
- **What:** Search Balenciaga products. Searches Balenciaga's storefront by keyword using the site's own product-grid fragment. q is required; sort accepts latest, price_ascending, or price_descending; page is one-based with 12 products per page; and filters accepts comma-separated exact field:value pairs from live facets. Repeat a field to OR multiple values within that facet. A genuine no-result query returns an empty products list.
- **Params:** `filters` (string, optional) — Comma-separated exact facet filters; repeat a field for OR values, for example akeneo_macroColor:BLACK,akeneo_macroColor:WHITE; `page` (integer, optional) — One-based page number, defaults to 1; `q` (string, **required**) — Free-text search query; `sort` (string, optional) — Sort order

### `balenciaga_store_countries`

- **HTTP:** `GET /balenciaga/store-countries`
- **What:** List Balenciaga store-locator countries. Lists the countries Balenciaga's store locator offers, each with a country `code` and `name`, plus a `count`. Each code is accepted by `balenciaga-stores`. The response also reports the storefront `country` and `language`.
- **Params:** _none_

### `balenciaga_stores`

- **HTTP:** `GET /balenciaga/stores`
- **What:** List Balenciaga stores. Returns Balenciaga's public physical-store directory for one country, including addresses, coordinates, phone numbers, opening hours, and store-service flags. Use balenciaga-store-countries to discover the complete accepted country enum.
- **Params:** `country` (string, **required**) — Two-letter country code

## Burberry (6)

### `burberry_categories`

- **HTTP:** `GET /burberry/categories`
- **What:** List Burberry categories. Lists every department, section, and leaf category from Burberry's own site navigation, flattened with a breadcrumb-style path. Each entry's url is exactly what burberry-category's own category parameter accepts. Filter to one top-level department with department (e.g. Women, Men, Children, Gifts, Trench, Scarves, Bags, Beauty & Fragrances, Sale); omit for every department. See the response's own departments field for the live list.
- **Params:** `department` (string, optional) — Top-level department to filter to, e.g. Women, Men, Children -- omit for every department

### `burberry_category`

- **HTTP:** `GET /burberry/category`
- **What:** Browse a Burberry category. Returns one page (20 products) of a Burberry category/browse listing. category is the site-relative category path, e.g. /l/womens-clothing/new-arrivals/ -- use burberry-categories to discover every valid value instead of guessing from site URLs. offset paginates in increments of 20 (the upstream's own fixed page size). sort selects the result order. The response includes the upstream's own available filters (facets) with live per-option result counts; feed a selection back in via facets, a comma-separated list of property:value pairs taken from this same response's facets field (e.g. benefit:bags,dotcomreportingcolour:black -- see a live response for the values valid for that category). At most one value per facet property; an unmatched or invalid combination returns a well-formed empty result, not an error.
- **Params:** `category` (string, **required**) — Site-relative category path -- see burberry-categories; `facets` (string, optional) — Comma-separated property:value facet filters, taken from this same response's own facets field, e.g. benefit:bags,dotcomreportingcolour:black -- at most one value per property; `offset` (integer, optional) — Zero-based result offset, in increments of 20; `sort` (string, optional) — Sort order

### `burberry_product`

- **HTTP:** `GET /burberry/product`
- **What:** Get a Burberry product. Returns product detail for one Burberry product page: name, sku, colour, material, description, price, stock status, every product image, and every other purchasable colourway of the same style. url is the site-relative product path, e.g. /check-cashmere-cardigan-p81336111, as returned by burberry-search's or burberry-category's own products[].url field.
- **Params:** `url` (string, **required**) — Site-relative product path, from a search or category result's url field

### `burberry_related`

- **HTTP:** `GET /burberry/related`
- **What:** Get related Burberry products. Returns the cross-sell surfaces a real Burberry product page itself loads for that product: similar_products (algorithmically similar items) and shop_the_look (other pieces in the same styled outfit, when the upstream has curated one -- most products have none, returned as a well-formed empty list, not an error). url is the site-relative product path, e.g. /check-cashmere-cardigan-p81336111, as returned by burberry-search's, burberry-category's, or burberry-product's own url field.
- **Params:** `url` (string, **required**) — Site-relative product path, from a search, category, or product result's url field

### `burberry_search`

- **HTTP:** `GET /burberry/search`
- **What:** Search Burberry products. Searches Burberry's product catalog by keyword. Returns product summaries plus the upstream's own available filters (facets) with live per-option result counts. offset paginates in increments of 20 (the upstream's own fixed page size). sort selects the result order. facets applies a facet selection back, a comma-separated list of property:value pairs taken from this same response's facets field (e.g. benefit:bags,dotcomreportingcolour:black). A query with no matches, or a facet combination with no matches, returns a well-formed empty result, not an error. Unlike burberry-category, this response has no true grand-total result count -- only the current page's own count.
- **Params:** `facets` (string, optional) — Comma-separated property:value facet filters, taken from this same response's own facets field, e.g. benefit:bags,dotcomreportingcolour:black -- at most one value per property; `offset` (integer, optional) — Zero-based result offset, in increments of 20; `query` (string, **required**) — Search keyword; `sort` (string, optional) — Sort order

### `burberry_suggest`

- **HTTP:** `GET /burberry/suggest`
- **What:** Get Burberry search-box suggestions. Returns Burberry's own search-box suggestions (typeahead) for a partial query: a flat list of suggested search phrases, each with its own live result count on the search index. Not product data.
- **Params:** `query` (string, **required**) — Partial search query

## Chrono24 (8)

### `chrono24_autocomplete`

- **HTTP:** `GET /chrono24/autocomplete`
- **What:** Get Chrono24 search-box suggestions. Fetches Chrono24's own search-box typeahead suggestions for a partial query: each suggested phrase with its own live result count, plus the Chrono24 search URL it resolves to. Useful for building a search box against chrono24-search without guessing a full query.
- **Params:** `query` (string, **required**) — Partial search text, e.g. \

### `chrono24_brands`

- **HTTP:** `GET /chrono24/brands`
- **What:** List Chrono24 watch brands. Returns Chrono24's full watch-brand index: every brand name and the slug identifying it, usable as the brand parameter on chrono24-models and chrono24-search. This is the discovery endpoint for that parameter, so every accepted value is obtainable from this API rather than by reading the website.
- **Params:** _none_

### `chrono24_dealer`

- **HTTP:** `GET /chrono24/dealer`
- **What:** Get a Chrono24 dealer's storefront. Fetches one Chrono24 dealer/seller's public storefront page: business description, trust badge, average buyer rating and review count, lifetime watches-sold count, and their current listed inventory in the same shape chrono24-search returns. slug is found in a chrono24-search or chrono24-listing result's seller link; there is no separate dealer-discovery endpoint since dealer slugs are not a closed set Chrono24 publishes an index of.
- **Params:** `slug` (string, **required**) — Dealer slug from a listing's seller link

### `chrono24_dealer_reviews`

- **HTTP:** `GET /chrono24/dealer/reviews`
- **What:** Get a Chrono24 dealer's buyer reviews. Fetches one page of a Chrono24 dealer/seller's buyer reviews: reviewer name and country, review date, star-rating breakdown (shipping/description/communication), whether the buyer recommends the seller, their free-text comment, and the dealer's own reply when present. slug is the same dealer slug chrono24-dealer takes.
- **Params:** `min_stars` (integer, optional) — Keep only reviews rating the dealer at least this many stars, 0-5. 0 returns every review; `page` (integer, optional) — One-based result page; `page_size` (integer, optional) — Reviews per page, 1-50; `slug` (string, **required**) — Dealer slug from a listing's seller link; `sort` (string, optional) — Result order. One of: relevance, newest, with_recommendation, without_recommendation

### `chrono24_facets`

- **HTTP:** `GET /chrono24/facets`
- **What:** Get a Chrono24 search filter's accepted values. Fetches every value Chrono24 accepts for one of chrono24-search's advanced-search filter params, each with its own live listing count: the discovery endpoint for condition, used_or_new, case_material, dial_color, bracelet_material, movement_type, gender, watch_type and stock_info.
- **Params:** `group` (string, **required**) — Filter to list values for

### `chrono24_listing`

- **HTTP:** `GET /chrono24/listing`
- **What:** Get a Chrono24 watch listing's detail. Fetches one Chrono24 listing's full detail page: brand, model, reference number, price with currency and negotiability, condition, year of production, movement, case material and diameter, bracelet material, location, availability, seller type, photos, and the complete raw spec table Chrono24 itself shows (grouped by section: Basic Info, Caliber, Case, Bracelet/strap, Functions). path is the listing URL from a chrono24-search result's url field; Chrono24 has no lookup by numeric id alone.
- **Params:** `path` (string, **required**) — Listing URL or path from a chrono24-search result's url field

### `chrono24_models`

- **HTTP:** `GET /chrono24/models`
- **What:** List Chrono24 models for a brand. Returns every model/collection Chrono24 lists for one watch brand (e.g. Rolex Submariner, Rolex Datejust), each with the slug identifying it, usable as the model parameter on chrono24-search. This is the discovery endpoint for that parameter, so every accepted value for a brand is obtainable from this API rather than by reading the website.
- **Params:** `brand` (string, **required**) — Brand slug from chrono24-brands

### `chrono24_search`

- **HTTP:** `GET /chrono24/search`
- **What:** Search Chrono24 watch listings. Searches Chrono24's luxury-watch marketplace by free-text keyword, or browses one brand's (optionally narrowed to one model's) current listings, returning result cards: title, price with currency, seller type, seller country, promotional badge, image, and the listing URL to pass to chrono24-listing. At least one of query or brand is required. Optional advanced-search filters (condition, used_or_new, case_material, dial_color, bracelet_material, movement_type, gender, watch_type, stock_info) narrow results further; each filter's accepted values are discoverable from chrono24-facets and echoed back in the response's filters field.
- **Params:** `bracelet_material` (string, optional) — Advanced-search filter, values from chrono24-facets group=braceletMaterial; `brand` (string, optional) — Brand slug from chrono24-brands. At least one of query or brand is required; `case_material` (string, optional) — Advanced-search filter, values from chrono24-facets group=caseMaterial; `condition` (string, optional) — Advanced-search filter, values from chrono24-facets group=condition; `dial_color` (string, optional) — Advanced-search filter, values from chrono24-facets group=dialColor; `gender` (string, optional) — Advanced-search filter, values from chrono24-facets group=gender; `model` (string, optional) — Model slug from chrono24-models (requires brand); `movement_type` (string, optional) — Advanced-search filter, values from chrono24-facets group=movementType; `page` (integer, optional) — One-based result page; `page_size` (integer, optional) — Results per page. Chrono24's own UI offers 30, 60 or 120; defaults to Chrono24's own default; `query` (string, optional) — Free-text keyword search, e.g. \; `sort` (string, optional) — Result order. One of: relevance, price_asc, price_desc, newest, popularity; `stock_info` (string, optional) — Advanced-search filter, values from chrono24-facets group=stockInfo; `used_or_new` (string, optional) — Advanced-search filter, values from chrono24-facets group=usedOrNew; `watch_type` (string, optional) — Advanced-search filter, values from chrono24-facets group=watchType

## Farfetch (4)

### `farfetch_categories`

- **HTTP:** `GET /farfetch/categories`
- **What:** Farfetch category directory. Returns every department's top-level category directory (name, slug, URL). Each slug is usable directly as the category filter on GET /farfetch/search. Public data sourced live from Farfetch's own listing pages.
- **Params:** _none_

### `farfetch_designers`

- **HTTP:** `GET /farfetch/designers`
- **What:** Farfetch designer directory. Returns a department's full designer directory (name, slug, URL). Each slug is usable directly as the designer filter on GET /farfetch/search. Public data sourced from Farfetch's own designer-directory pages.
- **Params:** `gender` (string, **required**) — Department: women, men, kids

### `farfetch_product`

- **HTTP:** `GET /farfetch/product`
- **What:** Farfetch product detail. Returns a Farfetch product's full detail: name, brand, color, description, images, category breadcrumb, and every size variant with its own price and availability. Public data sourced from Farfetch's own product pages.
- **Params:** `gender` (string, **required**) — Department: women, men, kids; `slug` (string, **required**) — Product URL slug from a search result's id field

### `farfetch_search`

- **HTTP:** `GET /farfetch/search`
- **What:** Search Farfetch listings. Browses Farfetch's luxury multi-brand marketplace by department plus a designer and/or category filter (at least one is required), returning listing summaries (name, brand, price, image, availability) and the upstream page count.
- **Params:** `category` (string, optional) — Category slug from GET /farfetch/categories; designer or category is required; `designer` (string, optional) — Designer slug from GET /farfetch/designers; designer or category is required; `gender` (string, **required**) — Department: women, men, kids; `page` (integer, optional) — 1-based page number; defaults to 1

## Fashionphile (12)

### `fashionphile_collection_products`

- **HTTP:** `GET /fashionphile/collections/{handle}/products`
- **What:** List Fashionphile collection products. Returns products from one Fashionphile (https://www.fashionphile.com) collection. The storefront URL is fixed server-side; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `fashionphile_collections`

- **HTTP:** `GET /fashionphile/collections`
- **What:** List Fashionphile collections. Returns collections from Fashionphile (https://www.fashionphile.com). The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `fashionphile_page`

- **HTTP:** `GET /fashionphile/pages/{handle}`
- **What:** Get a Fashionphile static page. Returns one Fashionphile static page by its required `handle`, such as `about`: title, URL, plain-text content, and created, updated and published dates. An unknown handle returns `404`. In a fallback mode flagged by `transport_mode: "ssr_embedded"`, the response omits `id`.
- **Params:** `handle` (string, **required**) — Page handle

### `fashionphile_pages`

- **HTTP:** `GET /fashionphile/pages`
- **What:** List Fashionphile static pages. Lists Fashionphile static pages, 50 per page by default (`limit`, max 250), with `page` starting at 1. Each page has its handle, title, URL, plain-text content, and created, updated and published dates. When `transport_mode` is `ssr_embedded`, items carry only `handle`, `url` and `updated_at`. Fetch a single page for its full content.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `fashionphile_product`

- **HTTP:** `GET /fashionphile/products/{handle}`
- **What:** Get a Fashionphile product. Returns product detail for one Fashionphile (https://www.fashionphile.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `fashionphile_product_recommendations`

- **HTTP:** `GET /fashionphile/products/{handle}/recommendations`
- **What:** List Fashionphile product recommendations. Returns recommended products for one Fashionphile (https://www.fashionphile.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `fashionphile_products`

- **HTTP:** `GET /fashionphile/products`
- **What:** List Fashionphile products. Returns products from Fashionphile's (https://www.fashionphile.com) public product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `fashionphile_search`

- **HTTP:** `GET /fashionphile/search`
- **What:** Search Fashionphile products. Returns ranked products from Fashionphile's (https://www.fashionphile.com) own full-text and faceted product search, including condition grade, discount percentage, and other filter attributes not available from the classic catalog endpoints in this family. The storefront URL is fixed server-side. Omitting `q` browses the full catalog subject to any condition/vendor/availability filters and the chosen sort. By default only in-stock listings are searched, matching the storefront; `availability=sold` searches the sold archive instead. `total_items` is the exact number of products matching the query and all filters.
- **Params:** `availability` (string, optional) — Which listings to search. Allowed values: available (in-stock only, default), sold (sold archive only), all; `condition` (string, optional) — Filter by condition grade. Allowed values: New, Excellent, Giftable, Shows Wear, Worn, Flawed, Fair; `limit` (integer, optional) — Maximum products, defaults to 20 and supports up to 50; `page` (integer, optional) — 1-based page, defaults to 1; `q` (string, optional) — Search query text; `sort` (string, optional) — Sort order. Allowed values: relevance, newest, price_asc, price_desc; `vendor` (string, optional) — Filter by exact designer/vendor name, e.g. Chanel

### `fashionphile_search_suggest`

- **HTTP:** `GET /fashionphile/search/suggest`
- **What:** Get Fashionphile search suggestions. Returns products, collections, and query suggestions from Fashionphile's (https://www.fashionphile.com) predictive search. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `fashionphile_sitemap_urls`

- **HTTP:** `GET /fashionphile/sitemap/urls`
- **What:** List Fashionphile sitemap URLs. Lists URL entries from Fashionphile's sitemaps, filtered by `type` (`all` by default, or `products`, `collections`, `pages`, `blogs`, `agentic_discovery`, `other`) and capped by `limit` (default 50, max 250). Each entry has its `loc`, inferred type, handle, last modified date, change frequency, and optional images.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `fashionphile_sitemaps`

- **HTTP:** `GET /fashionphile/sitemaps`
- **What:** List Fashionphile sitemaps. Lists the child sitemaps in Fashionphile's sitemap index, with no parameters. Each entry has its `loc` URL and an inferred `type`: `products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`. Product sitemap URLs may carry `from` and `to` query values.
- **Params:** _none_

### `fashionphile_store`

- **HTTP:** `GET /fashionphile/store`
- **What:** Get Fashionphile store metadata. Returns storefront metadata for Fashionphile (https://www.fashionphile.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_

## Grailed (11)

### `grailed_categories`

- **HTTP:** `GET /grailed/categories`
- **What:** List Grailed's facet taxonomy. Returns Grailed's full facet taxonomy for the enum-like parameters grailed-search/grailed-sold-listings accept: department, category, category_path (a more granular subcategory slug), condition, color, and size, each with its own live listing count. department and condition are exhaustive closed sets (2 and 5 values respectively); category/category_path/color/size are the full, exhaustive value space as of the request. Designer is NOT included here (7,363 values, far too large for a facet-count response) -- see grailed-designers for that discovery endpoint.
- **Params:** _none_

### `grailed_collection`

- **HTTP:** `GET /grailed/collection`
- **What:** Get one Grailed curated collection's listings. Returns one Grailed curated homepage collection's full listing set. id is the collection's numeric id, from grailed-collections' own collections[].id field. An unknown id returns a typed not-found error.
- **Params:** `id` (integer, **required**) — Collection id, from grailed-collections' own collections[].id field

### `grailed_collections`

- **HTTP:** `GET /grailed/collections`
- **What:** List Grailed's curated homepage collections. Returns Grailed's own curated homepage merchandising collections (e.g. "Trending: Apparel", "Dark Luxury", "Chromed Out") -- editorial/trending shelves distinct from a plain search or facet browse. Each collection's numeric id is the value grailed-collection's own id parameter accepts.
- **Params:** _none_

### `grailed_designers`

- **HTTP:** `GET /grailed/designers`
- **What:** List or search Grailed's designer/brand taxonomy. Returns a page of Grailed's full designer/brand taxonomy (7,363 designers as of 2026-09-09) -- the value space grailed-search/grailed-sold-listings' own designer parameter accepts (by name). q is an optional free-text filter (typo-tolerant, e.g. a partial name for typeahead-style lookup); an empty q lists the full taxonomy ordered by Grailed's own default ranking (most-listed designers first).
- **Params:** `limit` (integer, optional) — Results per page, defaults to 24, maximum 100; `page` (integer, optional) — One-based page number, defaults to 1; `q` (string, optional) — Free-text designer name filter

### `grailed_listing`

- **HTTP:** `GET /grailed/listing`
- **What:** Get a Grailed listing. Returns full listing-detail data for one Grailed listing: description, every photo, measurements, designers, and the seller's full profile -- richer than the flattened summary grailed-search/grailed-sold-listings return per listing. id is the listing's numeric id, from a search or sold-listings result's own listings[].id field.
- **Params:** `id` (integer, **required**) — Listing id, from a search or sold-listings result's own listings[].id field

### `grailed_search`

- **HTTP:** `GET /grailed/search`
- **What:** Search or browse Grailed active listings. Searches or browses Grailed's (grailed.com) peer-to-peer resale marketplace for currently-active listings. q, designer, department, category, size, color, condition, min_price, and max_price are all optional and combine as an AND -- a free-text q can be combined with any of the facet filters in the same request, or every field can be omitted to browse the full active catalog by Grailed's own "heat" relevance ranking. designer accepts one of the values grailed-designers' own designers[].name field returns; department, category, size, and color accept values from grailed-categories' own departments[].value/categories[].value/sizes[].value/colors[].value fields. condition and sort are fixed, closed enums (listed below). Keyword search uses typo-tolerant relevance ranking, not a guaranteed exact match. A query with genuinely zero matches returns a well-formed empty result rather than an error.
- **Params:** `category` (string, optional) — Category facet filter, from grailed-categories' own categories[].value field; `color` (string, optional) — Color facet filter, from grailed-categories' own colors[].value field; `condition` (string, optional) — Condition filter; `department` (string, optional) — Department filter; `designer` (string, optional) — Designer/brand name filter, from grailed-designers' own designers[].name field; `limit` (integer, optional) — Results per page, defaults to 24, maximum 100; `max_price` (number, optional) — Maximum price (inclusive), in USD; `min_price` (number, optional) — Minimum price (inclusive), in USD; `page` (integer, optional) — One-based page number, defaults to 1; `q` (string, optional) — Free-text search query; `size` (string, optional) — Size facet filter, from grailed-categories' own sizes[].value field; `sort` (string, optional) — Sort order, defaults to heat

### `grailed_seller`

- **HTTP:** `GET /grailed/seller`
- **What:** Get a Grailed seller's profile and active listings. Returns a Grailed seller's public profile plus a page of their current active listings (Grailed's own "shop" view of a seller). username is the seller's Grailed username, from a listing's own seller.username field or grailed.com/{username}. Listings only ever contains that seller's ACTIVE listings; use grailed-sold-listings with a designer/query filter for a broader sales-history lookup, since sold listings are not filterable by seller through this endpoint. An unknown username returns a typed not-found error.
- **Params:** `limit` (integer, optional) — Listings per page, defaults to 24, maximum 100; `page` (integer, optional) — One-based page number for the seller's listings, defaults to 1; `username` (string, **required**) — Grailed username

### `grailed_seller_reviews`

- **HTTP:** `GET /grailed/seller-reviews`
- **What:** Get a Grailed seller's buyer feedback. Returns a page of a Grailed seller's individual buyer feedback entries (rating, note, feedback tags, and the listing each review was left for) -- reputation detail grailed-seller does not carry (grailed-seller only exposes the aggregate rating_average/rating_count). username is the seller's Grailed username, from a listing's own seller.username field or grailed.com/{username}. An unknown username returns a typed not-found error.
- **Params:** `page` (integer, optional) — One-based page number, defaults to 1; `username` (string, **required**) — Grailed username

### `grailed_similar_listings`

- **HTTP:** `GET /grailed/similar-listings`
- **What:** Get listings similar to a Grailed listing. Returns the listings Grailed's own product page recommends as "similar" to one listing -- the same related-items shelf shown on grailed.com's own listing-detail page. id is the listing's numeric id, from a search, sold-listings, or collection result's own id field. An id for a listing that does not exist (deleted, sold and removed, or never valid) returns a typed not-found error.
- **Params:** `id` (integer, **required**) — Listing id to find similar listings for; `limit` (integer, optional) — Results to return, defaults to 30, maximum 99

### `grailed_sold_listings`

- **HTTP:** `GET /grailed/sold-listings`
- **What:** Search Grailed sold listings (sale price history). Searches Grailed's SOLD-listing index -- a separate dataset from active listings, carrying each item's final sale price and sale date. Same filter shape as grailed-search (q, designer, department, category, size, color, condition), but min_price/max_price filter the SOLD price, not the original asking price. Useful for sale-price-history/comparable-sales lookups (e.g. "what did this designer/category actually sell for recently"). A query with genuinely zero matches returns a well-formed empty result rather than an error.
- **Params:** `category` (string, optional) — Category facet filter, from grailed-categories' own categories[].value field; `color` (string, optional) — Color facet filter, from grailed-categories' own colors[].value field; `condition` (string, optional) — Condition filter; `department` (string, optional) — Department filter; `designer` (string, optional) — Designer/brand name filter, from grailed-designers' own designers[].name field; `limit` (integer, optional) — Results per page, defaults to 24, maximum 100; `max_price` (number, optional) — Maximum SOLD price (inclusive), in USD; `min_price` (number, optional) — Minimum SOLD price (inclusive), in USD; `page` (integer, optional) — One-based page number, defaults to 1; `q` (string, optional) — Free-text search query; `size` (string, optional) — Size facet filter, from grailed-categories' own sizes[].value field; `sort` (string, optional) — Sort order, defaults to recent

### `grailed_suggest`

- **HTTP:** `GET /grailed/suggest`
- **What:** Grailed search-box typeahead suggestions. Returns Grailed's own search-box typeahead suggestions for a partial query -- a flat list of suggested search phrases with a popularity score and live active-listing match count, no listing data. Pass a suggestion straight through to grailed-search/grailed-sold-listings' own q parameter. A query with no genuine matches returns a well-formed empty result rather than an error.
- **Params:** `q` (string, **required**) — Partial search query

## Gucci (10)

### `gucci_categories`

- **HTTP:** `GET /gucci/categories`
- **What:** List Gucci's category and subcategory taxonomy. Returns Gucci's full department/category/subcategory taxonomy, sourced directly from the site's own header navigation menu. Each entry's category value is exactly what gucci-category's own category parameter accepts. Filter to one department with department (e.g. women, men); omit for every department -- see the response's own departments field for the live list of top-level department labels to filter by.
- **Params:** `department` (string, optional) — Department label to filter to (case-insensitive substring match against the response's own departments field), e.g. women, men. Omit for every department.

### `gucci_category`

- **HTTP:** `GET /gucci/category`
- **What:** Browse a Gucci category listing. Returns one Gucci category/browse listing: products (name, price, colors, images, stock) plus the upstream's own product count, page count, sibling-category counts, and sort options. category comes from gucci-categories' own category field. page selects how many of the upstream's own batches to accumulate -- Gucci's own category pages page this way: requesting page=N returns every product from page 1 through page N combined (its own "Load All" button simply requests the last page), not a single page's worth. Defaults to 1 (the upstream's own first batch, 36 products); request page equal to the response's own pages_count to fetch a category's complete listing in one call.
- **Params:** `category` (string, **required**) — Category path from gucci-categories' own category field; `page` (integer, optional) — How many of the upstream's own batches to accumulate, defaults to 1 (see description)

### `gucci_product`

- **HTTP:** `GET /gucci/product`
- **What:** Get a Gucci product. Returns product detail for one style: name, price, images, stock, and PDP attributes available from Gucci's current storefront, including description, breadcrumbs, SKU, colors, materials, and sizes. style_code comes from gucci-search's or gucci-category's own style_code field. PDP-only fields are omitted if the detail page is unavailable.
- **Params:** `style_code` (string, **required**) — Product style code, from gucci-search's or gucci-category's own style_code field

### `gucci_recommendations`

- **HTTP:** `GET /gucci/recommendations`
- **What:** Gucci product recommendations. Returns one Gucci recommendations shelf: product summaries (name, price, image, stock) from either a given product's own "You May Also Like" carousel (style_code set) or the site's general trending-items shelf (style_code omitted). style_code comes from gucci-search's or gucci-category's own style_code field.
- **Params:** `max` (integer, optional) — Maximum products to return, defaults to 10, maximum 20; `style_code` (string, optional) — Product style code to get related items for; omit for the site's general trending-items shelf instead

### `gucci_search`

- **HTTP:** `GET /gucci/search`
- **What:** Search Gucci's product catalog. Searches Gucci's US product catalog by keyword using the storefront's public catalog. Results include card-level data and the live total count; per-product colors, materials, sizes, gender, and line are omitted when the search source does not provide them. A genuinely empty result returns a well-formed empty products list. The response's size_facets field lists live size values and counts -- pass one as size on a follow-up call to filter.
- **Params:** `limit` (integer, optional) — Results per page, defaults to 24, maximum 100; `page` (integer, optional) — One-based page number, defaults to 1; `q` (string, **required**) — Search keyword; `size` (string, optional) — Filter to products listing this exact size as available. See size_facets for live values -- omit size to see all sizes first.

### `gucci_size_guide`

- **HTTP:** `GET /gucci/size-guide`
- **What:** Gucci product size chart. Returns Gucci's own size-conversion chart for one product style, as a plain header row plus data rows. Not every style carries one -- a one-size accessory (a bag, a scarf) returns available: false with no headers/rows, a well-formed signal rather than an error. style_code comes from gucci-search's or gucci-category's own style_code field.
- **Params:** `style_code` (string, **required**) — Product style code

### `gucci_store`

- **HTTP:** `GET /gucci/store`
- **What:** Get a Gucci store's detail. Returns one Gucci store's full detail: name, phone, address, opening hours, and photos. slug comes from gucci-stores' own slug field.
- **Params:** `slug` (string, **required**) — Store slug, from gucci-stores' own slug field

### `gucci_store_search`

- **HTTP:** `GET /gucci/stores/search`
- **What:** Search Gucci stores in a map viewport. Searches Gucci's public store-map GeoJSON feed for locations inside the requested viewport. market selects the storefront locale and localized labels; it does not filter results by country. The supported, live-verified market values are ca (English), fr (French), jp (Japanese), uk (English), and us (English). Coordinates and viewport bounds determine the returned stores. The Gucci site's text field geocodes in the browser and its name parameter does not filter this feed, so callers must provide bounds and a center (geocode a place before calling). Dateline-crossing bounds are not supported.
- **Params:** `east` (number, **required**) — Viewport eastern longitude; `latitude` (number, **required**) — Viewport center latitude; `longitude` (number, **required**) — Viewport center longitude; `market` (string, **required**) — Gucci storefront locale; controls localization only, not geographic filtering; `north` (number, **required**) — Viewport northern latitude; `south` (number, **required**) — Viewport southern latitude; `west` (number, **required**) — Viewport western longitude

### `gucci_stores`

- **HTTP:** `GET /gucci/stores`
- **What:** List Gucci store locations. Returns Gucci's full US store-locator listing: name, address, phone, coordinates, product departments carried, and a link to book an in-store appointment for each location. Filter to stores carrying one department with department (e.g. jewelry, mens_shoes); omit for every store -- see the response's own departments field for the live list of department tags to filter by.
- **Params:** `department` (string, optional) — Department tag to filter to (case-insensitive substring match against the response's own departments field), e.g. jewelry, mens_shoes. Omit for every store.

### `gucci_suggest`

- **HTTP:** `GET /gucci/suggest`
- **What:** Gucci search-box suggestions. Returns Gucci's own search-box typeahead suggestions for a partial query. The current public suggestion source does not provide per-phrase result counts. Not product data -- pass a suggestion's query into gucci-search for results.
- **Params:** `limit` (integer, optional) — Maximum suggestions to return, defaults to 5, maximum 20; `q` (string, **required**) — Partial search query

## Hermes (8)

### `hermes_categories`

- **HTTP:** `GET /hermes/categories`
- **What:** List Hermès category codes. Returns every browsable Hermès category for a market: the category code hermes-category accepts, its display name, its page path and absolute URL, its parent code and its depth in the tree. This is the discovery endpoint for hermes-category's category parameter, so every accepted value is obtainable from this API rather than by reading the website. Editorial and story tiles that carry no browsable category page are excluded, so every code returned is one hermes-category will accept.
- **Params:** `locale` (string, optional) — Market and language. One of: at_de, au_en, be_en, be_fr, br_pt, ca_en, ca_fr, ch_de, ch_fr, cz_en, de_de, dh_en, dk_en, es_es, fi_en, fr_fr, gr_en, hk_en, ie_en, it_it, jp_ja, kr_ko, lu_fr, mo_en, mx_es, my_en, nl_en, no_en, pl_en, pt_en, ri_en, se_en, sg_en, th_en, tw_zh, uk_en, us_en

### `hermes_category`

- **HTTP:** `GET /hermes/category`
- **What:** Browse a Hermès category. Browses one Hermès product category and returns a page of products (SKU, title, price with currency, colour, size, stock, images) plus the facet groups Hermès offers for that category, and the category's own title and description. The category parameter takes a category code from hermes-categories, which is the discovery endpoint for every accepted value. Page size is fixed at 48 by Hermès and cannot be changed. Prices are returned with the ISO-4217 currency for the selected market, since Hermès itself publishes bare numbers.
- **Params:** `category` (string, **required**) — Hermès category code, from hermes-categories; `locale` (string, optional) — Market and language. One of: at_de, au_en, be_en, be_fr, br_pt, ca_en, ca_fr, ch_de, ch_fr, cz_en, de_de, dh_en, dk_en, es_es, fi_en, fr_fr, gr_en, hk_en, ie_en, it_it, jp_ja, kr_ko, lu_fr, mo_en, mx_es, my_en, nl_en, no_en, pl_en, pt_en, ri_en, se_en, sg_en, th_en, tw_zh, uk_en, us_en; `page` (integer, optional) — One-based result page; page size is fixed at 48. Page 1 is fully validated; pages beyond 1 are best-effort and provisional; `sort` (string, optional) — Result order. One of: relevance, priceasc, pricedsc. Non-default sorts are best-effort

### `hermes_product`

- **HTTP:** `GET /hermes/product`
- **What:** Get a Hermès product. Returns one Hermès product's full detail: title, description, dimensions, the Hermès colour name, country of manufacture, price with its market currency, stock, every product image, and the complete colour and size variant matrix with per-variant sku, price, stock and image. Care, gift and delivery text are returned as Hermès' own HTML fragments. sku accepts the reference-plus-colour form (H252013Z BM), the fuller listing sku that also carries size (H252013Z BM360), or the URL identifier returned by hermes-products (H252013ZvBM).
- **Params:** `locale` (string, optional) — Market and language. One of: at_de, au_en, be_en, be_fr, br_pt, ca_en, ca_fr, ch_de, ch_fr, cz_en, de_de, dh_en, dk_en, es_es, fi_en, fr_fr, gr_en, hk_en, ie_en, it_it, jp_ja, kr_ko, lu_fr, mo_en, mx_es, my_en, nl_en, no_en, pl_en, pt_en, ri_en, se_en, sg_en, th_en, tw_zh, uk_en, us_en; `sku` (string, **required**) — Hermès product sku, in any of the accepted forms

### `hermes_product_recommendations`

- **HTTP:** `GET /hermes/product/recommendations`
- **What:** Get a Hermès product's recommended items. Returns the cross-sell shelves Hermès shows on a product page: "keep exploring" (similar items) and "perfect partner" (items styled with it), each a list of products with price, stock and image. Takes the same sku forms as hermes-product. A product Hermès offers no recommendations for returns an empty shelves list rather than an error.
- **Params:** `locale` (string, optional) — Market and language. One of: at_de, au_en, be_en, be_fr, br_pt, ca_en, ca_fr, ch_de, ch_fr, cz_en, de_de, dh_en, dk_en, es_es, fi_en, fr_fr, gr_en, hk_en, ie_en, it_it, jp_ja, kr_ko, lu_fr, mo_en, mx_es, my_en, nl_en, no_en, pl_en, pt_en, ri_en, se_en, sg_en, th_en, tw_zh, uk_en, us_en; `sku` (string, **required**) — Hermès product sku, in any of the forms hermes-product accepts

### `hermes_products`

- **HTTP:** `GET /hermes/products`
- **What:** List the Hermès catalogue index. Returns a page of Hermès' full catalogue index for one market: each product's URL, slug, URL identifier and the date Hermès last modified it. Built from Hermès' own product sitemap, so it enumerates the entire catalogue for that market including items no category listing surfaces. Use changed_since to return only products added or updated on or after a date, which makes this a new-arrivals feed. The product_id is the identifier used in the product URL and is NOT the same string as the sku returned by hermes-category and hermes-search, which also encodes size.
- **Params:** `changed_since` (string, optional) — Return only products last modified on or after this YYYY-MM-DD date; `limit` (integer, optional) — Results per page, 1-500; `locale` (string, optional) — Market and language. One of: at_de, au_en, be_en, be_fr, br_pt, ca_en, ca_fr, ch_de, ch_fr, cz_en, de_de, dh_en, dk_en, es_es, fi_en, fr_fr, gr_en, hk_en, ie_en, it_it, jp_ja, kr_ko, lu_fr, mo_en, mx_es, my_en, nl_en, no_en, pl_en, pt_en, ri_en, se_en, sg_en, th_en, tw_zh, uk_en, us_en; `page` (integer, optional) — One-based result page

### `hermes_search`

- **HTTP:** `GET /hermes/search`
- **What:** Search the Hermès catalogue. Searches the Hermès catalogue by keyword and returns a page of products in the same shape as hermes-category. A query Hermès has no match for returns total 0 with an empty products array: Hermès itself renders unrelated fallback recommendations on a no-results page, and those are deliberately not returned as results. When Hermès applies its own spelling correction the corrected term is reported in results_for. Page size is fixed at 48 by Hermès and cannot be changed.
- **Params:** `locale` (string, optional) — Market and language. One of: at_de, au_en, be_en, be_fr, br_pt, ca_en, ca_fr, ch_de, ch_fr, cz_en, de_de, dh_en, dk_en, es_es, fi_en, fr_fr, gr_en, hk_en, ie_en, it_it, jp_ja, kr_ko, lu_fr, mo_en, mx_es, my_en, nl_en, no_en, pl_en, pt_en, ri_en, se_en, sg_en, th_en, tw_zh, uk_en, us_en; `page` (integer, optional) — One-based result page; page size is fixed at 48. Page 1 is fully validated; pages beyond 1 are best-effort and provisional; `query` (string, **required**) — Search keyword

### `hermes_stores`

- **HTTP:** `GET /hermes/stores`
- **What:** List Hermès stores. Returns Hermès' worldwide store directory: name, street address, city, postal code, country, geographic coordinates, phone, displayed opening hours, whether in-store appointments are offered, and store photos. Optionally narrowed to one country (by name or ISO-2 code) or city. Hermès publishes the same worldwide directory for every market, so locale selects the language names are returned in rather than which stores are listed.
- **Params:** `city` (string, optional) — Case-insensitive city filter; `country` (string, optional) — Case-insensitive country filter, matched against the country name or its ISO-2 code; `locale` (string, optional) — Market and language. One of: at_de, au_en, be_en, be_fr, br_pt, ca_en, ca_fr, ch_de, ch_fr, cz_en, de_de, dh_en, dk_en, es_es, fi_en, fr_fr, gr_en, hk_en, ie_en, it_it, jp_ja, kr_ko, lu_fr, mo_en, mx_es, my_en, nl_en, no_en, pl_en, pt_en, ri_en, se_en, sg_en, th_en, tw_zh, uk_en, us_en

### `hermes_suggest`

- **HTTP:** `GET /hermes/suggest`
- **What:** Hermès search suggestions. Returns Hermès' own search-box autocomplete for a partial term: matching categories with the number of items behind each, and matching products. The category codes returned are the same codes hermes-category accepts, so a suggestion feeds straight into a category browse. An empty query is supported and returns Hermès' default suggestions rather than an error.
- **Params:** `locale` (string, optional) — Market and language. One of: at_de, au_en, be_en, be_fr, br_pt, ca_en, ca_fr, ch_de, ch_fr, cz_en, de_de, dh_en, dk_en, es_es, fi_en, fr_fr, gr_en, hk_en, ie_en, it_it, jp_ja, kr_ko, lu_fr, mo_en, mx_es, my_en, nl_en, no_en, pl_en, pt_en, ri_en, se_en, sg_en, th_en, tw_zh, uk_en, us_en; `query` (string, optional) — Partial search term; may be empty for Hermès' default suggestions

## Moda Operandi (4)

### `modaoperandi_categories`

- **HTTP:** `GET /modaoperandi/categories`
- **What:** List Moda Operandi categories and facets. Returns the live category tree, designer, color, size, availability, and sort values discovered from Moda Operandi's public catalog. Returned category and designer slugs are valid for modaoperandi-search.
- **Params:** _none_

### `modaoperandi_designers`

- **HTTP:** `GET /modaoperandi/designers`
- **What:** List Moda Operandi designers. Lists the designers currently available in one Moda Operandi department, chosen with the required `gender` (`women` or `men`). Each designer has its name, slug and item count, and each slug can be passed as `designer` to `modaoperandi-search`. The response also carries the `count` of designers.
- **Params:** `gender` (string, **required**) — Department

### `modaoperandi_product`

- **HTTP:** `GET /modaoperandi/product`
- **What:** Get a Moda Operandi product. Returns one Moda Operandi product by its product page `url`: id, name, designer, color, price and currency, description, details, images, and the available sizes. It also reports `availability` and an `in_stock` flag for the product.
- **Params:** `url` (string, **required**) — Moda Operandi product URL

### `modaoperandi_search`

- **HTTP:** `GET /modaoperandi/search`
- **What:** Search Moda Operandi products. Searches or browses the Moda Operandi catalogue for one department, with `gender` (`women` or `men`) required and either `q` or `category` needed as well. Filter by `designer`, `color`, `size`, `availability`, price range or `on_sale`, and sort with `sort`. `limit` is 1 to 180 per page. Returns products plus facet counts and the `total`.
- **Params:** `attribute` (string, optional) — Attribute facet value; `availability` (string, optional) — Availability; `category` (string, optional) — Category slug from modaoperandi-categories; `color` (string, optional) — Color facet value; `designer` (string, optional) — Designer slug from modaoperandi-designers; `gender` (string, **required**) — Department; `limit` (integer, optional) — Results per page; `on_sale` (boolean, optional) — Sale items only; `page` (integer, optional) — 1-based page; `price_max` (number, optional) — Maximum price; `price_min` (number, optional) — Minimum price; `q` (string, optional) — Free-text search; `size` (string, optional) — Size facet value; `sort` (string, optional) — Sort

## Moncler (6)

### `moncler_categories`

- **HTTP:** `GET /moncler/categories`
- **What:** List Moncler categories. Returns Moncler's full category tree (id, name, description, and subcategories). Every id is a valid value for moncler-category's own category_id parameter. levels controls how many levels of subcategories are included.
- **Params:** `levels` (integer, optional) — How many levels of the category tree to return

### `moncler_category`

- **HTTP:** `GET /moncler/category`
- **What:** Browse a Moncler category. Lists products within one category. category_id must be a value returned by moncler-categories' own category_id field -- a closed set the upstream defines. Returns the same result and facet shape as moncler-search. Narrow the same results with the filter param below.
- **Params:** `category_id` (string, **required**) — Category id, from moncler-categories; `filter` (array, optional) — Repeatable, up to 10. Each value is \; `limit` (integer, optional) — Max results to return; `offset` (integer, optional) — Result offset for pagination; `sort` (string, optional) — Sort order

### `moncler_product`

- **HTTP:** `GET /moncler/product`
- **What:** Get a Moncler product's detail. Returns one product's full detail: name, brand, price, descriptions, color, composition and care instructions, size availability, live stock, variation attributes (color/size options), every orderable variant SKU, product images, "styled with" related products, and a size guide (per-size body measurements and/or a cross-region size conversion table) when the upstream provides one. product_id accepts either a variant-level id or a master/style-level id, both as returned by moncler-search/moncler-category's own result ids.
- **Params:** `product_id` (string, **required**) — Product or master id

### `moncler_search`

- **HTTP:** `GET /moncler/search`
- **What:** Search Moncler products. Searches Moncler's product catalog by keyword. Returns product results (name, price, image, orderable color/size variant ids, and live stock level) plus the search index's own sort options and facets (gender, category, color, size, and others) with live per-option result counts. Narrow the same results with the filter param below.
- **Params:** `filter` (array, optional) — Repeatable, up to 10. Each value is \; `limit` (integer, optional) — Max results to return; `offset` (integer, optional) — Result offset for pagination; `q` (string, **required**) — Search keyword; `sort` (string, optional) — Sort order

### `moncler_stores`

- **HTTP:** `GET /moncler/stores`
- **What:** List Moncler boutiques. Returns Moncler's full worldwide boutique list: name, coordinates, address, phone, email, opening hours, store type, and in-store service flags. This is the full list, not geo-filtered -- filter by country_code or proximity to coordinates client-side over the returned list.
- **Params:** _none_

### `moncler_suggest`

- **HTTP:** `GET /moncler/suggest`
- **What:** Get Moncler search-box suggestions. Returns the storefront's own search-box suggestions (typeahead) for a partial query: completed/corrected search terms, suggested full phrases, and matching categories. Not product data.
- **Params:** `q` (string, **required**) — Partial search query

## Prada (6)

### `prada_categories`

- **HTTP:** `GET /prada/categories`
- **What:** List Prada's category taxonomy and gender filter values. Returns Prada's (prada.com) full category taxonomy -- every browsable category with its own breadcrumb path and canonical URL -- plus the two gender values products.prada.com currently carries. categories[].id is exactly the value prada-category accepts as its own category_id parameter; genders[].value is exactly what prada-search and prada-category accept as their own gender parameter.
- **Params:** _none_

### `prada_category`

- **HTTP:** `GET /prada/category`
- **What:** Browse a Prada category. Browses one Prada category by ID, returning every product/color variant in it. category_id is required and must be one of prada-categories' own categories[].id values. gender optionally narrows to one of prada-categories' own genders[].value values. sort selects Prada's own relevance ranking or one of its price/newest orderings. A category with no products returns a well-formed empty result rather than an error.
- **Params:** `category_id` (string, **required**) — Category ID, from prada-categories' own categories[].id field; `gender` (string, optional) — Gender filter. Allowed values: Woman, Man; `limit` (integer, optional) — Results per page, defaults to 24, maximum 100; `page` (integer, optional) — One-based page number, defaults to 1; `sort` (string, optional) — Sort order. Allowed values: suggested, price_asc, price_desc, newest. Defaults to suggested (Prada's own relevance ranking)

### `prada_product`

- **HTTP:** `GET /prada/product`
- **What:** Get a Prada product. Returns product-detail data for one Prada product/color variant: name, price, stock, available sizes, breadcrumb, alternate colors, and images. pv is the product/color identifier, returned by prada-search's, prada-category's, and this endpoint's own products[].pv/other_colors[] fields (also the trailing path segment of a Prada product URL). description and the full image gallery are populated on a best-effort basis and may be briefly absent even for a valid pv; every other field is always populated. An unknown pv returns a not-found error.
- **Params:** `pv` (string, **required**) — Product/color identifier, from a search, category, or product result's own pv field

### `prada_search`

- **HTTP:** `GET /prada/search`
- **What:** Search Prada products. Searches Prada's (prada.com) product catalog by keyword, through its own public search index. q is required; gender and sort are the same optional values prada-category accepts. Keyword search is typo-tolerant relevance ranking, not a guaranteed exact match. A query with genuinely zero matches returns a well-formed empty result rather than an error.
- **Params:** `gender` (string, optional) — Gender filter. Allowed values: Woman, Man; `limit` (integer, optional) — Results per page, defaults to 24, maximum 100; `page` (integer, optional) — One-based page number, defaults to 1; `q` (string, **required**) — Free-text search query; `sort` (string, optional) — Sort order. Allowed values: suggested, price_asc, price_desc, newest. Defaults to suggested (Prada's own relevance ranking)

### `prada_stores`

- **HTTP:** `GET /prada/stores`
- **What:** Locate Prada retail stores. Locates Prada's (prada.com) physical retail stores worldwide, through its own public store-locator search. All parameters are optional: with none set, this returns Prada's full worldwide store list (up to limit). query is a free-text location search (city, country, or store name); lat/lng (both required together) narrow it to a geo-radius search, optionally sized with radius_km (defaults to 50, maximum 20000). A search with genuinely zero matches returns a well-formed empty result rather than an error.
- **Params:** `lat` (number, optional) — Search-center latitude, -90..90. Requires lng.; `limit` (integer, optional) — Maximum stores returned, defaults to 20, maximum 50; `lng` (number, optional) — Search-center longitude, -180..180. Requires lat.; `offset` (integer, optional) — Result offset for pagination, defaults to 0; `query` (string, optional) — Free-text location search (city, country, or store name); `radius_km` (number, optional) — Search radius in kilometers around lat/lng, defaults to 50, maximum 20000. Requires lat and lng.

### `prada_suggest`

- **HTTP:** `GET /prada/suggest`
- **What:** Get Prada search-box suggestions. Returns Prada's own search-box typeahead suggestions for a partial query -- a ranked list of suggested search phrases with the live result count each one would return. Pass a suggestion straight through to prada-search's own q parameter for product results. A query with no genuine matches returns a well-formed empty result rather than an error.
- **Params:** `limit` (integer, optional) — Maximum suggestions, defaults to 10, maximum 20; `q` (string, **required**) — Partial search query

## Rebag (12)

### `rebag_collection_products`

- **HTTP:** `GET /rebag/collections/{handle}/products`
- **What:** List Rebag collection products. Returns products from one Rebag (https://shop.rebag.com) collection. The storefront URL is fixed server-side; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `rebag_collections`

- **HTTP:** `GET /rebag/collections`
- **What:** List Rebag collections. Returns collections from Rebag (https://shop.rebag.com). The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `rebag_page`

- **HTTP:** `GET /rebag/pages/{handle}`
- **What:** Get a Rebag static page. Looks up a single Rebag static page by `handle`, for example `welcome-trendlee`. The response has the page's id, title, URL, publication and update times, and its `content` as plain text. Unknown handles return 404. If `transport_mode` is `ssr_embedded`, `id` is left out.
- **Params:** `handle` (string, **required**) — Page handle

### `rebag_pages`

- **HTTP:** `GET /rebag/pages`
- **What:** List Rebag static pages. Lists the static pages on Rebag's storefront, paged with `page` (from 1) and `limit` (default 50, max 250). Each entry has `handle`, `title`, `url`, plain-text `content` and its dates. An empty page of results returns an empty `pages` array. In `ssr_embedded` mode only `handle`, `url` and `updated_at` are filled.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `rebag_product`

- **HTTP:** `GET /rebag/products/{handle}`
- **What:** Get a Rebag product. Returns product detail for one Rebag (https://shop.rebag.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `rebag_product_recommendations`

- **HTTP:** `GET /rebag/products/{handle}/recommendations`
- **What:** List Rebag product recommendations. Returns recommended products for one Rebag (https://shop.rebag.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `rebag_products`

- **HTTP:** `GET /rebag/products`
- **What:** List Rebag products. Returns products from Rebag's (https://shop.rebag.com) public product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `rebag_search`

- **HTTP:** `GET /rebag/search`
- **What:** Search Rebag products. Returns ranked products from Rebag's (https://shop.rebag.com) own full-text product search, including a best-effort condition grade and colour derived from the product's own catalog tags -- attributes not available from the other catalog endpoints in this family. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 20 and supports up to 50; `page` (integer, optional) — 1-based page, defaults to 1; `q` (string, **required**) — Search query text; `sort` (string, optional) — Sort order. Allowed values: relevance, price_asc, price_desc

### `rebag_search_suggest`

- **HTTP:** `GET /rebag/search/suggest`
- **What:** Get Rebag search suggestions. Returns products, collections, and query suggestions from Rebag's (https://shop.rebag.com) predictive search. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `rebag_sitemap_urls`

- **HTTP:** `GET /rebag/sitemap/urls`
- **What:** List Rebag sitemap URLs. Lists URL entries from Rebag's sitemaps, filtered by `type` (`all`, `products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`; default `all`). Collection stops at `limit` entries (default 50, max 250). Each entry has `loc`, `type`, `handle`, `lastmod`, `changefreq` and, where present, `images` with caption, title and URL.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `rebag_sitemaps`

- **HTTP:** `GET /rebag/sitemaps`
- **What:** List Rebag sitemaps. Lists the child sitemaps in Rebag's sitemap index. Each entry has its `loc` and a `type` of `products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`, worked out from the sitemap URL. The endpoint takes no parameters.
- **Params:** _none_

### `rebag_store`

- **HTTP:** `GET /rebag/store`
- **What:** Get Rebag store metadata. Returns storefront metadata for Rebag (https://shop.rebag.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_

## The RealReal (11)

### `therealreal_autocomplete`

- **HTTP:** `GET /therealreal/autocomplete`
- **What:** Get The RealReal search-box suggestions. Returns The RealReal's own search-box typeahead suggestions for a partial query.
- **Params:** `term` (string, **required**) — Partial free-text query to get search-box suggestions for

### `therealreal_categories`

- **HTTP:** `GET /therealreal/categories`
- **What:** Get The RealReal category browse taxonomy. Returns The RealReal's full category (taxon) browse taxonomy: every department, category, and subcategory, nested, with each entry's id (usable directly against search's category_id), permalink (usable directly against the category endpoint's path), and live matching item count. This is reference data that changes rarely, so responses are cached.
- **Params:** _none_

### `therealreal_category`

- **HTTP:** `GET /therealreal/category`
- **What:** Browse The RealReal listings by category. Returns a page of The RealReal listings browsed by category (taxon) permalink path, e.g. women/handbags. Pass a previous response's next_after back as after to fetch the next page.
- **Params:** `after` (string, optional) — Opaque pagination cursor from a previous response's next_after. Omit for the first page; `available` (boolean, optional) — Only return items currently available to purchase (excludes sold and waitlisted items); `on_sale` (boolean, optional) — Only return items currently marked down from their original price; `path` (string, **required**) — Category permalink path, from the categories endpoint's permalink field

### `therealreal_collection`

- **HTTP:** `GET /therealreal/collection`
- **What:** Browse The RealReal listings by curated collection. Returns a page of The RealReal listings browsed by curated collection slug, e.g. on-sale-now -- sale campaigns, editor's picks, and similar merchandising collections distinct from category/designer browsing. Pass a previous response's next_after back as after to fetch the next page.
- **Params:** `after` (string, optional) — Opaque pagination cursor from a previous response's next_after. Omit for the first page; `slug` (string, **required**) — Collection slug, from the collections endpoint's slug field

### `therealreal_collections`

- **HTTP:** `GET /therealreal/collections`
- **What:** Get The RealReal curated collection slugs. Returns The RealReal's full published set of curated editorial and sale-campaign collection slugs (e.g. on-sale-now, hermes-birkin-bag), each usable directly against the collection endpoint's own slug field. This is reference data that changes rarely, so responses are cached.
- **Params:** _none_

### `therealreal_conditions`

- **HTTP:** `GET /therealreal/conditions`
- **What:** Get The RealReal condition-grading value space. Returns The RealReal's full authentication condition-grading scale: the closed 6-tier set (Pristine, Excellent, Very Good, Good, Fair, As Is) it defines, each with an id (usable directly against search's condition_id) and live matching item count. This is reference data that changes rarely, so responses are cached.
- **Params:** _none_

### `therealreal_designer`

- **HTTP:** `GET /therealreal/designer`
- **What:** Browse The RealReal listings by designer. Returns a page of The RealReal listings browsed by designer slug, e.g. gucci. Pass a previous response's next_after back as after to fetch the next page.
- **Params:** `after` (string, optional) — Opaque pagination cursor from a previous response's next_after. Omit for the first page; `available` (boolean, optional) — Only return items currently available to purchase (excludes sold and waitlisted items); `on_sale` (boolean, optional) — Only return items currently marked down from their original price; `slug` (string, **required**) — Designer slug, from the designers endpoint's slug field

### `therealreal_designers`

- **HTTP:** `GET /therealreal/designers`
- **What:** Get The RealReal designer directory. Returns every designer The RealReal recognizes in one department (not just designers with currently active listings), each with an id (usable directly against search's designer_id) and slug (usable directly against the designer endpoint). The directory is segmented by department -- pass category to select one; the response's categories field lists every accepted value. This is reference data that changes rarely, so responses are cached.
- **Params:** `category` (string, optional) — Designer-directory department. One of: women, men, fine-jewelry, watches, art, home, kids. Defaults to women

### `therealreal_listing`

- **HTTP:** `GET /therealreal/listing`
- **What:** Get a The RealReal listing detail. Returns a single The RealReal listing: description, condition detail, category context, and measurements, plus the shared summary fields (name, designer, condition, price, images). Looked up by the listing's full product URL, as returned in a search/category/designer response's url field.
- **Params:** `url` (string, **required**) — Full product URL, as returned in a search/category/designer response's url field

### `therealreal_search`

- **HTTP:** `GET /therealreal/search`
- **What:** Search The RealReal luxury consignment listings. Searches The RealReal's authenticated luxury resale catalog by keyword, optionally combined with category, designer, condition-grade, and price-range filters, returning listing summaries (name, designer, condition, price, images) plus the total matching count and an opaque pagination cursor. Pass a previous response's next_after back as after to fetch the next page.
- **Params:** `after` (string, optional) — Opaque pagination cursor from a previous response's next_after. Omit for the first page; `available` (boolean, optional) — Only return items currently available to purchase (excludes sold and waitlisted items); `category_id` (string, optional) — Category (taxon) id, from the categories endpoint's id field; `condition_id` (string, optional) — Condition grade id, from the conditions endpoint's id field; `designer_id` (string, optional) — Designer id, from the designers endpoint's id field; `on_sale` (boolean, optional) — Only return items currently marked down from their original price; `price_from` (number, optional) — Minimum price in USD; `price_to` (number, optional) — Maximum price in USD; `query` (string, **required**) — Free-text keyword search

### `therealreal_similar`

- **HTTP:** `GET /therealreal/similar`
- **What:** Get The RealReal similar-item recommendations. Returns The RealReal's own "Similar Items" visual-similarity recommendations for one product, looked up by the product's numeric id (from any other The RealReal endpoint's listing response id field).
- **Params:** `product_id` (string, **required**) — The RealReal numeric product id, from a search/category/designer/listing/collection response's id field

## Tiffany & Co. (8)

### `tiffany_categories`

- **HTTP:** `GET /tiffany/categories`
- **What:** List Tiffany & Co. categories. Lists every category id Tiffany & Co.'s own product catalog accepts, each with a human-readable label, a kind (category for a real navigable department/subcategory, curated_shop for a curated gift/merchandising shelf), and a live product count. Each id is exactly what tiffany-category's own category parameter accepts -- resolves the category-discovery gap that parameter would otherwise leave as "find one from a storefront URL".
- **Params:** _none_

### `tiffany_category`

- **HTTP:** `GET /tiffany/category`
- **What:** Browse a Tiffany & Co. category. Returns one page of a Tiffany & Co. category/browse listing. category is a category id from tiffany-categories's own id field (e.g. ecommerce_us_jewelry_necklaces_and_pendants). sort selects recommended (default), price_asc, price_desc, or newest. material, gemstone, color, product_type, gender, and designer are optional single-value filters -- see tiffany-filters for the live covered value space for each. A hub-level or emptied-out category id, or a filter combination with no matches, returns a well-formed empty result rather than an error.
- **Params:** `category` (string, **required**) — Category id -- see tiffany-categories; `color` (string, optional) — Color filter -- see tiffany-filters; `designer` (string, optional) — Designer/collection filter -- see tiffany-filters; `gemstone` (string, optional) — Gemstone filter -- see tiffany-filters; `gender` (string, optional) — Gender filter -- see tiffany-filters; `material` (string, optional) — Material filter -- see tiffany-filters; `page` (integer, optional) — One-based page; `per_page` (integer, optional) — Results per page; `product_type` (string, optional) — Product type filter -- see tiffany-filters; `sort` (string, optional) — Sort order

### `tiffany_content_search`

- **HTTP:** `GET /tiffany/content-search`
- **What:** Search Tiffany & Co. editorial content. Searches Tiffany & Co.'s own editorial pages -- style guides, gift guides, and other "World of Tiffany" articles -- by free-text keyword. Not product data: no price, stock, or item id fields. A genuine non-matching keyword returns a well-formed empty result (zero total_results).
- **Params:** `keyword` (string, **required**) — Search keyword; `page` (integer, optional) — One-based page; `per_page` (integer, optional) — Results per page

### `tiffany_filters`

- **HTTP:** `GET /tiffany/filters`
- **What:** List Tiffany & Co. search/category filter values. Lists every value tiffany-search's and tiffany-category's material, gemstone, color, product_type, gender, and designer filter parameters accept, each with a live product count -- resolves the discovery gap those parameters would otherwise leave as "find one on the live site's own filter sidebar".
- **Params:** _none_

### `tiffany_product`

- **HTTP:** `GET /tiffany/product`
- **What:** Get a Tiffany & Co. product. Returns full product detail for one item: name, description, brand, collection, designer, material, gemstone, USD price, live stock status, category tree, every color/style variation, and images. product_id is Tiffany & Co.'s own item id, as returned by tiffany-search's or tiffany-category's own products[].id field.
- **Params:** `product_id` (string, **required**) — Item id, from a search or category result's id field

### `tiffany_search`

- **HTTP:** `GET /tiffany/search`
- **What:** Search Tiffany & Co. products. Searches Tiffany & Co.'s product catalog by free-text keyword. Returns product summaries with USD pricing, live stock status, material, gemstone, collection, and designer. sort selects recommended (default), price_asc, price_desc, or newest. material, gemstone, color, product_type, gender, and designer are optional single-value filters -- see tiffany-filters for the live covered value space for each. A genuine non-matching keyword, or a filter combination with no matches, returns a well-formed empty result (zero total_products).
- **Params:** `color` (string, optional) — Color filter -- see tiffany-filters; `designer` (string, optional) — Designer/collection filter -- see tiffany-filters; `gemstone` (string, optional) — Gemstone filter -- see tiffany-filters; `gender` (string, optional) — Gender filter -- see tiffany-filters; `keyword` (string, **required**) — Search keyword; `material` (string, optional) — Material filter -- see tiffany-filters; `page` (integer, optional) — One-based page; `per_page` (integer, optional) — Results per page; `product_type` (string, optional) — Product type filter -- see tiffany-filters; `sort` (string, optional) — Sort order

### `tiffany_stores`

- **HTTP:** `GET /tiffany/stores`
- **What:** Find Tiffany & Co. store locations. Finds Tiffany & Co. physical stores, boutiques, and cafes near a coordinate, ordered by distance. Each result includes address, phone, opening hours, in-store services and specialities, and live open/closed status.
- **Params:** `latitude` (number, **required**) — Latitude, -90 to 90; `limit` (integer, optional) — Maximum stores to return; `longitude` (number, **required**) — Longitude, -180 to 180; `radius` (number, optional) — Search radius in miles

### `tiffany_suggest`

- **HTTP:** `GET /tiffany/suggest`
- **What:** Get Tiffany & Co. search-box suggestions. Returns Tiffany & Co.'s own search-box suggestions (typeahead) for a partial query -- a flat list of suggested search phrases, each with its own live total result count on the product catalog. Not product data.
- **Params:** `query` (string, **required**) — Partial search query

## Vestiaire (8)

### `vestiaire_brands`

- **HTTP:** `GET /vestiaire/brands`
- **What:** Vestiaire Collective's full brand directory. Returns Vestiaire Collective's full brand directory (id, name, url), not just brands with active listings for a given search -- resolves search's otherwise-opaque brand_id filter, and a search response's facets.brands, to the complete set of valid ids. Public data, sourced from Vestiaire Collective's own brand-directory page.
- **Params:** _none_

### `vestiaire_categories`

- **HTTP:** `GET /vestiaire/categories`
- **What:** Vestiaire Collective category taxonomy. Returns the full Vestiaire Collective category taxonomy: universes (Women, Men, Kids) at the root, with up to three nested category levels beneath each. Every id returned here is accepted by /vestiaire/search's category_id filter.
- **Params:** _none_

### `vestiaire_conditions`

- **HTTP:** `GET /vestiaire/conditions`
- **What:** Vestiaire Collective condition values. Returns the fixed set of condition ids accepted by /vestiaire/search's condition_id filter, with each id's display name and current listing count.
- **Params:** _none_

### `vestiaire_product`

- **HTTP:** `GET /vestiaire/product`
- **What:** Vestiaire Collective listing detail. Returns a single Vestiaire Collective listing's public detail: price, brand, category, condition, material, color, size, seller summary, and photos. `path` is the listing's URL or site-relative path, as returned by /vestiaire/search's `url` field -- the numeric id alone cannot be resolved to a page. Public data, sourced from Vestiaire Collective's own listing page.
- **Params:** `path` (string, **required**) — Listing URL or path, from a search result's url field

### `vestiaire_search`

- **HTTP:** `GET /vestiaire/search`
- **What:** Vestiaire Collective listing search. Searches Vestiaire Collective's public pre-owned luxury resale catalog by keyword, category, brand, and condition, with sort and pagination. `sort` values: `relevance`, `price_asc`, `price_desc`, `recency`. `category_id` and `condition_id` come from /vestiaire/categories and /vestiaire/conditions. `page` * `per_page` cannot exceed an offset of 1000 (the upstream service's own pagination limit) -- narrow the query instead of paging deeper. Public data, sourced from Vestiaire Collective's own search service.
- **Params:** `brand_id` (string, optional) — Brand id, from a prior search's facets.brands; `category_id` (string, optional) — Category id, from /vestiaire/categories; `condition_id` (string, optional) — Condition id. Allowed values: 1, 2, 3, 4, 5; `page` (integer, optional) — Page number, starting at 1; `per_page` (integer, optional) — Results per page, up to 60; `q` (string, optional) — Keyword search text; `sort` (string, optional) — Sort order. Allowed values: relevance, price_asc, price_desc, recency

### `vestiaire_search_sellers`

- **HTTP:** `GET /vestiaire/search-sellers`
- **What:** Search Vestiaire Collective sellers by name. Finds Vestiaire Collective sellers by username or first name. A matched result's id can be passed directly to GET /vestiaire/seller for that seller's full public storefront profile. Public data, sourced from Vestiaire Collective's own member-search service.
- **Params:** `q` (string, **required**) — Seller username or first name to search for

### `vestiaire_seller`

- **HTTP:** `GET /vestiaire/seller`
- **What:** Vestiaire Collective seller profile. Returns a Vestiaire Collective seller's public storefront profile: username, country, segment, aggregate sold/listed/bought counts, and follower/following counts. `id` is the numeric seller id, as returned by /vestiaire/search's `seller_id` field or /vestiaire/product's `seller.id`. Public data, sourced from Vestiaire Collective's own seller profile page.
- **Params:** `id` (string, **required**) — Seller id

### `vestiaire_suggest`

- **HTTP:** `GET /vestiaire/suggest`
- **What:** Vestiaire Collective search-box autocomplete. Returns Vestiaire Collective's own search-box autocomplete suggestions for a partial query: matching brands plus completed search phrases. Public data, sourced from Vestiaire Collective's own search-suggestions service.
- **Params:** `q` (string, **required**) — Partial search query to autocomplete

## YOOX (4)

### `yoox_categories`

- **HTTP:** `GET /yoox/categories`
- **What:** List YOOX categories. Lists YOOX categories grouped by department (`women`, `men` and `kids`), each with its name, slug and URL. Every category slug is valid as `category` in YOOX search. Calls can take up to about 80 seconds, and a call that cannot finish, or one made while YOOX shows its maintenance page, returns `503`.
- **Params:** _none_

### `yoox_designers`

- **HTTP:** `GET /yoox/designers`
- **What:** List YOOX designers. Lists YOOX designers for the required `department` (`women`, `men` or `kids`), with the `count` and each designer's name, slug and URL. Every designer slug is valid as `designer` in YOOX search. A call that cannot finish within about 80 seconds returns `503`, as does one made during YOOX maintenance.
- **Params:** `department` (string, **required**) — Department

### `yoox_product`

- **HTTP:** `GET /yoox/product`
- **What:** Get a YOOX product. Returns a YOOX product by item `id`, the path segment before `/item` in a product URL, for example `17734181OO`. The older `url` parameter still works instead. The response has name, brand, price, currency, `in_stock`, description, images and category. Calls can take up to about 80 seconds and return `503` if they cannot finish.
- **Params:** `id` (string, optional) — YOOX item id, for example 17734181OO; `url` (string, optional) — Legacy YOOX product URL

### `yoox_search`

- **HTTP:** `GET /yoox/search`
- **What:** Search YOOX products. Searches or browses YOOX products in the required `department`. Optional filters are `q`, `category`, `designer`, `color`, `size`, `price_min`, `price_max` and `on_sale`; `sort` takes `relevance`, `newest`, `price_asc`, `price_desc` or `discount`; `limit` is 1 to 100. Each product has brand, name, price, currency, stock status, image and URL, with `facets` for colors, sizes and sorts. May return `503`.
- **Params:** `category` (string, optional) — Category slug from yoox-categories; `color` (string, optional) — Color filter; `department` (string, **required**) — Department; `designer` (string, optional) — Designer slug from yoox-designers; `limit` (integer, optional) — Results per page; `on_sale` (boolean, optional) — Sale items only; `page` (integer, optional) — 1-based page; `price_max` (number, optional) — Maximum price; `price_min` (number, optional) — Minimum price; `q` (string, optional) — Free-text search; `size` (string, optional) — Size filter; `sort` (string, optional) — Sort

## Depop (10)

### `depop_brands`

- **HTTP:** `GET /depop/brands`
- **What:** Depop's full brand directory. Returns Depop's full brand directory (id, name, slug), not just brands with active listings for a given search -- resolves the search endpoint's otherwise-opaque brand_ids filter to human-readable names. Public data sourced from Depop's own brand-directory API.
- **Params:** _none_

### `depop_categories`

- **HTTP:** `GET /depop/categories`
- **What:** Get Depop's category taxonomy. Returns Depop's full department, category, and subcategory taxonomy -- every value usable with /depop/search's and /depop/shop/{username}'s category/subcategory filters. Tries a live refresh from Depop's own category-filter API first and falls back to a static snapshot on any failure, so this never errors.
- **Params:** _none_

### `depop_item`

- **HTTP:** `GET /depop/item/{slug}`
- **What:** Get Depop item detail. Returns a Depop item-detail page: description, all photos, price, condition, brand, size, seller info, and a "similar items" carousel when the page has one.
- **Params:** `slug` (string, **required**) — Depop item URL slug, e.g. from a search result's id field

### `depop_item_similar`

- **HTTP:** `GET /depop/item/{slug}/similar`
- **What:** Get Depop items similar to a listing. Returns items similar to a given Depop listing, via Depop's dedicated similar-items API -- richer and paginated (up to 150 per page) compared to the small, non-paginated "similar items" carousel already included in item detail. Public data sourced from Depop's own similar-items API.
- **Params:** `after` (string, optional) — Opaque pagination cursor from a previous response's next_cursor field. Omit for the first page.; `limit` (integer, optional) — Max results per page, 1-150; `slug` (string, **required**) — Depop item URL slug, e.g. from a search result's id field

### `depop_search`

- **HTTP:** `GET /depop/search`
- **What:** Search Depop listings. Searches Depop's resale-fashion marketplace by free-text keyword, with optional price, condition, colour, category, subcategory, gender, kids-department, brand, discount, and sort filters, returning listing summaries (title, price, brand, condition, like count, photos, sizes), a pagination cursor, and the total matching count.
- **Params:** `after` (string, optional) — Opaque pagination cursor from a previous response's next_cursor field. Omit for the first page.; `brand_ids` (string, optional) — Comma-separated Depop internal numeric brand ids. Not documented by Depop -- find a brand's id by browsing its depop.com/brands/<slug>/ page.; `category` (string, optional) — Depop category slug: tops, bottoms, dresses, coats-jackets, jumpsuit-and-playsuit, suits, footwear, accessories, nightwear, underwear, swim-beach-wear, fancy-dress, sleepsuits-and-bodysuits, bundles, beauty, face-masks, home, tech-accessories, film, art, books-and-magazine, music, party-supplies, sports-equipment-accesories, toys, umbrella. See GET /depop/categories for a machine-readable enumeration with names and subcategories.; `colours` (string, optional) — Comma-separated colour filter: black, grey, white, brown, tan, cream, yellow, red, burgundy, orange, pink, purple, blue, navy, green, khaki, multi; `condition` (string, optional) — Comma-separated condition filter: brand_new, used_like_new, used_excellent, used_good, used_fair; `gender` (string, optional) — Department filter: female, male; `is_kids` (boolean, optional) — Kids-department filter: true restricts results to kids items only, false excludes them, omitted returns both.; `on_sale` (boolean, optional) — Restrict results to discounted listings; `price_max` (number, optional) — Maximum listing price in USD; `price_min` (number, optional) — Minimum listing price in USD; `query` (string, **required**) — Free-text keyword search; `sizes` (string, optional) — Comma-separated Depop size composite ids (format {size_set_id}.{id}, e.g. \; `sort` (string, optional) — Sort order: relevance, price_low_to_high, price_high_to_low; `subcategory` (string, optional) — Comma-separated Depop subcategory slug(s), scoped within category. See GET /depop/categories for the full list per category.

### `depop_search_facets`

- **HTTP:** `GET /depop/search/facets`
- **What:** Depop search result-count breakdowns. Returns result-count breakdowns per department/category/subcategory for a search query, via Depop's dedicated aggregates API -- a distinct upstream call from search itself, not embedded in its response. Public data sourced from Depop's own search-aggregates API.
- **Params:** `query` (string, **required**) — Free-text keyword search

### `depop_search_sellers`

- **HTTP:** `GET /depop/search-sellers`
- **What:** Search Depop sellers by name. Finds Depop users/sellers by name or username. A matched result's username can be passed directly to GET /depop/shop/{username} for that seller's full shop. Public data sourced from Depop's own user-search API.
- **Params:** `query` (string, **required**) — Seller name or username to search for

### `depop_shop`

- **HTTP:** `GET /depop/shop/{username}`
- **What:** Get a Depop seller's shop. Returns a Depop seller's public shop: profile (rating, sold count, followers, bio) plus current listings, with optional price, condition, colour, category, subcategory, gender, discount, and sort filters. Public data sourced from Depop's own shop pages.
- **Params:** `category` (string, optional) — Depop category slug: tops, bottoms, dresses, coats-jackets, jumpsuit-and-playsuit, suits, footwear, accessories, nightwear, underwear, swim-beach-wear, fancy-dress, sleepsuits-and-bodysuits, bundles, beauty, face-masks, home, tech-accessories, film, art, books-and-magazine, music, party-supplies, sports-equipment-accesories, toys, umbrella. See GET /depop/categories for a machine-readable enumeration with names and subcategories.; `colours` (string, optional) — Comma-separated colour filter: black, grey, white, brown, tan, cream, yellow, red, burgundy, orange, pink, purple, blue, navy, green, khaki, multi; `condition` (string, optional) — Comma-separated condition filter: brand_new, used_like_new, used_excellent, used_good, used_fair; `gender` (string, optional) — Department filter: female, male; `on_sale` (boolean, optional) — Restrict results to discounted listings; `price_max` (number, optional) — Maximum listing price in USD; `price_min` (number, optional) — Minimum listing price in USD; `sizes` (string, optional) — Comma-separated Depop size composite ids (format {size_set_id}.{id}, e.g. \; `sort` (string, optional) — Sort order: relevance, price_low_to_high, price_high_to_low, recently_listed; `subcategory` (string, optional) — Comma-separated Depop subcategory slug(s), scoped within category. See GET /depop/categories for the full list per category.; `username` (string, **required**) — Depop seller username, e.g. from a shop page URL segment

### `depop_sizes`

- **HTTP:** `GET /depop/sizes`
- **What:** Get Depop's size taxonomy. Returns Depop's full, multi-region size taxonomy -- every composite id usable with /depop/search's and /depop/shop/{username}'s sizes filter. Public data sourced from Depop's own size-filter API.
- **Params:** _none_

### `depop_suggest`

- **HTTP:** `GET /depop/suggest`
- **What:** Depop search-box autocomplete. Returns Depop's own search-box autocomplete suggestions for a partial query, including the category a suggestion maps to when relevant. Public data sourced from Depop's own search-suggestions API.
- **Params:** `query` (string, **required**) — Partial search query to autocomplete

## GOAT (10)

### `goat_collection`

- **HTTP:** `GET /goat/collection`
- **What:** Get a GOAT curated product collection. Returns a page of one of GOAT's curated product collections (an editorial rail like "top trending" or "new arrivals"), as shown in GOAT's own product-page "you may also like" rails and homepage modules. Collection slugs are not enumerable by this API -- capture one from a live GOAT page.
- **Params:** `exclude_product_ids` (string, optional) — Omit specific products by id, comma-separated; `limit` (integer, optional) — Results per page, defaults to 12, maximum 100; `page` (integer, optional) — 1-indexed result page, defaults to 1; `slug` (string, **required**) — GOAT collection slug, e.g. as seen in a curated rail on GOAT's own site

### `goat_countries`

- **HTTP:** `GET /goat/countries`
- **What:** Get GOAT countries. Returns every country GOAT recognizes -- the accepted values for GET /goat/product/{slug}'s country_code parameter -- with the currency and size unit (us, uk, eu) GOAT localizes to for each, plus whether GOAT ships and accepts returns there. Every country is listed, not only the shippable ones, because country_code localizes pricing and is accepted for all of them; filter on ships_to if you want only GOAT's shipping destinations.
- **Params:** _none_

### `goat_curated`

- **HTTP:** `GET /goat/curated`
- **What:** Get GOAT curated links. Returns the shelf of editorially curated links GOAT is currently promoting in its own search box: seasonal collections, specific product searches, and browse-all entry points. Every link is actionable against this API -- a collection link carries a value for GET /goat/collection, a search link carries a query for GET /goat/search.
- **Params:** _none_

### `goat_listings_count`

- **HTTP:** `GET /goat/listings/count`
- **What:** Get GOAT live listing count. Returns how many listings GOAT currently has live across its whole marketplace. This is the only way to see GOAT's true catalog size, because GET /goat/search's total_results saturates at 10000 on a broad query and cannot report a total above that ceiling.
- **Params:** _none_

### `goat_product`

- **HTTP:** `GET /goat/product/{slug}`
- **What:** Get GOAT product detail. Returns a GOAT product: identity/descriptive metadata (name, brand, SKU, colorway, designer, silhouette, taxonomy, materials, release date, retail price, editorial story, images, full size range, other products featured alongside it), plus live per-size/condition pricing and stock status (lowest price, GOAT Instant Ship price, last sold price, highest current buyer offer).
- **Params:** `country_code` (string, optional) — ISO 3166-1 alpha-2 country code used to localize per-size pricing, defaults to US; `slug` (string, **required**) — GOAT product URL slug, the path segment of a https://www.goat.com/sneakers/{slug} product page

### `goat_product_recommended`

- **HTTP:** `GET /goat/product/{slug}/recommended`
- **What:** Get GOAT recommended products for a product. Returns the recommended/related products GOAT's own product page shows for a given product (other colorways, similar products) -- descriptive metadata only, no live pricing.
- **Params:** `count` (integer, optional) — Number of recommended products to return, defaults to 8, maximum 24; `slug` (string, **required**) — GOAT product URL slug to find related products for

### `goat_search`

- **HTTP:** `GET /goat/search`
- **What:** Search GOAT products. Searches or browses GOAT's sneaker/streetwear/collectibles catalog by free-text query and/or facet filters (category, footwear sub-type, activity, color, gender, condition, brand, release year, price range, release-date range, silhouette, designer, in-stock/under-retail/instant-ship, curated collection), returning product summaries (brand, silhouette, category, image, stock status, headline pricing across all sizes) plus the total matching count. Query is optional -- a facet filter alone browses the catalog the same way GOAT's own category/brand pages do.
- **Params:** `activities` (string, optional) — Filter by activity (sneakers only), comma-separated for multiple values; `brands` (string, optional) — Filter by one or more brand slugs, comma-separated, e.g. air-jordan,nike. GET /goat/search/facets lists GOAT's top brands; long-tail brands are valid here even when absent from that list; `categories` (string, optional) — Filter by category, comma-separated for multiple values. See GET /goat/search/facets for the current live list; `collection_slug` (string, optional) — Scope results to a GOAT curated collection (see GET /goat/collection), combinable with query, every other filter, and sort; `colors` (string, optional) — Filter by color, comma-separated for multiple values; `conditions` (string, optional) — Filter by item condition, comma-separated for multiple values; `designers` (string, optional) — Filter by one or more designers, comma-separated, matching GOAT's own naming (see a product's designer field); `genders` (string, optional) — Filter by gender, comma-separated for multiple values; `in_stock` (boolean, optional) — Only include products currently in stock; `instant_ship` (boolean, optional) — Only include products with GOAT Instant Ship availability; `limit` (integer, optional) — Results per page, defaults to 12, maximum 100; `page` (integer, optional) — 1-indexed result page, defaults to 1; `price_cents_max` (integer, optional) — Only include results priced at or below this amount, in cents; `price_cents_min` (integer, optional) — Only include results priced at or above this amount, in cents; `product_types` (string, optional) — Filter by footwear sub-type, comma-separated for multiple values; `query` (string, optional) — Free-text search query, e.g. a model name, colorway, or style code. Optional -- omit to browse by facet filters alone; `released_after` (string, optional) — Only include products released on or after this date (YYYY-MM-DD, UTC); `released_before` (string, optional) — Only include products released on or before this date (YYYY-MM-DD, UTC); `silhouettes` (string, optional) — Filter by one or more silhouettes, comma-separated, matching GOAT's own naming (see a product's silhouette field); `sort` (string, optional) — Result sort order, defaults to relevance; `under_retail` (boolean, optional) — Only include products currently trading below original retail price; `years` (string, optional) — Filter by season year(s), comma-separated, e.g. 2025,2026. See GET /goat/search/facets for the current live list

### `goat_search_facets`

- **HTTP:** `GET /goat/search/facets`
- **What:** Get GOAT search facet values. Returns the accepted values for goat_search's filter parameters: categories, colors, genders, conditions, brands, and years are returned live so a value GOAT adds is discoverable without any client-side change, while product_types and activities are served from a maintained list because GOAT exposes no live facet for them. brands is GOAT's top brands ordered by product count, not the complete brand list -- when brands_truncated is true, brands beyond the ones listed exist and remain valid goat_search values.
- **Params:** _none_

### `goat_suggest`

- **HTTP:** `GET /goat/suggest`
- **What:** Autocomplete a GOAT search. Returns GOAT's own search-box autocomplete for a partial query: matching curated collections and matching products. The collections carry the slug values accepted by GET /goat/collection and by GET /goat/search's collection_slug parameter, making this the way to discover collection slugs.
- **Params:** `limit` (integer, optional) — Maximum curated collections to return. Defaults to 8, maximum 20. Does not affect the product count, which upstream fixes at 25; `query` (string, **required**) — Partial search text to autocomplete

### `goat_trending_searches`

- **HTTP:** `GET /goat/searches/trending`
- **What:** Get GOAT trending searches. Returns the search terms GOAT is currently surfacing as popular, in GOAT's own ranking order -- the same list its own search box shows. Each term is free text ready to pass to GET /goat/search's query parameter.
- **Params:** _none_

## Poshmark (8)

### `poshmark_brand`

- **HTTP:** `GET /poshmark/brand/{name}`
- **What:** Browse Poshmark listings by brand. Returns a page of Poshmark listings for a given brand name (e.g. Nike), the same browsing view as Poshmark's own brand pages. Pass a previous response's next_max_id back as max_id to fetch the next page.
- **Params:** `max_id` (string, optional) — Opaque pagination cursor from a previous response's next_max_id. Omit for the first page; `name` (string, **required**) — Poshmark brand name, matching the path segment of a /brand/{name} URL

### `poshmark_brands`

- **HTTP:** `GET /poshmark/brands`
- **What:** Get the full Poshmark brand directory. Returns Poshmark's full brand directory: every brand Poshmark recognizes (name, slug, logo, known aliases), not just brands with active listings for a given search or category filter. Useful for resolving a brand name to the exact value the brand/search filters expect.
- **Params:** _none_

### `poshmark_categories`

- **HTTP:** `GET /poshmark/categories`
- **What:** Get the Poshmark department/category browse taxonomy. Returns Poshmark's full department/category browse taxonomy (e.g. Women > Shoes, Men > Jackets & Coats). Each entry's path resolves directly against the category endpoint. This is reference data that changes rarely, so responses are cached.
- **Params:** _none_

### `poshmark_category`

- **HTTP:** `GET /poshmark/category/{path}`
- **What:** Browse Poshmark listings by category. Returns a page of Poshmark listings for a given category path (e.g. Women-Shoes, Men-Shirts), the same browsing view as Poshmark's own category pages. Pass a previous response's next_max_id back as max_id to fetch the next page.
- **Params:** `max_id` (string, optional) — Opaque pagination cursor from a previous response's next_max_id. Omit for the first page; `path` (string, **required**) — Poshmark category path segment, e.g. Women-Shoes, Men-Shirts

### `poshmark_closet`

- **HTTP:** `GET /poshmark/closet/{username}`
- **What:** Get Poshmark seller closet (storefront). Returns a Poshmark closet (seller storefront) page: the seller's public profile and reputation stats (followers, ratings, items sold) plus a first page of their currently available listings and total listing count. Pass a previous response's next_max_id back as max_id to fetch the next page of listings; paginated responses omit the seller profile, so fetch without max_id first to get seller fields.
- **Params:** `max_id` (string, optional) — Opaque pagination cursor from a previous response's next_max_id. Omit for the first page; `username` (string, **required**) — Poshmark seller username, the path segment of a /closet/{username} URL

### `poshmark_listing`

- **HTTP:** `GET /poshmark/listing/{id}`
- **What:** Get Poshmark listing detail. Returns a Poshmark item-detail page: the full listing (description, all photos, size/brand/condition, inventory), its seller's profile, public comments, and similar listings Poshmark itself surfaces on the same page.
- **Params:** `id` (string, **required**) — Poshmark listing id, the trailing id segment of a /listing/{slug}-{id} URL

### `poshmark_search`

- **HTTP:** `GET /poshmark/search`
- **What:** Search Poshmark listings. Searches Poshmark for clothing, shoes, and accessory listings, returning listing summaries (title, price, brand, size, condition, seller, images) plus the total matching count and an opaque pagination cursor. Pass a previous response's next_max_id back as max_id to fetch the next page.
- **Params:** `department` (string, optional) — Department filter, e.g. Women, Men, Kids; `max_id` (string, optional) — Opaque pagination cursor from a previous response's next_max_id. Omit for the first page; `query` (string, **required**) — Free-text keyword search

### `poshmark_trend`

- **HTTP:** `GET /poshmark/trend/{id}`
- **What:** Browse a Poshmark trend/showroom collection. Returns a page of Poshmark listings for a curated trend/showroom collection (e.g. "Vintage Celine Handbags"), the same browsing view as Poshmark's own trend pages. Pass a previous response's next_max_id back as max_id to fetch the next page.
- **Params:** `id` (string, **required**) — Poshmark trend/showroom id, the trailing id segment of a /trend/{slug}-{id} URL; `max_id` (string, optional) — Opaque pagination cursor from a previous response's next_max_id. Omit for the first page

## StockX (5)

### `stockx_brands`

- **HTTP:** `GET /stockx/brands`
- **What:** Get StockX brand catalog. Returns StockX's full brand catalog (name and URL slug for every brand in its own brand directory), suitable for building GET /stockx/search's brand parameter or GET /stockx/search's model parameter's required single-brand context.
- **Params:** _none_

### `stockx_categories`

- **HTTP:** `GET /stockx/categories`
- **What:** Get StockX category/subcategory taxonomy. Returns StockX's full category/subcategory reference: the 7 top-level categories accepted by GET /stockx/search's category parameter, each with its subcategories (e.g. Shoes -> Boots, Cleats, Clogs).
- **Params:** _none_

### `stockx_product`

- **HTTP:** `GET /stockx/product/{slug}`
- **What:** Get StockX product detail. Returns a StockX product: identity (title, brand, model, colorway, style id, retail price, release date, description, image), current market data (lowest ask, highest bid, last sale, trailing average price/sales count, delivery-speed ask tiers), individual seller listings (price, condition, size), related-product recommendations (other colorways/siblings StockX surfaces on the product page), and any promotional badges.
- **Params:** `slug` (string, **required**) — StockX product URL slug (the urlKey), the path segment of a https://stockx.com/{slug} product page

### `stockx_releases`

- **HTTP:** `GET /stockx/releases`
- **What:** Get StockX upcoming release calendar. Returns a date-ordered page (release date ascending) of StockX's upcoming release calendar: new and restocked products releasing on or after the given date, with product summaries, headline pricing, and each item's published release date.
- **Params:** `from` (string, optional) — Only include releases on or after this date (YYYY-MM-DD, UTC). Defaults to today; `limit` (integer, optional) — Results per page, defaults to 20, maximum 100; `page` (integer, optional) — 1-indexed result page, defaults to 1

### `stockx_search`

- **HTTP:** `GET /stockx/search`
- **What:** Search/browse StockX products. Browses StockX's product catalog by category with optional free-text keyword search and facet filters (gender, brand, color, shoe height, activity, availability), returning product summaries with headline pricing plus the total matching count.
- **Params:** `activity` (string, optional) — Filter by activity, comma-separated for multiple values; `available_now` (boolean, optional) — Only include products with at least one active ask; `below_retail` (boolean, optional) — Only include products currently trading below original retail price; `brand` (string, optional) — Filter by one or more brand slugs, comma-separated, e.g. jordan,nike; `category` (string, **required**) — StockX top-level category; `color` (string, optional) — Filter by color, comma-separated for multiple values; `gender` (string, optional) — Filter by gender, comma-separated for multiple values; `limit` (integer, optional) — Results per page, defaults to 20, maximum 100; `model` (string, optional) — Filter by a single model slug, e.g. air-force-1. Requires exactly one value in brand; `page` (integer, optional) — 1-indexed result page, defaults to 1; `query` (string, optional) — Free-text keyword search within the category, e.g. a model name or colorway; `shoe_height` (string, optional) — Filter by shoe height, comma-separated for multiple values; `sort` (string, optional) — Result sort order, defaults to featured; `xpress_ship` (boolean, optional) — Only include products with StockX Xpress Ship availability
