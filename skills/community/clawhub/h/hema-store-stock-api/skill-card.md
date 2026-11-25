## Description:

Provides HEMA product, store stock, price, promotion, review, search, and store information across supported European markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shopping assistants, developers, and retail researchers use the skill to retrieve HEMA store stock reported at a given time, product details, market-specific online prices and promotions, store information, and customer reviews. It supports the Netherlands, Belgium, France, and Germany webshops, plus store lookups in Luxembourg and Austria.

### Deployment Geography for Use:

Netherlands, Belgium, France, Germany, Luxembourg, and Austria.

## Known Risks and Mitigations:

Risk: Store stock lookups may send a user's location and article numbers to Scavio; scanner coverage was incomplete.

Mitigation: Use only the location detail needed for the lookup, avoid sensitive personal locations, and review returned stock and price details before relying on them.

## Reference(s):

- [Scavio HEMA API overview](https://scavio.dev/hema-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api)
- [HEMA store stock API documentation](https://scavio.dev/docs/hema-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api)
- [HEMA product API documentation](https://scavio.dev/docs/hema-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api)
- [HEMA reviews API documentation](https://scavio.dev/docs/hema-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=hema-store-stock-api)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON data with concise explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live, market-specific results; each endpoint call costs one credit.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
