## Description:

Guides agents in wiring Go applications with uber-go/dig, including Provide/Invoke, parameter and result objects, named values, value groups, optional dependencies, scopes, Decorate, and testing patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when adopting or maintaining uber-go/dig in Go services, especially to wire startup dependency graphs, choose dig versus fx, and avoid common dependency-injection mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Go wiring guidance or file edits could introduce incorrect dependency graph behavior if applied without review.

Mitigation: Review proposed changes before applying them and validate wiring with tests such as dig.DryRun where appropriate.

Risk: Suggested commands such as go get, git operations, or graph file generation can modify dependencies or local files.

Mitigation: Run commands only in the intended repository and inspect diffs before committing or deploying.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samber/skills/golang-uber-dig)
- [ClawHub Publisher Profile](https://clawhub.ai/user/samber)
- [OpenClaw Homepage](https://github.com/samber/cc-skills-golang)
- [pkg.go.dev/go.uber.org/dig](https://pkg.go.dev/go.uber.org/dig)
- [uber-go/dig GitHub Repository](https://github.com/uber-go/dig)
- [Advanced uber-go/dig Guidance](references/advanced.md)
- [uber-go/dig Recipes](references/recipes.md)
- [Testing with uber-go/dig](references/testing.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown responses with Go code examples and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose code edits, dependency commands, and graph-validation patterns for Go projects using uber-go/dig.]

## Skill Version(s):

1.2.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
