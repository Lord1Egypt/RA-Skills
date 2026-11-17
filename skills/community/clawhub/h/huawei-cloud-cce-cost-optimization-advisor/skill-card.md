## Description:

Analyzes Huawei Cloud CCE cluster cost optimization opportunities by identifying idle resources, oversized CPU and memory requests, low-utilization nodes, utilization trends, HPA recommendations, and node autoscaler policy improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to assess Huawei Cloud CCE clusters for cost-reduction opportunities and generate read-only reports, HPA YAML previews, autoscaler suggestions, execution plans, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaged commands can read Kubernetes secrets and change or delete cloud resources outside the advertised cost-advisor scope.

Mitigation: Review before installing, restrict production use to an allowlist of cost-advisor commands, and use Kubernetes RBAC that denies secrets and write operations.

Risk: The confirm=true path can apply real infrastructure changes.

Mitigation: Use preview mode first and pass confirm=true only after explicit user approval, with rollback steps and verification metrics documented.

Risk: Cloud credentials may grant broader access than required for cost analysis.

Mitigation: Use tightly scoped read-only Huawei IAM credentials and do not provide administrator credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pintudeyudi/skills/huawei-cloud-cce-cost-optimization-advisor)
- [Workflow](references/workflow.md)
- [Risk Rules](references/risk-rules.md)
- [Output Schema](references/output-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON summaries, HPA YAML previews, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write cost-optimization summary JSON and report Markdown when an output directory is provided.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
