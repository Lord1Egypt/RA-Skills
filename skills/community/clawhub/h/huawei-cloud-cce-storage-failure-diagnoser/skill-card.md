## Description:

Diagnoses Huawei Cloud CCE Kubernetes storage failures across PVC provisioning, binding, attach and mount, runtime I/O, capacity, permission, and teardown stages, producing Markdown diagnosis reports from collected evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to investigate Huawei Cloud CCE storage incidents such as PVC Pending, FailedMount, FailedAttachVolume, EVS attach issues, SFS/SFS Turbo NFS timeouts, OBS credential failures, capacity exhaustion, and PVC termination protection. It collects read-oriented Kubernetes and cloud evidence and turns it into a concise diagnosis with confidence and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that the shipped dispatcher exposes broad cloud and Kubernetes administration actions beyond the storage diagnosis behavior users would expect.

Mitigation: Install and run the skill only with tightly scoped read-only Huawei IAM and Kubernetes RBAC credentials, and restrict available dispatcher actions to storage diagnosis and read-only evidence collection.

Risk: The scanner guidance identifies secret data return, kubeconfig export, and mutation handlers as actions that could increase credential exposure or operational impact.

Mitigation: Hard-block secret-reading, kubeconfig export, cluster or workload mutation, node drain, ECS/EIP/AOM management, and any delete or patch handlers before production use.

Risk: Storage remediation advice can affect data consistency when incidents involve EVS residual mounts, read-only filesystems, PVC finalizers, or database workloads.

Mitigation: Treat remediation as a reviewed plan with impact scope, rollback method, and verification standards; do not force detach, force mount, remove finalizers, or restart stateful workloads without explicit operator approval and filesystem consistency checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pintudeyudi/skills/huawei-cloud-cce-storage-failure-diagnoser)
- [Workflow](references/workflow.md)
- [Output schema](references/output-schema.md)
- [Risk rules](references/risk-rules.md)
- [Huawei Cloud Python SDK Documentation](https://doc.huihua.com/api/sdk/python.html)
- [Huawei Cloud API Explorer](https://support.huaweicloud.com/apiexplorer/index.html)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON with an embedded Markdown diagnosis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include findings, evidence snapshots, top causes, confidence, conclusions, and recommended verification steps.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
