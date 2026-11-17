## Description:

Interact with GitHub using the `gh` CLI for issues, pull requests, CI runs, and advanced GitHub API queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hucy](https://clawhub.ai/user/hucy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent for GitHub CLI commands and guidance for repository tasks such as inspecting pull requests, checking CI status, viewing workflow runs, and querying GitHub API fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide use of an existing GitHub CLI login, including access to private or organization repositories.

Mitigation: Install only when that access pattern is acceptable, and ensure the active `gh` account and repository target are correct before running commands.

Risk: Mutating GitHub CLI actions could affect issues, pull requests, CI workflows, or repository data.

Mitigation: Review commands before execution and use explicit `--repo owner/repo` targets or direct URLs to avoid acting on the wrong repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hucy/skills/logo-generator-12)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on the user's existing GitHub CLI authentication and repository access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
