## Description:

AI-native configuration and setup guides for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxzyma](https://clawhub.ai/user/maxzyma)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to apply setup guides for multi-agent workflows, memory search, AI provider routing, cost controls, and proactive monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installer commands may execute unreviewed code.

Mitigation: Download, inspect, and verify installer contents before running any install command.

Risk: Monitoring and automation settings can scan local data, spawn workers, retry tasks, and send reports.

Mitigation: Keep monitoring, auto-spawn, auto-recovery, webhooks, and memory indexing disabled until paths, destinations, retention rules, and approval gates are explicitly chosen.

Risk: Provider API keys and secrets may be exposed through local configuration.

Mitigation: Store keys with restrictive permissions or a secret manager, and review generated environment files before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxzyma/skills/ohmyopenclaw)
- [Setup Guides Index](guides/_index.md)
- [Agent Swarm Architecture Guide](guides/agent-swarm.md)
- [Memory Optimization Guide](guides/memory-optimized.md)
- [Proactive Monitoring Guide](guides/monitor.md)
- [Chinese Providers Guide](guides/chinese-providers.md)
- [Cost Optimization Guide](guides/cost-optimization.md)
- [Alibaba Cloud DashScope documentation](https://help.aliyun.com/zh/dashscope/)
- [Zhipu GLM API documentation](https://open.bigmodel.cn/dev/api)
- [Baidu Wenxin Workshop documentation](https://cloud.baidu.com/doc/WENXINWORKSHOP/)
- [DeepSeek API documentation](https://platform.deepseek.com/api-docs/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides may propose workspace file edits, monitoring settings, API-provider configuration, and validation steps for a human or agent to review before applying.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
