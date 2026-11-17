## Description:

Manage multiple Outlook, Microsoft 365, 163, and QQ email accounts to read, send, search, auto-reply, draft, summarize, sync, and handle attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanfan-2011](https://clawhub.ai/user/fanfan-2011)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to manage personal or work mailboxes across Outlook/Microsoft 365, 163, and QQ accounts. It supports reading, sending, searching, drafting, summarizing, scheduled syncing, attachment handling, and managed auto-reply rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can receive read, write, and send permissions for configured mailboxes.

Mitigation: Install only when that level of mailbox access is acceptable, prefer a dedicated Microsoft app registration, and revoke provider tokens or app passwords when the skill is no longer needed.

Risk: Mailbox credentials and tokens may persist locally, including plaintext fallback paths when system keyring support is unavailable.

Mitigation: Install and verify a working system keyring, keep the email-assistant data directory private and out of backups or repositories, and avoid commands that print access tokens.

Risk: Auto-reply behavior can send messages or attachments to unintended recipients, including broad catch-all matches.

Mitigation: Use dry-run previews, require explicit user consent before sending, prefer narrow sender or keyword rules, and review attachments before enabling auto-replies.

## Reference(s):

- [Microsoft Graph API Reference](references/microsoft_graph.md)
- [Email Protocols Reference](references/email_protocols.md)
- [Auto Reply Rules Reference](references/auto_reply_rules.md)
- [ClawHub Publishing Reference](references/clawhub_publishing.md)
- [ClawHub Skill Page](https://clawhub.ai/fanfan-2011/skills/mail-assistant)
- [Publisher Profile](https://clawhub.ai/user/fanfan-2011)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with Python and shell command examples, plus JSON outputs from mailbox and rule-management scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform mailbox API calls and local file updates when configured and user consent is provided for write or send operations.]

## Skill Version(s):

1.8.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
