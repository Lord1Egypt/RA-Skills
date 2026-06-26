## Description: <br>
Read and send email via IMAP/SMTP, including checking unread messages, fetching content, searching mailboxes, marking messages read or unread, and sending emails with attachments across multiple accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmundi3210](https://clawhub.ai/user/tmundi3210) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate configured email accounts through standard IMAP and SMTP servers. It supports mailbox review, message search, attachment download, and outbound email workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read mailbox contents and send email from configured accounts. <br>
Mitigation: Install only for mailboxes the agent is allowed to access, and review recipients, message bodies, body files, and attachments before sending. <br>
Risk: Email credentials are stored locally for IMAP and SMTP access. <br>
Mitigation: Use provider app passwords or authorization codes instead of primary account passwords, and keep the configuration file permissions restricted. <br>
Risk: Attachment and body-file operations can read or write local files. <br>
Mitigation: Keep ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS narrowly scoped to directories intended for agent use. <br>
Risk: Disabling certificate validation can weaken transport security. <br>
Mitigation: Leave IMAP_REJECT_UNAUTHORIZED and SMTP_REJECT_UNAUTHORIZED enabled unless a trusted environment requires otherwise. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tmundi3210/imap-smtp-email-disabled-20260401-113327) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Command-line text output, configuration values, and downloaded attachment files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operations depend on configured IMAP/SMTP accounts and local read/write allowlists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
