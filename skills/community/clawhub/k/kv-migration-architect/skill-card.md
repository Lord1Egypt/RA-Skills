## Description:

Helps agents plan and validate zero-downtime database, service, infrastructure, and hybrid migrations with phased plans, compatibility analysis, rollback procedures, runbooks, stakeholder communication templates, and success metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felix-antonio-sl](https://clawhub.ai/user/felix-antonio-sl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and migration leads use this skill to turn database, service, infrastructure, or hybrid migration requests into phased zero-downtime plans with compatibility checks, rollback triggers, validation checkpoints, and stakeholder communication artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate ready-to-run destructive SQL, rollback, infrastructure, and service commands.

Mitigation: Review generated SQL, rollback runbooks, Terraform, Kubernetes, AWS, systemctl, and curl commands manually before execution.

Risk: Automatic rollback guidance can cause service or data disruption if executed without preparation.

Mitigation: Require explicit human approval, tested backups, staging validation, scoped credentials, and rollback drills before enabling automatic rollback actions.

Risk: Migration plans may involve irreversible data loss or target systems that cannot preserve all source constraints.

Mitigation: Require the plan to declare irreversible data loss risk, include phase-specific rollback procedures, and validate checkpoints between phases before continuing.

## Reference(s):

- [Migration Patterns Catalog](artifact/references/migration_patterns_catalog.md)
- [Data Reconciliation Strategies](artifact/references/data_reconciliation_strategies.md)
- [Zero-Downtime Migration Techniques](artifact/references/zero_downtime_techniques.md)
- [ClawHub skill page](https://clawhub.ai/felix-antonio-sl/skills/kv-migration-architect)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and optional JSON files from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include phased plans, runbook checklists, rollback procedures, validation checkpoints, success metrics, and stakeholder communication templates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
