## Description:

LX Agent Optimizer helps agents learn from operational failures, apply proactive behavior patterns, manage cron jobs, and reduce token cost over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paoloxiamn](https://clawhub.ai/user/paoloxiamn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit and tune OpenClaw-style agents, including behavior learning, proactive notifications, cron discipline, token cost control, skill awareness, memory recall, and task quality tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage broad reads of logs, memory, session files, and workspace directories.

Mitigation: Constrain use to explicitly approved logs and directories before running audits or token reports.

Risk: The skill may update persistent memory, improvement logs, skill registries, workspace files, or commits.

Mitigation: Require user confirmation before persistent memory updates, workspace writes, or commits.

Risk: The skill may propose recurring cron reviews, channel probes, and automation changes.

Mitigation: Review cron schedules, target sessions, model choices, and external-message behavior before enabling or changing recurring jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paoloxiamn/skills/lx-agent-optimizer)
- [Behavior Learning](references/behavior-learning.md)
- [Proactive Patterns](references/proactive-patterns.md)
- [Cron Discipline](references/cron-discipline.md)
- [Cost Control](references/cost-control.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file-update recommendations, cron configuration snippets, and token usage reports.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
