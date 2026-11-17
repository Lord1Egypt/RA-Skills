## Description:

Research luxury resale listings, sold comparables, condition, and seller signals across specialist marketplaces for sourcing and evidence comparison, not buying or appraisal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers, sourcing teams, and resale researchers compare public luxury-fashion and watch listings, sold evidence where available, and seller or condition signals without treating asking prices as completed sales.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketplace searches, listing URLs, seller identifiers, and product interests are sent to Crawlora.

Mitigation: Use the skill only when sharing those research details with Crawlora is acceptable; avoid confidential sourcing strategies.

Risk: Listings and seller or condition labels may be mistaken for verified sales, authenticity, or appraisal evidence.

Mitigation: Separate asking prices from documented sales, identify source-stated claims, and leave unavailable costs or sale details unestimated.

## Reference(s):

- [Luxury Resale Research on ClawHub](https://clawhub.ai/crawlora-org/skills/luxury-resale-research)
- [Endpoint reference](artifact/reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Comparison table or JSON list with separate active-ask and sold-evidence summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Listing source and retrieval time, price and currency, condition and seller signals, sale date when available, and explicit gaps for unsupported fields.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
