## Description:

Free host health check for OpenClaw deployments. Check system status, updates, security settings, and provide recommendations. No paid tools required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bwtomekk-bit](https://clawhub.ai/user/bwtomekk-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Hostcheck to request a read-only health and security posture report for OpenClaw hosts, including system status, update, SSH, firewall, backup, and OpenClaw service checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrator-level remediation suggestions such as update, upgrade, or package-install commands could affect production hosts if run without review.

Mitigation: Treat remediation commands as recommendations only; require an administrator to review and approve them before execution.

Risk: The skill does not include virus scanning, real-time protection, or automatic firewall installation.

Mitigation: Use the report as a basic host-health checklist and add dedicated security tools or manual controls when those protections are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bwtomekk-bit/skills/hostcheck)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status report with concise findings and optional inline shell commands for administrator-reviewed remediation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; remediation commands are recommendations and require user consent before changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
