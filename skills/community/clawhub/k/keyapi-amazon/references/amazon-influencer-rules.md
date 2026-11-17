# Amazon Influencer Module Rules

## 1. Module Scope

Use this module for Amazon Influencer storefront profile, posts, list posts, and featured products.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Storefront identity and profile

- Documentation: `https://docs.keyapi.ai/en/amazon/influencer-profile.md`
- Purpose: Retrieve Influencer storefront metadata before post or product analysis.

### Best Suited For

- creator storefront validation
- influencer profile summaries
- storefront metadata capture

### Routing Rules

- Use storefront name as the primary input when the docs require it.
- Do not confuse Amazon Influencer storefronts with Amazon seller IDs.
- Use profile first when the user asks for a creator/storefront report.

## 3. Post and content audit

- Documentation: `https://docs.keyapi.ai/en/amazon/influencer-posts.md`
- Purpose: Retrieve Influencer posts including lists, photos, and videos.

### Best Suited For

- storefront content audit
- idea-list review
- creator product curation research
- post keyword or scope filtering

### Routing Rules

- Use posts after resolving the storefront profile or when the storefront name is already known.
- Preserve post IDs/types for downstream list-product retrieval.
- Do not call post-products unless the post type supports it.

## 4. Featured products from list posts

- Documentation: `https://docs.keyapi.ai/en/amazon/influencer-post-products.md`
- Documentation: `https://docs.keyapi.ai/en/amazon/product-details.md`
- Purpose: Retrieve products featured inside a specific Influencer list post.

### Best Suited For

- creator-to-product mapping
- featured product analysis
- affiliate storefront product research

### Routing Rules

- Use only for List posts as documented.
- Preserve ASINs for product details, offers, and reviews when the user wants product evidence.
- Use cursor pagination according to the docs when more list products are requested.

## 5. Common Workflows

- Influencer report: influencer profile -> influencer posts -> post products for selected list posts -> product details/offers/reviews.
- Product sourcing from creators: influencer posts -> list post products -> shortlist ASINs -> product module enrichment.
