## Description:

Gmail: Reply to a message (handles threading automatically).

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to compose Gmail replies by message ID, optionally adding recipients, aliases, HTML content, attachments, or saving the response as a draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send email replies and attachments through the configured Gmail account.

Mitigation: Confirm the Gmail account and trust the gws CLI before use; prefer --dry-run or --draft for sensitive replies.

Risk: Replies may include unintended recipients, aliases, HTML content, or attachments.

Mitigation: Review recipients, sender alias, message body, HTML rendering, and attachments before sending.

## Reference(s):

- [Gws Gmail Reply on ClawHub](https://clawhub.ai/googleworkspace-bot/skills/gws-gmail-reply)
- [googleworkspace-bot Publisher Profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command option guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Gmail reply commands that send immediately, save drafts, run dry-runs, or include recipients, aliases, HTML, and attachments.]

## Skill Version(s):

1.0.14 (source: server release metadata; source skill metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
