## Description:

Manage GitHub Projects v2 with the GitHub CLI by listing backlog items, editing project fields, commenting on issues, creating issues, and managing sub-issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freddydk](https://clawhub.ai/user/freddydk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project maintainers use this skill to have an agent propose GitHub CLI commands for managing GitHub Projects v2 backlog items, fields, and related issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide authenticated GitHub mutations, including project field edits, issue comments, issue creation, and project item assignment.

Mitigation: Require explicit approval before running write commands and use the least-privileged GitHub account or token practical.

Risk: The skill recommends installing an unpinned third-party GitHub CLI extension for sub-issue management.

Mitigation: Prefer built-in GitHub CLI or reviewed GraphQL calls, and only use the extension after it has been reviewed and pinned.

Risk: The skill requires the GitHub `project` scope, increasing the impact of an exposed or over-privileged token.

Mitigation: Refresh authentication only for accounts that need project access and avoid using broad personal tokens when a narrower credential is available.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with GitHub CLI command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may mutate GitHub Projects and issues; execution should require user approval.]

## Skill Version(s):

1.0.0 (source: release evidence and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
