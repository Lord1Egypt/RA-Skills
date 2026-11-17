## Description:

Analyzes Huawei Cloud CCE incidents across alarms, rollout state, events, logs, topology, changes, nodes, network, and metrics to produce Markdown root-cause reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and platform engineers use this skill to investigate multi-domain Huawei Cloud CCE incidents and produce structured root-cause reports with evidence chains, impact scope, likely causes, confidence, and remediation handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the package exposes undeclared actions that can read Kubernetes Secrets and modify or delete cloud and cluster resources.

Mitigation: Review the package carefully before installing and test only with tightly scoped read-only Huawei IAM and Kubernetes RBAC credentials.

Risk: Credentials with broad privileges could permit destructive cluster, workload, node, alarm, or secret access beyond the stated read-only diagnosis posture.

Mitigation: Do not provide credentials capable of deleting or modifying clusters, workloads, nodes, alarms, or reading Secret contents unless the package is split or constrained by an enforced dispatcher allowlist.

Risk: Root-cause conclusions may be misleading if based on a single alarm or incomplete timeline.

Mitigation: Require a timeline or evidence chain, counter-evidence, and clearly labeled confidence before acting on remediation recommendations.

## Reference(s):

- [Workflow](references/workflow.md)
- [Risk Rules](references/risk-rules.md)
- [Output Schema](references/output-schema.md)
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html)
- [Huawei Cloud CCE API Reference](https://support.huaweicloud.com/api-cce/cce_02_0113.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance, Shell commands]

**Output Format:** [Markdown root-cause report with structured JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include investigation steps, timelines, evidence chains, impact scope, top root causes, confidence, counter-evidence, and remediation recommendations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
