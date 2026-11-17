## Description:

Guides agents to write, review, and audit idiomatic Go error handling, including error creation, wrapping, inspection, joining, panic/recover boundaries, and structured logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to have an agent create, review, or audit Go code for robust error handling, structured logging, and production-safe propagation patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-proposed Go edits or audit findings may introduce incorrect behavior if accepted without review.

Mitigation: Review proposed diffs, run relevant Go tests, and confirm error-handling changes match project conventions before merging.

Risk: The skill can invoke Go, lint, and git commands during coding or audit workflows.

Mitigation: Confirm command scope before execution and inspect command output before using it to change source code.

Risk: Parallel sub-agent audits can surface noisy or overlapping findings across error creation, wrapping, logging, and panic/recover categories.

Mitigation: Consolidate findings, deduplicate issues, and validate each recommendation against the local code path before remediation.

## Reference(s):

- [Project homepage](https://github.com/samber/cc-skills-golang)
- [Error Creation](references/error-creation.md)
- [Error Handling Patterns and Logging](references/error-handling.md)
- [Error Wrapping and Inspection](references/error-wrapping.md)
- [samber/oops](https://github.com/samber/oops)
- [log/slog package](https://pkg.go.dev/log/slog)
- [samber/slog-http](https://github.com/samber/slog-http)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with Go code examples, audit findings, and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to Go files, run Go/lint/git command suggestions, and coordinate sub-agent audits; review outputs before applying.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
