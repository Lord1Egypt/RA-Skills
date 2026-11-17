## Description:

Diagnoses Huawei Cloud CCE workload rollout failures, replica shortages, probe-related readiness failures, ReplicaSet creation blocks, and controller observation lag.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to investigate Huawei Cloud CCE Deployment, StatefulSet, and DaemonSet rollout failures using workload state, ReplicaSet ownership, Pod health, Events, logs, and metrics. It returns ranked causes and handoff recommendations for pod, node, network, storage, root-cause, or remediation follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill presents as read-only diagnosis while shipping runnable cloud and Kubernetes mutation capabilities.

Mitigation: Review before installing, restrict execution to the declared diagnosis actions, and use tightly scoped read-only Huawei Cloud IAM and Kubernetes RBAC credentials.

Risk: The security review flags unsafe temporary credential-file handling and TLS verification issues.

Mitigation: Do not provide admin or long-lived credentials; fix credential-file handling and TLS verification before production use.

## Reference(s):

- [Workflow](references/workflow.md)
- [Output Schema](references/output-schema.md)
- [Risk Rules](references/risk-rules.md)
- [Verification Method](references/verification-method.md)
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html)
- [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON diagnosis outputs and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ranked top causes, evidence timelines, warnings, and handoff recommendations.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
