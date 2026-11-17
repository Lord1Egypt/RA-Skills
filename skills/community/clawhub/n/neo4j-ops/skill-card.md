## Description:

Use for Neo4j install, Cypher, schema design, and graph ops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueboyzx](https://clawhub.ai/user/blueboyzx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to install and connect to Neo4j, design graph schemas, write and tune Cypher, and handle data import, backup, and routine operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scan coverage is incomplete because some local references could not be resolved.

Mitigation: Review unresolved references and rescan the complete package before installation.

Risk: Database write and maintenance commands can change or replace data.

Mitigation: Require explicit authorization for writes, verify backups before restore or maintenance, and read back changes.

## Reference(s):

- [2026.x Operations](artifact/references/ops-2026.md)
- [Vector and Full-Text Search](artifact/references/vector-search.md)
- [Neo4j Deployment Center](https://neo4j.com/deployment-center)
- [ClawHub Release](https://clawhub.ai/blueboyzx/skills/neo4j-ops)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Cypher, Python, PowerShell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes query guardrails and operational procedures.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
