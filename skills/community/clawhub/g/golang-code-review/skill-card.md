## Description:

Provides Go code review support by checking formatting, quality, best practices, and security concerns, then producing Markdown review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[knifean](https://clawhub.ai/user/knifean)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review Go changes for formatting, static-analysis findings, best-practice issues, security concerns, and actionable remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional setup commands install Go tools with @latest, which can change behavior over time.

Mitigation: Pin tool versions before installation when repeatable review behavior is required.

Risk: Formatting commands such as gofmt -w can rewrite local files.

Mitigation: Review diffs before committing formatter changes and run write-mode commands only in an intended workspace.

Risk: The optional Git hook can run checks and formatting automatically on future commits.

Mitigation: Install the hook only when automatic commit-time checks are desired and documented for the repository.

Risk: Documentation and generated review messages are primarily Chinese-language.

Mitigation: Install only where Chinese-language documentation and output are acceptable for reviewers.

## Reference(s):

- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Go Error Handling Best Practices](https://github.com/golang/go/wiki/ErrorHandlingBestPractices)
- [Effective Go](https://golang.org/doc/effective_go.html)
- [Staticcheck](https://staticcheck.io)
- [ClawHub Skill Page](https://clawhub.ai/knifean/skills/golang-code-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with issue summaries, severity labels, metrics, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Go tool commands and file-formatting recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
