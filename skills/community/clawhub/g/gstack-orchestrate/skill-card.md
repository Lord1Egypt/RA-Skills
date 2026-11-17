## Description:

Gstack Orchestrate takes a gstack implementation plan and executes it through wave-based parallel Claude Code subagents in isolated git worktrees, then verifies and hands off to review and ship.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to execute a completed gstack implementation plan by splitting work into isolated, wave-based subagent tasks and integrating successful commits after verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make substantial repository changes through delegated agents.

Mitigation: Use only on trusted repositories and branches, approve the task decomposition before dispatch, and review resulting changes before shipping.

Risk: Shell state serialization may run unintended commands when untrusted repository data is stored in env.sh or telemetry state.

Mitigation: Avoid untrusted repositories until the state serialization is changed to shell-safe quoting or JSON, and review generated state files before relying on them.

Risk: Telemetry can report remotely when the local gstack telemetry tier is configured for community or anonymous reporting.

Mitigation: Disable telemetry when remote reporting is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaicianflone/skills/gstack-orchestrate)
- [Project homepage](https://github.com/kaicianflone/gstack-orchestrate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, task plans, JSON checkpoint/result files, and agent handoff instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates delegated agents and may produce repository changes through those agents.]

## Skill Version(s):

1.6.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
