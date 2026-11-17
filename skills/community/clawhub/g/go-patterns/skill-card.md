## Description:

Go language patterns for 2026 - concurrency with errgroup, error wrapping, HTTP servers, gRPC, database access, testing, and CLI with Cobra.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msruruguay](https://clawhub.ai/user/msruruguay)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as a Go reference for backend patterns, including concurrency, context propagation, HTTP servers, PostgreSQL access, gRPC, testing, CLI tools, and profiling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example HTTP client code may be copied without response status checks, response-size limits, or production timeout configuration.

Mitigation: Treat snippets as starting points; add status validation, bounded reads, and explicit client timeout settings before production use.

## Reference(s):

- [Effective Go](https://go.dev/doc/effective_go)
- [Context Best Practices](https://go.dev/blog/context)
- [Error Handling in Go 1.13+](https://go.dev/blog/go1.13-errors)
- [Chi Router](https://github.com/go-chi/chi)
- [pgx Documentation](https://github.com/jackc/pgx)
- [gRPC in Go](https://grpc.io/docs/languages/go/)
- [Cobra CLI](https://github.com/spf13/cobra)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Go code snippets and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference material only; no executable payload. Review and adapt snippets before production use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
