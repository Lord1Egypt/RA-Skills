## Description: <br>
Dependency injection guidance for Go projects using samber/do v2, covering service containers, lifecycle management, scopes, health checks, graceful shutdown, testing, and module organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add or maintain samber/do v2 dependency injection in Go codebases. It helps agents propose service registration, composition-root organization, lifecycle hooks, scopes, testing overrides, health checks, graceful shutdown, and related Go tooling commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated dependency-injection changes can alter service wiring, lifecycle behavior, or go.mod dependencies in a Go project. <br>
Mitigation: Review go.mod, provider registration, scope, lifecycle, and shutdown changes; run the relevant Go tests and linters before relying on the result. <br>
Risk: Guidance or code examples may be applied to the wrong samber/do major version. <br>
Mitigation: Use samber/do v2 import paths and verify generated code does not import github.com/samber/do without the /v2 suffix. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-samber-do) <br>
- [Skill Homepage](https://github.com/samber/cc-skills-golang) <br>
- [samber/do v2 Go Package](https://pkg.go.dev/github.com/samber/do/v2) <br>
- [samber/do Documentation](https://do.samber.dev) <br>
- [samber/do Repository](https://github.com/samber/do) <br>
- [Advanced Usage](references/advanced.md) <br>
- [Testing with samber/do](references/testing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Go code examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include go get, go test, and golangci-lint commands when implementation work is requested.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and skill frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
