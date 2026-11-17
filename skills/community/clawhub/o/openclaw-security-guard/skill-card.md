## Description:

Security audit CLI + live dashboard for OpenClaw. Scans for secrets, config issues, prompt injections, vulnerable dependencies, and unverified MCP servers. Zero telemetry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miloudbelarebia](https://clawhub.ai/user/miloudbelarebia)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to audit OpenClaw installations, review security posture, apply configuration hardening, monitor activity through a local dashboard, and generate reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic fixes can change OpenClaw configuration.

Mitigation: Run audit and dry-run modes first, review the proposed changes, and confirm backups before using fix --auto on important configurations.

Risk: The dashboard loads scripts from external CDNs.

Mitigation: Avoid using the dashboard in sensitive environments unless those scripts are removed, vendored, or pinned and reviewed.

Risk: Installing hooks can replace an existing Git pre-commit hook.

Mitigation: Use hooks install only in repositories where replacing or managing the existing pre-commit hook is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/miloudbelarebia/skills/openclaw-security-guard)
- [Publisher Profile](https://clawhub.ai/user/miloudbelarebia)
- [Project Homepage](https://github.com/2pidata/openclaw-security-guard)
- [Getting Started Guide](docs/guides/getting-started.md)
- [CLI Reference](docs/api/cli.md)
- [Programmatic API Reference](docs/api/programmatic.md)
- [npm Package](https://www.npmjs.com/package/openclaw-security-guard)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [CLI output, Markdown or JSON reports, shell commands, and configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local OpenClaw audits and may write reports, update OpenClaw configuration, or install a Git pre-commit hook when those commands are used.]

## Skill Version(s):

1.0.0 (source: server release, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
