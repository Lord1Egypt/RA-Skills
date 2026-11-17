## Description:

OpenClaw 多 Agent 协作架构 - 混合层级 + 物理隔离 + 逻辑隔离的完美组合

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoopools](https://clawhub.ai/user/zoopools)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to set up a multi-agent workflow with separate writer and media roles, task routing, review expectations, and troubleshooting guidance. It is intended for coordinating creative generation and social-media publishing tasks while keeping role responsibilities explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes agent behavior through SOUL.md templates.

Mitigation: Review and manually merge the templates into existing SOUL.md files instead of overwriting local behavior without review.

Risk: The media role may perform public posting or broad third-party tool use without clear confirmation gates.

Mitigation: Add explicit approval gates before social-media posting or third-party tool invocation.

Risk: Wildcard baoyu-* authorization can allow more tools than the reviewer intended.

Mitigation: Replace wildcard authorization with an explicit, reviewed list of allowed skills and pin dependent skills where possible.

Risk: Task memory guidance may store user task data without a clear retention boundary.

Mitigation: Define what task data may be stored, where it is stored, and how users can delete it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoopools/skills/multi-agent-hybrid-architecture)
- [Architecture guide](docs/architecture.md)
- [Task flow guide](docs/task-flow.md)
- [Troubleshooting guide](docs/troubleshooting.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command examples and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SOUL.md role templates and a bash configuration-check script.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
