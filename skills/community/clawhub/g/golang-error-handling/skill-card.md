## Description: <br>
Guides agents to write, review, and audit idiomatic Go error handling, including wrapping, inspection, structured logging, panic boundaries, and production error context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill when creating, reviewing, or auditing Go code that returns, wraps, inspects, logs, or aggregates errors. It helps agents produce maintainable error paths, avoid duplicate logging, keep operational messages low-cardinality, and use Go error APIs consistently. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to edit repository files, run Go, golangci-lint, or git commands, and launch audit sub-agents. <br>
Mitigation: Use it only in trusted workspaces, review proposed commands and diffs before accepting changes, and keep normal repository safeguards such as tests and code review in place. <br>
Risk: Audit or review findings may be incomplete or overbroad when applied to large codebases or unfamiliar error-handling conventions. <br>
Mitigation: Scope audits to relevant packages, verify findings against the code, and treat generated guidance as review input rather than an automatic policy decision. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-error-handling) <br>
- [Project Homepage](https://github.com/samber/cc-skills-golang) <br>
- [Error Creation](references/error-creation.md) <br>
- [Error Wrapping and Inspection](references/error-wrapping.md) <br>
- [Error Handling Patterns and Logging](references/error-handling.md) <br>
- [samber/oops](https://github.com/samber/oops) <br>
- [slog package](https://pkg.go.dev/log/slog) <br>
- [samber/slog-http](https://github.com/samber/slog-http) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Analysis] <br>
**Output Format:** [Markdown guidance with Go code snippets and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or apply code edits and run Go, golangci-lint, or git commands when the host agent permits.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
