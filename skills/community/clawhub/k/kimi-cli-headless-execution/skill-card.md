## Description:

教 OpenClaw 在自动化脚本、后台任务、CI/CD 和无 TTY 等非交互场景中，正确使用 Kimi Code CLI 的无头执行参数完成命令构造、输出选择、会话管理、错误处理和安全防护。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiyouwolegequ](https://clawhub.ai/user/aiyouwolegequ)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要在自动化脚本、后台任务或 CI/CD 环境中调用 Kimi CLI 的开发者和工程团队，帮助 Agent 选择 `--quiet`、`--print`、`--wire` 等模式，构造可执行的无头命令并处理结果与风险。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Headless Kimi CLI modes can enable automatic file changes or shell execution without enough scoping or containment.

Mitigation: Use the skill only in trusted, isolated project directories and require explicit approval before any `--quiet`, `--print`, or `--yolo` run that could modify files or execute commands.

Risk: CI environments may expose secrets or sensitive project state to automated CLI execution.

Mitigation: Avoid CI environments with secrets unless they are tightly sandboxed, and verify the Kimi CLI package source with pinned, isolated installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aiyouwolegequ/skills/kimi-cli-headless-execution)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and concise execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include constructed Kimi CLI commands, execution summaries, exit codes, warnings, and next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
