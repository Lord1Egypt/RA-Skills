## Description:

Configures OpenClaw with self-learning memory, proactive behavior rules, heartbeat checks, correction logging, and structured memory management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenpengyu1016](https://clawhub.ai/user/chenpengyu1016)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agent developers use this skill to add persistent self-improvement, preference and correction logging, proactive checks, and memory-maintenance routines to an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes persistent changes to agent memory, workspace memory, and behavior configuration.

Mitigation: Back up AGENTS.md, SOUL.md, HEARTBEAT.md, MEMORY.md, and ~/self-improving before installation, then review every template before appending it.

Risk: Automatic preference, correction, and pattern logging can store sensitive or inaccurate user information.

Mitigation: Use restrictive permissions on memory files and require confirmation before promoting tentative preferences or patterns into always-loaded memory.

Risk: Proactive checks and heartbeat behavior can cause the agent to initiate work or notifications beyond the user's immediate request.

Mitigation: Keep cooldowns enabled, disable external monitoring unless needed, and require user confirmation before high-impact changes or deletion of memory.

## Reference(s):

- [Learning Signals Reference](references/learning-signals.md)
- [ClawHub skill page](https://clawhub.ai/chenpengyu1016/skills/instant-genius)
- [Publisher profile](https://clawhub.ai/user/chenpengyu1016)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions and configuration additions for AGENTS.md, SOUL.md, HEARTBEAT.md, and OpenClaw memory files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
