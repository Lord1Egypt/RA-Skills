## Description:

Look up Amazon product listings by ASIN or URL and return pricing, availability, ratings, features, and seller details through looot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidboulanouar](https://clawhub.ai/user/walidboulanouar)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to look up one or more Amazon listings by ASIN or product URL. The agent returns key listing details and compares products while showing the marketplace used for pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each product lookup run is billed, and provider prices may differ.

Mitigation: Inspect the endpoint price, show it to the user, and get approval before running; report the total cost after a batch.

Risk: Amazon prices and availability vary by marketplace and delivery location.

Mitigation: Set the marketplace and delivery country before lookup, and identify the marketplace used when reporting prices.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/walidboulanouar/skills/looot-amazon-product)
- [looot skill setup instructions](https://looot.ai/skill.md)
- [looot Amazon product skill page](https://looot.ai/agent-skills/amazon-product)

## Skill Output:

**Output Type(s):** [Text, Structured product details]

**Output Format:** [Product listing summary with title, price, availability, rating, review count, features, and seller details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pricing and availability depend on the selected marketplace and delivery location.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
