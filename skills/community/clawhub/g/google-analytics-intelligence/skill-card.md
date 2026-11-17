## Description:

Analyze GA4 data, detect traffic anomalies, and generate actionable growth recommendations. Use when the user needs revenue tracking, anomaly detection, or traffic optimization insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, SaaS founders, e-commerce managers, and growth analysts use this skill to turn GA4 property data into traffic anomaly checks, revenue tracking summaries, and growth recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GA4 credentials or property data could be exposed through broad agent access or generated analytics reports.

Mitigation: Use least-privilege GA4 credentials and grant access only to properties the agent needs.

Risk: Slack delivery can disclose revenue or customer-behavior summaries to unintended audiences.

Mitigation: Keep the Slack webhook private, send reports only to restricted channels, and review generated summaries before broad sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/google-analytics-intelligence)
- [Google Analytics 4](https://analytics.google.com)
- [Google Cloud Console](https://console.cloud.google.com)
- [Slack API](https://api.slack.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain text reports with metrics, anomaly summaries, recommendations, and Slack-ready alert text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference GA4 credentials, property IDs, report time windows, anomaly sensitivity, currency, timezone, and optional Slack delivery settings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
