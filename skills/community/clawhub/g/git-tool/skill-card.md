## Description:

Useful Git commands for repository management. Use when user needs to manage git repositories, create branches, view history, stash changes, or automate git workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage Git repositories from an agent workflow, including repository initialization, branch and history inspection, stash operations, diffs, and commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: State-changing Git operations can modify repository state through add, commit, stash, pull, or push.

Mitigation: Review status and diffs before running mutation commands, and confirm file selections, remotes, and branches before commit, pull, or push.

Risk: Commit stages files by default when no file list is supplied.

Mitigation: Pass an explicit file list for targeted commits or review staged changes before committing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/git-tool)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve real Git repository mutations when state-changing commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
