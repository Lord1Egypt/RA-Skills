## Description:

Mailbox helps agents read, search, send, and manage email across Gmail, QQ, 163, Outlook, and IMAP/SMTP accounts through the mailbox command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Mailbox when an assistant needs to inspect, search, triage, send, or clean up messages across configured email accounts while preserving machine-readable JSON responses and dry-run safeguards for mutations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing the mailbox CLI through a remote shell installer.

Mitigation: Prefer a pinned release with checksum or signature verification before installation.

Risk: Mailbox credentials and cached email data are sensitive and may persist on disk or in a background daemon.

Mitigation: Use app-specific credentials, restrict permissions on ~/.config/mailbox/auth.json, and install the daemon only when persistent mailbox sync is intended.

Risk: Email sending, deletion, marking, moving, and cleanup can change user mailbox state.

Mitigation: Keep destructive operations in dry-run mode until the user explicitly approves and the command includes the required confirmation flag.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leeguooooo/skills/mailbox)
- [Server-Resolved GitHub Source](https://github.com/leeguooooo/Mailbox/tree/main/skills/mailbox)
- [Project Homepage](https://github.com/leeguooooo/Mailbox)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to request JSON output, check success fields, and require confirmation before mutating mailbox state.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
