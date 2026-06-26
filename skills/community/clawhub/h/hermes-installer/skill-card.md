## Description: <br>
Hermes Installer guides agents through installing, updating, diagnosing, and configuring Hermes Agent for CLI use, model providers, and messaging gateways. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongyu23](https://clawhub.ai/user/dongyu23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install Hermes Agent, choose CLI or Docker deployment, configure model API providers, migrate OpenClaw settings, and set up Telegram, Discord, Feishu, or related gateway access. It also provides shell commands for updating, uninstalling, and running health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation, update, Docker, and uninstall commands can modify or remove local Hermes files and configuration. <br>
Mitigation: Review commands before execution, confirm install and uninstall paths, use --keep-config when preserving configuration, and avoid running destructive steps without explicit user confirmation. <br>
Risk: Configuration workflows handle API keys, bot tokens, gateway secrets, and migrated OpenClaw credentials. <br>
Mitigation: Keep ~/.hermes/.env private and out of source control, import API keys only when needed, and use migration dry-run or user-data presets before importing secrets. <br>
Risk: Gateway setup can expose messaging access if pairing codes or allowed users are misconfigured. <br>
Mitigation: Verify gateway pairing codes, restrict GATEWAY_ALLOWED_USERS, and review platform credentials before starting gateway services. <br>
Risk: The health-check script can send an authenticated test request to the configured API endpoint. <br>
Mitigation: Run doctor.sh only against trusted endpoints and understand that it uses the configured API key and base URL. <br>


## Reference(s): <br>
- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/) <br>
- [Hermes Agent GitHub repository](https://github.com/NousResearch/hermes-agent) <br>
- [OpenRouter documentation](https://openrouter.ai/docs) <br>
- [Zhipu AI API documentation](https://open.bigmodel.cn/dev/api) <br>
- [Kimi API documentation](https://platform.kimi.com/docs/api/chat) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [Discord Developer Portal](https://discord.com/developers/applications) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, PowerShell, YAML, and environment-variable snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file changes under ~/.hermes, Docker commands, package installation commands, and authenticated API connectivity checks.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
