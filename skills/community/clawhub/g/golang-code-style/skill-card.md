## Description: <br>
Golang code style conventions for line length, variable declarations, control flow clarity, and useful comments when writing or reviewing Go code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to apply opinionated Go style guidance during implementation and review. It helps improve readability across line breaking, variable initialization, control flow, function design, collection handling, and file organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Style-driven edits can change Go source files or produce recommendations that should not be accepted blindly. <br>
Mitigation: Review diffs, run the relevant Go tests or checks, and confirm that readability changes preserve intended behavior. <br>
Risk: The skill can run Go, golangci-lint, git, and sub-agent review workflows in a repository. <br>
Mitigation: Use it only in repositories where those actions are appropriate and inspect proposed commands before execution. <br>


## Reference(s): <br>
- [Code Style Details](references/details.md) <br>
- [Source Homepage](https://github.com/samber/cc-skills-golang) <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-code-style) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with Go code examples and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or make source edits and may run Go, golangci-lint, git, or sub-agent review workflows when appropriate.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
