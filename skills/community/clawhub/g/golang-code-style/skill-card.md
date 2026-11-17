## Description:

Golang code style conventions for line breaking, variable declarations, control flow clarity, comments, and project coding standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill when writing or reviewing Go code for human-judged style concerns such as readability, control flow, function shape, collection initialization, and file organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests permission to edit Go project files while applying style guidance.

Mitigation: Use review-only, read-only, or approval-gated operation when evaluating untrusted repositories or when changes should remain advisory.

Risk: The skill may run Go, Git, and golangci-lint commands, which can execute repository-controlled code or perform repository operations.

Mitigation: Avoid remote Git operations, generators, tests, and linters for untrusted projects unless the commands are reviewed and approved.

Risk: The skill can delegate review work to agents for broad codebase style reviews.

Mitigation: Limit delegated reviews to clearly scoped Go files and review findings before applying any edits.

## Reference(s):

- [Code Style Details](references/details.md)
- [Project homepage](https://github.com/samber/cc-skills-golang)
- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-code-style)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown guidance with Go code snippets and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or apply edits to Go files when the host grants write or tool access.]

## Skill Version(s):

1.3.0 (source: ClawHub release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
