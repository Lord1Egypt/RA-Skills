## Description:

Runs an OpenClaw autonomous iteration loop that modifies files, verifies the result, keeps successful changes, and discards failed changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run repeated code-change and verification cycles against a stated goal and verification command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run arbitrary shell commands and may commit, reset, or delete repository changes.

Mitigation: Review the task and verification command before execution, use a disposable or clean Git worktree, and avoid repositories with uncommitted or sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-autoresearch-loop)
- [uditgoenka/autoresearch](https://github.com/uditgoenka/autoresearch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown summaries, shell commands, local state JSON, and git commits when configured]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a caller-supplied goal, verification command, iteration limits, scope globs, and local state files.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
