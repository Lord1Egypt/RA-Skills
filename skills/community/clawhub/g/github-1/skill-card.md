## Description:

Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khurramjamil12](https://clawhub.ai/user/khurramjamil12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to ask an agent for GitHub CLI guidance for pull requests, issues, workflow runs, CI checks, and direct GitHub API queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated `gh` commands act with whatever GitHub permissions are available to the local CLI token.

Mitigation: Review commands before execution, especially `gh api` calls, mutations, and operations on private or organization repositories.

Risk: A command that omits or misstates the repository target can operate on the wrong GitHub repository.

Mitigation: Use `--repo owner/repo` when not already in the intended git repository, or use explicit GitHub URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/khurramjamil12/skills/github-1)
- [Publisher profile](https://clawhub.ai/user/khurramjamil12)

## Skill Output:

**Output Type(s):** [shell commands, API calls, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include `gh` commands that operate with the user's local GitHub CLI authentication and repository permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
