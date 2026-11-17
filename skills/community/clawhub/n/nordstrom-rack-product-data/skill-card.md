## Description:

Retrieve Nordstrom Rack product, pricing, clearance, review, SKU availability, store pickup, store location, and autocomplete data as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shopping and retail research agents use this skill to look up Nordstrom Rack products, prices, discounts, reviews, sizes, inventory, and pickup locations. Developers can use the returned structured data to support product search and comparison workflows.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Product queries and store lookups may send a ZIP code or coordinates to Scavio; the security evidence also reports incomplete reference resolution.

Mitigation: Share only the location detail needed for a store lookup, and review Scavio's privacy information before sending location data. Treat the scan as incomplete when assessing security.

## Reference(s):

- [Scavio Nordstrom Rack Product API Documentation](https://scavio.dev/docs/nordstromrack-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON API results with concise explanatory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product listings, pricing, SKU details, reviews, inventory, and store data vary by request and may change over time.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
