## Description: <br>
Opinionated Go development setup with golangci-lint v2, gofumpt, gotestsum, golang-migrate, and just for project setup, linting, formatting, testing, CI/CD, Justfiles, and migration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to bootstrap or modernize Go projects with a consistent toolchain for formatting, linting, testing, CI, task running, and database migrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation commands can fetch moving tool versions when examples use latest. <br>
Mitigation: Review commands before running them, prefer pinned and verified tool versions, and install only the tools needed for the project. <br>
Risk: Auto-fix commands and Git hook setup can modify working tree or staged files. <br>
Mitigation: Run auto-fix and hook installation in a clean branch, review diffs, and keep backups or commits before applying broad changes. <br>
Risk: Migration rollback or drop commands can affect the wrong database if DATABASE_URL points to production or shared data. <br>
Mitigation: Verify DATABASE_URL targets a safe non-production database and take a backup before running rollback, force, or drop operations. <br>


## Reference(s): <br>
- [go-dev ClawHub release](https://clawhub.ai/tenequm/go-dev) <br>
- [Go Official Docs](https://go.dev/doc/) <br>
- [golangci-lint Docs](https://golangci-lint.run/) <br>
- [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck) <br>
- [golangci-lint Reference](references/golangci-lint-reference.md) <br>
- [gofumpt Reference](references/gofumpt-reference.md) <br>
- [gotestsum Reference](references/gotestsum-reference.md) <br>
- [Go Testing Reference](references/go-testing-reference.md) <br>
- [golang-migrate Reference](references/go-migrate-reference.md) <br>
- [Justfile Reference](references/justfile-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, YAML, Justfile, and Go code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tool installation commands, CI snippets, project structure guidance, and configuration templates.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
