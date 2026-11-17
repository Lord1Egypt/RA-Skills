## Description:

Guides inspection, operation, hardening, troubleshooting, and schema management for local YDB deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[astandrik](https://clawhub.ai/user/astandrik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage local YDB Docker deployments, diagnose health and access issues, and plan or apply schema, authentication, and storage changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Container, volume, storage, or schema changes could disrupt a deployment or cause data loss.

Mitigation: Review the plan and backups, require confirmation before changes, and verify outcomes with a rollback path.

Risk: Authentication or public monitoring changes could expose access or lock out users.

Mitigation: Review credentials and access settings, keep secrets out of shared output, and verify access before admitting clients.

## Reference(s):

- [ClawHub release](https://clawhub.ai/astandrik/skills/local-ydb)
- [Topology reference](references/topology.md)
- [Authentication hardening](references/auth-hardening.md)
- [Storage migration](references/storage-migration.md)
- [Verification](references/verification.md)
- [MCP tool scenarios](references/mcp-tool-scenarios.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with shell commands, configuration, and SQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans for live changes include impact, confirmation, verification, and rollback steps.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
