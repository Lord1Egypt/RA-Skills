## Description:

Safely initialize, sanitize, commit, create, and push a local project with private runtime data to a separate private GitHub repository. Use when the user asks to back up or upload a local data-bearing project to a private GitHub repo while keeping public Skills separate. Never uploads credentials, environments, caches, or public Skill source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this workflow to back up a specifically scoped local project to a separate private GitHub repository while excluding credentials, environments, caches, and public Skill source. It requires explicit scope and approval before uploading sensitive runtime data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recovery instruction permits a forced remote rollback despite the stated prohibition, which could remove others’ commits.

Mitigation: Review the recovery instructions before use. Do not force-reset over history that may belong to others; stop if ownership or the last known good commit is uncertain.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/haiyangchenbj/skills/private-github-repo-upload)
- [Publisher profile](https://clawhub.ai/user/haiyangchenbj)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown workflow with shell commands and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scope, exclusions, and repository details must be explicit or use a documented default confirmed by the user.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
