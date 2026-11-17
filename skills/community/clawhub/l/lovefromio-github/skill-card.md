## Description:

Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovefromio](https://clawhub.ai/user/lovefromio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent for GitHub CLI commands and guidance for issues, pull requests, CI runs, and advanced `gh api` queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated `gh api` or mutation commands can change repository or organization resources.

Mitigation: Review proposed GitHub CLI commands before execution, especially when authenticated to organization repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovefromio/skills/lovefromio-github)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include `gh` commands that require review before execution when authenticated to GitHub repositories.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
