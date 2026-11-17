## Description:

GitHub 操作工具 - 通过 GitHub API 管理仓库、Issues、PRs、Actions 等

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical operators use this skill to manage GitHub repositories, issues, pull requests, commits, Actions workflows, searches, files, and user information through GitHub API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad GitHub token access and can perform repository-changing actions.

Mitigation: Use a fine-grained, short-lived GitHub token limited to the repositories and actions required for the task.

Risk: Issue, pull request, merge, review, edit, close, and workflow-dispatch actions can change repository state.

Mitigation: Require explicit user confirmation before creating, closing, editing, merging, reviewing, or dispatching workflows.

Risk: A leaked token could expose private repositories or allow unwanted changes.

Mitigation: Store the token only in protected configuration or environment variables and avoid writing it to code, logs, or shared files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaoren36-arch/skills/github-api-tool)
- [GitHub REST API endpoint pattern](https://api.github.com/{endpoint})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and API call templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GitHub token supplied through configuration or environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
