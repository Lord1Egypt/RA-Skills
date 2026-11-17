## Description:

Delegate coding tasks to Codex, Claude Code, Pi, or OpenCode from bash with safe launch modes, background monitoring, and repo-isolated review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielsinewe](https://clawhub.ai/user/danielsinewe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate repository implementation, review, issue triage, and repeated run/fix/verify loops to a selected coding agent while keeping work scoped and reviewable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated coding agents can run with broad autonomy, including permission-bypassing or fully automated modes.

Mitigation: Use conservative permission settings, disposable containers or VMs for untrusted repositories, remove inherited secrets, and inspect commands and file changes before accepting results.

Risk: Agent-generated edits or review guidance can introduce incorrect behavior or miss repository-specific constraints.

Mitigation: Keep each delegated session scoped to one repository and one objective, then review diffs and run the relevant tests or lint checks before merging.

## Reference(s):

- [OpenClaw Coding Agent Workflows on ClawHub](https://clawhub.ai/danielsinewe/skills/openclaw-coding-agent-workflows)
- [danielsinewe publisher profile](https://clawhub.ai/user/danielsinewe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and text prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for agent orchestration, background session monitoring, and repo-isolated review workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
