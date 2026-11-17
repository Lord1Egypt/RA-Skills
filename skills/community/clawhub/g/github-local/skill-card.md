## Description:

Interact with GitHub using the `gh` CLI for issues, pull requests, CI runs, and API queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morrison230](https://clawhub.ai/user/morrison230)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to inspect GitHub issues, pull requests, workflow runs, logs, and API fields through an existing GitHub CLI setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub CLI commands may access private repositories and account-scoped data available to the configured `gh` credentials.

Mitigation: Review `gh` authentication, token scopes, organization access, and target repository selection before using the skill.

Risk: Issue, pull request, workflow, log, and API query results may expose repository-sensitive information in agent output.

Mitigation: Run commands only against intended repositories and review outputs before sharing them outside the authorized audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/morrison230/skills/github-local)
- [ClawHub publisher profile](https://clawhub.ai/user/morrison230)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the caller's existing GitHub CLI authentication and repository access.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
