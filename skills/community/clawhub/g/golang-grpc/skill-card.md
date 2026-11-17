## Description:

Provides gRPC usage guidelines, protobuf organization, and production-ready patterns for Golang microservices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement, review, and debug Go gRPC services and clients, including protobuf layout, code generation, interceptors, error handling, TLS or mTLS, graceful shutdown, streaming, and bufconn tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to run Go or protobuf tooling, fetch documentation, install dependencies, edit Go files, or use git commands.

Mitigation: Review proposed commands, generated files, dependency installs, and repository changes before allowing them in sensitive projects.

Risk: Incorrect or incomplete gRPC guidance could affect production behavior, including status codes, deadlines, authentication, TLS or mTLS, reflection, health checks, and graceful shutdown.

Mitigation: Validate generated code and advice against project requirements, run focused tests, and confirm security-sensitive settings before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-grpc)
- [Project homepage](https://github.com/samber/cc-skills-golang)
- [Protobuf & Code Generation Reference](references/protoc-reference.md)
- [gRPC Testing Reference](references/testing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Go, protobuf, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for Go gRPC projects and may include review findings, implementation patterns, generated-command recommendations, and configuration snippets.]

## Skill Version(s):

1.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
