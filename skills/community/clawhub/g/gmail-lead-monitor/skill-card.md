## Description:

Monitors a Gmail inbox for unseen messages, sends Telegram alerts with sender, subject, and snippets, and stars messages that match configured keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[themsquared](https://clawhub.ai/user/themsquared)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a Python monitor that watches Gmail for lead, order, or support messages and sends Telegram notifications while marking keyword matches in Gmail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The monitor can forward Gmail message metadata and body snippets to the configured Telegram chat for every unseen message processed, not only keyword matches.

Mitigation: Review or modify alerting behavior before use, keep the Telegram bot private, and avoid mailboxes containing sensitive personal, financial, legal, or regulated information unless forwarding is tightly controlled.

Risk: Gmail and Telegram credentials are stored in a plaintext local configuration file.

Mitigation: Use a dedicated Gmail app password, restrict config file permissions, rotate credentials if exposed, and store the config only on trusted systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/themsquared/skills/gmail-lead-monitor)
- [Google Account Security](https://myaccount.google.com/security)
- [Telegram BotFather](https://t.me/BotFather)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Python code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runnable monitor can create local config and state files and can send Gmail message metadata and body snippets to Telegram.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
