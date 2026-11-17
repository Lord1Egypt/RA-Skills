## Description:

Golang OpenAPI/Swagger documentation with swaggo/swag: annotation comments, swag init code generation, framework integrations, security definitions, and struct tags for Go API projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add, maintain, or audit Swagger/OpenAPI documentation in Go services that use swaggo/swag and common HTTP frameworks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs the third-party swag CLI using a mutable @latest version.

Mitigation: Pin swag to a specific reviewed version before use in controlled or production repositories.

Risk: The skill may edit Go project files and run go or swag tooling in the target repository.

Mitigation: Run it in a repository-scoped environment without unnecessary secrets and review diffs and commands before accepting changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-swagger)
- [Source homepage](https://github.com/samber/cc-skills-golang)
- [swag CLI reference](references/swag-cli.md)
- [swaggo/swag issue tracker](https://github.com/swaggo/swag/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Go code blocks, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include edits to Go source files, Swagger annotations, generated-docs commands, and framework-specific route wiring.]

## Skill Version(s):

1.1.0 (source: server release evidence, artifact frontmatter, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
