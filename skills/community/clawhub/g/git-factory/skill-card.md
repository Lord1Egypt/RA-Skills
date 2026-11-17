## Description:

Provision and manage isolated git worktrees for individual coding tasks, enabling parallel branches and clean PR workflows without merge conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spaztazim](https://clawhub.ai/user/spaztazim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to isolate coding tasks in per-task git worktrees, branches, and PR workflows so parallel changes can be reviewed and merged with fewer conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced PowerShell scripts are not included in the reviewed artifact.

Mitigation: Confirm the scripts come from a trusted source and review them before using this workflow.

Risk: The documented workflow modifies git state and can push branches or open pull requests when those commands are selected.

Mitigation: Run commands from the intended repository and review branch, commit, push, and pull request settings before execution.

Risk: Multiple worktrees share the same git directory, and cleanup can be affected by branch reuse, lock contention, or open files.

Mitigation: Use unique per-task branches, avoid concurrent heavy git operations when possible, and close processes before cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spaztazim/skills/git-factory)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes worktree, branch, commit, PR, and cleanup conventions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
