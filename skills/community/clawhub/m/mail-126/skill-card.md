## Description: <br>
126.com 网易邮箱管理 CLI，支持收取、发送、搜索、管理和统计邮件，并以 JSON 格式返回命令结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slamw](https://clawhub.ai/user/slamw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage a configured 126.com mailbox from the command line, including reading, sending, searching, organizing, downloading attachments, and generating mailbox statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants continuing access to read, send, reply, forward, move, download, and permanently delete mail from the configured 126.com mailbox. <br>
Mitigation: Use a dedicated mailbox or app-specific authorization code, limit which agents can invoke the skill, and review mailbox actions before execution. <br>
Risk: Mailbox credentials are stored in ~/mail126_data/config.json with only Base64 encoding. <br>
Mitigation: Restrict filesystem permissions on the config file, remove it when the skill is not in active use, and rotate the authorization code if exposure is suspected. <br>
Risk: Sending, forwarding, attachment download, and permanent deletion can expose data or cause irreversible mailbox changes. <br>
Mitigation: Require manual confirmation for outbound messages, downloads, moves, and delete operations, especially in scheduled or cross-skill workflows. <br>


## Reference(s): <br>
- [Mail-126 data schema](references/data-schema.md) <br>
- [ClawHub release page](https://clawhub.ai/slamw/mail-126) <br>
- [Publisher profile](https://clawhub.ai/user/slamw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [JSON command responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are non-interactive and return status, data, and message fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
