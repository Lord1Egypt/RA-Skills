## Description: <br>
Read and send email via IMAP/SMTP. Check for new/unread messages, fetch content, search mailboxes, mark as read/unread, and send emails with attachments. Supports multiple accounts. Works with any IMAP/SMTP server including Gmail, Outlook, 163.com, vip.163.com, 126.com, vip.126.com, 188.com, and vip.188.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arry8](https://clawhub.ai/user/arry8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent inspect, search, manage, and send email through configured IMAP and SMTP accounts. It is suited for workflows that need mailbox access, attachment handling, and outbound messages across common mail providers or custom servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access an email account that reads mail and sends real messages. <br>
Mitigation: Install only for accounts where that access is acceptable, and prefer app-specific credentials instead of primary account passwords. <br>
Risk: Default configuration and setup behavior may create credential and TLS safety concerns. <br>
Mitigation: Replace the bundled config.env with user-specific settings, keep certificate verification enabled, and ensure ~/.openclaw/.env exists with restrictive permissions before running setup. <br>
Risk: Credentials may be exposed if setup prints them because ~/.openclaw/.env is missing. <br>
Mitigation: Create ~/.openclaw/.env with owner-only permissions before setup, and rotate the email credential if it was ever printed in terminal output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arry8/imap-smtp-email-fixed) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>
- [Yahoo account security](https://login.yahoo.com/account/security) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and email operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read mailbox content, download attachments to allowed directories, and send email through configured accounts.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
