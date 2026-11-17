## Description:

This skill lets agents query Kuaidi100 for courier tracking, carrier identification, shipping price estimates, and delivery time estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuaidi100-api](https://clawhub.ai/user/kuaidi100-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer package-tracking questions and estimate shipment price or delivery time through Kuaidi100.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send tracking numbers, phone numbers, sender and recipient addresses, logistics history, and API-key-backed requests to Kuaidi100.

Mitigation: Use the skill only when sharing shipment data with Kuaidi100 is acceptable, and prefer a narrowly scoped API key that can be rotated.

Risk: Broad activation language may trigger courier lookups from ambiguous package-related messages.

Mitigation: Confirm user intent before invoking the skill when a message is ambiguous or may contain sensitive shipment data.

Risk: A configured API key may be exposed through misuse or overly broad deployment access.

Mitigation: Store the key in controlled configuration or environment settings, rotate it when needed, and avoid sharing logs that may contain request details.

## Reference(s):

- [Kuaidi100 API Platform](https://api.kuaidi100.com)
- [ClawHub Skill Page](https://clawhub.ai/kuaidi100-api/skills/kuaidi100-skill)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text returned from Kuaidi100 lookups, with Node.js command invocations and configuration guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use config.json or KUAIDI100_API_KEY for an API key; some carrier lookups require a phone number.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
