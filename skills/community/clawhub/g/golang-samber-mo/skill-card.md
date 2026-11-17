## Description:

Monadic types for Golang using samber/mo: Option, Result, Either, Future, IO, Task, and State types for type-safe nullable values, error handling, and functional composition with pipeline sub-packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill when adopting or maintaining Go code that imports github.com/samber/mo and needs guidance on monadic Option, Result, Either, Future, IO, Task, State, and pipeline patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to propose commands or code changes that affect a Go project, including go get, git operations, database writes, file reads, or HTTP calls.

Mitigation: Review proposed commands and generated code before execution, and apply changes in a controlled branch or disposable environment when project state matters.

Risk: The skill is documentation guidance and is not a substitute for current package, vulnerability, or codebase-specific checks.

Mitigation: Verify package facts with pkg.go.dev or the recommended Go tooling before relying on version, API, importer, or vulnerability details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-samber-mo)
- [Publisher profile](https://clawhub.ai/user/samber)
- [Skill homepage](https://github.com/samber/cc-skills-golang)
- [pkg.go.dev/github.com/samber/mo](https://pkg.go.dev/github.com/samber/mo)
- [github.com/samber/mo](https://github.com/samber/mo)
- [Functional Programming and Monads in Go](references/monads-guide.md)
- [Option[T] API Reference](references/option.md)
- [Result[T] API Reference](references/result.md)
- [Either[L, R] API Reference](references/either.md)
- [Pipeline Sub-Packages Reference](references/pipelines.md)
- [Advanced Types Reference](references/advanced-types.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Go code snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend Go package installation, Go code changes, and project-specific checks when requested by the user.]

## Skill Version(s):

1.1.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
