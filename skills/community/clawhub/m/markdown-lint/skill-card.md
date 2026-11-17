## Description:

Check markdown files for common issues including heading structure, link validity, list formatting, trailing whitespace, and code block language tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation maintainers, and agents use this skill to lint Markdown files and directories before reviews, commits, onboarding audits, or CI checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive directory linting on untrusted folders may encounter unknown symbolic links before symlink containment or cycle handling is added.

Mitigation: Avoid running recursive directory mode on untrusted repositories or folders that may contain unknown symbolic links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/markdown-lint)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON lint results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports errors, warnings, affected files, line and column numbers, rule identifiers, messages, summaries, and exit codes.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
