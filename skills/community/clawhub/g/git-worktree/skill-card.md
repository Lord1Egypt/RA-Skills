## Description:

Git Worktree guides agents through scoped parallel development in the current Git worktree, including repository and task identification, workspace checks, code changes, testing guidance, and commit-message suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to work on one feature or fix inside the current Git worktree while preserving scope boundaries across parallel worktrees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-directed code changes or commits may affect the current branch.

Mitigation: Review the agent plan, git status, and proposed changes before approving work or commits.

Risk: Using the skill outside the intended worktree could modify unrelated code.

Mitigation: Confirm the current worktree path, branch, and repository before starting, and keep changes scoped to the active task directory.

## Reference(s):

- [Git Worktree ClawHub Skill Page](https://clawhub.ai/weidongkl/skills/git-worktree)
- [weidongkl ClawHub Publisher Profile](https://clawhub.ai/user/weidongkl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and commit-message suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include changed-file summaries, design rationale, risk notes, and testing recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
