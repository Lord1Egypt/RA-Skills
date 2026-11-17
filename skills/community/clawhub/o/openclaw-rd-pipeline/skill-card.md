## Description:

Orchestrates OpenClaw R&D delivery in Feishu from requirement intake through project context building, coding and PR flow, read-only review/testing gates, bug-loop rework, and owner notification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinlihudong](https://clawhub.ai/user/yinlihudong)

### License/Terms of Use:


## Use Case:

Developers and delivery teams use this skill to run Feishu-backed R&D tasks with PM, developer, reviewer, and tester role handoffs, validated status transitions, PR review, test gates, bug rework, and closure notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to act across Feishu project records and repository workflows.

Mitigation: Use scoped Feishu and git credentials, confirm the owner and project mapping before execution, and review copied wiki or historical context in PRs and notifications.

Risk: Workflow runs may leave isolated tmux sessions or git worktrees behind.

Mitigation: Clean up tmux sessions and worktrees after the run when required by the operating environment.

## Reference(s):

- [Feishu Field Mapping](references/feishu-fields.md)
- [Templates](references/templates.md)
- [OpenClaw RD Pipeline on ClawHub](https://clawhub.ai/yinlihudong/skills/openclaw-rd-pipeline)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, YAML/JSON objects, PR comments, status updates, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu status snapshots and requires UI evidence metadata when frontend changes are present.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
