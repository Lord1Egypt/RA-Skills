## Description:

Automates and troubleshoots batch and single-source migrations to Huawei Cloud, including SMS and rsync fallback workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud engineers and developers use this skill to migrate AWS, GCP, VMware, and on-premises workloads to Huawei Cloud ECS, then check migration status and troubleshoot network or boot issues.

### Deployment Geography for Use:

Global, using the Huawei Cloud regions configured for the migration.

## Known Risks and Mitigations:

Risk: Administrator passwords or SSH credentials may be exposed, and root access or temporary migration keys may remain enabled after recovery.

Mitigation: Have an administrator review password handling and SSH restoration before production use. Use narrowly scoped credentials, rotate repair passwords after use, and verify temporary key removal and SSH/firewall restoration.

Risk: Cleanup or repair actions may delete or change servers beyond the intended target.

Mitigation: Use isolated migration resources and explicit target IDs, keep backups, and require approval for project changes, password resets, restarts, and deletions.

Risk: Live cloud effects and checkpoint recovery have not been verified by the security review.

Mitigation: Review the cleanup, password handling, SSH verification, and rollback behavior, then validate checkpoint recovery and target state before relying on a run.

## Reference(s):

- [ClawHub release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-mgc-migration-ecs-gcp-to-hw)
- [Migration runbook](references/runbook.md)
- [IAM permissions](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Migration lessons learned](references/lessons-learned.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON]

**Output Format:** [Markdown guidance, shell commands, configuration examples, and JSON migration status artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include migration checkpoints, task results, and verification guidance.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
