## Description:

Gmail: Reply-all to a message (handles threading automatically).

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to prepare or send Gmail reply-all responses while preserving message threading. It supports recipient adjustments, attachments, HTML replies, dry-run review, and draft creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare or send reply-all messages from a configured Gmail account.

Mitigation: Use dry-run or draft mode for important threads and review the message body, recipients, and attachments before sending.

Risk: Reply-all behavior may expose a response to unintended original or added recipients.

Mitigation: Review To, CC, BCC, and removed recipients before sending, especially when using recipient adjustment flags.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-gmail-reply-all)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and a configured Gmail account.]

## Skill Version(s):

1.0.14 (source: server release metadata); 0.22.5 (source: SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
