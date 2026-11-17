## Description:

Guides agents in designing and refactoring Go dependency injection using manual constructor injection and comparisons of google/wire, uber-go/dig, uber-go/fx, and samber/do.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose, implement, test, or refactor dependency injection patterns in Go services and applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Go wiring or refactor edits could introduce incorrect architecture changes or regressions in an important codebase.

Mitigation: Review generated code changes, run Go tests and linting, and apply refactors incrementally.

Risk: DI library APIs can change, especially for google/wire, uber-go/dig, uber-go/fx, and samber/do examples.

Mitigation: Check the official library documentation before relying on exact API signatures or generated code.

Risk: Large refactors may require broad source inspection and helper-agent analysis.

Mitigation: Limit the work to the intended Go project scope and review the consolidated migration plan before applying edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-dependency-injection)
- [Skill homepage](https://github.com/samber/cc-skills-golang)
- [Manual Constructor Injection](references/manual-di.md)
- [google/wire - Compile-Time Code Generation](references/google-wire.md)
- [samber/do - Generics-Based DI](references/samber-do.md)
- [uber-go/dig + uber-go/fx - Reflection-Based DI](references/uber-dig-fx.md)
- [samber/do documentation](https://do.samber.dev)
- [samber/do GitHub repository](https://github.com/samber/do)
- [google/wire user guide](https://github.com/google/wire/blob/main/docs/guide.md)
- [uber-go/fx documentation](https://uber-go.github.io/fx/)
- [uber-go/dig GitHub repository](https://github.com/uber-go/dig)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single response stream; may include migration plans, wiring code, tests, and DI library selection guidance.]

## Skill Version(s):

1.3.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
