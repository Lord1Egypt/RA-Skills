## Description:

Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yqghlx](https://clawhub.ai/user/yqghlx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to have an agent propose GitHub CLI commands for issues, pull requests, workflow runs, CI checks, logs, and GitHub API queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub CLI commands can access or modify repository data when run with authenticated GitHub credentials.

Mitigation: Review commands before execution, especially `gh api`, issue, and pull request commands that may change repository data.

Risk: Commands could target the wrong repository if repository context is ambiguous.

Mitigation: Specify `--repo owner/repo` when not in the intended git directory, or use explicit GitHub URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yqghlx/skills/github-test)
- [ClawHub publisher profile](https://clawhub.ai/user/yqghlx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended to be reviewed before execution and may use the authenticated GitHub CLI context.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
