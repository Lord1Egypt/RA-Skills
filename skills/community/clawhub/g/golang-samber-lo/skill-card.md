## Description:

Helps agents work with Go code that uses samber/lo functional helpers, including package selection, API usage, performance tradeoffs, and safer alternatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to read, write, refactor, and review Go code that imports github.com/samber/lo or could benefit from functional collection transforms. It helps choose between core lo helpers, stdlib alternatives, parallel or mutable variants, lazy iterators, and related samber packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest dependency changes or edits to Go source files.

Mitigation: Review generated diffs, run the project's Go tests and linters, and confirm dependency changes before merging.

Risk: Mutable, parallel, lazy, and experimental samber/lo variants can change behavior, require newer Go versions, or add performance tradeoffs.

Mitigation: Prefer stdlib or core lo helpers by default, check the module's Go version, and use profiling evidence before adopting lom, lop, loi, or experimental SIMD helpers.

Risk: Panic-oriented helpers such as lo.Must can be unsafe in request-handling or long-running production paths.

Mitigation: Use non-Must variants with explicit error handling outside tests, initialization, or intentional startup-failure paths.

## Reference(s):

- [Package Guide](references/package-guide.md)
- [API Reference](references/api-reference.md)
- [Advanced Patterns](references/advanced-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/samber/skills/golang-samber-lo)
- [Skill Source Homepage](https://github.com/samber/cc-skills-golang)
- [samber/lo GitHub Repository](https://github.com/samber/lo)
- [samber/lo Documentation](https://lo.samber.dev)
- [pkg.go.dev github.com/samber/lo](https://pkg.go.dev/github.com/samber/lo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Go dependency commands and code edits; review generated changes before applying them.]

## Skill Version(s):

1.2.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
