## Description:

Git Worktree Ops helps agents manage isolated parallel development workspaces with git worktree.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soponcd](https://clawhub.ai/user/soponcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to create, list, and remove isolated Git worktrees for parallel development. It provides command patterns for a local git_worktree_manager.sh helper script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells the agent to use a repository-local tools/git_worktree_manager.sh script that is not bundled in the reviewed artifact.

Mitigation: Inspect tools/git_worktree_manager.sh in the target repository before running create or remove operations.

Risk: The source instructions are in Chinese, which may be misunderstood by reviewers or operators who do not read Chinese.

Mitigation: Confirm the intended create, remove, and list commands before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soponcd/skills/git-worktree-ops)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled executable code; command guidance depends on a repository-local git worktree manager script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
