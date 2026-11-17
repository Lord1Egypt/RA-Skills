## Description:

Send emails via Mailgun API for newsletters, notifications, alerts, and automated reports using configured Mailgun credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manifoldor](https://clawhub.ai/user/manifoldor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send transactional or operational emails through Mailgun from an agent workflow. Typical tasks include alerts, reports, confirmations, newsletters, and scheduled reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The credential-file fallback can execute local shell code if ~/.config/mailgun/credentials is untrusted, writable by others, or replaced with a symlink.

Mitigation: Prefer environment variables or a non-executable config format; only use the credential file when it is trusted, user-owned, non-symlinked, and locked down.

Risk: The skill sends outbound email, so mistakes in recipient, sender, or message content can leak information or send unintended mail.

Mitigation: Confirm the resolved recipient and sender before use, use a narrowly scoped Mailgun sending key, and avoid sensitive content unless sending is intentional.

## Reference(s):

- [Mailgun Documentation](https://documentation.mailgun.com/)
- [Mailgun API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/manifoldor/skills/mailgun)
- [Project Homepage](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Mailgun API key, domain, sender, and recipient configuration.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence, released 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
