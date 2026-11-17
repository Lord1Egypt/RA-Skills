## Description:

Automates a Linear-centered workflow for task intake, notifications, task execution, status updates, generated task files, and optional Git synchronization with webhook health checks and quota-aware fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent builders, and small teams use this skill to connect Linear tasks to notification channels, automated execution, Linear status updates, task artifacts, and Git synchronization. It is intended for teams that rely on Linear and want a configurable task workflow with webhook recovery and quota controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run commands, update Linear issues, write files, send webhook or notification data, and push Git changes.

Mitigation: Use least-privilege Linear and Discord tokens, restrict the repository path, keep autoPush disabled unless needed, and review generated commands and Git changes before unattended use.

Risk: Task details may be sent to configured notification or webhook services.

Mitigation: Limit connected services to approved destinations and avoid routing sensitive task content through channels that are not authorized for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/linear-workflow-bot)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Skill homepage](https://skillhub.cn/skill/)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Code, Markdown, Files]

**Output Format:** [Markdown guidance with JSON configuration examples, shell command examples, and structured task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update Linear issues, send notifications, write task artifacts, and create Git commits or pushes when configured.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
