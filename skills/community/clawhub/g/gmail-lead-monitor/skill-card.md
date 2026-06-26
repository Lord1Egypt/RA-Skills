## Description: <br>
Monitor a Gmail inbox for new emails matching keywords and send real-time Telegram alerts while starring important messages in Gmail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[themsquared](https://clawhub.ai/user/themsquared) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and small teams can use this skill to configure an agent-assisted Gmail monitoring workflow that detects lead, order, or support-related messages and sends Telegram notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email subjects and body snippets may be forwarded to Telegram, exposing mailbox content beyond the Gmail account. <br>
Mitigation: Use a dedicated private Telegram bot and chat, restrict the monitored mailbox to content suitable for forwarding, and consider removing snippets or alerting only on keyword-matching messages. <br>
Risk: The local configuration stores a Gmail app password and Telegram bot token in plaintext. <br>
Mitigation: Protect the configuration file with restrictive filesystem permissions, use a dedicated Gmail app password, and rotate credentials if the host or file may have been exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/themsquared/gmail-lead-monitor) <br>
- [Google Account security](https://myaccount.google.com/security) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance and runnable local monitoring code that connects Gmail IMAP to Telegram alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
