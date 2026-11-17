## Description:

Send plain-text emails using your local msmtp config (Gmail app password already set up in ~/.msmtprc). Strictly send-only; no reading, fetching, or inbox access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[izombix](https://clawhub.ai/user/izombix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to send short plain-text notifications, test messages, and alerts to known recipients through a local msmtp configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send email from the user's configured msmtp account without a built-in confirmation step.

Mitigation: Use it only for intentional messages to trusted recipients, and review the recipient, subject, and body before execution.

Risk: The local msmtp configuration may contain account credentials, and email content may include sensitive information.

Mitigation: Harden ~/.msmtprc permissions and avoid sending sensitive content unless the message and recipient have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/izombix/skills/msmtp-send)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [Google app passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, Guidance]

**Output Format:** [Plain text email sent through a local shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires msmtp and an existing ~/.msmtprc configuration; supports send-only plain-text messages without attachments, HTML, inbox access, or message retrieval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
