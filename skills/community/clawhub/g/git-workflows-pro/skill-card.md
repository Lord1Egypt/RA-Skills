## Description:

Handle advanced git workflows and recovery tasks. Use when the user needs help with interactive rebase, commit cleanup, conflict resolution, reflog recovery, cherry-pick, stash, worktree, bisect, submodule vs subtree decisions, sparse checkout, branch archaeology, or undoing dangerous history mistakes in real repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darinrowe](https://clawhub.ai/user/darinrowe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute advanced Git workflows, including history cleanup, recovery from mistakes, conflict handling, branch archaeology, and repository topology decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Git history operations such as reset, rebase, and force-push can discard local state or rewrite shared history when used on the wrong branch or commit.

Mitigation: Review commands before execution, inspect repository state first, and create a recovery branch before destructive or hard-to-reverse operations.

Risk: Recovery commands can move a repository to the wrong historical state if the target reflog entry or commit is selected incorrectly.

Mitigation: Inspect reflog and commit graph output before changing refs, and use the actual verified commit or reflog entry for recovery.

Risk: Force-pushing after history surgery can overwrite collaborators' work on shared branches.

Mitigation: Avoid rewriting shared history unless explicitly intended, and prefer force-with-lease when a rewritten branch must be updated remotely.

## Reference(s):

- [Advanced Patterns](references/advanced-patterns.md)
- [History Surgery](references/history-surgery.md)
- [Recovery](references/recovery.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with inline shell commands and concise decision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk level, safe first checks, recommended commands, rollback path, and shared-history warnings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
