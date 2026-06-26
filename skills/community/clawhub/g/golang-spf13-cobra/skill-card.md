## Description: <br>
Guides agents working on Go CLI projects that use spf13/cobra, including command trees, RunE hooks, argument validators, flags, completions, documentation generation, and command testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to build, extend, or review Go command-line applications that rely on spf13/cobra. It helps produce idiomatic command definitions, flag handling, completions, documentation generation, and test patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated changes to command wiring, flags, completions, or tests may alter CLI behavior in ways the user did not intend. <br>
Mitigation: Review proposed diffs before relying on them and run the project's Go test suite for affected commands. <br>
Risk: The skill may guide an agent to run Go or git commands during implementation work. <br>
Mitigation: Keep command execution scoped to the project, inspect command intent before running it, and avoid commands that publish, push, or modify remote state unless explicitly requested. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-spf13-cobra) <br>
- [Publisher Profile](https://clawhub.ai/user/samber) <br>
- [Metadata Homepage](https://github.com/samber/cc-skills-golang) <br>
- [spf13/cobra Package Documentation](https://pkg.go.dev/github.com/spf13/cobra) <br>
- [spf13/cobra Repository](https://github.com/spf13/cobra) <br>
- [Cobra Documentation](https://cobra.dev) <br>
- [Commands and Arguments Reference](references/commands-and-args.md) <br>
- [Flags Reference](references/flags.md) <br>
- [Completions Reference](references/completions.md) <br>
- [Generators Reference](references/generators.md) <br>
- [Testing Reference](references/testing.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Go code examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to edit project files, run Go or git commands, and fetch official or library documentation when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
