## Description:

Harbor Freight product data as structured JSON - search harborfreight.com and list clearance with national price, sale price and end date, public coupon price, Inside Track member price and the competitor compare-at price, read one product with UPC, specifications, manuals and variants, batch prices for up to 50 items, find stores near a ZIP, check in-stock, limited or out-of-stock status and aisle for up to 20 items at nearby stores, and page customer reviews. 7 endpoints, 1 credit each.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents can search Harbor Freight products, compare listed prices and promotions, find nearby stores, check reported stock and aisle details, and retrieve product specifications or reviews.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Store lookups send the supplied ZIP code or coordinates to Scavio.

Mitigation: Share only the location detail needed for the lookup, or use selected store IDs when practical.

Risk: Requests require an API key, which could be exposed if embedded in source code.

Mitigation: Keep SCAVIO_API_KEY in an environment variable or secret store and out of source control.

Risk: API requests consume credits.

Mitigation: Use only the needed endpoints and batch price lookups where possible.

Risk: Store availability comes from a daily inventory snapshot and may be stale for same-day plans.

Mitigation: Check the inventory timestamp and confirm availability with the store before traveling.

## Reference(s):

- [Scavio Harbor Freight API documentation](https://scavio.dev/docs/harborfreight-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api)
- [Scavio API rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=harbor-freight-api)
- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/harbor-freight-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [Structured JSON containing product, pricing, store, availability, specification, or review data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each endpoint call costs one API credit; batch prices support up to 50 items and availability supports up to 20 items.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
