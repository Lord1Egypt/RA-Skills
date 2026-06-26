## Description: <br>
Huo15 Wecom Plugin connects OpenClaw agents to WeCom through Bot WebSocket, Bot Webhook, Agent app, and customer-service channels, with multi-account routing, encrypted media handling, document and calendar tools, MCP integration, and outbound messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and administrators use this skill to connect OpenClaw agents with enterprise WeCom messaging, customer-service, media, document, calendar, and multi-account workflows. It is intended for WeCom, not personal WeChat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill gives agents broad company-chat, document, calendar, account, and local-file powers. <br>
Mitigation: Review the skill before installation, use least-privilege WeCom apps and secrets, and add human approval around delete, share, permission, calendar, and account actions. <br>
Risk: The security evidence advises against exposure to untrusted chats or customer-service users without additional controls. <br>
Mitigation: Restrict who can message the bot, avoid untrusted customer-service exposure by default, and apply organization-specific policy controls before broad rollout. <br>
Risk: The release requires sensitive WeCom credentials and can read configured local media paths. <br>
Mitigation: Store secrets in managed configuration, rotate them as needed, and narrow or disable local media roots unless the deployment explicitly needs local file access. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhaobod1/huo15-wecom-plugin) <br>
- [Project homepage](https://cnb.cool/huo15/ai/huo15-wecom-plugin) <br>
- [README](README.md) <br>
- [Changelog 2.9.5](CHANGELOG.md) <br>
- [WeCom Calendar API documentation](https://developer.work.weixin.qq.com/document/path/93329) <br>
- [WeCom app share information documentation](https://developer.work.weixin.qq.com/document/path/95813) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, TypeScript plugin behavior, JSON/YAML configuration examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send WeCom messages, upload or download media, and invoke WeCom document, calendar, and MCP tools when configured.] <br>

## Skill Version(s): <br>
2.9.5 (source: package.json, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
