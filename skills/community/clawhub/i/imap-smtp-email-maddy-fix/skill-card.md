## Description:

Read and send email via IMAP/SMTP, including checking messages, fetching content, searching mailboxes, marking messages read or unread, downloading attachments, and sending email with attachments across multiple accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[troioi-vn](https://clawhub.ai/user/troioi-vn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to let an agent inspect, search, manage, and send email through configured IMAP and SMTP accounts. It is useful for workflows that need mailbox triage, message lookup, attachment handling, or outbound email from a local CLI-backed skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured accounts grant mailbox read access and send-as-email authority.

Mitigation: Use app passwords or provider authorization codes where available, dedicate the mailbox or account scope to the intended workflow, and rotate credentials if the skill is removed or no longer needed.

Risk: Attachment download and message-body file reads can expose or write local files when broad directories are allowed.

Mitigation: Set ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS to the narrowest practical directories and avoid directories writable by unrelated processes.

Risk: Setup resolves npm dependencies before the skill runs.

Mitigation: Review the dependency set and lock or audit npm resolution in the target environment before running setup for sensitive accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/troioi-vn/skills/imap-smtp-email-maddy-fix)
- [Publisher profile](https://clawhub.ai/user/troioi-vn)
- [Gmail App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Node.js/npm and configured IMAP/SMTP credentials; mailbox reads, message changes, attachment downloads, and outbound sends occur through the configured accounts.]

## Skill Version(s):

0.0.14 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
