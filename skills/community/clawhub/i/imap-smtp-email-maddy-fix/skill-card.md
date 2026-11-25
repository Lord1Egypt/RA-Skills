## Description:

Read and send email via IMAP/SMTP. Check for new/unread messages, fetch content, search mailboxes, mark as read/unread, create mailboxes, copy or move messages between mailboxes, and send emails with attachments. Supports multiple accounts and servers without the IMAP ID extension, such as Maddy. Passwords can be Passbolt references, which it fetches by running the local passbolt CLI. Works with any IMAP/SMTP server including Gmail, Outlook, 163.com, vip.163.com, 126.com, vip.126.com, 188.com, and vip.188.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[troioi-vn](https://clawhub.ai/user/troioi-vn)

### License/Terms of Use:

MIT No Attribution

## Use Case:

People who manage email through an agent can use this skill to read, search, organize and send messages across IMAP and SMTP accounts, including downloading attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Three of eight components were only partially inspected, leaving some behavior unresolved.

Mitigation: Review all skill scripts and setup steps before installing or using the skill.

Risk: Dependency version ranges and the lockfile's trust and use during installation remain unresolved in the security assessment.

Mitigation: Review the dependency lockfile and install dependencies from a trusted source.

Risk: The skill can read mailbox contents, send messages, and download attachments using configured account credentials.

Mitigation: Limit configured accounts and file-access directories, protect the credentials, and review recipients and attachments before sending or downloading. Keep TLS certificate verification enabled.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/troioi-vn/skills/imap-smtp-email-maddy-fix)
- [Google Account App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [Text, Email content, Mailbox results, Email messages]

**Output Format:** [Plain text email content and command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include email attachments when requested.]

## Skill Version(s):

0.0.20 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
