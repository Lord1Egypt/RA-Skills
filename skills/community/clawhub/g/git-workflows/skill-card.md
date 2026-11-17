## Description:

Advanced git operations beyond add/commit/push. Use when rebasing, bisecting bugs, using worktrees for parallel development, recovering with reflog, managing subtrees/submodules, resolving merge conflicts, cherry-picking across branches, or working with monorepos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as an advanced Git workflow reference for history cleanup, bug bisection, parallel branch work, recovery, conflict resolution, repository sharing patterns, and monorepo checkouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some examples use history-changing or destructive Git operations such as rebase, reset --hard, stash clear, tag deletion, and rm -rf.

Mitigation: Read each command carefully, confirm branches, remotes, and paths, and make a backup or stash before running history-changing commands.

Risk: The example bisect script uses a fixed /tmp path, which can be unsafe on shared machines.

Mitigation: Use a unique or project-local temporary script path and inspect the script contents before executing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitgoodordietrying/skills/git-workflows)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git; examples should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
