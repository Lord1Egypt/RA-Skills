## Description:

GitHub Assistant Skill helps agents view GitHub Trending, search repositories, and manage repositories, issues, pull requests, code content, releases, Actions, users, notifications, and organizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonforcode](https://clawhub.ai/user/leonforcode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users can use this skill to have an agent inspect GitHub trends, find projects, and perform repository collaboration tasks. It is suited to browsing repositories, managing issues and pull requests, reading or updating code files, and operating release or workflow metadata when the user has appropriate GitHub access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can request broad GitHub access for repository, issue, pull request, Actions, and content operations.

Mitigation: Use a fine-grained, short-lived GitHub token scoped to selected repositories and only the permissions needed for the current task.

Risk: Stored GitHub tokens and browser sessions can expose account access if the local configuration directory is compromised.

Mitigation: Treat ~/.github-assistant as sensitive, avoid sharing the environment, and remove stored credentials when they are no longer needed.

Risk: Browser login, hosts-file changes, third-party mirrors, and --ipc=host Docker usage can increase operational risk in untrusted environments.

Mitigation: Prefer API-only operation where possible and use browser login, hosts-file changes, mirrors, or host IPC only after explicit review.

## Reference(s):

- [GitHub API Endpoints Reference](artifact/references/github_api_endpoints.md)
- [GitHub Assistant Skill on ClawHub](https://clawhub.ai/leonforcode/skills/github-assistant-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and structured GitHub operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include repository metadata, issue and pull request details, code content, API results, and setup guidance.]

## Skill Version(s):

1.0.0 (source: target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
