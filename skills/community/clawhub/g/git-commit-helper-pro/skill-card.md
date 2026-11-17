## Description:

Automatically generates standardized Git commit messages by analyzing staged Git changes, supporting Chinese and English output in Conventional Commits format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oct1st85](https://clawhub.ai/user/oct1st85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to draft Conventional Commit messages from staged Git changes before committing code. It is useful for routine development, team workflows, open-source contributions, review preparation, and keeping commit history consistent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commit messages can misstate code changes because the implementation analyzes staged file names and change counts rather than full code semantics.

Mitigation: Review and edit the generated message before using it in a commit.

Risk: Installing with an unpinned latest installer command can change installer behavior over time.

Mitigation: Use a trusted or pinned ClawHub installer version when installing from the README.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oct1st85/skills/git-commit-helper-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style commit message text with a Conventional Commits title and optional bullet body]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese or English language selection and analyzes staged Git diff statistics.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
