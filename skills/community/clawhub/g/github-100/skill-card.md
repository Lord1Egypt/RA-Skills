## Description:

Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyserkazi1](https://clawhub.ai/user/keyserkazi1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent for GitHub CLI commands and workflows for issues, pull requests, CI runs, and GitHub API queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub commands run through the local gh CLI can use the authenticated account's repository permissions.

Mitigation: Review the active gh authentication and repository permissions before asking the agent to run GitHub commands.

Risk: Commands that query or modify GitHub resources can target the wrong repository if context is ambiguous.

Mitigation: Specify `--repo owner/repo` or use explicit GitHub URLs when operating outside a git directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keyserkazi1/skills/github-100)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub CLI commands that use the local gh authentication context.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
