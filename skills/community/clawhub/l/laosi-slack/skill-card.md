## Description: <br>
Slack助手 - 发送消息/搜索历史/管理频道/集成通知，基于Slack API的Python实现，支持Webhook和Socket Mode <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate Slack API guidance and Python examples for sending messages, creating notifications, managing channels, searching message history, and uploading files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Slack API actions may post messages, invite users, create channels, search history, or upload files without clear confirmation. <br>
Mitigation: Use a dedicated Slack app with only the scopes needed and require explicit confirmation before posting, inviting users, creating channels, searching history, or uploading files. <br>
Risk: Slack OAuth tokens, webhook URLs, or local file paths can expose secrets or sensitive content. <br>
Mitigation: Keep credentials out of prompts and shared files, rotate leaked tokens, and do not provide sensitive local file paths unless the file is intended to be shared in Slack. <br>


## Reference(s): <br>
- [Slack API App Management](https://api.slack.com/apps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, YAML, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Slack credentials and selected Slack API scopes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
