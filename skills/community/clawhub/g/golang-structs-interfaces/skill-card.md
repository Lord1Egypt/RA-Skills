## Description:

Golang struct and interface design patterns - composition, embedding, type assertions, type switches, interface segregation, dependency injection via interfaces, struct field tags, and pointer vs value receivers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design Go structs and interfaces, choose receiver styles, apply composition and embedding, and handle type assertions, field tags, generics, dependency injection, and compile-time interface checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose edits to Go source files.

Mitigation: Review proposed diffs before accepting them, especially changes to public interfaces, receiver types, serialization tags, and dependency boundaries.

Risk: The skill can suggest or run Go, golangci-lint, and git commands in compatible coding harnesses.

Mitigation: Review command intent and scope before execution, and avoid approving git operations that stage, commit, or rewrite unrelated work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-structs-interfaces)
- [Publisher profile](https://clawhub.ai/user/samber)
- [Project homepage](https://github.com/samber/cc-skills-golang)
- [Go sync noCopy reference](https://pkg.go.dev/sync#noCopy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Go code examples and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Go file edits and Go tooling commands when used in a coding harness.]

## Skill Version(s):

1.2.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
