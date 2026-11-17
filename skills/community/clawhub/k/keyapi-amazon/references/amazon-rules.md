# Amazon Rules

Use this file for platform-level routing boundaries, identifier discipline, and output expectations. Use module files for scenario-specific workflows.

## Entity Scope

products, ASINs, GTINs, categories, deals, promo codes, offers, reviews, sellers, and Amazon Influencer storefronts

## Identifier Discipline

- Preserve ASINs from every product, deal, category, seller, and influencer workflow for downstream detail, offers, reviews, and identifier conversion.
- Use GTIN conversion only when catalog matching or external identifier normalization is part of the task.
- Seller IDs and influencer storefront names are different entity identifiers; do not substitute one for the other.

## Scenario Module Routing

- Use `amazon-product-rules.md` for product discovery, category/best-seller research, deals, offers, reviews, promo codes, and ASIN/GTIN conversion.
- Use `amazon-seller-rules.md` for seller profile, seller catalog, seller feedback, and offer comparison workflows.
- Use `amazon-influencer-rules.md` for Amazon Influencer storefront profiles, posts, list posts, and featured products.
- If a request spans multiple modules, load the smallest set of module files needed and confirm report scope before broad multi-endpoint execution.

## Documentation Hints

- Filter `https://docs.keyapi.ai/llms.txt` for links under `https://docs.keyapi.ai/en/amazon/`.
- Treat endpoint titles as search hints, not stable tool names.
- Extract the current REST method and `/v1/...` path from the endpoint docs page before calling the API.
- Use examples from the docs page only after replacing sample identifiers with user-provided or resolved identifiers.

## Output Guidance

- For product discovery, return ranked candidates with ASIN, title, marketplace, price/rating evidence when available, and the next enrichment step.
- For seller work, separate seller-level reputation from product-level offer facts.
- For review work, distinguish review samples, top helpful reviews, and single review detail.
- For reports, organize findings by entity, evidence, limitations, and recommended follow-up calls.
