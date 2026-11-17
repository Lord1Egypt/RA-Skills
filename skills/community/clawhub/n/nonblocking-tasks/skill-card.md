## Description:

Helps OpenClaw agents keep the main conversation responsive by delegating work to sub-agents, tracking active tasks, running heartbeat checks, and proactively notifying users of results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinxu1-sys](https://clawhub.ai/user/colinxu1-sys)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to keep an assistant responsive during long-running or multi-step work by delegating tasks, recording status, and pushing completion updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change workspace agent behavior by updating AGENTS.md, MEMORY.md, active_tasks.md, HEARTBEAT.md, and a recurring monitor.

Mitigation: Review and approve those file and schedule changes before enabling the skill, and disable the heartbeat monitor when it is not needed.

Risk: The skill can send task status through external chat channels such as Feishu or WeCom.

Mitigation: Enable notifications only for approved workspaces and channels, and verify that completion messages do not expose sensitive task details.

Risk: The skill can read same-day cross-channel conversation history from ~/.openclaw when a user asks about another channel.

Mitigation: Confirm that cross-channel history access is expected, scoped to the intended user, and allowed by the workspace's data-handling policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/colinxu1-sys/skills/nonblocking-tasks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline configuration and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace task-tracking and heartbeat files and schedule recurring status checks when enabled.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
