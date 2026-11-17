## Description:

End-to-end Kubernetes cluster migration assistant for migrating self-hosted, on-premise, or third-party cloud Kubernetes workloads to Huawei Cloud Cloud Container Engine (CCE).

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud platform and Kubernetes engineers use this skill to assess, plan, and carry out workload migrations from external Kubernetes clusters to Huawei Cloud CCE, including storage, images, configuration, and traffic cutover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image mapping mistakes or unverified image tags can deploy unintended or altered workloads.

Mitigation: Have a cluster administrator review image-name mappings and verify image digests before production use.

Risk: Bulk updates or restores can disrupt workloads or overwrite target data.

Mitigation: Limit changes to approved clusters and workloads, preserve replica counts and pull secrets, and back up target data before destructive synchronization or restore steps.

Risk: Incorrect Secret exclusion filters can expose or overwrite sensitive cluster credentials.

Mitigation: Review and repair Secret filters, exclude cluster-specific credentials as directed by the migration guides, and protect backup archives.

Risk: Downloaded tools and live cloud behavior have not been verified in the release evidence.

Mitigation: Validate tool sources and test migration behavior in a controlled environment before production use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cce-cluster-migrator)
- [Pre-migration checklist and sizing](artifact/references/pre-migration-checklist.md)
- [External dependency and network audit](artifact/references/external-dependency-audit-guide.md)
- [Kubernetes metadata cloning with k8clone](artifact/references/k8clone-migration-guide.md)
- [Storage and persistent volume migration](artifact/references/storage-pv-migration-guide.md)
- [Container image synchronization to SWR](artifact/references/swr-image-sync-guide.md)
- [ConfigMap and Secret migration](artifact/references/configmap-secret-migration-guide.md)
- [Velero workload backup and restore](artifact/references/velero-migration-guide.md)
- [Traffic cutover](artifact/references/traffic-cutover-guide.md)
- [Migration verification methods](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands, Configuration files, Code]

**Output Format:** [Markdown plans and guidance with shell commands, YAML/JSON templates, and shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Migration steps depend on confirmed cluster, region, storage, image, and cutover choices; the skill calls for user confirmation before provisioning, data migration, or traffic switchover.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
