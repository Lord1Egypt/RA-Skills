## Description:

Queries and analyzes recent Google Trends hot searches for a selected time window and supported country or region.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agents use this skill to discover recent Google search trends, breakout queries, and regional hot topics across supported markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trend queries, session metadata, and feedback content may be sent to LinkFox services.

Mitigation: Install only when this data sharing is acceptable, and avoid including sensitive or unnecessary information in queries or feedback.

Risk: The skill supports account login, API-key issuance, and payment-order creation.

Mitigation: Use the self-service LinkFox website for credentials when possible, do not share SMS codes unnecessarily, and confirm billing choices before creating an order.

Risk: API keys may be exposed if stored carelessly in shell profiles or logs.

Mitigation: Store credentials in the recommended environment variable only in trusted environments, avoid printing keys, and rotate credentials if exposure is suspected.

Risk: LINKFOX_* endpoint environment variables can redirect requests if controlled by another party.

Mitigation: Run the skill only where endpoint environment variables are trusted and review those variables before use.

## Reference(s):

- [API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-google-trend-get-trend-by-time)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown summaries, tables, JSON responses, and shell commands for API and onboarding workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trend calls save the full JSON response to a local linkfox session data file; small responses may also print in full, and large responses print a summary unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
