## Description:

Provides PostgreSQL DBA diagnostics and guided maintenance through cluster health, query, index, table, replication, and lock analysis, plus guarded write operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT

## Use Case:

Database administrators and developers use this skill to inspect PostgreSQL health, investigate slow queries, bloat, vacuum activity, locks, and replication, and carry out maintenance operations with previews and audit records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious because it points to an external OpenClaw plugin whose behavior could not be verified; the scan reports incomplete coverage.

Mitigation: Review the plugin implementation and safeguards and confirm its advertised PostgreSQL capabilities before installing, following the security guidance.

Risk: The skill can make database changes, including operations that have no safe undo; audit records do not determine whether a write is authorized.

Mitigation: Use a least-privilege PostgreSQL role, inspect dry-run previews and confirmation prompts, and reserve irreversible operations for explicitly intended work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zw008/skills/postgres-aiops)
- [Project homepage](https://github.com/AIops-tools/Postgres-AIops)
- [Capabilities reference](artifact/references/capabilities.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Setup and security guide](artifact/references/setup-guide.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Structured tool results with concise text or Markdown summaries, shell commands, and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis reports cite measured findings; limited reads report whether results were truncated.]

## Skill Version(s):

0.13.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
