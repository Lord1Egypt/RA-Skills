## Description:

Search Menards products and stores, returning store-specific prices, rebates, inventory, product details, and aisle locations as structured data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and agents can find Menards stores, search products at a selected store, and retrieve current product prices, rebates, availability, specifications, and aisle information.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Shopping queries, selected products, and supplied ZIP code or city and state are sent to Scavio; service-side data retention is not verified.

Mitigation: Share only the location and product details needed for the lookup, and avoid including sensitive information in queries.

Risk: API requests consume credits, with different costs for searches, product details, and store-specific product lookups.

Mitigation: Check the documented credit cost and use direct API calls when the optional MCP tools are unnecessary.

Risk: An exposed Scavio API key could be used to make requests against the account.

Mitigation: Keep SCAVIO_API_KEY in an environment variable or secret store rather than source code.

## Reference(s):

- [Menards API overview](https://scavio.dev/menards-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=menards-product-data)
- [Menards search documentation](https://scavio.dev/docs/menards-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=menards-product-data)
- [Menards product documentation](https://scavio.dev/docs/menards-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=menards-product-data)
- [Menards stores documentation](https://scavio.dev/docs/menards-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=menards-product-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=menards-product-data)

## Skill Output:

**Output Type(s):** [Structured data, JSON]

**Output Format:** [JSON product, price, rebate, inventory, and store lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are specific to the selected store when a store ID is provided.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
