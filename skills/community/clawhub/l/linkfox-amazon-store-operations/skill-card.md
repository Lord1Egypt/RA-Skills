## Description:

A LinkFox Amazon SP-API operations toolkit for store authorization, orders, listings, pricing, catalog lookup, reports, feeds, customer feedback, uploads, A+ Content, External Fulfillment, and FBA workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, e-commerce operators, and developers use this skill to run Amazon seller operations through LinkFox-backed SP-API workflows, including authorization, reporting, catalog/listing management, pricing checks, feed uploads, shipment actions, customer feedback analysis, and FBA tasks.

### Deployment Geography for Use:

Global, subject to supported Amazon marketplaces and matching SP-API authorization regions.

## Known Risks and Mitigations:

Risk: Amazon seller credentials, tokens, reports, and operational data may be exposed if the workspace, endpoint configuration, or inline output is mishandled.

Mitigation: Install only in a trusted workspace, use official trusted HTTPS LinkFox endpoints, avoid inline output for sensitive results, and keep credentials out of shared logs.

Risk: Write, delete, upload, shipment, feed, listing, A+ Content, External Fulfillment, and FBA operations can change live seller data or trigger operational actions.

Mitigation: Confirm the seller, region, marketplace, SKU, ASIN, file path, report type, feed type, and request body before executing any state-changing script.

Risk: Downloaded reports and local HTTP download links can expose sensitive seller data if served too broadly or retained longer than necessary.

Mitigation: Keep report serving bound to 127.0.0.1 or disable it, limit serving duration, and remove downloaded report files when they are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-operations)
- [Quick Start](references/quick-start.md)
- [Authorization Flow](references/authorization-flow.md)
- [Amazon Store Auth](references/linkfox-amazon-store-auth.md)
- [Orders](references/linkfox-amazon-store-orders.md)
- [Listings](references/linkfox-amazon-store-listings.md)
- [Pricing](references/linkfox-amazon-store-pricing.md)
- [Catalog](references/linkfox-amazon-store-catalog.md)
- [Reports](references/linkfox-amazon-store-report.md)
- [Feeds](references/linkfox-amazon-store-feeds.md)
- [Customer Feedback](references/linkfox-amazon-store-customer-feedback.md)
- [Uploads](references/linkfox-amazon-store-uploads.md)
- [A+ Content](references/linkfox-amazon-store-aplus-content.md)
- [External Fulfillment](references/linkfox-amazon-store-external-fulfillment.md)
- [FBA](references/linkfox-amazon-store-fba.md)
- [Report Types](references/report-types.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files, API calls]

**Output Format:** [Markdown guidance, shell commands, JSON parameters, saved JSON result files, and concise API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LinkFox API key configuration and Amazon store authorization before most SP-API operations.]

## Skill Version(s):

1.2.3 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
