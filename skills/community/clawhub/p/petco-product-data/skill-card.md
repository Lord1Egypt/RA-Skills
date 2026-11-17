## Description:

Search Petco products and categories, compare prices and variants, retrieve product details, find nearby stores, and check store inventory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to look up Petco product details, prices, variants, store locations, and local inventory in response to pet-supply queries.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Search terms and ZIP codes are sent to Scavio; its data-retention practices were not verified.

Mitigation: Avoid including sensitive details and provide a ZIP code only when needed for store lookup.

Risk: API requests consume account credits.

Mitigation: Track credit usage and check the account balance before making repeated lookups.

Risk: An exposed SCAVIO_API_KEY could be used to make requests on the account.

Mitigation: Keep the key in an environment variable or secret store and out of source control.

Risk: Enabling the Scavio MCP server for Petco can add the Petco platform to its enabled platform set.

Mitigation: Review the enabled platforms and limit them to those needed for the task.

## Reference(s):

- [ClawHub release](https://clawhub.ai/scavio-ai/skills/petco-product-data)
- [Scavio Petco API overview](https://scavio.dev/petco-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data)
- [Petco search API](https://scavio.dev/docs/petco-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data)
- [Petco category API](https://scavio.dev/docs/petco-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data)
- [Petco product API](https://scavio.dev/docs/petco-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data)
- [Petco stores API](https://scavio.dev/docs/petco-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data)
- [Petco store inventory API](https://scavio.dev/docs/petco-store-inventory?utm_source=agent-skills&utm_medium=skill&utm_campaign=petco-product-data)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON containing Petco product, pricing, fulfillment, store, and inventory data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the supplied query, product or category identifiers, ZIP code, and store selection.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
