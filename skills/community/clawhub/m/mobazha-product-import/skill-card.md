## Description:

Import products from Shopify, Amazon, Etsy, or CSV into a Mobazha store. Use when the user wants to migrate or copy listings from another platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengzie](https://clawhub.ai/user/fengzie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and store operators use this skill to migrate or copy product listings from Shopify, Amazon, Etsy, WooCommerce, or CSV sources into a Mobazha store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example scraping and API code could send requests or credentials to unintended sites if copied without validation.

Mitigation: Use CSV exports or official APIs where possible, keep tokens least-privileged, and validate all destination hosts before making API or pagination requests.

Risk: Amazon product and image download guidance can fetch external URLs into local import packages.

Mitigation: Fetch only known public product and image URLs, respect robots.txt and rate limits, and write downloads into a controlled local directory.

Risk: Imported listings may contain incorrect pricing, shipping, or product data after transformation.

Mitigation: Review transformed listings before upload, verify prices and shipping profiles, and prefer the bulk import flow for consistent validation.

## Reference(s):

- [Mobazha Product Import Skill](https://clawhub.ai/fengzie/skills/mobazha-product-import)
- [Shopify Data Export Reference](references/shopify-api.md)
- [Amazon Product Scraping Reference](references/amazon-scrape.md)
- [Universal Field Mapping: External Platforms to Mobazha](references/mapping.md)
- [Shopify Products API](https://shopify.dev/docs/api/admin-rest/current/resources/product)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON, Python, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include import JSON schemas, API request examples, field mappings, and migration steps.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
