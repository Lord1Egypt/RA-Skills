## Description:

为 OpenClaw 构建集中化配置管理系统，告别硬编码和配置分散，实现"改一处，生效全局"的现代化运维体验。包含配置加载器、主配置融合、记忆同步、AGENTS.md 模板、memoryFlush、memorySearch、多 Agent 配置、ClawRouter 成本优化等核心功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoopools](https://clawhub.ai/user/zoopools)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to centralize OpenClaw configuration, adapt reusable templates for agents, memory, channels, and ClawRouter, and apply safer operational practices for secret handling and cost monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes high-impact setup paths such as curl-to-bash, Docker images, and source installs.

Mitigation: Review installation commands before use; avoid curl-to-bash where possible; pin and verify Docker images or source installs.

Risk: Configuration templates include placeholders for API keys, bot tokens, Feishu app secrets, and wallet-related setup.

Mitigation: Treat credentials as secrets, replace placeholders only in private local configs, keep sensitive files out of public repositories, and use 600-style permissions for secret-bearing files.

Risk: Remote memorySearch can send indexed memory content to an external embedding provider.

Mitigation: Enable remote memorySearch only after accepting that data flow, or use a local provider for memory that should not leave the environment.

Risk: The security verdict is suspicious because the release recommends configuration and installation patterns that need tightening before deployment.

Mitigation: Review and scan the templates before deployment, restrict Feishu access to approved users or groups, and test changes in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoopools/skills/openclaw-config-center)
- [ClawRouter GitHub](https://github.com/blockrunai/ClawRouter)
- [ClawRouter cost optimization guide](https://blockrun.ai/docs/cost-optimization)
- [OpenClaw advanced configuration guide](https://tbbbk.com/openclaw-advanced-config-guide/)
- [OpenClaw multi-agent configuration guide](https://tbbbk.com/openclaw-multi-agent-config-guide/)
- [BGE-M3 paper](https://arxiv.org/abs/2402.03216)

## Skill Output:

**Output Type(s):** [markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown templates with JSON configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes placeholders for local secrets and deployment-specific values; users must replace them before use.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
