## Description:

OpenClaw Chinese installation and configuration helper that checks the local environment, configures DeepSeek, Zhipu GLM, and DashScope/Qwen credentials, and tests model API connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users in Chinese-language environments use this skill to check local prerequisites, configure Chinese AI provider credentials, update OpenClaw model settings, and test API connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider API keys are stored locally in ~/.openclaw/.env.

Mitigation: Restrict ~/.openclaw/.env permissions to the local user account and avoid sharing the file.

Risk: The installation flow may use a mutable clawhub installer command.

Mitigation: Prefer a pinned installer version when available and review the installed scripts before execution.

Risk: Connection tests send requests to DeepSeek, Zhipu, or DashScope using configured API keys.

Mitigation: Run tests only with intended provider accounts and monitor provider usage or billing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-cn-installer)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [DeepSeek platform](https://platform.deepseek.com)
- [Zhipu AI platform](https://open.bigmodel.cn)
- [DashScope console](https://dashscope.console.aliyun.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Node.js script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include terminal status output, local OpenClaw configuration updates, and provider API connection results.]

## Skill Version(s):

1.0.1 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
