## Description:

Kubernetes backup and restore with Velero. Use when creating backups, restoring applications, managing disaster recovery, or migrating workloads between clusters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kubernetes operators use this skill to create, inspect, schedule, and restore Velero backups for application recovery, disaster recovery, and workload migration between clusters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup and restore actions can affect the wrong cluster or namespaces, or write to an unsuitable destination.

Mitigation: Confirm the target cluster, namespaces, and backup destination before running operations.

Risk: Backups may contain credentials and application data and may be exposed through storage permissions.

Mitigation: Protect the backup storage and verify encryption settings and storage permissions.

Risk: A restore or recurring schedule may cause unintended changes to production workloads.

Mitigation: Test restores outside production and review scheduled backups before creating them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/rohitg00/skills/k8s-backup)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with tool-call examples, shell commands, and YAML manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operational examples for Velero backup, restore, and schedule workflows.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
