## Description:

轻量级主动代理，支持自动任务执行、异常告警、周期性监控、智能提醒能力。无需人工触发，自动在后台完成预设任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure lightweight background automation for periodic task execution, monitoring, alerts, reminders, and repeatable operational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes broad unattended background automation for commands, data checks, notifications, and external task actions without enough scoping or user-control detail.

Mitigation: Install only after review, use least-privilege accounts, and require audit logs, rollback, and a clear stop mechanism before enabling unattended operation.

Risk: Automatic task claiming or custom command execution could perform actions without sufficient approval.

Mitigation: Keep auto-claiming disabled unless explicit rules and approval gates are in place, and do not allow custom commands, backups, mail access, or notifications to run unattended until controls are verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/proactive-agent-lite-paudy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose unattended background automation settings and command execution workflows.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
