## Description: <br>
Implements dependency injection in Golang using uber-go/dig, including reflection-based containers, Provide/Invoke, dig.In/dig.Out parameter and result objects, named values, value groups, optional dependencies, scopes, and Decorate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to wire Go applications with uber-go/dig, including constructor registration, graph invocation, parameter and result objects, named values, value groups, scopes, decorators, and graph validation patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose Go source changes, dependency updates, or Git commands as part of wiring uber-go/dig. <br>
Mitigation: Review generated code, go.mod/go.sum changes, and Git commands before committing or pushing. <br>
Risk: Incorrect dependency injection wiring can hide missing providers, cycles, or unintended service-locator patterns until startup or test time. <br>
Mitigation: Validate the graph with tests, keep the container at the composition root, and inspect constructor errors before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-uber-dig) <br>
- [Publisher profile](https://clawhub.ai/user/samber) <br>
- [Source homepage](https://github.com/samber/cc-skills-golang) <br>
- [uber-go/dig documentation](https://pkg.go.dev/go.uber.org/dig) <br>
- [uber-go/dig repository](https://github.com/uber-go/dig) <br>
- [Advanced uber-go/dig reference](references/advanced.md) <br>
- [uber-go/dig recipes](references/recipes.md) <br>
- [Testing with uber-go/dig](references/testing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Go code examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Go source edits, go.mod/go.sum changes, go test commands, and git commands for review.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
