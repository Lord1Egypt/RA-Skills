## Description:

Provides linting best practices and golangci-lint configuration guidance for Go projects, including running linters, configuring .golangci.yml, suppressing warnings, and interpreting lint output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up, run, and interpret Go linting workflows with golangci-lint. It helps configure .golangci.yml, apply targeted nolint directives, prioritize fixes, and troubleshoot common linter issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage broad automated repository edits, especially when using golangci-lint --fix or parallel cleanup agents.

Mitigation: Run lint first, apply fixes only to explicit scopes, review git diff afterward, and use parallel cleanup agents only when the work is planned and isolated.

Risk: Automated lint guidance can introduce incorrect or misleading code changes if applied without review.

Mitigation: Review proposed commands, configuration changes, nolint directives, and code edits before deployment.

## Reference(s):

- [Linter Reference](artifact/references/linter-reference.md)
- [Nolint Directives](artifact/references/nolint-directives.md)
- [ClawHub Skill Page](https://clawhub.ai/samber/skills/golang-linter)
- [Project Homepage](https://github.com/samber/cc-skills-golang)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Go, YAML, Makefile, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose golangci-lint commands and configuration changes; running commands requires go and golangci-lint.]

## Skill Version(s):

1.1.1 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
