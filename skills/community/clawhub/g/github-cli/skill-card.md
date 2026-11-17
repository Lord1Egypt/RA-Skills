## Description:

Comprehensive GitHub CLI (gh) reference. Covers repos, issues, PRs, Actions, releases, gists, search, projects v2, API, secrets/variables, labels, codespaces, extensions, auth, and advanced GraphQL patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tag-assistant](https://clawhub.ai/user/tag-assistant)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill as a GitHub CLI reference for repository, issue, pull request, Actions, release, project, API, secret, variable, codespace, and authentication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can perform live GitHub account, repository, secret, variable, workflow, release, project, and API changes.

Mitigation: Verify the repo, org, account, scopes, command effects, and destructive flags before running examples against a real GitHub account.

Risk: Token and secret examples can expose or modify sensitive credentials if copied without review.

Mitigation: Use least-privilege tokens, avoid printing tokens, protect shell history and logs, and rotate credentials if exposure is suspected.

Risk: Extension and raw API or GraphQL examples can execute third-party extension behavior or mutate resources outside common CLI workflows.

Mitigation: Install only trusted extensions and review raw API payloads before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tag-assistant/skills/github-cli)
- [Publisher profile](https://clawhub.ai/user/tag-assistant)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash, JSON, and GraphQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the GitHub CLI binary `gh`; examples may require GitHub authentication, environment tokens, and feature-specific scopes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
