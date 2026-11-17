## Description:

Go安全质量检查免费版 helps Go developers run govulncheck-based dependency vulnerability scans, assess impact, and get remediation guidance for a single project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill in Go projects before release, dependency updates, or CI setup to run govulncheck, review known vulnerability impact, and draft remediation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause the skill to be selected for non-Go or general security tasks.

Mitigation: Use it only for Go project vulnerability and quality checks, and confirm the repository contains a Go module before running commands.

Risk: Dependency-update snippets can modify go.mod and go.sum.

Mitigation: Review each command, commit or back up go.mod and go.sum first, and treat update snippets as manual remediation steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/go-security-vuln-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, YAML, and command output snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose dependency update commands that should be reviewed before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
