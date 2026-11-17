## Description:

Answers questions about website traffic from Google Analytics 4, including top pages, traffic sources, recent changes, and live activity, using read-only Google Analytics API access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anatoli-iliev](https://clawhub.ai/user/anatoli-iliev)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and developers use this skill to let an agent answer natural-language GA4 traffic questions, run preset or custom read-only reports, help diagnose setup, and summarize returned rows in the conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A credential with broad GA4 access can expose every Analytics property that identity can read.

Mitigation: Use a dedicated Google service account with Viewer access only on the specific GA4 properties intended for this skill.

Risk: Ambient personal gcloud credentials may grant broader Analytics access than expected.

Mitigation: Prefer the dedicated service-account credential path and use personal gcloud credentials only when the broader access tradeoff is understood.

Risk: Enabling the audit log creates a local record of report requests.

Mitigation: Set GA4_AUDIT_LOG only when a local request audit trail is needed, and store the log according to the user's data-handling requirements.

Risk: GA4 dimension values can contain visitor-authored text that may be misleading if treated as instructions.

Mitigation: Keep report rows framed as data, preserve redaction by default, and require human review before using GA4 strings to trigger actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anatoli-iliev/skills/open-ga4)
- [Publisher Profile](https://clawhub.ai/user/anatoli-iliev)
- [Project Homepage](https://github.com/anatoli-iliev/open-ga4)
- [Setup Guide](SETUP.md)
- [Privacy Behavior](PRIVACY.md)
- [Security Policy](SECURITY.md)
- [Design Notes](docs/DESIGN.md)
- [Google Analytics](https://analytics.google.com/analytics/web/)
- [Google Cloud Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
- [Google Analytics Data API](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com)
- [Google Analytics Admin API](https://console.cloud.google.com/apis/library/analyticsadmin.googleapis.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries with inline shell commands, Markdown tables, and JSON setup diagnostics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on read-only GA4 API responses; report dimension values are redacted by default before being shown to the agent.]

## Skill Version(s):

0.2.1 (source: frontmatter, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
