## Description: <br>
Defensive Golang coding to prevent panics, silent data corruption, and subtle runtime bugs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review and edit Go code for nil-safety, slice and map aliasing, numeric conversion, resource lifecycle, and zero-value design issues. It is intended for Go projects where an agent should produce safer code, review findings, or scoped Go-related commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose repository edits and scoped Go, linter, or git commands. <br>
Mitigation: Review proposed changes and commands before applying them in important repositories. <br>
Risk: Some guidance depends on the target project's Go version, such as range-loop scoping and reflection type assertions. <br>
Mitigation: Check the project's go.mod version and available Go toolchain before applying version-specific recommendations. <br>


## Reference(s): <br>
- [Nil Safety Deep Dive](references/nil-safety.md) <br>
- [Slice and Map Safety Deep Dive](references/slice-map-safety.md) <br>
- [cc-skills-golang homepage](https://github.com/samber/cc-skills-golang) <br>
- [Golang Safety on ClawHub](https://clawhub.ai/samber/golang-safety) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Go code examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository edits and scoped Go, golangci-lint, and git commands.] <br>

## Skill Version(s): <br>
1.2.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
