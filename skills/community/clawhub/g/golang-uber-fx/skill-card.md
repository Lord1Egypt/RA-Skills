## Description:

Guides agents working on Go services that use go.uber.org/fx for application wiring, lifecycle hooks, modules, annotations, logging, testing, and related fx patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill when building, adopting, or refactoring Go services with uber-go/fx. It helps produce guidance, Go snippets, test patterns, and tool-aware recommendations for dependency graphs, lifecycle hooks, modules, annotations, logging, and graceful startup or shutdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broader agent powers than its Go fx guidance usually needs.

Mitigation: Review requested permissions before installation and restrict remote Git actions, outbound fetching, and delegated agents unless explicitly needed.

Risk: Suggested dependency or wiring changes can affect go.mod, go.sum, or service startup and shutdown behavior.

Mitigation: Pin and review go.uber.org/fx dependency changes, validate the fx graph in tests, and review lifecycle hooks before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-uber-fx)
- [Publisher profile](https://clawhub.ai/user/samber)
- [Skill homepage](https://github.com/samber/cc-skills-golang)
- [go.uber.org/fx package documentation](https://pkg.go.dev/go.uber.org/fx)
- [Uber Fx documentation](https://uber-go.github.io/fx/)
- [Uber Fx GitHub repository](https://github.com/uber-go/fx)
- [Advanced uber-go/fx reference](artifact/references/advanced.md)
- [uber-go/fx recipes](artifact/references/recipes.md)
- [Testing with uber-go/fx](artifact/references/testing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with Go code examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend Go tooling and documentation lookup when available; does not produce standalone artifacts unless the agent applies its guidance.]

## Skill Version(s):

1.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
