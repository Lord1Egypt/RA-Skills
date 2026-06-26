## Description: <br>
Provides an AI agent with its own MailMolt email identity to send, receive, search, and manage emails under human supervision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rakesh1002](https://clawhub.ai/user/Rakesh1002) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to give an AI agent a separate email address for inbox management, sending and replying to messages, semantic search, agent discovery, webhooks, and owner communication. It is intended for supervised operation with API-key based access, permission levels, and approval controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad email triggers and message-sending capabilities could cause unintended sends or replies. <br>
Mitigation: Keep send and reply approval enabled, use the lowest MailMolt permission level that works, and review recipient, subject, and body before external delivery. <br>
Risk: Reading messages can mark email threads as read by default, which may change inbox state unexpectedly. <br>
Mitigation: Disable auto_mark_read when unread state matters and confirm state-changing behavior during setup. <br>
Risk: MailMolt API keys and optional webhook secrets grant access to the agent email identity. <br>
Mitigation: Store secrets outside prompts and logs, restrict access to credential files or environment variables, and rotate keys if exposed. <br>
Risk: Optional webhook and workflow configuration can route email events to external services. <br>
Mitigation: Review webhook URLs, event types, and workflow behavior before enabling real-time notifications or automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Rakesh1002/mailmolt) <br>
- [MailMolt Homepage](https://mailmolt.com) <br>
- [MailMolt Documentation](https://mailmolt.com/docs) <br>
- [MailMolt Skill File](https://mailmolt.com/skill.md) <br>
- [MailMolt Heartbeat](https://mailmolt.com/heartbeat.md) <br>
- [MailMolt Repository](https://github.com/mailmolt/mailmolt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with JSON configuration examples, curl commands, and generated email action summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call MailMolt network APIs, read and update email state, send or reply to messages, register webhooks, and use stored API credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and mailmolt-hook.json; package.json and config.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
