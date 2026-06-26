## Description: <br>
Idiomatic Golang design patterns covering functional options, constructors, error flow and cascading, resource management and lifecycle, graceful shutdown, resilience, architecture, dependency injection, data handling, streaming, and related production Go design choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent for idiomatic Go design guidance, review existing Go code for design issues, and implement patterns such as functional options, explicit constructors, resource cleanup, timeouts, streaming, and architecture boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to read and edit code and run Go, lint, and git commands in a repository. <br>
Mitigation: Use it only in Go repositories where normal coding-agent authority is acceptable, and review proposed edits and commands before applying them. <br>
Risk: Architecture and design-pattern advice can introduce unnecessary abstraction if applied without project context. <br>
Mitigation: Apply the skill's smallest-sufficient-pattern guidance and confirm architecture preferences before broad refactors. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-design-patterns) <br>
- [Project Homepage](https://github.com/samber/cc-skills-golang) <br>
- [Architecture Patterns](references/architecture.md) <br>
- [Clean Architecture in Go](references/clean-architecture.md) <br>
- [Data Handling Patterns](references/data-handling.md) <br>
- [Domain-Driven Design (DDD) in Go](references/ddd.md) <br>
- [Hexagonal Architecture (Ports & Adapters) in Go](references/hexagonal-architecture.md) <br>
- [Resource Management Patterns](references/resource-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Go code examples and optional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose code edits, Go commands, lint commands, git commands, and agent-assisted review steps when appropriate.] <br>

## Skill Version(s): <br>
1.1.4 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
