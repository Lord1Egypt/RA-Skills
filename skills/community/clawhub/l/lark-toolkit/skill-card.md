## Description: <br>
Comprehensive Lark/Feishu API skill for OpenClaw agents covering Lark operations through the claw-lark plugin, MCP tools, and direct Open API curl examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pengxiao-Wang](https://clawhub.ai/user/Pengxiao-Wang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace administrators use this skill to guide OpenClaw agents through Lark/Feishu messaging, group management, contacts, calendar, docs, bitable, wiki, OKR, task, webhook, bot setup, and troubleshooting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward Lark/Feishu administration and workspace actions, including reading histories, sending messages, sharing documents, managing members, and modifying business data. <br>
Mitigation: Use a dedicated low-privilege Lark app and require explicit approval before performing sensitive workspace actions. <br>
Risk: The token helper and examples depend on user-provided App Secret values and temporary access tokens. <br>
Mitigation: Protect App Secret and access tokens, keep ~/.openclaw/openclaw.json out of source control and logs, and avoid exposing credentials in prompts or command output. <br>


## Reference(s): <br>
- [Lark API Reference](references/api-reference.md) <br>
- [Lark Bot Setup Playbook](references/bot-setup.md) <br>
- [Lark MCP Tools](references/mcp-tools.md) <br>
- [Lark API Permissions Reference](references/permissions.md) <br>
- [Lark Troubleshooting](references/troubleshooting.md) <br>
- [Webhook & Tunnel Setup](references/webhook-setup.md) <br>
- [Lark Developer Console](https://open.larksuite.com/app) <br>
- [Feishu Developer Console](https://open.feishu.cn/app) <br>
- [Lark Open API Base](https://open.larksuite.com/open-apis/) <br>
- [Feishu Open API Base](https://open.feishu.cn/open-apis/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples, MCP tool invocations, permission checklists, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
