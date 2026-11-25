## Description:

A governed MySQL and MariaDB DBA assistant for server health checks, query and replication diagnosis, and guarded maintenance operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Database administrators and developers use the skill to inspect and troubleshoot MySQL 8.x and MariaDB 10.6+ servers. It analyzes slow queries, lock waits, replication lag, indexes, and table fragmentation, and can perform guarded maintenance when configured with suitable privileges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the skill suspicious for instruction-scope concerns. Its scan was incomplete: obfuscated instruction text was not fully evaluated and only 80% of components were scanned, so it does not establish that the artifact is safe.

Mitigation: Review the flagged concerns and the skill before installation. While assessing it, connect with a read-only, least-privilege database account; enable write privileges only after reviewing the audit setup and intended operations.

## Reference(s):

- [Project homepage](https://github.com/AIops-tools/MySQL-AIops)
- [Capabilities reference](references/capabilities.md)
- [Setup and security guide](references/setup-guide.md)
- [CLI reference](references/cli-reference.md)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Configuration instructions]

**Output Format:** [Structured database results with concise diagnostic guidance and, for operations, command or SQL previews.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live findings depend on database connectivity and privileges; write operations are guarded and require confirmation.]

## Skill Version(s):

0.13.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
