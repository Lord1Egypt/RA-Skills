## Description:

Ops Maintenance helps agents inspect local, remote, and clustered servers for health, logs, performance, ports, processes, disk usage, password expiry, networking, reporting, audit logs, Docker health, SSL certificates, and security posture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to ask an agent to run or plan operational checks across local and SSH-accessible servers. It supports health monitoring, log analysis, security audits, network diagnostics, Docker and SSL checks, alerting, scheduled patrols, and maintenance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can provide administrative visibility into local and remote systems.

Mitigation: Install only for users who need that access, use a dedicated low-privilege SSH account, and limit configured servers to the intended maintenance scope.

Risk: Fleet command execution against production systems can create operational impact if a command is wrong or too broad.

Mitigation: Review the exact command and target group before running fleet execution, especially for production hosts.

Risk: Credentials, alert tokens, SMTP passwords, configuration snapshots, and audit logs can expose sensitive operational data.

Mitigation: Prefer key-based authentication, avoid password authentication, avoid saving alert or SMTP secrets in config files, verify host keys outside the skill, and treat generated logs and snapshots as sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fish1981bimmer/skills/ops-maintenance)
- [Architecture documentation](artifact/doc/ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command output, tables, JSON snippets, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive operational findings, configuration snapshots, audit log summaries, and remote command results.]

## Skill Version(s):

3.3.10 (source: server release metadata, package.json, target metadata; artifact skill frontmatter differs)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
