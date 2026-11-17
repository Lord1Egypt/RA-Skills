## Description:

Create new OpenClaw agents and connect them to messaging channels (Telegram, Discord, Slack, Feishu, WhatsApp, Signal, Google Chat). Includes workspace scaffolding and channel configuration guide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joansongjr](https://clawhub.ai/user/joansongjr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create an OpenClaw agent workspace, register the agent, and connect it to a supported messaging channel through a guided setup flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messaging bot tokens, app secrets, and service-account keys can grant broad account or workspace access if shared in chat or stored insecurely.

Mitigation: Provision credentials through a secret manager, protected local configuration, or environment variables, and avoid pasting real secrets into chat.

Risk: The setup flow can create or modify persistent OpenClaw workspace files and gateway configuration before an agent is activated.

Mitigation: Use simple validated agent identifiers, inspect generated workspace files and openclaw.json changes before activation, and keep the generated configuration backup.

Risk: Restarting a live gateway can affect existing channel bindings or active agents.

Mitigation: Review and scan the skill before deployment, then test changes in a non-live environment before restarting a production gateway.

## Reference(s):

- [Multi-Agent Create on ClawHub](https://clawhub.ai/joansongjr/skills/multi-agent-create)
- [Telegram BotFather](https://t.me/BotFather)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Slack API Apps](https://api.slack.com/apps)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Lark Developer](https://open.larksuite.com/)
- [Google Cloud Console](https://console.cloud.google.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, JSON configuration examples, and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose OpenClaw CLI commands, channel credential setup steps, workspace file templates, and gateway configuration changes.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
