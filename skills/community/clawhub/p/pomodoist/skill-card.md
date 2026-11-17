## Description:

Manage the user's Pomodoist tasks, projects, deadlines and synchronized Focus sessions through the configured Pomodoist MCP connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kabanya](https://clawhub.ai/user/kabanya)

### License/Terms of Use:

MIT-0

## Use Case:

Pomodoist users can ask an OpenClaw agent to review tasks, projects, deadlines and Focus activity, or make requested changes after enabling write access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task data is shared with the connected Pomodoist service.

Mitigation: Connect only to a trusted Pomodoist or self-hosted endpoint, and limit summaries to requested information.

Risk: Enabled write tools can change tasks or Focus sessions.

Mitigation: Start read-only, enable writes only when needed, and confirm destructive actions or stopping Focus before execution.

## Reference(s):

- [Pomodoist skill listing](https://clawhub.ai/kabanya/skills/pomodoist)
- [Project homepage (listed in skill metadata)](https://github.com/Kabanya/Pomodoist/tree/main/tool/openclaw)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions]

**Output Format:** [Markdown responses with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only connection by default; write tools require explicit enablement.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
