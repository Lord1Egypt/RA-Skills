## Description: <br>
Linting best practices and golangci-lint configuration for Golang projects, including running linters, configuring .golangci.yml, suppressing warnings with nolint directives, interpreting lint output, and selecting linters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to configure golangci-lint, interpret Go lint findings, apply safe fixes, and decide when lint warnings should be fixed or narrowly suppressed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autofix and legacy cleanup workflows may modify many Go files or configuration files. <br>
Mitigation: Review generated diffs before committing, and prefer scoped lint runs or batched cleanup for large repositories. <br>
Risk: Incorrect suppression guidance can hide real correctness, security, or resource-leak findings. <br>
Mitigation: Require specific nolint directives with justifications, and fix security and correctness findings unless there is a documented false positive. <br>


## Reference(s): <br>
- [Golang Lint ClawHub page](https://clawhub.ai/samber/golang-lint) <br>
- [Publisher profile](https://clawhub.ai/user/samber) <br>
- [Project homepage](https://github.com/samber/cc-skills-golang) <br>
- [Linter Reference](references/linter-reference.md) <br>
- [Nolint Directives](references/nolint-directives.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Go, YAML, Makefile, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file edits and golangci-lint commands; users should review generated code and configuration changes before committing.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
