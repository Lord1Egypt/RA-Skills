## Description:

Helps agents manage Kit email-marketing data and automations through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers and developers use this skill to review and manage Kit subscribers, tags, forms, sequences, broadcasts, purchases, and webhooks, with user approval before account changes or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account changes or broadcast and sequence actions can modify audiences or send email.

Mitigation: Start with read-only calls and confirm each write, broadcast, or sequence enrollment with the user.

Risk: Webhooks, triggers, or destinations can forward future subscriber and event data until removed.

Mitigation: Review event types, destination URLs, and data exposure with the user before enabling them; remove unused automations.

Risk: Connecting Kit grants Maton access to the authorized account.

Mitigation: Obtain explicit approval for the connection and use only the access needed for the task.

## Reference(s):

- [Kit skill on ClawHub](https://clawhub.ai/byungkyu/skills/kit)
- [Kit API overview](https://developers.kit.com/api-reference/overview)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-authorized Kit connection; confirm writes, broadcasts, webhooks, and automations before execution.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
