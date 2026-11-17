## Description:

Huawei Cloud CCE node failure diagnosis skill using a Python SDK dispatcher to collect node status, lease, event, pod, metric, and security evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to investigate Huawei Cloud CCE Kubernetes node NotReady states, node pressure, kubelet or runtime symptoms, network issues, pod impact, and related events or metrics. It produces a diagnosis report and runbook-style recommendations for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill is presented as read-only node diagnosis, but the packaged dispatcher exposes cluster mutations and secret retrieval beyond that purpose.

Mitigation: Install only after constraining execution to dedicated read-only Huawei IAM and Kubernetes RBAC that cannot delete, scale, drain, cordon, reboot, modify alarms, change vulnerability status, or read Secret values.

Risk: The security verdict is suspicious.

Mitigation: Review and constrain the packaged dispatcher before deployment, and treat remediation recommendations as human-reviewed guidance rather than authorized automated actions.

## Reference(s):

- [Skill source](https://clawhub.ai/pintudeyudi/skills/huawei-cloud-cce-node-failure-diagnoser)
- [Workflow](references/workflow.md)
- [Risk Rules](references/risk-rules.md)
- [Output Schema](references/output-schema.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Common Pitfalls](references/common-pitfalls.md)
- [Huawei Cloud API Explorer](https://support.huaweicloud.com/apiexplorer/index.html)
- [Huawei Cloud IAM Console](https://console.huaweicloud.com/iam/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown diagnosis report with structured JSON evidence from dispatcher actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include node status, kube-node-lease freshness, liveness classification, root-cause category, confidence, evidence tables, pod impact, health items, metrics, and remediation recommendations.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
