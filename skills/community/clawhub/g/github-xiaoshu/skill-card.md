## Description:

Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaomaju-888](https://clawhub.ai/user/xiaomaju-888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide GitHub CLI work for issues, pull requests, CI runs, and advanced API queries. It is useful when an agent needs to propose concise `gh` commands and structured output filters for repository workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to use the user's configured `gh` CLI account for GitHub tasks.

Mitigation: Install only when that account access is intended for the agent's GitHub workflow.

Risk: Proposed commands may change repository, issue, pull request, workflow, or organization data.

Mitigation: Review commands before approving actions that could mutate GitHub resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaomaju-888/skills/github-xiaoshu)
- [Publisher profile](https://clawhub.ai/user/xiaomaju-888)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, API calls, JSON]

**Output Format:** [Markdown with inline bash command examples and JSON output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read or modify GitHub resources depending on the selected `gh` subcommand.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
