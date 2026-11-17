## Description:

GLM Swarm helps an agent split complex multi-step work into parallel worker tasks, pass compact context packets, aggregate results, and clean up temporary swarm state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a task explicitly calls for swarm or parallel processing, or when the task meets the documented complexity gates of at least two independent subtasks and three or more tool calls. It provides planning patterns, worker context-packet rules, aggregation guidance, and cleanup commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted task ID could cause setup or cleanup scripts to write or delete outside the intended /tmp/swarm workspace.

Mitigation: Generate or validate simple task IDs, resolve canonical paths, and enforce containment under /tmp/swarm before any write or delete.

Risk: Parallel workers may propose code changes, deployments, or persistent result storage that need operator review.

Mitigation: Require explicit confirmation after aggregation before external actions, code changes, deployments, or persistent result storage.

## Reference(s):

- [Context Packet protocol](references/context-packet.md)
- [Pattern library](references/patterns.md)
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/glm-swarm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON task templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Worker outputs are guided to stay within 300 tokens; aggregation returns a short summary when worker output exceeds 500 tokens.]

## Skill Version(s):

1.1.1 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
