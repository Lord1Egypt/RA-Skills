## Description: <br>
Read and send email via IMAP/SMTP, including checking, fetching, searching, changing read state, and sending messages with attachments on standard IMAP/SMTP servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welderjustin](https://clawhub.ai/user/welderjustin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect mailbox contents, download email attachments, manage read state, and send SMTP messages from a configured account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores mailbox credentials locally and can access the configured mailbox. <br>
Mitigation: Install only for publishers you trust, prefer a dedicated mailbox or revocable app password, and do not commit the .env file. <br>
Risk: The skill can send email, download attachments, and change read or unread state. <br>
Mitigation: Require human review before sending messages, attaching files, downloading attachments, or changing message state. <br>
Risk: Attachment and file-body operations can read from or write to local paths. <br>
Mitigation: Keep ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS limited to the minimum directories needed. <br>
Risk: The setup flow tests SMTP by sending a message to the configured account. <br>
Mitigation: Run setup only when a test email is acceptable and review the resulting configuration before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/welderjustin/imap-smtp-email-disabled) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [JSON CLI output, setup/configuration guidance, shell commands, and downloaded attachment files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMAP and SMTP credentials plus explicit read/write directory allowlists for file access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
