# Amazon Seller Module Rules

## 1. Module Scope

Use this module for seller profile, seller catalog, seller feedback, and seller-side offer or assortment analysis.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Seller identity and reputation

- Documentation: `https://docs.keyapi.ai/en/amazon/seller-profile.md`
- Documentation: `https://docs.keyapi.ai/en/amazon/seller-reviews.md`
- Purpose: Retrieve seller profile metadata and buyer feedback.

### Best Suited For

- seller credibility checks
- marketplace seller due diligence
- feedback review and rating analysis
- seller comparison

### Routing Rules

- Use seller profile first when the user asks who a seller is or whether a seller is trustworthy.
- Use seller reviews when the user asks for feedback, reputation, complaints, or service quality.
- Keep seller feedback separate from product reviews.

## 3. Seller catalog and assortment

- Documentation: `https://docs.keyapi.ai/en/amazon/seller-products.md`
- Documentation: `https://docs.keyapi.ai/en/amazon/product-details.md`
- Purpose: Retrieve product listings for a seller and enrich selected products.

### Best Suited For

- seller assortment audits
- brand storefront research
- catalog comparison
- identifying products worth detail enrichment

### Routing Rules

- Use seller products when a seller ID is known.
- Apply product details only to shortlisted ASINs, not every catalog item by default.
- Use product offers when the user asks how the seller competes on specific ASINs.

## 4. Seller competitiveness through offers

- Documentation: `https://docs.keyapi.ai/en/amazon/product-offers.md`
- Purpose: Compare seller presence and offer conditions on selected products.

### Best Suited For

- offer competitiveness checks
- Prime/free-shipping/condition comparison
- multi-seller ASIN analysis

### Routing Rules

- Use offers after resolving ASINs from seller products, product search, or user input.
- Do not infer seller-level quality from offers alone; combine with seller profile/reviews when needed.

## 5. Common Workflows

- Seller report: seller profile -> seller products -> seller reviews -> selected product offers/details.
- Assortment comparison: seller products for each seller -> normalize ASINs -> product details for overlaps or high-value items.
