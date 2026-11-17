## Description:

Reviews Go code for idiomatic patterns, error handling, concurrency safety, and common mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Go changes with version-aware checks for error handling, concurrency safety, interfaces, resources, naming, and style before reporting findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a sibling review-verification-protocol skill that can affect the review process.

Mitigation: Confirm that the sibling verification skill is present, trusted, and reviewed before relying on this workflow.

Risk: The skill may produce incorrect or misleading code review findings if applied without reading the target code context and Go version baseline.

Mitigation: Require reviewers to record the go.mod baseline, read enclosing code context, scope relevant checklist blocks, and complete pre-report verification before reporting findings.

## Reference(s):

- [Error Handling](references/error-handling.md)
- [Concurrency](references/concurrency.md)
- [Interfaces and Types](references/interfaces.md)
- [Common Mistakes](references/common-mistakes.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review findings with file and line references, severity, and concise descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are gated by the detected go.mod version and by referenced checklist blocks.]

## Skill Version(s):

2.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
