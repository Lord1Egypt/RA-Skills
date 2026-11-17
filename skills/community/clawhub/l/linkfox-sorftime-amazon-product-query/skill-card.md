## Description:

This skill helps agents search and filter Sorftime Amazon product data across 14 marketplaces for product discovery, competitor research, brand or seller analysis, and historical snapshot comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers, ecommerce analysts, and agent users use this skill to discover and compare products by category, brand, seller, ASIN similarity, price, sales, ratings, fulfillment, seasonality, and historical month snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkFox/Sorftime receives product-search requests and may receive phone-authentication and payment-related data during onboarding.

Mitigation: Disclose the third-party data flow before use and obtain explicit user consent before authentication, payment, or account setup steps.

Risk: API keys and authentication tokens can be exposed through logs, shell history, or shared output.

Mitigation: Use environment variables for credentials, avoid pasting secrets into shared logs or transcripts, and rotate credentials if exposure is suspected.

Risk: The onboarding flow can list plans and create payment orders.

Mitigation: Require explicit user approval before creating any payment order, and show plan, method, and cost information before proceeding.

Risk: The search script persists full API responses under LinkFox session directories.

Mitigation: Review stored files before sharing the workspace and remove response files that contain sensitive commercial, account, or research data.

Risk: Custom endpoint environment variables can redirect requests to non-default services.

Mitigation: Use default endpoints unless the requester has verified and approved the custom endpoint.

Risk: The skill can submit feedback about user experience or results to a LinkFox feedback endpoint.

Mitigation: Get explicit consent before submitting feedback that includes user intent, comments, or result quality details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-sorftime-amazon-product-query)
- [Sorftime API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON files]

**Output Format:** [Markdown guidance with JSON API parameters, shell command examples, and saved JSON response files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The product-search script stores full responses in a LinkFox session data directory, uses a 24-hour cache for repeated parameter sets, and may print either full JSON or a compact summary depending on response size.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
