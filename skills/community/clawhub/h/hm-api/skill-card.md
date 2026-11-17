## Description:

H&M API for H&M prices by country - one article's price, sale price, member price and online stock by size in each H&M market, in that market's currency (article codes are the same in every market); keyword search, product detail with composition, the 10 latest reviews and fit feedback, online stock per size, stores with opening hours, category, sale and new-arrival grids, search suggestions and where an article is made. 47 countries. 9 endpoints, 1 credit each (product 2). No price history (poll), no store stock per size, no full review list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve H&M product, price, online size availability, store, category, sale, new-arrival, search suggestion, and production information across supported markets.

### Deployment Geography for Use:

Global (47 H&M markets, with endpoint-specific country availability).

## Known Risks and Mitigations:

Risk: Store lookups may disclose location details to Scavio; the security scan is partial and identifies a location privacy disclosure gap.

Mitigation: Before using store lookup, consider what lookup details you are comfortable sharing and use a city or postal code when that is sufficient.

## Reference(s):

- [Scavio H&M API documentation](https://scavio.dev/docs/hm-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=hm-api)
- [ClawHub release page](https://clawhub.ai/scavio-ai/skills/hm-api)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Code, Configuration instructions, Guidance]

**Output Format:** [Structured JSON API responses and Markdown guidance with code examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices are returned in each market's currency; availability and returned fields vary by endpoint and country.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
