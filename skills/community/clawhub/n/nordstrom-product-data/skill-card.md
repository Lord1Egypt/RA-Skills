## Description:

Retrieves structured Nordstrom product, category, brand, price, stock, pickup, store, autocomplete, and review data through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Nordstrom listings and retrieve product details, prices, SKU availability, store pickup options, store information, and customer reviews.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Store searches can share the user's ZIP code with Scavio.

Mitigation: Only provide a ZIP code when the user is comfortable sharing location information; otherwise omit the location-specific store search.

## Reference(s):

- [Scavio Nordstrom Product API Documentation](https://scavio.dev/docs/nordstrom-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data)
- [Scavio Nordstrom API Overview](https://scavio.dev/nordstrom-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON containing Nordstrom product and retail data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fields vary by endpoint and request.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
