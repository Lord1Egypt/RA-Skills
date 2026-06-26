## Description: <br>
Provides a guide for setting up Golang project layouts and workspaces. Use when starting a new Go project, organizing an existing codebase, setting up a monorepo with multiple packages, creating CLI tools with multiple main packages, deciding between cmd/internal/pkg directory conventions, or discussing package restructuring, package splits, or module splits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan or revise Go project structure, including module naming, cmd/internal/pkg boundaries, test placement, application configuration, and go.work workspace use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to edit Go project files or run Go-related commands. <br>
Mitigation: Review generated diffs and command output before committing or releasing changes. <br>
Risk: Project-structure guidance can be misapplied if the agent over-structures a small project or assumes architecture preferences. <br>
Mitigation: Confirm project scope, architecture preference, and dependency-injection approach before applying layout changes. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/samber/cc-skills-golang) <br>
- [12-Factor App](https://12factor.net/) <br>
- [Directory Layouts](references/directory-layouts.md) <br>
- [Application Configuration with Cobra + Viper](references/config.md) <br>
- [Tests, Benchmarks, and Examples](references/testing-layout.md) <br>
- [Go Workspaces for Multi-Package Repositories](references/workspaces.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Go file tree examples, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask clarifying questions about architecture and dependency injection choices before proposing project structure.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
