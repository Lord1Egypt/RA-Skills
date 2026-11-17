## Description:

This skill retrieves Lowe's store-specific product prices, stock, aisle locations, nearby-store availability, store locations, and customer reviews as structured JSON through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to find Lowe's products, store-specific prices and stock, aisle locations, nearby availability, store locations, and customer reviews. The agent uses Scavio's Lowe's API to retrieve the requested information and present the structured results.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Requests share ZIP codes, search terms, and product identifiers with Scavio, and API calls consume credits.

Mitigation: Share only the location and product details needed for the lookup, and check credit usage before repeated requests.

Risk: The skill requires a Scavio API key.

Mitigation: Keep SCAVIO_API_KEY in a secret store or environment variable and do not include it in source files or shared prompts.

Risk: The supplied instructions do not audit external packages or the live service.

Mitigation: Review the service and any optional MCP tools before enabling them; use direct API calls or enable only the tools needed.

## Reference(s):

- [Scavio Lowe's API overview](https://scavio.dev/lowes-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data)
- [Product endpoint documentation](https://scavio.dev/docs/lowes-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data)
- [Search endpoint documentation](https://scavio.dev/docs/lowes-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data)
- [Store locator endpoint documentation](https://scavio.dev/docs/lowes-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data)
- [Reviews endpoint documentation](https://scavio.dev/docs/lowes-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data)
- [Scavio account setup](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON API results with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices and inventory are tied to the selected store; endpoint calls consume credits.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
