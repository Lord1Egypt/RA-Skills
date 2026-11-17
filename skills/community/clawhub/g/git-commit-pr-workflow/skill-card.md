## Description:

Guides an agent through a safe git workflow to create a branch when needed, commit relevant changes, push, and create or update a pull request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn a working tree into a ready pull request by inspecting git state, committing intended changes, pushing a branch, and preparing a concise PR body with a test plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish code changes to a remote repository through commits, branch pushes, and pull requests.

Mitigation: Review the working tree before use and stage only intended files before committing or pushing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wimi321/skills/git-commit-pr-workflow)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with git commands and pull request summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in a new commit, pushed branch, and created or updated pull request when authorized by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
