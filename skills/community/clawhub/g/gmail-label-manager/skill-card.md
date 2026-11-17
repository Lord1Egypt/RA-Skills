## Description:

Automatically organizes unread Gmail messages by applying relevant labels, removing unnecessary labels, and archiving messages based on patterns from archived email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coenenp](https://clawhub.ai/user/coenenp)

### License/Terms of Use:


## Use Case:

People who automate Gmail triage use this skill to classify unread messages, update labels, and archive handled messages. The artifact also supports Telegram notifications and Google Calendar event creation for selected message categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive email details can be forwarded to Telegram or written to logs.

Mitigation: Disable Telegram forwarding unless explicitly opted in, and redact email content from notifications and logs.

Risk: The script can mutate Gmail labels and archive real mailbox messages.

Mitigation: Test in a dry-run mode or limited mailbox before running against a real account.

Risk: Email-derived calendar fields can reach shell evaluation during Calendar event creation.

Mitigation: Remove eval, sanitize calendar fields, and gate Calendar writes behind explicit review or configuration.

Risk: Calendar events may be created from under-documented automated classifications.

Mitigation: Document Calendar write behavior and require explicit opt-in before enabling event creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coenenp/skills/gmail-label-manager)

## Skill Output:

**Output Type(s):** [shell commands, text, configuration]

**Output Format:** [Shell execution with text logs and external Gmail, Telegram, and Calendar effects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one unread email per run by default; may modify Gmail labels and archive state, send Telegram notifications, and create Google Calendar events.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
