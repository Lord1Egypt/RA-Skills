## Description:

Opinionated Go setup with golangci-lint v2, gofumpt, gotestsum, golang-migrate, and just. Use when starting a Go project, configuring lint, format, test, coverage or CI, writing a Justfile, wiring migrations, or leaving a Makefile workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to scaffold or update project tooling for formatting, linting, tests, CI, task running, Git hooks, and database migrations, with pinned tool versions and ready-to-adapt examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing downloaded Go tools brings executable code into the project environment.

Mitigation: Use pinned versions and verified downloads, and review the tool source or release before installation.

Risk: Git hook recipes can run commands and modify files during commits or pushes.

Mitigation: Review generated changes and hook behavior before enabling the hooks.

Risk: Migration commands can change or remove data in the configured database.

Mitigation: Confirm the target database and maintain a backup before applying migrations or resets.

Risk: Migration recipes use a database connection string, and downloaded tools may access network resources.

Mitigation: Keep credentials scoped to the project and use isolated container networking where practical.

Risk: Externally downloaded software is outside the artifact review, and optional additional skills have separate behavior.

Mitigation: Verify downloaded software and review optional skills separately before global installation.

## Reference(s):

- [Go Toolchain Reference](artifact/references/go-toolchain-reference.md)
- [Go Correctness Reference](artifact/references/go-correctness-reference.md)
- [Go Testing Reference](artifact/references/go-testing-reference.md)
- [golangci-lint Reference](artifact/references/golangci-lint-reference.md)
- [gofumpt Reference](artifact/references/gofumpt-reference.md)
- [gotestsum Reference](artifact/references/gotestsum-reference.md)
- [golang-migrate Reference](artifact/references/go-migrate-reference.md)
- [Justfile Reference](artifact/references/justfile-reference.md)
- [Lefthook Reference](artifact/references/lefthook-reference.md)
- [Go Official Docs](https://go.dev/doc/)
- [Go 1.27 Release Notes](https://go.dev/doc/go1.27)
- [Go vulnerability checker](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)
- [ClawHub skill page](https://clawhub.ai/tenequm/skills/go-dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Go, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference material and ready-to-adapt project templates]

## Skill Version(s):

0.7.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
