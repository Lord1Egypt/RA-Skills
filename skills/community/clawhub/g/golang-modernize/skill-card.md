## Description:

Modernize Golang code to use recent language features, standard library improvements, and idiomatic patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review and modernize Go projects with version-aware language, standard library, testing, security, and CI/tooling improvements. It supports contextual suggestions during active development and broader modernization scans when explicitly invoked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated modernization changes can be broad and may affect behavior across a Go codebase.

Mitigation: Use explicit full-scan mode for repository-wide work and review the generated worktree before merging changes.

Risk: Toolchain or dependency updates may introduce compatibility changes.

Mitigation: Approve updates only after checking resolved versions, changelogs, and test results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-modernize)
- [Project homepage](https://github.com/samber/cc-skills-golang)
- [Go Version Modernizations](references/versions.md)
- [Tooling Modernization](references/tooling.md)
- [Go 1.21 Release Notes](https://go.dev/doc/go1.21)
- [Go 1.22 Release Notes](https://go.dev/doc/go1.22)
- [Go 1.23 Release Notes](https://go.dev/doc/go1.23)
- [Go 1.24 Release Notes](https://go.dev/doc/go1.24)
- [Go 1.25 Release Notes](https://go.dev/doc/go1.25)
- [Go 1.26 Release Notes](https://go.dev/doc/go1.26)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Go code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or apply codebase-wide modernization edits in an isolated worktree when explicitly invoked.]

## Skill Version(s):

1.3.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
