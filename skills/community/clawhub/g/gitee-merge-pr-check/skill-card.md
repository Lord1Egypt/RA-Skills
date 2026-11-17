## Description:

Checks whether a Gitee pull request is ready to merge through a configured Gitee MCP server and can merge it after explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oschina](https://clawhub.ai/user/oschina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to assess Gitee pull request readiness, review PR status, comments, approvals, and changed files, then merge only after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A confirmed merge is irreversible and may affect the wrong repository, pull request, or target branch.

Mitigation: Before confirming a merge, verify the repository, PR number, target branch, CI status, and review state.

Risk: The skill depends on configured Gitee MCP access that may have permission to merge pull requests.

Mitigation: Install and enable it only for intended repositories and use Gitee credentials with the minimum permissions required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oschina/skills/gitee-merge-pr-check)
- [Publisher profile](https://clawhub.ai/user/oschina)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown merge readiness report with a confirmation prompt when a merge is appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request a Gitee merge action only after explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
