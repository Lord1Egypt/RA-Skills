## Description: <br>
Read and send email via IMAP/SMTP. Check for new/unread messages, fetch content, search mailboxes, mark as read/unread, and send emails with attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gzlicanyi](https://clawhub.ai/user/gzlicanyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure IMAP/SMTP accounts, inspect mailbox state, retrieve messages and attachments, update read status, and send email through supported providers or custom mail servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles mailbox credentials and message data. <br>
Mitigation: Use app passwords or provider authorization codes when available, and avoid sharing primary account passwords. <br>
Risk: The skill can send real email, including during the SMTP test command. <br>
Mitigation: Confirm the configured account and recipients before sending or testing SMTP. <br>
Risk: Attachment and body-file operations can access local files inside configured directories. <br>
Mitigation: Keep ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS limited to the minimum directories needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gzlicanyi/imap-smtp-email) <br>
- [Publisher profile](https://clawhub.ai/user/gzlicanyi) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands; command results are plain text summaries and downloaded attachment files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read mailbox content, send messages, and download attachments within configured allowlisted directories.] <br>

## Skill Version(s): <br>
0.0.16 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
