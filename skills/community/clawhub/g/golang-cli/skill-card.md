## Description: <br>
Supports developers building, modifying, or reviewing Go CLI tools, including command structure, flags, configuration layering, version embedding, exit codes, I/O patterns, signal handling, shell completion, argument validation, and CLI unit testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build, extend, and review Go command-line applications with predictable command trees, flags, configuration, output behavior, signal handling, completions, and tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to edit Go source files or run Go, golangci-lint, and git commands. <br>
Mitigation: Review generated changes and proposed git actions before applying them. <br>
Risk: CLI guidance can produce incorrect behavior around flags, configuration, exit codes, or stdout and stderr handling if applied without project context. <br>
Mitigation: Run the project's tests, CLI-specific tests, and linting after changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-cli) <br>
- [Source Homepage](https://github.com/samber/cc-skills-golang) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Go code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose source edits and Go toolchain, golangci-lint, or git commands for user review.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
