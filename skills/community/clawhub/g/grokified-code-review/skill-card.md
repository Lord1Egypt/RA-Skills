## Description:

Review a git diff for bugs, security issues and missing tests with the grok-build-0.1 model through the Grokified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imfaisii](https://clawhub.ai/user/imfaisii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to get a second-opinion review of local git changes, branches, or commits for bugs, security issues, and missing tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed git diffs are sent to a third-party API; filename-based exclusions do not catch secrets in ordinary source files.

Mitigation: Inspect the diff before sending and do not use the skill on changes containing secrets, customer data, private keys, or code that cannot be shared with third-party model APIs.

Risk: Review findings can be inaccurate because the model sees the diff rather than the full repository.

Mitigation: Verify findings against the code and run relevant tests before making changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/imfaisii/skills/grokified-code-review)
- [Grokified documentation](https://grokified.com/docs)
- [Grokified models](https://grokified.com/docs/models)
- [Grokified homepage](https://grokified.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain-text code review with findings and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include file, diff line, severity, issue, and suggested fix; reports no issues found if none are identified.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
