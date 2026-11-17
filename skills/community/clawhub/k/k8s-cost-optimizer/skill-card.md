## Description:

Finds and ranks Kubernetes cost-saving opportunities from kubectl, metrics-server, kube-state-metrics, and cloud billing, then produces savings estimates, YAML patches, and implementation guidance for EKS, GKE, and AKS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and FinOps teams use this skill to audit Kubernetes clusters, prioritize cost reductions, and prepare safe rollout plans for right-sizing, autoscaling, storage, load balancer, node-pool, spot, and commitment changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated kubectl, YAML, deletion, scaling, spot-migration, or savings-plan recommendations may affect production workloads or cloud spend if applied without review.

Mitigation: Review each recommendation before use and apply changes through normal change control, canaries, monitoring, and rollback plans.

Risk: Cluster metrics and billing exports can expose sensitive infrastructure and cost information.

Mitigation: Provide only approved data, redact secrets and sensitive identifiers, and limit shared exports to the scope needed for cost analysis.

Risk: Cost estimates and right-sizing recommendations can be misleading when based on short or unrepresentative metrics windows.

Mitigation: Use at least 30 days of representative data when possible and validate recommendations against production safety constraints before rollout.

## Reference(s):

- [K8s Cost Optimizer on ClawHub](https://clawhub.ai/charlie-morrison/skills/k8s-cost-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with YAML patches and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ranked recommendations, monthly savings estimates, implementation plans, and safety gates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
