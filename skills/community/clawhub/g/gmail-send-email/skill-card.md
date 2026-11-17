## Description:

Atomic node skill to send an email via Gmail using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to send Gmail messages through the gog CLI when a task requires emailing one or more recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email recipient, subject, or body text could be unsafe if hostile content is interpolated into a shell command.

Mitigation: Pass gog arguments as a structured argument array with shell execution disabled, validate recipients and message content, and require confirmation before sending.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zvirb/skills/gmail-send-email)

## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [Terminal command invocation and plain-text send confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog binary and configured Gmail access.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
