## Description:

Design OpenClaw-native automation systems using cron, HEARTBEAT.md, spawned sessions, specialist-agent delegation, first-class tools, MCPs, and local scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lsj210001](https://clawhub.ai/user/lsj210001)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to choose execution planes and design OpenClaw-native automation workflows for reminders, scheduled reports, monitoring, alerting, and agent orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation recommendations may lead to persistent cron jobs, heartbeat tasks, or spawned agents that continue running after the initial design session.

Mitigation: Review schedules, delivery targets, state storage, deduplication, and failure behavior before enabling recurring or background automation.

Risk: Workflows that send external messages or touch business-critical data can create operational impact if configured without approval gates.

Mitigation: Require explicit human approval before external sends, destructive actions, or changes involving sensitive production data.

## Reference(s):

- [Decision Matrix](references/decision-matrix.md)
- [OpenClaw Workflow Patterns](references/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/lsj210001/skills/openclaw-automation-architecture)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with recommendations, plans, and inline code or shell commands when implementation is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include state, deduplication, failure-handling, and delivery plans for automations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
