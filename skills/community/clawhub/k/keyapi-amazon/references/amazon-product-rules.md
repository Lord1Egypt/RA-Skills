# Amazon Product Module Rules

## 1. Module Scope

Use this module for product discovery, category and best-seller research, product detail enrichment, deals, offer economics, customer reviews, promo codes, and ASIN/GTIN conversion.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Product discovery and first-pass candidate collection

- Documentation: `https://docs.keyapi.ai/en/amazon/search.md`
- Documentation: `https://docs.keyapi.ai/en/amazon/products-by-category.md`
- Documentation: `https://docs.keyapi.ai/en/amazon/product-category-list.md`
- Purpose: Find product candidates from keyword, ASIN-like input, category browsing, or marketplace/category navigation.

### Best Suited For

- keyword product research
- brand or competitor lookup
- category browsing before enrichment
- candidate collection for later detail, offers, or reviews

### Routing Rules

- Use product search when the user starts from a keyword, brand, ASIN-like text, or broad product idea.
- Use product category list when the user needs category discovery or lacks a category ID/path.
- Use products by category after the category is known.
- Preserve ASINs from every result for detail, offers, reviews, seller, and GTIN workflows.
- Do not enrich every product by default; shortlist first unless the user requests a broad export.

## 3. Ranking, best-seller, and demand scan

- Documentation: `https://docs.keyapi.ai/en/amazon/best-sellers.md`
- Purpose: Retrieve marketplace/category ranking lists such as best sellers, new releases, movers, most wished for, and gift ideas.

### Best Suited For

- top product lists
- category demand snapshots
- new-release and mover monitoring
- gift or wishlist research

### Routing Rules

- Use this when the user asks for top, best-selling, new, movers, wished-for, or gift ideas.
- State marketplace, category, list type, and ranking position when available.
- Enrich only selected ASINs with product details, offers, or reviews.
- Do not treat a ranking list as a complete category catalog.

## 4. Product detail and catalog normalization

- Documentation: `https://docs.keyapi.ai/en/amazon/product-details.md`
- Documentation: `https://docs.keyapi.ai/en/amazon/asin-to-gtin.md`
- Purpose: Retrieve detailed product records and convert ASINs to GTIN when external catalog matching is needed.

### Best Suited For

- product profile reports
- price/rating/spec/image/availability checks
- batch enrichment of shortlisted ASINs
- catalog matching with UPC/EAN/GTIN systems

### Routing Rules

- Use product details after search, category, best-seller, deal, seller, or influencer results identify ASINs.
- Check current docs for batch limits before sending multiple ASINs.
- Use ASIN to GTIN only when identifier normalization is part of the user goal.
- Keep ASIN and GTIN facts separate because GTIN coverage may vary by marketplace/product.

## 5. Offer economics and seller comparison

- Documentation: `https://docs.keyapi.ai/en/amazon/product-offers.md`
- Purpose: Retrieve available purchase offers for ASINs and compare offer-level conditions.

### Best Suited For

- seller/offer comparison
- Prime/free-shipping or condition filtering
- price and delivery option analysis
- buy-box style evidence where returned

### Routing Rules

- Use after product resolution when the user asks who sells an item, what offers exist, or how prices differ.
- Keep offer-level facts separate from product-level detail facts.
- Use seller module only when the user wants seller profile, seller catalog, or seller feedback beyond offers.

## 6. Deals and promotional research

- Documentation: `https://docs.keyapi.ai/en/amazon/deals.md`
- Documentation: `https://docs.keyapi.ai/en/amazon/deal-products.md`
- Documentation: `https://docs.keyapi.ai/en/amazon/promo-code-details.md`
- Purpose: Find active deals, inspect products inside a known deal, or analyze a promo code.

### Best Suited For

- discount monitoring
- Prime or Lightning Deal research
- deal product analysis
- coupon or promotional-code investigation

### Routing Rules

- Use deals for broad discount discovery.
- Use deal products only after a deal ID is known.
- Use promo code detail only when a promo code is provided or requested.
- Enrich deal ASINs with details, offers, or reviews only after the user selects candidates.

## 7. Review and buyer-signal analysis

- Documentation: `https://docs.keyapi.ai/en/amazon/product-reviews.md`
- Documentation: `https://docs.keyapi.ai/en/amazon/top-product-reviews.md`
- Documentation: `https://docs.keyapi.ai/en/amazon/product-review-details.md`
- Purpose: Collect customer review evidence, top helpful reviews, or a single review record.

### Best Suited For

- customer objection mining
- quality and sentiment checks
- review evidence for product comparison
- single review verification

### Routing Rules

- Use product reviews for paginated review collection.
- Use top product reviews when helpful-review evidence is enough.
- Use product review details only after a review ID is known.
- State review sort/filter assumptions and do not overgeneralize from a small sample.

## 8. Common Workflows

- Product discovery: product search or category browse -> shortlist ASINs -> product details -> offers/reviews as needed.
- Category demand scan: category list -> best seller or products by category -> selected product details.
- Deal analysis: deals -> deal products -> details/offers/reviews for selected ASINs.
- Review analysis: product resolution -> product reviews or top reviews -> selected review detail.
