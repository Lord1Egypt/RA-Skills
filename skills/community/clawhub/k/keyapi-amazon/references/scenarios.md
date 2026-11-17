# Scenario Cards

Use these scenario cards to translate natural-language Amazon requests into a small, stable set of inputs. They are routing hints only; the exact method, `/v1/...` path, parameters, body shape, pagination, and response contract must come from `https://docs.keyapi.ai/llms.txt` and the linked endpoint page before execution.

Do not start by listing raw endpoints. First identify the user's business goal, choose the closest scenario, collect only missing high-value inputs, resolve the current docs, then execute through `scripts/keyapi-api.mjs` when available.

## Core Entities

products, ASINs, GTINs, categories, deals, promo codes, offers, reviews, sellers, and Amazon Influencer storefronts

## Scenario Modules

| User intent | Reference module | Docs path family |
|---|---|---|
| Product discovery, category exploration, rankings, deals, offers, reviews, and identifier conversion | `amazon-product-rules.md` | /amazon/ |
| Seller profile, seller catalog, seller feedback, and offer comparison | `amazon-seller-rules.md` | /amazon/ |
| Influencer storefront profile, posts, list posts, and featured products | `amazon-influencer-rules.md` | /amazon/ |

## 1. Product discovery and category exploration

- User intent: Find products in a marketplace by keyword, category, best-seller list, price, rating, or availability signal.
- Primary entity: product / category
- Ask for: marketplace, keyword or category path, optional filters such as price/rating/Prime, sort preference, and top N.
- Default workflow: Start with product search for keyword intent, category list/products-by-category for browse intent, and best-seller for ranking/list-type intent; enrich shortlisted ASINs with details or offers only when needed.
- Reference module: `amazon-product-rules.md`
- Endpoint shortlist:
  - [Product Search](https://docs.keyapi.ai/en/amazon/search.md) - Search Amazon products by keyword or ASIN. Filter by category, price range, brand, Prime eligibility, and customer ratings. Sort results by relevance, price, reviews, or newest arrivals.
  - [Product Category List](https://docs.keyapi.ai/en/amazon/product-category-list.md) - Retrieve the list of top-level product categories available on Amazon for a given marketplace.
  - [Products by Category](https://docs.keyapi.ai/en/amazon/products-by-category.md) - Retrieve a paginated list of products within a specific Amazon category using the category ID. Supports sorting by price or relevance, and filtering by price range.
  - [Best Seller](https://docs.keyapi.ai/en/amazon/best-sellers.md) - Retrieve best-selling products for a specified Amazon category or subcategory. Supports multiple list types: Best Sellers, New Releases, Movers & Shakers, Most Wished For, and Gift Ideas. Category path can be found in Amazon's Best Sellers URLs.
  - [Product Details](https://docs.keyapi.ai/en/amazon/product-details.md) - Retrieve detailed product information for one or more ASINs (up to 10 per request). Returns title, price, images, ratings, specifications, and availability.

## 2. Product detail, identifiers, and offer economics

- User intent: Understand one or more ASINs, compare buying options, or convert an identifier for downstream matching.
- Primary entity: ASIN / GTIN / offer
- Ask for: ASIN list or GTIN task, marketplace, product condition or delivery filters when comparing offers.
- Default workflow: Use product details for up to the documented batch size, convert ASIN to GTIN when identifier matching is required, then inspect offers or promo code detail for purchase economics.
- Reference module: `amazon-product-rules.md`
- Endpoint shortlist:
  - [Product Details](https://docs.keyapi.ai/en/amazon/product-details.md) - Retrieve detailed product information for one or more ASINs (up to 10 per request). Returns title, price, images, ratings, specifications, and availability.
  - [Asin to Gtin](https://docs.keyapi.ai/en/amazon/asin-to-gtin.md) - Convert an Amazon product ASIN to its corresponding GTIN (Global Trade Item Number). Supports 24 Amazon marketplaces.
  - [Product Offers](https://docs.keyapi.ai/en/amazon/product-offers.md) - Retrieve available purchase offers for one or more products (up to 10 ASINs per request). Filter by product condition (new, used, refurbished) and delivery options (Prime, Free Shipping, etc.).
  - [Promo Code Detail](https://docs.keyapi.ai/en/amazon/promo-code-details.md) - Retrieve products and discount details associated with a specific Amazon promotional code.

## 3. Deals and promotion research

- User intent: Find active discounts or inspect all products in a specific deal or promo campaign.
- Primary entity: deal / promo code / product
- Ask for: marketplace, category or deal ID, discount/star/price filters, and sorting preference.
- Default workflow: Use deals for broad discovery, deal products for a known deal ID, and promo code detail when the user provides a code; enrich interesting ASINs with details/offers.
- Reference module: `amazon-product-rules.md`
- Endpoint shortlist:
  - [Deals](https://docs.keyapi.ai/en/amazon/deals.md) - Retrieve active Amazon deals with rich filtering options. Filter by category, star rating, price range, discount percentage, and deal type (Lightning Deals, Prime Exclusive, Prime Early Access).
  - [Deal Products](https://docs.keyapi.ai/en/amazon/deal-products.md) - Retrieve all products included in a specific Amazon deal by deal ID. Results can be sorted by featured, price, reviews, or newest.
  - [Promo Code Detail](https://docs.keyapi.ai/en/amazon/promo-code-details.md) - Retrieve products and discount details associated with a specific Amazon promotional code.
  - [Product Details](https://docs.keyapi.ai/en/amazon/product-details.md) - Retrieve detailed product information for one or more ASINs (up to 10 per request). Returns title, price, images, ratings, specifications, and availability.
  - [Product Offers](https://docs.keyapi.ai/en/amazon/product-offers.md) - Retrieve available purchase offers for one or more products (up to 10 ASINs per request). Filter by product condition (new, used, refurbished) and delivery options (Prime, Free Shipping, etc.).

## 4. Review and customer signal analysis

- User intent: Analyze buyer feedback, inspect top reviews, or retrieve a specific review.
- Primary entity: product review
- Ask for: ASIN, marketplace, star filter, sorting preference, review ID if known, and requested sample size.
- Default workflow: Use product reviews for paginated review collection, top product reviews for helpful-review summaries, and review details when the user provides a review ID.
- Reference module: `amazon-product-rules.md`
- Endpoint shortlist:
  - [Product Reviews](https://docs.keyapi.ai/en/amazon/product-reviews.md) - Retrieve paginated customer reviews for a product by ASIN. Sort by top reviews or most recent. Supports filtering by star rating and verified purchase status.
  - [Top Product Reviews](https://docs.keyapi.ai/en/amazon/top-product-reviews.md) - Retrieve the most helpful (top) customer reviews for a product by ASIN. Supports field projection to return only the review fields you need.
  - [Product Review Details](https://docs.keyapi.ai/en/amazon/product-review-details.md) - Retrieve the full details of a specific product review by review ID, including rating, title, body text, and reviewer information.

## 5. Seller intelligence and assortment analysis

- User intent: Evaluate an Amazon seller, inspect its catalog, feedback, or offer competitiveness.
- Primary entity: seller
- Ask for: seller ID, marketplace, catalog page depth, review sentiment filter, and whether offer comparison is required.
- Default workflow: Fetch seller profile first, then seller products and seller reviews; use product offers on key ASINs when comparing seller competitiveness.
- Reference module: `amazon-seller-rules.md`
- Endpoint shortlist:
  - [Seller Profile](https://docs.keyapi.ai/en/amazon/seller-profile.md) - Retrieve profile information for an Amazon seller, including business name, ratings, response rate, and storefront details.
  - [Seller Products](https://docs.keyapi.ai/en/amazon/seller-products.md) - Retrieve product listings for a specific Amazon seller by seller ID. Supports sorting by price or relevance, with pagination.
  - [Seller Reviews](https://docs.keyapi.ai/en/amazon/seller-reviews.md) - Retrieve customer feedback and reviews for a specific Amazon seller. Filter by star rating (positive/negative/all) with pagination support.
  - [Product Offers](https://docs.keyapi.ai/en/amazon/product-offers.md) - Retrieve available purchase offers for one or more products (up to 10 ASINs per request). Filter by product condition (new, used, refurbished) and delivery options (Prime, Free Shipping, etc.).

## 6. Amazon Influencer storefront research

- User intent: Audit an influencer storefront, browse posts, and retrieve products featured in list posts.
- Primary entity: Amazon Influencer / storefront post
- Ask for: storefront name, post scope or keyword, post type, cursor depth, and whether featured products should be expanded.
- Default workflow: Fetch influencer profile, then posts; for posts of type List, call influencer post products to retrieve featured ASINs and optionally enrich those products.
- Reference module: `amazon-influencer-rules.md`
- Endpoint shortlist:
  - [Influencer Profile](https://docs.keyapi.ai/en/amazon/influencer-profile.md) - Retrieve profile details for an Amazon Influencer by their storefront name, including bio, follower count, and storefront metadata.
  - [Influencer Posts](https://docs.keyapi.ai/en/amazon/influencer-posts.md) - Retrieve posts from an Amazon Influencer's storefront, including idea lists, photos, and videos. Supports keyword search, scope filtering, and cursor-based pagination.
  - [Influencer Post Products](https://docs.keyapi.ai/en/amazon/influencer-post-products.md) - Retrieve the products featured in a specific Amazon Influencer list post. Only applicable to posts with type 'List'. Supports cursor-based pagination.
  - [Product Details](https://docs.keyapi.ai/en/amazon/product-details.md) - Retrieve detailed product information for one or more ASINs (up to 10 per request). Returns title, price, images, ratings, specifications, and availability.

## Docs Search Strategy

1. Map the user's natural-language request to the closest scenario and API concept, then search `llms.txt` for the platform slug plus that semantic entity/action. Do not rely on literal keyword matching when the user wording is vague, translated, or business-oriented.
2. Prefer the narrowest endpoint whose title and description match the requested workflow.
3. Resolve the selected endpoint page before any live call; never infer method or path from this file.
4. Compose multiple endpoints only when the user asks for a report, comparison, enrichment, or explanation that one endpoint cannot answer.
5. API calls are live by default. Repeating the same parameters calls the API again. Large payloads may return a stdout preview; when complete fields are needed for analysis, rerun the same documented request with `--output-file <temp-or-workspace-.tmp-keyapi-file>.json` and read the API payload from `data.data`. Use a user-facing output path only when the user asks to save or export results.

## User Input Compression

Compress parameter-heavy tasks into:

- Goal: search, detail, enrichment, ranking, comparison, monitoring, or report
- Entity: the object being searched, analyzed, compared, ranked, or monitored
- Scope: market, country, language, category, keyword, identifier, date window, and page depth
- Sort or metric: freshness, relevance, growth, engagement, rating, sales, price, audience, or other documented metric
- Pagination depth: one page, top N, until enough evidence, or all available within the user's approved scope
- Output format: concise answer, table, raw JSON, or structured report
