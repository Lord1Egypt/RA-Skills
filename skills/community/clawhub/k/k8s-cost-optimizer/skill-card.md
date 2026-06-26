## Description: <br>
Find and rank Kubernetes cost-saving opportunities from kubectl, metrics-server, kube-state-metrics, and cloud billing, including right-sizing, idle resource cleanup, autoscaling, node strategy, and purchase-plan recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, DevOps teams, and FinOps practitioners use this skill to audit EKS, GKE, and AKS clusters, estimate monthly savings, and prepare Kubernetes cost-optimization recommendations with YAML patches or implementation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated kubectl commands, YAML patches, delete actions, scale-to-zero steps, or PV migration plans could disrupt production workloads if applied without review. <br>
Mitigation: Treat all generated operational changes as proposals, confirm the target cluster and account, and route changes through normal production change review before applying them. <br>
Risk: Billing exports, cluster inventories, and metrics may contain sensitive infrastructure or cost data. <br>
Mitigation: Provide redacted or read-only cluster and billing data where possible, and avoid sharing secrets, credentials, or unnecessary account details. <br>
Risk: Savings-plan, committed-use, or reservation recommendations can create financial commitments. <br>
Mitigation: Have cloud finance or FinOps owners review purchase recommendations against current commitments and post-optimization baseline usage before buying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/k8s-cost-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with tables, YAML patches, kubectl commands, implementation plans, and report sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include estimated monthly savings, effort and risk ratings, and cloud-provider-specific Kubernetes recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
