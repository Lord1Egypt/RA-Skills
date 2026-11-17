## Description:

Queries Amazon product historical time-series data for a single ASIN, including price, BSR, rating, seller-count, and monthly-sales trends across supported Amazon marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers, marketplace analysts, and developers use this skill to retrieve and interpret product-level historical trends for a specific ASIN. It is suited to price tracking, BSR trend review, fulfillment price comparison, seller-count changes, rating trends, and monthly sales history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires LinkFox account onboarding and API credentials for authenticated requests.

Mitigation: Configure credentials only through the documented LinkFox flow, treat API keys and SMS codes as secrets, and avoid exposing them in prompts or logs.

Risk: Queries may consume paid quota or trigger billing flows.

Mitigation: Review cost and payment actions before approval, and avoid repeated retries or broad probing when a request fails or returns empty data.

Risk: Full API responses are persisted locally and may contain product research data or account-session context.

Mitigation: Store outputs in an appropriate workspace, review saved response files before sharing, and delete local artifacts that are no longer needed.

Risk: Custom LINKFOX_* endpoint variables can redirect requests away from the default LinkFox services.

Mitigation: Use the default endpoints unless a trusted administrator has explicitly provided alternate endpoints for the session.

Risk: The skill includes automatic external feedback reporting behavior.

Mitigation: Review feedback content before sending and avoid including secrets, personal data, or confidential product research.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-keepa-product-series)
- [Keepa Amazon Price History API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses or summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved locally; small responses can be printed inline, while large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
