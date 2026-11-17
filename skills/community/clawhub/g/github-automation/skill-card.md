## Description:

Automates common GitHub tasks such as creating issues, checking pull request status, listing repositories, and reviewing notifications from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcompile](https://clawhub.ai/user/cloudcompile)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate routine GitHub repository, issue, pull request, and notification workflows without switching to a browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub token interception due to disabled TLS verification in API requests.

Mitigation: Fix TLS verification before use. Until then, avoid valuable or broad GitHub tokens and prefer a fine-grained token limited to the specific repositories and actions needed.

Risk: Issue creation can publish user-provided content to GitHub without an extra confirmation prompt.

Mitigation: Review issue titles, bodies, labels, and target repositories before execution, and avoid including sensitive data.

Risk: Broad GitHub token permissions can expose repositories, issues, pull requests, and notifications.

Mitigation: Use least-privilege fine-grained tokens scoped to the required repositories and GitHub operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloudcompile/skills/github-automation)
- [GitHub API endpoint](https://api.github.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, command output summaries, and GitHub URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GITHUB_TOKEN environment variable for authenticated GitHub operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
