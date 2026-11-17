## Description:

Create and manage Instantly.ai email campaigns via API for cold email campaigns, lead imports, email sequences with variables, A/B testing variants, campaign activation, and outbound email automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polzer1999](https://clawhub.ai/user/polzer1999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to have an agent create and manage Instantly.ai outbound email campaigns, including campaign setup, message sequences, lead import, custom variables, A/B variants, and activation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can import leads and activate outbound email campaigns.

Mitigation: Require explicit confirmation before importing leads, changing campaigns, or activating sends.

Risk: Lead records and email content may contain personal or sensitive business data.

Mitigation: Review lead fields, custom variables, and message content before sending them to Instantly.ai.

Risk: Broad Instantly.ai API permissions can allow wider campaign or lead changes than intended.

Mitigation: Use the narrowest available API key scopes for campaign and lead operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/polzer1999/skills/instantly-campaign-builder)
- [Instantly API base URL](https://api.instantly.ai)

## Skill Output:

**Output Type(s):** [guidance, API Calls, JSON, configuration]

**Output Format:** [Markdown with JSON request examples and API endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires INSTANTLY_API_KEY and may include campaign, sequence, lead, variable, and activation payloads.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
