## Description:

Safely initialize, sanitize, commit, create, and push a local project with private runtime data to a separate private GitHub repository. Use when the user asks to back up or upload a local data-bearing project to a private GitHub repo while keeping public Skills separate. Never uploads credentials, environments, caches, or public Skill source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project owners use this workflow to back up a clearly scoped, data-bearing local project to a private GitHub repository while keeping public Skill source separate. It guides scope selection, sensitive-file exclusions, staging review, and remote verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is limited by four unresolved local references and partial scan coverage.

Mitigation: Before installing or following the workflow, inspect the unresolved references and review the skill's behavior; the benign scanner verdict is not a guarantee of safety.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/haiyangchenbj/skills/private-github-repo-upload)
- [Publisher profile](https://clawhub.ai/user/haiyangchenbj)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls]

**Output Format:** [Markdown workflow guidance with shell commands and GitHub API procedures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scope, exclusions, and repository name must be explicit or confirmed; uploads and remote changes require user authorization.]

## Skill Version(s):

1.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
