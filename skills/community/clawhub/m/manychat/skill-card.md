## Description:

Helps agents manage ManyChat subscribers, tags, custom fields, messages, and automations through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to look up and manage ManyChat subscribers, send messages, and configure approved automations through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account grants access to authorized ManyChat data, including personal subscriber information.

Mitigation: Obtain user approval for the connection, use only necessary permissions, and limit displayed subscriber details.

Risk: Messages, data changes, hosted functions, and triggers can act on an account or forward event data automatically.

Mitigation: Confirm each write and automation with the user; review recipients, payloads, schedules, and destinations before enabling them.

Risk: Using a raw API key where the CLI is unavailable can expose a long-lived credential.

Mitigation: Prefer CLI authentication; if a key is necessary, keep it out of logs, files, and command arguments.

## Reference(s):

- [ManyChat skill release](https://clawhub.ai/byungkyu/skills/manychat)
- [Maton](https://maton.ai)
- [ManyChat API documentation](https://api.manychat.com/swagger)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include subscriber data; show only the fields needed for the task.]

## Skill Version(s):

1.2.9 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
