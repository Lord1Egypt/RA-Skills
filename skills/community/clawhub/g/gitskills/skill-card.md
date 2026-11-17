## Description:

Manages GitHub repositories, branches, pull requests, and issues through the GitHub API; it is not intended for repository cloning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to manage GitHub repositories, branches, pull requests, and issues with a token-authenticated GitHub API workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a GitHub token that may allow repository, pull request, issue, and branch changes.

Mitigation: Use a fine-grained token limited to the repositories and actions needed for the task.

Risk: Repository deletion is irreversible.

Mitigation: Review the target repository carefully and proceed only after the explicit deletion confirmation prompt.

Risk: Dependency vulnerability exposure can return if patched dependencies are downgraded or left stale.

Mitigation: Keep python-dotenv at the patched 1.0.1 version or newer before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and short text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided GITHUB_TOKEN with appropriate GitHub permissions.]

## Skill Version(s):

1.5.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
