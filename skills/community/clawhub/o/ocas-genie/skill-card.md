## Description:

Safely audits and reclaims VPS/Linux disk space, investigates root-filesystem growth, and enforces backup retention when disk usage is high or maintenance is requested; use keywords disk cleanup, disk full, disk usage, snapshots, backups, stale repos, or disk spike. NOT for database maintenance beyond read-only analysis, logrotate configuration, or real-time monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Genie to assess Linux disk usage, identify reclaimable files, run dry-run cleanup plans, and perform scoped disk maintenance on VPS or workstation environments. It is intended for filesystem cleanup and backup-retention workflows, not database repair, logrotate configuration, or real-time monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete broad local data during cleanup.

Mitigation: Run dry-run first, review the proposed cleanup scope, and tightly limit or disable /tmp and snapshot cleanup unless explicitly needed.

Risk: Silent self-updates can change cleanup behavior without a trusted release process.

Mitigation: Use self-update only through a trusted release process and review the resolved version before running cleanup on production or shared systems.

Risk: Database rebuild or repair helpers can modify data beyond the stated read-only analysis posture.

Mitigation: Treat database helpers as separate manual maintenance actions that require explicit approval and current backups.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/indigokarasu/skills/ocas-genie)
- [Root Audit and Backup Retention](references/root-audit-and-backup-retention.md)
- [Clone Deletion Safety](references/clone-deletion-safety.md)
- [Genie Snapshot Retention Bug](references/genie-snapshot-retention-bug.md)
- [Genie Gotchas](references/genie-gotchas.md)
- [State DB Vacuum Feasibility](references/state-db-vacuum-feasibility.md)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and optional JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write filesystem discovery manifests and cleanup journals when the bundled scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
