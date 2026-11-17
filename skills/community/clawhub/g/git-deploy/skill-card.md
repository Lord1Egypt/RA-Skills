## Description:

Simple deployment skill for local git operations that helps add, commit, and push changes to the Git repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirenday](https://clawhub.ai/user/sirenday)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to perform a quick local Git deployment workflow from a project root by staging changes, committing with a supplied message, and pushing to the current branch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A repository token is exposed in the skill documentation.

Mitigation: Revoke and remove the exposed token before installation or use, then configure credentials through a secure Git credential mechanism.

Risk: The deploy workflow can commit and push all local changes without a confirmation step.

Mitigation: Check git status and review the intended diff before running the deploy script.

Risk: The release references an HTTP repository remote and pre-configured credentials.

Mitigation: Replace the HTTP remote and embedded credential setup with a secure authenticated remote before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sirenday/skills/git-deploy)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Text with shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a commit message and a local Git repository.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
