## Description: <br>
Openclaw Ref is a Chinese-language reference for OpenClaw configuration, CLI commands, troubleshooting, model management, channels, automation, providers, tools, installation, and security topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[astralwaveorg](https://clawhub.ai/user/astralwaveorg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill as an operational reference when editing openclaw.json, running OpenClaw CLI commands, configuring gateways, channels, providers, automation, tools, and troubleshooting OpenClaw deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents powerful OpenClaw administrative features involving credentials, webhooks, shell or exec settings, node device commands, plugins, hooks, and reset or uninstall commands. <br>
Mitigation: Treat those examples as sensitive operational guidance, prefer environment variables for secrets, and require explicit user approval for shell, elevated, node, and destructive operations. <br>
Risk: OpenClaw channel and group examples can expose private conversations, group history, reasoning output, or unauthorized recipients if access is too broad. <br>
Mitigation: Keep Telegram and group access allowlisted, avoid sending reasoning or private group history unless intentional, and review channel targets before enabling delivery. <br>
Risk: Migration, cleanup, and configuration changes can affect the local ~/.openclaw state and running gateway behavior. <br>
Mitigation: Back up ~/.openclaw before migration or cleanup and validate configuration with OpenClaw diagnostic commands before restarting services. <br>


## Reference(s): <br>
- [OpenClaw Reference Skill Index](artifact/SKILL.md) <br>
- [Configuration Fields Reference](artifact/core/config-fields.md) <br>
- [CLI Reference](artifact/core/cli.md) <br>
- [Model Management Reference](artifact/core/models.md) <br>
- [Gateway Reference](artifact/core/gateway.md) <br>
- [Channels Overview](artifact/channels/overview.md) <br>
- [Automation Hooks and Webhooks Reference](artifact/automation/hooks-webhooks.md) <br>
- [Tools Overview](artifact/tools/overview.md) <br>
- [API and Security Reference](artifact/reference/api-security.md) <br>
- [Installation and Deployment Reference](artifact/setup/install.md) <br>
- [General Troubleshooting Reference](artifact/troubleshooting/general.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-style configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language operational reference material for OpenClaw administration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
