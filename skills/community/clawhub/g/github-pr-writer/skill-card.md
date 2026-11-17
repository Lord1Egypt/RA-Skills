## Description:

Write clear, structured GitHub pull request descriptions using a standardized template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft or update GitHub pull request descriptions from branch diffs, commit history, and provided change context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect branch diffs and commit history, which can contain private implementation details or sensitive issue references.

Mitigation: Review the generated pull request description before publishing it, especially for private repositories.

Risk: Generated pull request descriptions can omit important testing gaps, impact details, or breaking changes if the repository context is incomplete.

Mitigation: Verify every section of the PR template against the actual code changes before sharing or submitting the description.

## Reference(s):

- [GitHub PR Writer on ClawHub](https://clawhub.ai/djc00p/skills/github-pr-writer)
- [Pull Request Template](artifact/assets/pull_request_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown pull request description with optional shell commands for gathering repository context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git and GitHub CLI when collecting repository context from a local branch.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
