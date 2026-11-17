## Description:

Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huadafenqi](https://clawhub.ai/user/huadafenqi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent operate the GitHub CLI for repository issues, pull requests, CI runs, and GitHub API queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may use the user's existing `gh` authentication, including access to private repositories or organizations.

Mitigation: Confirm the GitHub account context before use and prefer repository-scoped commands such as `--repo owner/repo`.

Risk: Advanced `gh api` requests can access or change GitHub resources beyond the common issue, pull request, and run commands.

Mitigation: Review each `gh api` request before execution, especially when the account has private repository or organization access.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub CLI commands, `gh api` requests, and JSON output filtering examples.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server release evidence, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
