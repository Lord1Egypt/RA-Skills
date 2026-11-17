## Description:

Interact with GitHub via the GitHub CLI to list repositories, issues, pull requests, and create issues in repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m3159](https://clawhub.ai/user/m3159)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to ask an agent to list GitHub repositories, issues, and pull requests, or to create issues through an authenticated GitHub CLI session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use the user's authenticated GitHub CLI permissions to create issues.

Mitigation: Review the target repository, title, and issue body before asking the agent to create an issue.

Risk: Repository, issue, and pull request listings may expose information available to the authenticated account.

Mitigation: Use the skill only in workspaces where sharing GitHub CLI output with the agent is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/m3159/skills/myfirstgit)
- [Publisher profile](https://clawhub.ai/user/m3159)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the local authenticated GitHub CLI context for GitHub operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
