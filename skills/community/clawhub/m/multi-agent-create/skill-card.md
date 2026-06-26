## Description: <br>
Create new OpenClaw agents and connect them to messaging channels (Telegram, Discord, Slack, Feishu, WhatsApp, Signal, Google Chat). Includes workspace scaffolding and channel configuration guide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joansongjr](https://clawhub.ai/user/joansongjr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create a new agent workspace, register the agent, and connect it to a supported messaging channel. It guides credential collection, channel configuration, gateway restart, verification, and user pairing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to handle powerful messaging tokens and app secrets while configuring external channels. <br>
Mitigation: Use least-privilege test credentials, avoid pasting production secrets into chat, store secrets in protected configuration or a secrets manager, and rotate or revoke credentials if setup is abandoned. <br>
Risk: The setup process can create persistent agent and channel access to external messaging services. <br>
Mitigation: Review the generated workspace and gateway configuration before restart, verify bindings with OpenClaw status commands, and remove the bot or revoke credentials when it is no longer needed. <br>
Risk: Unsafe agent names could lead to confusing workspace paths or unintended configuration entries. <br>
Mitigation: Use a simple safe agent name without slashes, dots, or shell-sensitive characters before running setup commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joansongjr/multi-agent-create) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>
- [Discord Developer Portal](https://discord.com/developers/applications) <br>
- [Slack API apps](https://api.slack.com/apps) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Lark Developer](https://open.larksuite.com/) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent OpenClaw agent workspace files and channel bindings when the helper script or commands are run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
