## Description:

Go application architecture with net/http 1.22+ routing, project structure patterns, graceful shutdown, and dependency injection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, scaffold, or review Go web servers with standard-library routing, explicit dependency injection, production shutdown behavior, and maintainable project structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example API, database, email, and shutdown snippets could be copied into production without adapting routes, timeouts, secrets handling, or data-mutating behavior.

Mitigation: Review and test adapted code before deployment, especially routes that mutate or delete application data.

Risk: Guidance that uses Go 1.22+ ServeMux features may be incompatible with projects pinned to older Go toolchains.

Mitigation: Check `go version` before applying method-and-path patterns, `r.PathValue`, or wildcard routing, and use compatible routing patterns when the toolchain is older than Go 1.22.

## Reference(s):

- [Dependency Injection in Go](references/dependency-injection.md)
- [Graceful Shutdown](references/graceful-shutdown.md)
- [Go Project Structure](references/project-structure.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Go code examples and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
