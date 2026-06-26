## Description: <br>
Kubernetes backup and restore with Velero. Use when creating backups, restoring applications, managing disaster recovery, or migrating workloads between clusters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rohitg00](https://clawhub.ai/user/rohitg00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, platform engineers, and SREs use this skill to plan and operate Velero backups, restores, scheduled backups, disaster recovery, and workload migration for Kubernetes clusters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Velero operations use the active Kubernetes context and may target the wrong cluster or namespace. <br>
Mitigation: Verify the target cluster, namespace mappings, backup name, and included or excluded resources before creating backups or restores. <br>
Risk: Restores and backup storage may include Kubernetes Secrets or other credentials. <br>
Mitigation: Confirm whether Secrets should be restored and protect access to backup storage. <br>
Risk: Backup schedules can create recurring changes with storage and retention impact. <br>
Mitigation: Review schedule timing, TTL, and namespace scope before applying schedule manifests. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review Kubernetes cluster context, namespace mappings, backup names, included resources, and restore behavior before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
