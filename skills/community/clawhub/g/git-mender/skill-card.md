## Description:

git-mender helps an agent read a GitHub issue, analyze the target repository, implement a fix, verify the change, and prepare a pull request after user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4ydx3906](https://clawhub.ai/user/4ydx3906)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to work from a GitHub issue URL through repository analysis, code changes, local verification, and pull request preparation. It is intended for issue-fix workflows where the user can review diffs and approve any push or pull request creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read untrusted GitHub issue content and use it to guide repository changes.

Mitigation: Use it only with repositories and issue authors you trust, or run it in a disposable or sandboxed development environment.

Risk: The skill can edit repositories and run repository-defined commands such as tests or linters on the user's machine.

Mitigation: Review proposed commands and inspect diffs before accepting changes or allowing follow-up actions.

Risk: The skill can push branches and create pull requests after approval.

Mitigation: Confirm the target repository, branch, pull request text, and final diff before approving any push or pull request creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/4ydx3906/skills/git-mender)
- [GitHub CLI](https://cli.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks, code diffs, commit messages, and pull request text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GitHub issue URL; push and pull request creation are gated on user approval.]

## Skill Version(s):

1.1.0 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
