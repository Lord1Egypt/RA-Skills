## Description:

Queries and analyzes Amazon Brand Analytics search-term data across 15 Amazon marketplaces using nearly three years of weekly data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce analysts use this skill to query ABA search-term rankings, click share, conversion share, seasonal trends, competitor keyword coverage, and market-opportunity patterns.

### Deployment Geography for Use:

Global, with documented ABA data coverage for US, DE, BR, CA, AU, JP, AE, ES, FR, IT, SA, TR, MX, SE, and NL marketplaces.

## Known Risks and Mitigations:

Risk: ABA query content, account identifiers, API keys, phone/SMS login data, and billing/order data may be sent to LinkFox services.

Mitigation: Use the skill only after reviewing the LinkFox service flow, minimize sensitive business details in queries, and share login or billing data only when needed to resolve authentication or quota issues.

Risk: API keys and endpoint override environment variables can affect where credentials and query data are sent.

Mitigation: Store API keys in session-scoped or project-scoped environments where possible, avoid global shell startup files, and do not set custom LinkFox endpoint overrides unless the endpoint is explicitly trusted.

Risk: Saved query responses, cached results, feedback reports, and downloaded CSV links can contain sensitive marketplace or business data.

Mitigation: Treat generated linkfox data directories and feedback content as sensitive, restrict access to the workspace, and review or remove saved files when they are no longer needed.

Risk: Queries and onboarding can consume paid compute credits or create payment orders.

Mitigation: Confirm user intent before additional searches, downloads, plan purchases, or order creation, and present billing or quota errors plainly before proceeding.

## Reference(s):

- [ABA Intelligent Query API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-aba-intelligent-query)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, API calls, guidance]

**Output Format:** [Markdown guidance with query tables, JSON API responses, saved JSON files, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full query responses are saved under a local linkfox session data directory; large responses may be summarized in stdout, and optional CSV download links may be requested.]

## Skill Version(s):

1.0.12 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
