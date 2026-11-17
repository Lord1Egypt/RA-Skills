## Description:

Operate GitHub repositories, issues, pull requests, files, labels, and code search using GitHub REST API curl commands with personal access token authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaolfun](https://clawhub.ai/user/gaolfun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to manage GitHub issues, pull requests, labels, repository files, and searches from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a write-capable GitHub token for high-impact repository actions such as comments, closes, merges, file updates, and deletions.

Mitigation: Use a fine-grained, short-lived PAT scoped to specific repositories and the minimum permissions needed; require explicit confirmation of repo, branch, issue or PR number, path, and payload before write operations.

Risk: Examples that print or read the token file can expose a GitHub PAT.

Mitigation: Do not print token files, avoid pasting tokens into chat or logs, store tokens with restricted file permissions, and rotate or revoke any token that may have been exposed.

Risk: Unquoted or unvalidated curl URL inputs can cause unintended GitHub API requests.

Mitigation: Quote and validate owner, repository, branch, path, label, issue, PR, and query values before running documented commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gaolfun/skills/github-integration)
- [GitHub API Base URL](https://api.github.com)
- [GitHub Personal Access Tokens](https://github.com/settings/tokens)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GitHub personal access token and jq for many examples.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
