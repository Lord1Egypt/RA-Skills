## Description:

基于《实践论》的自我迭代系统。当需要自动整理记忆、反思改进、或创建新技能时使用。包含Heartbeat检查清单、Cron定时任务配置、和技能创建工作流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongchenga](https://clawhub.ai/user/kongchenga)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to organize long-term memory, run periodic reflection checklists, configure cron reminders, and create reusable skills when repeated needs emerge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic long-term memory management may persist conversation details that should not be retained.

Mitigation: Decide what conversations may be retained, avoid storing secrets, and keep memory files inspectable, editable, deletable, and recoverable.

Risk: Cron jobs and automated memory updates can run with limited user control.

Mitigation: Review or remove cron commands before enabling the skill and add a manual approval step before MEMORY.md updates.

Risk: Automated skill update behavior may change agent behavior unexpectedly.

Mitigation: Review and scan skill changes before deployment or installation.

## Reference(s):

- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and checklist templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or update memory files, HEARTBEAT.md, cron configuration, and skill files when enabled by the agent environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
