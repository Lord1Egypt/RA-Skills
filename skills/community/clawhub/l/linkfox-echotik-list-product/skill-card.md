## Description:

Searches and analyzes TikTok Shop product data across supported marketplaces, including sales, GMV, pricing, ratings, commission rates, and influencer promotion signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketers, and product researchers use this skill to find and compare TikTok Shop products by marketplace, sales performance, GMV, price, rating, commission, and influencer promotion activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a LinkFox API key and account flows for authentication, billing, and feedback.

Mitigation: Use a dedicated secret manager or environment variable for credentials, avoid printing API keys into logs, and review account and billing actions before running onboarding commands.

Risk: Product research responses and cached results may contain sensitive commercial research data.

Mitigation: Review and delete the local linkfox response cache and saved JSON files when the research data should not persist in the workspace.

Risk: Endpoint override environment variables can redirect requests away from the default LinkFox services.

Mitigation: Use endpoint override variables only in controlled test environments.

Risk: The server security verdict is suspicious because the skill handles credentials, payments, local storage, and silent feedback reporting.

Mitigation: Install only after reviewing the security summary and confirming that these behaviors are acceptable for the intended agent environment.

## Reference(s):

- [EchoTik API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-echotik-list-product)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON API responses, command examples, and tabular summaries of product search results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved as JSON data files in the local linkfox workspace; large responses are summarized in stdout, and repeated parameter combinations may use a 24-hour local cache.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
