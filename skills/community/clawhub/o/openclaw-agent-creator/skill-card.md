## Description:

创建新的 OpenClaw Agent。用于当用户要求创建新 agent、添加新机器人、配置新模型测试环境时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to scaffold a new OpenClaw agent workspace, copy required Markdown templates, create model and authentication configuration files, and update openclaw.json for agent routing and optional Feishu bindings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: New agents may inherit or expose credentials if auth.json is copied from a main agent or if Feishu appSecret values are pasted into chat or stored directly in configuration.

Mitigation: Prefer an empty auth.json for new agents, use separate scoped credentials per agent, and store secrets through a secure secret mechanism or environment reference.

Risk: Bundled memory templates may seed generated agents with personal or project-specific context.

Mitigation: Replace MEMORY.md personal and project data with neutral placeholders before generating agents.

Risk: The skill modifies OpenClaw agent routing and optional channel bindings, which can affect how agents receive work.

Mitigation: Review the generated openclaw.json changes before installing or using the new agent configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/openclaw-agent-creator)
- [Publisher profile](https://clawhub.ai/user/axelhu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces checklist-style setup steps and file/configuration templates for creating OpenClaw agents.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
