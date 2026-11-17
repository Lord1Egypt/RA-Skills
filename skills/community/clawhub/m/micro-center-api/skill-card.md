## Description:

Micro Center product data as structured JSON at the store you choose - search by keyword or category with price, original price and that store's stock count (capped at 25+), open-box units and price, read one product with specs, UPC, recent reviews, the store's open-box units and which stores have it, and list every Micro Center store id. 3 endpoints; search and product 2 credits, stores 1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping assistants use the skill to find Micro Center products, compare prices, check store specific stock and open-box availability, and retrieve product specifications and reviews.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Search terms and selected stores are sent to Scavio, and API requests consume account credits.

Mitigation: Avoid sensitive search terms and monitor credit use, especially during repeated lookups.

Risk: An exposed API key could allow unauthorized use of the account.

Mitigation: Keep SCAVIO_API_KEY private and restrict the optional MCP integration to the tools needed.

Risk: External SDK and MCP code, along with Scavio's service-side handling, were outside this review.

Mitigation: Review those components and service terms before relying on them.

## Reference(s):

- [Scavio Micro Center API overview](https://scavio.dev/microcenter-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api)
- [Micro Center search endpoint documentation](https://scavio.dev/docs/microcenter-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api)
- [Micro Center product endpoint documentation](https://scavio.dev/docs/microcenter-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api)
- [Micro Center stores endpoint documentation](https://scavio.dev/docs/microcenter-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api)
- [Scavio API rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured product and store data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Store-specific stock and open-box availability; reported stock counts are capped at 25+.]

## Skill Version(s):

1.0.0 (source: evidence.json release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
