## Description:

Diagnoses Huawei Cloud CCE autoscaling failures across HPA, Cluster Autoscaler or CCE elastic engine behavior, metrics, resource requests, Pending Pods, scheduling constraints, node pool limits, subnet IPs, quotas, and IAM permission signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to investigate why Huawei Cloud CCE workloads or nodes are not scaling as expected and to produce an evidence-backed Markdown diagnosis report with conclusions, confidence, data gaps, and next-step recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is described as read-only diagnosis, but server security evidence says the packaged dispatcher can also read Kubernetes Secrets and perform destructive cloud or Kubernetes changes.

Mitigation: Install only with tightly scoped read-only Huawei IAM and Kubernetes RBAC permissions, exclude Secret access and mutation permissions, and narrow the package to a diagnosis-only dispatcher before routine use.

Risk: Credential exposure or over-privileged cloud access could affect Huawei Cloud resources during diagnosis.

Mitigation: Use a dedicated least-privilege IAM identity, avoid root credentials, keep AK/SK values in environment variables only, and do not include credential values in reports or logs.

Risk: Generated HTML reports may include remote scripts that create unnecessary network exposure when opened.

Mitigation: Do not open generated HTML reports with network access until remote scripts are removed or integrity-pinned.

## Reference(s):

- [Workflow](artifact/references/workflow.md)
- [Output Schema](artifact/references/output-schema.md)
- [Capability Map](artifact/references/capability-map.md)
- [Risk Rules](artifact/references/risk-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/pintudeyudi/skills/huawei-cloud-cce-autoscaling-diagnoser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnosis report with structured JSON evidence from dispatcher actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnosis process, key evidence, root cause conclusion, confidence, data gaps, and recommendations.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
