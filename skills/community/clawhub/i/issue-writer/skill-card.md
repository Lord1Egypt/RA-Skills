## Description:

Use when drafting, restructuring, reviewing, or submitting GitHub issues from investigation findings, bugs, security reviews, regressions, feature requests, or technical debt; selects the right issue shape and keeps evidence, impact, recommendations, and acceptance criteria appropriate to the issue type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiluoduyu](https://clawhub.ai/user/xiluoduyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to turn investigation notes, bugs, security findings, regressions, feature requests, or technical debt into structured GitHub issues with evidence, impact, recommendations, and acceptance criteria. When explicitly requested, it can help submit an issue after confirming repository details and reviewing sensitive content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated issue bodies may include private details, secrets, or excessive exploit detail when source findings contain sensitive information.

Mitigation: Review and redact issue bodies before posting, especially for security findings.

Risk: Optional submission can create GitHub issues using the user's existing GitHub authentication.

Mitigation: Submit only after confirming the target repository, title, labels, and issue body.

## Reference(s):

- [Bug Or Regression Issue Shape](references/bug-issue.md)
- [Epic Or Technical Debt Issue Shape](references/epic-issue.md)
- [Security Issue Shape](references/security-issue.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown issue drafts with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create GitHub issues only when explicitly requested and authenticated GitHub tooling is available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
