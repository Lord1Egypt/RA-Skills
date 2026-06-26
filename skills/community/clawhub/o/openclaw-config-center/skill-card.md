## Description: <br>
为 OpenClaw 构建集中化配置管理系统，告别硬编码和配置分散，实现"改一处，生效全局"的现代化运维体验。包含配置加载器、主配置融合、记忆同步、AGENTS.md 模板、memoryFlush、memorySearch、多 Agent 配置、ClawRouter 成本优化等核心功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zoopools](https://clawhub.ai/user/Zoopools) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to centralize OpenClaw configuration, manage AGENTS.md and memory templates, and add ClawRouter-based routing, caching, and cost monitoring guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote installer commands and Docker images require high trust before execution. <br>
Mitigation: Inspect remote install scripts before running them, prefer pinned Docker images where possible, and review the skill before installing. <br>
Risk: Configuration examples involve API keys, bot tokens, and local secret files. <br>
Mitigation: Keep real secrets out of Git and logs, replace placeholders only in private files, and set secret configuration files to mode 600. <br>
Risk: Wallet funding and third-party model routing can expose spend and data to external services. <br>
Mitigation: Use a dedicated low-balance wallet when funding is required and enable remote memory search or multi-provider routing only for data suitable for third-party processing. <br>
Risk: OpenClaw configuration and memory changes can affect persistent agent behavior. <br>
Mitigation: Back up OpenClaw configuration and memory before restarting or applying generated configuration. <br>


## Reference(s): <br>
- [OpenClaw 集中配置管理系统 on ClawHub](https://clawhub.ai/Zoopools/openclaw-config-center) <br>
- [ClawRouter GitHub repository](https://github.com/blockrunai/ClawRouter) <br>
- [ClawRouter cost optimization documentation](https://blockrun.ai/docs/cost-optimization) <br>
- [SiliconFlow API endpoint](https://api.siliconflow.cn/v1) <br>
- [artifact/AGENTS.md 配置模板.md](artifact/AGENTS.md 配置模板.md) <br>
- [artifact/ClawRouter 安装指南.md](artifact/ClawRouter 安装指南.md) <br>
- [artifact/clawrouter.json 配置模板.md](artifact/clawrouter.json 配置模板.md) <br>
- [artifact/多 Agent 配置模板.md](artifact/多 Agent 配置模板.md) <br>
- [artifact/成本监控模板.md](artifact/成本监控模板.md) <br>
- [artifact/记忆系统配置模板.md](artifact/记忆系统配置模板.md) <br>
- [artifact/配置模板合集（脱敏版）.md](artifact/配置模板合集（脱敏版）.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown documentation with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces templates and operational guidance; users must replace placeholders with their own secrets and environment-specific values.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
