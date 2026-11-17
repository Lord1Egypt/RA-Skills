## Description:

HERA Mail is an internal email system for HERA agents to send, receive, read, and manage direct messages with optional file attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzr818181](https://clawhub.ai/user/wzr818181)

### License/Terms of Use:

MIT-0

## Use Case:

HERA agents and developers use this skill to coordinate multi-agent work by listing inboxes, reading messages, sending direct messages, and sharing attachments inside a HERA workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox file paths can be abused to read outside the intended mailbox if callers are not trusted.

Mitigation: Use only in a controlled HERA workspace and require path containment and safe filename validation before broader deployment.

Risk: Messages can impersonate other agents because sender identity is provided by command-line input.

Mitigation: Restrict callers to trusted agents and add sender authentication before relying on the skill for multi-agent workflows.

Risk: Attachments may copy sensitive local files into agent mailboxes.

Mitigation: Avoid sending secrets or sensitive files as attachments and define retention guidance for mailbox and attachment storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzr818181/skills/hera-mail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal text with Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads mailbox files and optional attachment copies inside the configured HERA workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
