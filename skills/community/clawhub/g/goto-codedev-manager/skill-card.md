## Description:

GoTo CodeDev Manager is a unified OpenClaw skill for coordinating multiple IDE and AI coding-agent CLIs to perform code development, Git diff analysis, EF Core entity detection, migration handoff, test/build execution, and development reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feixuelingcloud](https://clawhub.ai/user/feixuelingcloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to delegate coding work across local agent or IDE tools, inspect resulting repository changes, identify .NET/EF Core database changes, generate schema handoff artifacts, and run build or test checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured coding-agent and IDE CLIs execute against local repositories and should be treated as trusted tools with repository access.

Mitigation: Review and lock down adapters.yaml and workspace configuration before installation; enable only the CLIs required for the target environment.

Risk: Database migration workflows can affect the wrong database if workspace credentials or policy settings are unsafe.

Mitigation: Do not provide production database credentials, including in fields named test_db_connection; keep production migration actions forbidden and require confirmation for migration generation and local or test updates.

Risk: Security evidence rates the release suspicious because database and automatic execution safeguards are not tight enough for high-impact use.

Mitigation: Fix the production migration policy and secret redaction before use in sensitive or production-connected environments, and review policies.yaml before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feixuelingcloud/skills/goto-codedev-manager)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON handoff files, generated code changes, shell command output, and plain-text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include schema contract handoff data, migration/test/build results, and Chinese development reports.]

## Skill Version(s):

1.0.0 (source: frontmatter, pyproject.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
