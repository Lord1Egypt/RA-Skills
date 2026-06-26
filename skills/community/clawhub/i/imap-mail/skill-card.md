## Description: <br>
Imap Mail lets an agent send, read, search, organize, schedule, and receive push notifications for email through a user-configured IMAP/SMTP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polumish](https://clawhub.ai/user/polumish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent to a personal or service mailbox over standard IMAP/SMTP for inbox triage, search, sending replies, folder management, scheduled sends, and local push notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad mailbox actions, including sending, deleting, moving, marking, scheduling, and rule-driven changes. <br>
Mitigation: Review before installing, keep the API bound to 127.0.0.1, and confirm that persistent rules, scheduled sends, contact notes, and automated mailbox changes are acceptable before enabling the service. <br>
Risk: Configured IMAP IDLE webhooks can forward full message contents to the webhook URL. <br>
Mitigation: Avoid setting MAIL_IDLE_WEBHOOK unless the endpoint is trusted and preferably local. <br>
Risk: Saving attachments may overwrite files when filenames are not sanitized. <br>
Mitigation: Use --save-attachments only with a controlled destination and remain cautious until filenames are sanitized. <br>
Risk: Mailbox credentials are stored in a local environment file. <br>
Mitigation: Use an app-specific mail password and lock down the env file permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/polumish/imap-mail) <br>
- [Full API reference](references/api.md) <br>
- [Systemd service setup](references/systemd.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local API JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 with fastapi and uvicorn, plus user-provided IMAP/SMTP credentials.] <br>

## Skill Version(s): <br>
1.5.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
