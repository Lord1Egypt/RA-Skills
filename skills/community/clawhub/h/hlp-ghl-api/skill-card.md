## Description:

HubLinkPro GoHighLevel API skill helps agents manage contacts, pipelines, workflows, and messaging for Tri-Cities real estate lead generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbright4497](https://clawhub.ai/user/mbright4497)

### License/Terms of Use:

MIT-0

## Use Case:

External users or developers supporting HubLinkPro use this skill to generate GoHighLevel API commands for Tri-Cities Tennessee real estate lead operations, including contact management, opportunity updates, notes, workflows, and SMS messaging.

### Deployment Geography for Use:

United States (Tri-Cities, Tennessee use case)

## Known Risks and Mitigations:

Risk: Live CRM write and SMS commands can create or alter customer records, trigger workflows, or send messages without built-in approval safeguards.

Mitigation: Use least-privilege GoHighLevel API keys, separate read-only use from write and SMS actions, and require explicit human confirmation of the recipient, record, and payload before live actions.

Risk: Inline shell JSON and query parameters can be malformed if values contain quotes or special characters.

Mitigation: Harden production use with jq-built JSON payloads and proper URL encoding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mbright4497/skills/hlp-ghl-api)
- [LeadConnector API base endpoint](https://services.leadconnectorhq.com)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline curl and jq shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require GHL_API_KEY, GHL_LOCATION_ID, curl, and jq; API responses are commonly piped through jq.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
