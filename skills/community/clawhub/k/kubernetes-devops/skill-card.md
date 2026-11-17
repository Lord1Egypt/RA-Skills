## Description:

Creates production-ready Kubernetes manifests for Deployments, StatefulSets, CronJobs, Services, Ingresses, ConfigMaps, Secrets, and PersistentVolumeClaims with security contexts, health checks, and resource management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and platform engineers use this skill to generate, organize, and validate Kubernetes YAML for application workloads, services, ingress, configuration, secrets, storage, and multi-environment deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Kubernetes YAML can expose services publicly or broaden network access if LoadBalancer, NodePort, Ingress, or open CIDR settings are used without review.

Mitigation: Review exposure settings against cluster security policy before applying manifests.

Risk: Generated examples may include Secrets or placeholder credentials that are unsafe to commit or apply directly.

Mitigation: Use an approved secret-management system and replace placeholders before deployment.

Risk: Installing with mutable package selectors such as @latest can make releases less reproducible.

Mitigation: Prefer a pinned package version or immutable commit when installing.

## Reference(s):

- [Kubernetes skill page](https://clawhub.ai/wpank/skills/kubernetes-devops)
- [Kubernetes Deployment Specification Reference](references/deployment-spec.md)
- [Kubernetes Service Specification Reference](references/service-spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Kubernetes YAML and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated manifests should be reviewed before applying to a cluster.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
