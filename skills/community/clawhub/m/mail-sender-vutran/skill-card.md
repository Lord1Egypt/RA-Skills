## Description:

Send emails via SMTP with a custom subject and body using configured SMTP server credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaskies](https://clawhub.ai/user/jaskies)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they need an agent to send a plain-text email through a configured SMTP account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP credentials can be exposed if a password is supplied as a command-line argument or pasted into conversation history.

Mitigation: Provide SMTP_PASS through a protected environment variable or secret manager, use a provider-specific app password with limited scope, and rotate any exposed credential.

Risk: The skill sends email through the configured account, so incorrect recipient, subject, or body values can result in unintended outbound messages.

Mitigation: Review recipient and message fields before execution and use an SMTP account scoped for the intended sending workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaskies/skills/mail-sender-vutran)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and plain-text send status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SMTP server, port, username, password, sender, recipient, subject, and body values.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
