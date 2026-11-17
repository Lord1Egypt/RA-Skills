## Description:

Advanced Git operations as tools: interactive rebase with autosquash, worktree management, reflog recovery, subtree/submodule handling, cherry-pick across forks, PR automation with human-written intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neroagent](https://clawhub.ai/user/neroagent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run advanced Git workflows through agent tools, including rebase planning, worktree setup, reflog recovery, subtree imports, pull request creation, and changelog generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool inputs can be turned into arbitrary shell commands.

Mitigation: Do not install this version in environments that may receive untrusted branch names, paths, tags, URLs, PR text, or other tool inputs; revise subprocess calls to pass argument arrays and validate refs and paths.

Risk: Git operations can make repository changes without strong safeguards.

Mitigation: Constrain worktree destinations and require explicit confirmation or dry-run previews for force-updates, subtree imports, and pull request creation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [JSON tool responses with markdown changelogs and human-facing Git guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Git and GitHub CLI operations that change repositories or create pull requests.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
