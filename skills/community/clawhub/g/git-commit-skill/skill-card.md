## Description:

Analyzes Git working tree changes, proposes a Gitmoji commit message, checks for likely sensitive information, and helps an agent stage, commit, and optionally push after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tedburner](https://clawhub.ai/user/tedburner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn current repository changes into reviewed Gitmoji commit messages and user-approved Git commit actions. It is intended for repositories where an agent may inspect diffs and run Git commands after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may inspect repository diffs that contain secrets, credentials, or environment files.

Mitigation: Review detected sensitive files and diff content before allowing the workflow to continue.

Risk: Staging, committing, or pushing the wrong files can publish unintended changes.

Mitigation: Require explicit user confirmation for the generated commit message, staged file list, commit action, and optional push.

## Reference(s):

- [Gitmoji reference](references/gitmojis.md)
- [ClawHub skill page](https://clawhub.ai/tedburner/skills/git-commit-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with inline Git commands and commit message blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before staging, committing, or pushing changes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
