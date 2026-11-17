## Description:

Analyzes repository changes, stages related files, and creates Conventional Commits messages and commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[return054](https://clawhub.ai/user/return054)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review changes, stage related files, and create descriptive Git commits using the Conventional Commits format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Staging changes could include unintended files or secrets in a commit.

Mitigation: Review git status and the staged diff before each commit; exclude sensitive files.

## Reference(s):

- [Git Conventional Commit on ClawHub](https://clawhub.ai/return054/skills/git-commit)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with Git commands and commit messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can stage files and create local Git commits; requires git.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
