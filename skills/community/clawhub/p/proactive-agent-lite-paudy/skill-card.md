## Description: <br>
轻量级主动代理，支持自动任务执行、异常告警、周期性监控、智能提醒能力。无需人工触发，自动在后台完成预设任务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a lightweight background agent for scheduled task execution, monitoring, alerts, reminders, and repeatable automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes unattended background automation with broad task, command, account, and data access. <br>
Mitigation: Verify the external proactive-agent implementation, run it with least privilege, and keep account-mutating actions disabled unless explicitly needed. <br>
Risk: Scheduled tasks, monitoring, and reminders can act repeatedly without direct user review. <br>
Mitigation: Require visible start and stop controls, logs, notification settings, data redaction behavior, and per-task approvals before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/proactive-agent-lite-paudy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes recurring automation settings and command examples; automatic actions should be reviewed before enabling.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
