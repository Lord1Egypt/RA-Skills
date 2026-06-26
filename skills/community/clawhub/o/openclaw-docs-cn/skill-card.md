## Description: <br>
OpenClaw 官方文档知识库。当用户询问 OpenClaw 相关问题时自动触发，包括：安装配置、CLI 命令、渠道设置（飞书/钉钉/WhatsApp 等）、定时任务（cron）、技能开发、故障排查。提供命令示例和配置模板。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z13777869196](https://clawhub.ai/user/z13777869196) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill as a Chinese-language reference helper for installation, configuration, CLI commands, channel setup, cron jobs, skill development, and troubleshooting. It provides concise command examples, configuration templates, and links to OpenClaw documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest commands that install daemons, create cron jobs, restart gateways, or configure channel credentials. <br>
Mitigation: Review package names and command effects before execution, especially for daemon installation, scheduled jobs, gateway restarts, and channel credential setup. <br>
Risk: Configuration examples may involve API keys, app secrets, phone numbers, or other sensitive values. <br>
Mitigation: Use placeholders in chat and keep real secrets in local secret stores or configuration files outside the conversation. <br>
Risk: Broad activation keywords may cause the skill to appear in unrelated chats. <br>
Mitigation: Confirm the user is asking about OpenClaw before applying this documentation guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/z13777869196/openclaw-docs-cn) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw CLI reference](https://docs.openclaw.ai/cli/index.md) <br>
- [OpenClaw channel configuration](https://docs.openclaw.ai/channels/index.md) <br>
- [OpenClaw cron jobs](https://docs.openclaw.ai/automation/cron-jobs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholders for credentials and other sensitive values.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
