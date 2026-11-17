## Description:

Provides HEB and HEB Mexico product search, detailed product data, and store lookup through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping agents use the skill to find HEB products, prices, nutrition, and stock, look up nearby US stores, and retrieve HEB Mexico product and promotion data.

### Deployment Geography for Use:

Texas, United States, and northeastern Mexico, where HEB operates the services described by the skill.

## Known Risks and Mitigations:

Risk: Search queries and supplied ZIP codes or cities are received by Scavio, and its privacy policy says request logs may be retained for up to 90 days.

Mitigation: Send only the location detail needed for the lookup and avoid including sensitive personal information.

Risk: Calls require a Scavio API key and consume account credits.

Mitigation: Keep the API key in a secret store or environment variable and monitor credit usage.

## Reference(s):

- [Scavio HEB API overview](https://scavio.dev/heb-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data)
- [HEB search documentation](https://scavio.dev/docs/heb-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data)
- [HEB product documentation](https://scavio.dev/docs/heb-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data)
- [HEB store locator documentation](https://scavio.dev/docs/heb-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=heb-grocery-data)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON product and store data, suitable for a concise natural-language summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices are returned in cents; US prices, stock, and aisle details can be store-specific, while HEB Mexico data uses its default store.]

## Skill Version(s):

1.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
