## Description:

Openclaw Config Expert helps agents validate, repair, optimize, migrate, and recover OpenClaw configuration, including agent settings, model routing, plugin management, and Gateway recovery workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samlinfj](https://clawhub.ai/user/samlinfj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to manage OpenClaw configuration, validate and repair configuration files, tune agent and model routing settings, manage plugins, migrate versions, and recover from broken Gateway or dashboard states.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change OpenClaw configuration, restart services, manage plugins, and set scheduled jobs.

Mitigation: Install only for administrators who expect those capabilities, require explicit confirmation before rollback, restart, migration, or plugin changes, and review scheduled jobs before enabling them.

Risk: Broad automatic routing for mutating configuration commands can cause unintended changes.

Mitigation: Avoid broad auto-routing for mutating commands and keep human approval in the workflow before applying configuration edits.

Risk: The security scan reports an undeclared persistent prompt rewrite in scripts/knowledge_optimization.py.

Mitigation: Review or remove scripts/knowledge_optimization.py before installation, especially in environments where persistent prompt changes are not expected.

Risk: Backups and configuration templates may contain API keys, channel secrets, or other sensitive settings.

Mitigation: Protect OpenClaw configuration files, backups, and recovery logs with restrictive file permissions and avoid committing populated secret values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samlinfj/skills/openclaw-config-expert)
- [OpenClaw architecture documentation](https://docs.openclaw.ai/concepts/architecture)
- [DeepSeek platform](https://platform.deepseek.com)
- [Alibaba Cloud DashScope](https://dashscope.aliyun.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify OpenClaw configuration files and operational commands when the host agent executes the bundled scripts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
