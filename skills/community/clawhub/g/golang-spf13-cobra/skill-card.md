## Description:

Guides agents working on Go command-line applications that use spf13/cobra, including command trees, RunE hooks, argument validators, flags, completions, documentation generation, and test patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to build, extend, or review Go CLIs that use spf13/cobra. It helps produce idiomatic command definitions, argument validation, flag handling, completions, generated docs, and testable command handlers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Go module or tool installation commands may use latest third-party versions.

Mitigation: Pin Go module and tool versions, then review `go.mod` and `go.sum` changes before committing or deploying.

Risk: Scaffolding or generated commands can modify project files in ways that affect CLI behavior.

Mitigation: Run commands in normal project directories without elevated privileges and review the resulting diffs and tests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-spf13-cobra)
- [Publisher profile](https://clawhub.ai/user/samber)
- [Skill homepage](https://github.com/samber/cc-skills-golang)
- [Cobra package documentation](https://pkg.go.dev/github.com/spf13/cobra)
- [Cobra GitHub repository](https://github.com/spf13/cobra)
- [Cobra documentation site](https://cobra.dev)
- [Cobra commands, hooks, and args validators](references/commands-and-args.md)
- [Cobra flags reference](references/flags.md)
- [Cobra shell completions reference](references/completions.md)
- [Cobra documentation and scaffolding generators](references/generators.md)
- [Testing Cobra commands](references/testing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits, command snippets, tests, and review findings for Go projects using spf13/cobra.]

## Skill Version(s):

1.1.0 (source: artifact frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
