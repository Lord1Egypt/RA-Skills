## Description:

Helps database operators diagnose MySQL and MariaDB performance, locks, replication, and table health, with tools for approved maintenance actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Database administrators and developers use this skill to inspect MySQL 8.x or MariaDB 10.6+ servers, investigate slow queries, lock waits, replication lag, and fragmentation, and perform deliberate maintenance when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live database write tools have no built-in MCP approval or read-only control.

Mitigation: Start with a dedicated read-only, least-privilege database account; grant write privileges only for explicitly authorized maintenance.

Risk: Maintenance actions can change production state or disrupt active queries.

Mitigation: Review the target and preview actions before execution; treat MCP write access as production change authority.

Risk: Database credentials and connections require protection.

Mitigation: Replace placeholder passwords, protect MYSQL_AIOPS_MASTER_PASSWORD, and restrict account access by host and TLS.

## Reference(s):

- [Skill capabilities](references/capabilities.md)
- [CLI reference](references/cli-reference.md)
- [Setup and security guide](references/setup-guide.md)
- [Agent guardrails](references/agent-guardrails.md)
- [Project homepage (release metadata)](https://github.com/AIops-tools/MySQL-AIops)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance and structured tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports live database diagnostics and offline analysis of supplied records.]

## Skill Version(s):

0.12.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
