## Description:

Provides structured Kohl's product, pricing, promotion, store, pickup availability, and coupon data through Scavio's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to search and monitor Kohl's products, prices, promotions, variants, and local pickup stock. It also supports store lookup, search suggestions, and public coupon-code checks.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: ClawScan reports a benign verdict, but its analysis was partial and flags a privacy disclosure gap: product or search details and location information such as a ZIP code may be sent to Scavio.

Mitigation: Avoid sensitive search terms and provide a ZIP code only when store-local availability is needed.

## Reference(s):

- [Scavio Kohl's API documentation](https://scavio.dev/docs/kohls-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data)
- [Scavio Kohl's API overview](https://scavio.dev/kohls-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data)
- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/kohls-product-data)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON with concise explanatory text when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live product prices, promotions, and inventory can change.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
