## Description:

Guides users through permanently removing files from Git repository history with git-filter-repo, including backup, verification, force-push, collaborator, and secret-rotation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhjin](https://clawhub.ai/user/hhjin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need guidance for removing sensitive data, large files, or other unwanted paths from all Git branches and tags. It helps plan the history rewrite, verify removal, push rewritten history, and coordinate follow-up actions such as credential rotation and collaborator notification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Git history rewrites and force pushes can disrupt remote branches, tags, and collaborators' local clones.

Mitigation: Make a verified backup, confirm repository-owner authorization, coordinate with collaborators, and prefer narrow branch or tag pushes where possible.

Risk: Removing secrets from Git history does not revoke credentials or eliminate copies that may exist in forks, caches, or local clones.

Mitigation: Treat exposed secrets as compromised, rotate or revoke them immediately, and check forks, CI/CD caches, and retained local clones.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hhjin/skills/git-clear-committed-file-history)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides step-by-step operational guidance; users must confirm repository details and authorization before destructive history-rewrite commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
