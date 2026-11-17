## Description:

Analyzes Amazon item and browse node customer feedback by querying review topics, review trends, return topics, and return trends through the Customer Feedback API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers, operators, and marketplace analysts use this skill to inspect aggregated review and return feedback for ASINs or browse nodes, including topics, mention volume, star-rating impact, and trend data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security scan marks this release suspicious because it handles seller feedback data, onboarding, billing, API keys, and locally retained response files.

Mitigation: Install only when the publisher is trusted, use scoped pre-provisioned credentials, avoid shared workspaces, and delete retained LinkFox output files when they are no longer needed.

Risk: The artifact supports environment overrides for service URLs used by its scripts.

Mitigation: Prefer the default service endpoints and avoid environment URL overrides unless the replacement endpoint has been reviewed and approved.

Risk: Repeated failed SP-API calls can trigger temporary store/interface protection responses.

Mitigation: Do not retry automatically after repeated 400, 403, 404, or 429 responses; fix parameters or authorization first and respect retry timing before trying again.

## Reference(s):

- [Skill API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [Amazon Customer Feedback API v2024-06-01 Use Case Guide](https://developer-docs.amazon.com/sp-api/docs/customer-feedback-api-v2024-06-01-use-case-guide)
- [Amazon getItemReviewTopics Reference](https://developer-docs.amazon.com/sp-api/reference/getitemreviewtopics)
- [Amazon getItemBrowseNode Reference](https://developer-docs.amazon.com/sp-api/reference/getitembrowsenode)
- [Amazon getBrowseNodeReviewTopics Reference](https://developer-docs.amazon.com/sp-api/reference/getbrowsenodereviewtopics)
- [Amazon getItemReviewTrends Reference](https://developer-docs.amazon.com/sp-api/reference/getitemreviewtrends)
- [Amazon getBrowseNodeReviewTrends Reference](https://developer-docs.amazon.com/sp-api/reference/getbrowsenodereviewtrends)
- [Amazon getBrowseNodeReturnTopics Reference](https://developer-docs.amazon.com/sp-api/reference/getbrowsenodereturntopics)
- [Amazon getBrowseNodeReturnTrends Reference](https://developer-docs.amazon.com/sp-api/reference/getbrowsenodereturntrends)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full API responses under a local linkfox session data directory and may print either full JSON or a summary depending on response size.]

## Skill Version(s):

1.0.8 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
