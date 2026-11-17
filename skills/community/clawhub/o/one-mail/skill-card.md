## Description:

one-mail is a command-line skill for managing Gmail, Outlook, and NetEase 163/126 mail accounts from a single interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangbaixun](https://clawhub.ai/user/huangbaixun)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use one-mail to let an agent configure supported mail accounts, fetch, read, and search messages, send mail with optional attachments, and report mailbox statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provided security evidence reports serious command-injection risk in the current implementation.

Mitigation: Patch the eval and Python interpolation issues before using real mailboxes, and run only with trusted inputs until the fixes are reviewed.

Risk: Mailbox credentials, app passwords, client secrets, and refresh tokens are stored locally under ~/.onemail/credentials.json.

Mitigation: Use the skill only on a trusted machine, keep credentials file permissions restricted, prefer revocable OAuth tokens or app-specific passwords, and rotate or revoke secrets after testing.

Risk: Email sending, attachments, and unattended mailbox automation can expose data or send unintended messages.

Mitigation: Verify recipients, message content, and attachment paths before sending, and avoid unattended forwarding or cron jobs until the skill has been reviewed and patched.

## Reference(s):

- [Troubleshooting Guide](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/huangbaixun/skills/one-mail)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, text, guidance]

**Output Format:** [CLI output, JSON email records, and Markdown-style command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local provider credentials and account configuration before mailbox operations can run.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
