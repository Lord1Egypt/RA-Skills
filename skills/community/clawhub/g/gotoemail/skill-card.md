## Description: <br>
绑定邮箱账户并管理邮件，支持 163、126、QQ、Yahoo、Gmail 和自定义企业邮箱的 IMAP/SMTP 配置，不支持需要 OAuth 的 Outlook、M365 或 iCloud 邮箱。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feixuelingcloud](https://clawhub.ai/user/feixuelingcloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and agents use this skill to bind a mailbox, test IMAP/SMTP connectivity, list and read messages, and send email through supported providers. It is most relevant when mail access can be delegated through revocable app passwords or provider-specific authorization codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles mailbox credentials and can read and send mail. <br>
Mitigation: Use revocable app passwords or mail-specific authorization codes where possible, avoid primary corporate mailbox passwords unless approved, and confirm each read or send action before execution. <br>
Risk: Reading a message can mark it as read by default. <br>
Mitigation: Set mark_as_read to false when preserving unread state matters. <br>
Risk: Mailbox configuration or credentials may remain available to the host after binding. <br>
Mitigation: Verify where saved mailbox credentials can be deleted or revoked, and rotate or revoke app passwords after use. <br>


## Reference(s): <br>
- [GoToEmail provider reference](references/providers.md) <br>
- [ClawHub release page](https://clawhub.ai/feixuelingcloud/gotoemail) <br>
- [Publisher profile](https://clawhub.ai/user/feixuelingcloud) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing guidance invokes Python scripts that read JSON from stdin and return JSON status, mailbox metadata, message content, or send results.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
