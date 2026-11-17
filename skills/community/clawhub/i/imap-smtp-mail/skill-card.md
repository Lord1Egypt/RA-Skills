## Description:

Read and send email via IMAP/SMTP using local Node scripts for inbox checks, message search and fetch, attachment handling, approval-based outbound mail, and optional inbox watching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xvespertine](https://clawhub.ai/user/0xvespertine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect configured mailboxes, retrieve email content and attachments, prepare replies, and send approved outbound email through standard IMAP and SMTP providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional inbox watcher can expose raw mailbox credentials to a spawned OpenClaw process.

Mitigation: Enable the watcher only in trusted local environments and prefer app-specific mailbox passwords.

Risk: Mailbox attachments and outbound attachments involve local file reads and writes.

Mitigation: Keep ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS narrowly scoped, and avoid symlinks in those directories.

Risk: SMTP test and approved send commands transmit real email.

Mitigation: Use the draft preview flow and require explicit user approval before sending.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xvespertine/skills/imap-smtp-mail)
- [Google Account App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, json]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outbound sending requires explicit approval; attachment parsing is limited by file type and size.]

## Skill Version(s):

1.0.4 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
