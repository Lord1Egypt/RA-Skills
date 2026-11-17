## Description:

Provides idiomatic Go design-pattern guidance for constructors, error flow, resource lifecycle, resilience, architecture, dependency injection, data handling, and streaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to choose and apply idiomatic Go patterns when designing APIs, reviewing existing code, or implementing production service structure. It helps an agent propose code, markdown guidance, and shell command suggestions for Go projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide or edit Go code and may suggest Go, lint, or git commands when the host permits tool use.

Mitigation: Review proposed code edits and commands before execution, especially in production repositories.

Risk: Design-pattern guidance can be misapplied, adding complexity to small Go projects.

Mitigation: Use the skill's project-size guidance and prefer the smallest pattern that satisfies the concrete requirement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-design-patterns)
- [Project homepage](https://github.com/samber/cc-skills-golang)
- [Architecture Patterns](references/architecture.md)
- [Clean Architecture in Go](references/clean-architecture.md)
- [Data Handling Patterns](references/data-handling.md)
- [Domain-Driven Design in Go](references/ddd.md)
- [Hexagonal Architecture in Go](references/hexagonal-architecture.md)
- [Resource Management Patterns](references/resource-management.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Go code examples and optional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed edits or commands scoped to Go files when the host agent allows those actions.]

## Skill Version(s):

1.2.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
