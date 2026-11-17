## Description:

Use this skill when the user asks to create a PR, open a pull request, "create-pr", "submit a pull request", or "open a merge request". Requires Gitee MCP Server to be configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oschina](https://clawhub.ai/user/oschina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to draft a structured Gitee pull request from branch differences and create it through a configured Gitee MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The create_pull action publishes repository-visible PR content.

Mitigation: Review the generated PR title, body, source branch, and target branch before creation.

Risk: Missing or incorrect repository and branch details can create a pull request against the wrong target.

Mitigation: Confirm repository owner, repository name, source branch, and target branch with the user before invoking create_pull.

Risk: The skill depends on a configured Gitee MCP server to read branch differences and create the pull request.

Mitigation: Use only a trusted, intended Gitee MCP server configuration for repositories where PR creation is permitted.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown PR title and body with Gitee MCP create_pull parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires repository owner, repository name, source branch, target branch, and an optional issue number.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
