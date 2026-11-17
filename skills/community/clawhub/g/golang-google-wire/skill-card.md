## Description:

Provides guidance for using google/wire compile-time dependency injection in Go projects, including provider sets, injectors, interface bindings, struct providers, values, cleanup functions, generated files, code generation, and testing patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when adopting or maintaining google/wire in Go codebases. It helps agents explain dependency graph design, update provider sets and injectors, regenerate wire_gen.go, and troubleshoot common compile-time DI errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing Wire with @latest can change the code generator version used by a project.

Mitigation: Pin github.com/google/wire/cmd/wire to an approved version in stricter environments.

Risk: Wire code generation rewrites generated Go files in the working tree.

Mitigation: Run generation in a least-privileged development or CI context and review diffs before committing generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-google-wire)
- [cc-skills-golang repository](https://github.com/samber/cc-skills-golang)
- [google/wire package documentation](https://pkg.go.dev/github.com/google/wire)
- [google/wire repository](https://github.com/google/wire)
- [google/wire user guide](https://github.com/google/wire/blob/main/docs/guide.md)
- [google/wire best practices](https://github.com/google/wire/blob/main/docs/best-practices.md)
- [Advanced google/wire reference](references/advanced.md)
- [google/wire recipes](references/recipes.md)
- [google/wire testing guidance](references/testing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Go code examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to Go source files, injector files, provider sets, generated-code workflow, and CI checks.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
