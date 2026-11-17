## Description:

Cluster API lifecycle management for provisioning, scaling, and upgrading Kubernetes clusters. Use when managing cluster infrastructure or multi-cluster operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to inspect Cluster API resources and provision, scale, or upgrade Kubernetes clusters. It provides lifecycle workflows and guidance for reviewing cluster state and changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provisioning, scaling, or upgrading clusters can increase infrastructure costs or interrupt workloads.

Mitigation: Review the target cluster, manifests, replica counts, and versions before applying changes.

Risk: Cluster kubeconfig output contains credentials that grant access to a workload cluster.

Mitigation: Keep returned kubeconfig credentials private and share them only with authorized users.

## Reference(s):

- [ClawHub release](https://clawhub.ai/rohitg00/skills/k8s-capi)
- [Publisher profile](https://clawhub.ai/user/rohitg00)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance, code examples, and Kubernetes configuration manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cluster status information or kubeconfig returned during cluster operations.]

## Skill Version(s):

2.0.0 (source: server-resolved release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
