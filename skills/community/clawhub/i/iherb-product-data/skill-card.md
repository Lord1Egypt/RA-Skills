## Description:

Search iHerb products and retrieve prices, supplement details, ratings, and review summaries through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product research agents can use this skill to look up iHerb products, compare current US prices and stock, inspect supplement facts and ingredients, and summarize ratings and selected reviews.

### Deployment Geography for Use:

Global; product data is from the US iHerb store and prices are in USD.

## Known Risks and Mitigations:

Risk: Product searches and identifiers may reveal health interests to Scavio.

Mitigation: Send only the product terms and identifiers needed; omit personal or medical details.

Risk: An exposed API key can enable account use, and requests consume credits.

Mitigation: Keep the API key in a secret store or environment variable and check credit use before making repeated calls.

Risk: The behavior of optional SDK packages and server-side data retention was not established by this artifact review.

Mitigation: Review optional packages and enabled MCP platforms before using them; avoid sending unnecessary sensitive search details.

## Reference(s):

- [Scavio iHerb API overview](https://scavio.dev/iherb-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data)
- [iHerb search endpoint](https://scavio.dev/docs/iherb-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data)
- [iHerb product endpoint](https://scavio.dev/docs/iherb-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data)
- [iHerb prices endpoint](https://scavio.dev/docs/iherb-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data)
- [iHerb reviews endpoint](https://scavio.dev/docs/iherb-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=iherb-product-data)

## Skill Output:

**Output Type(s):** [JSON, Product data]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live US-store product data in USD; endpoint calls cost 2 credits each.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
