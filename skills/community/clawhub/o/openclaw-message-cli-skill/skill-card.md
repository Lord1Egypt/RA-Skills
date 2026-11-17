## Description:

Use when the user explicitly wants to send outbound messages with the OpenClaw CLI rather than built-in tools, especially for `openclaw message send` commands with a specific channel, target, and message body.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoustc](https://clawhub.ai/user/leoustc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill when they explicitly need an agent to provide OpenClaw CLI message-send command guidance for a selected channel, target, and message body. It is scoped to outbound client delivery with the OpenClaw CLI, not normal in-session replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound messages can reach external people or services.

Mitigation: Confirm the recipient, channel, and message content before sending.

Risk: Shell-sensitive characters in message text can change command behavior if quoted incorrectly.

Mitigation: Quote message text safely before running or sharing the OpenClaw CLI command.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
