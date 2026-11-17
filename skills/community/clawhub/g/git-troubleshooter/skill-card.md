## Description:

Diagnose a tangled git situation and give the exact, safe commands to fix it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Git users use this skill to diagnose stuck repository states and receive ordered, safer recovery commands with explanations and undo guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested Git commands may rewrite history, discard local changes, or affect shared remote branches if applied to the wrong repository state.

Mitigation: Read each command explanation and warning before execution, confirm the current repository and remote state, and prefer the non-destructive recovery path when available.

Risk: Incomplete user-provided Git status or error output can lead to assumptions about the repository state.

Mitigation: Treat labeled assumptions as points to confirm before running commands, and use recovery notes such as reflog-based rollback when results differ from expectations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/git-troubleshooter)
- [Skill Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/git-troubleshooter.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with ordered command sequences and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnosis, command explanations, destructive-action warnings, and recovery notes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
