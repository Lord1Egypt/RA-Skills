## Description: <br>
Read and send email via IMAP/SMTP. Check for new/unread messages, fetch content, search mailboxes, mark as read/unread, and send emails with attachments. Works with any IMAP/SMTP server including Gmail, Outlook, 163.com, vip.163.com, 126.com, vip.126.com, 188.com, and vip.188.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lRoccoon](https://clawhub.ai/user/lRoccoon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and users configure this skill to let an agent read, search, move, mark, and send mail through a configured IMAP/SMTP account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured account grants broad mailbox authority, including reading, searching, moving, marking, downloading attachments, and sending mail. <br>
Mitigation: Use a dedicated mailbox or app password, protect credentials, and review recipients, mailbox operations, and attachment paths before execution. <br>
Risk: Attachment downloads can write files from email content to a chosen directory. <br>
Mitigation: Download attachments only from trusted messages, sanitize filenames, and confine writes to an intended directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lRoccoon/imap-smtp-email-plus) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, mutate, download from, and send mail for the configured account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
