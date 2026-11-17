## Description:

Helps agents manage GoHighLevel contacts, sales pipelines, calendars, conversations, payments, and marketing automation using an authorized Private Integration Token connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and developers use this skill to retrieve and manage GoHighLevel CRM, scheduling, sales, and marketing data through a user-authorized connection, with optional scheduled or event-driven automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad account access or unintended changes to CRM records.

Mitigation: Review each connection, grant the narrowest available token scopes, and confirm writes and deletions before execution.

Risk: Hosted functions, triggers, or destinations may create ongoing data forwarding.

Mitigation: Confirm the intended function, trigger, and destination with the user before enabling automation.

## Reference(s):

- [GoHighLevel skill listing](https://clawhub.ai/byungkyu/skills/highlevel-api)
- [Maton](https://maton.ai)
- [Related API gateway skill](https://clawhub.ai/byungkyu/api-gateway)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.2.5 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
