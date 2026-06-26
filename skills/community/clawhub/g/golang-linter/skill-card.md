## Description: <br>
Provides Go linting guidance, golangci-lint configuration support, lint output interpretation, and disciplined nolint suppression practices for Go projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure and run golangci-lint, interpret lint findings, apply safe suppressions, and maintain Go code quality workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lint auto-fix commands and parallel cleanup can change repository code. <br>
Mitigation: Run code-changing lint actions on a branch, prefer targeted paths where possible, and review git diffs and tests before accepting changes. <br>
Risk: Incorrect or overly broad nolint suppressions can hide real correctness, security, or resource-management issues. <br>
Mitigation: Require linter-specific nolint directives with justification, and avoid suppressing security and resource-leak linters without strong review. <br>


## Reference(s): <br>
- [Golang Linter on ClawHub](https://clawhub.ai/samber/golang-linter) <br>
- [Source homepage](https://github.com/samber/cc-skills-golang) <br>
- [Linter Reference](artifact/references/linter-reference.md) <br>
- [Nolint Directives](artifact/references/nolint-directives.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, Go, YAML, and Makefile snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend code-changing lint fix commands and configuration changes that should be reviewed before acceptance.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
