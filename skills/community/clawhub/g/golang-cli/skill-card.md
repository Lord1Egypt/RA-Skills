## Description:

Golang CLI helps agents build, modify, and review Go command-line tools, including command structure, flags, configuration, versioning, exit codes, I/O, signal handling, completions, argument validation, and tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agents that create, extend, or review Go CLI applications. It focuses on Cobra/Viper command structure, configuration layering, Unix-friendly output, shell completions, graceful shutdown, and CLI test patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to edit Go CLI code and run Go, lint, or git commands.

Mitigation: Review proposed file edits and commands before execution, especially in repositories with production release workflows.

Risk: Proposed git commands could publish changes or rewrite repository history.

Mitigation: Require explicit human review before running git push, force-push, reset, rebase, or history-rewriting commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-cli)
- [Project homepage](https://github.com/samber/cc-skills-golang)
- [Cobra](https://github.com/spf13/cobra)
- [Viper](https://github.com/spf13/viper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Go code examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file edits, test guidance, and review findings for Go CLI projects.]

## Skill Version(s):

1.3.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
