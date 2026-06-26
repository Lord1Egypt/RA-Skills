## Description: <br>
Read and send email via IMAP/SMTP, including checking unread messages, fetching content, searching mailboxes, marking messages read or unread, and sending email with attachments across multiple accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[troioi-vn](https://clawhub.ai/user/troioi-vn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to standard IMAP and SMTP mail servers for mailbox lookup, message retrieval, attachment download, and outbound email workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access real mailbox contents and send email through configured accounts. <br>
Mitigation: Use a dedicated app password or provider authorization code and configure only accounts that are appropriate for agent access. <br>
Risk: Stored IMAP and SMTP credentials may expose mailbox access if the local configuration is mishandled. <br>
Mitigation: Store credentials in the configured user-level environment file, avoid main account passwords, and rotate credentials if the environment is shared or compromised. <br>
Risk: Email attachments and file-backed message content can expose local files or introduce untrusted downloaded content. <br>
Mitigation: Keep ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS narrow, review outgoing attachments before sending, and treat downloaded attachments as untrusted files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/troioi-vn/imap-smtp-email-maddy-fix) <br>
- [Publisher profile](https://clawhub.ai/user/troioi-vn) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell command examples and CLI JSON/text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read mailbox contents, send email, and write downloaded attachments only within configured account and directory settings.] <br>

## Skill Version(s): <br>
0.0.14 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
