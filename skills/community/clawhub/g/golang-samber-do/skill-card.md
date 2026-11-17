## Description:

Dependency injection in Golang using samber/do: service containers, lifecycle management, scopes, health checks, graceful shutdown, and module organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when adopting or maintaining samber/do in Go projects, especially when setting up dependency injection containers, service lifecycles, package registration, testing overrides, health checks, and graceful shutdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to edit Go files, run Go tooling, or add github.com/samber/do/v2 to a module.

Mitigation: Review Go source changes, go.mod, and go.sum, and run the project's normal Go tests before accepting dependency-injection changes.

Risk: Using the wrong samber/do import path or lifecycle pattern can create incorrect dependency-injection behavior.

Mitigation: Verify generated code uses github.com/samber/do/v2, keeps container access at the composition root, and follows the skill's service lifecycle guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-samber-do)
- [Skill homepage](https://github.com/samber/cc-skills-golang)
- [pkg.go.dev samber/do v2](https://pkg.go.dev/github.com/samber/do/v2)
- [samber/do documentation](https://do.samber.dev)
- [samber/do source repository](https://github.com/samber/do)
- [Advanced Usage](references/advanced.md)
- [Testing with samber/do](references/testing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Go code examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Go file edits and Go module dependency changes when requested by the user.]

## Skill Version(s):

1.3.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
