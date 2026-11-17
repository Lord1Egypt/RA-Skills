## Description:

GoToEmail binds mailbox accounts and lets agents test IMAP/SMTP access, list and read messages, and send email for 163, 126, QQ, Yahoo, Gmail app-password accounts, and custom enterprise mail servers; OAuth-only providers such as Outlook, M365, and iCloud are not supported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feixuelingcloud](https://clawhub.ai/user/feixuelingcloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to bind supported email accounts, validate mailbox connectivity, retrieve message lists and message content, and send email through IMAP/SMTP. It is most useful when a workflow needs direct mailbox operations with app passwords, authorization codes, or trusted custom mail servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful mailbox credentials and documented examples pass secrets through shell echo commands.

Mitigation: Use disposable app passwords or authorization codes where possible, avoid typing real mailbox secrets directly into shell history, and rotate credentials that may have been exposed.

Risk: The skill authenticates to user-supplied IMAP and SMTP hosts.

Mitigation: Only connect to trusted mail servers that the user intends to authenticate to, and confirm custom enterprise hostnames and ports before use.

Risk: Reading a message marks it as read by default.

Mitigation: Set mark_as_read to false when preserving unread state matters.

## Reference(s):

- [GoToEmail provider guide](references/providers.md)
- [GoToEmail ClawHub release](https://clawhub.ai/feixuelingcloud/skills/gotoemail)
- [163 Mail](https://mail.163.com)
- [QQ Mail](https://mail.qq.com)
- [Google account security](https://myaccount.google.com)
- [Yahoo account login](https://login.yahoo.com)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON inputs or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python scripts that exchange JSON through stdin and stdout; email body HTML is truncated to 5000 characters when reading a message.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
