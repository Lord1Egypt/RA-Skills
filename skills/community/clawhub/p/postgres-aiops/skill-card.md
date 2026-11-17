## Description:

Helps agents diagnose PostgreSQL health, slow queries, bloat, and blocking locks, and perform database maintenance when authorized.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Database administrators and developers use this skill to inspect PostgreSQL clusters, investigate performance and replication issues, and plan or perform authorized maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database write tools can make production-impacting changes without an enforced approval gate.

Mitigation: Use a read-only PostgreSQL role by default; restrict write credentials to a narrow target during an approved maintenance window, with a separate approval process for agent writes.

Risk: Local credentials, audit records, and undo records may expose sensitive operational metadata.

Mitigation: Protect POSTGRES_AIOPS_HOME, the master password, audit.db, and undo.db from unauthorized access.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zw008/skills/postgres-aiops)
- [Project homepage](https://github.com/AIops-tools/Postgres-AIops)
- [Capabilities](artifact/references/capabilities.md)
- [Setup and security guide](artifact/references/setup-guide.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report diagnostic findings and suggested maintenance actions.]

## Skill Version(s):

0.12.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
