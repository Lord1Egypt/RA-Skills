## Description:

Manage multiple Kubernetes clusters, switch contexts, and perform cross-cluster operations. Use when working with multiple clusters, comparing environments, or managing cluster lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to inspect, compare, and manage Kubernetes clusters across contexts, including cluster lifecycle, GitOps, service mesh, and cross-cluster operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross-cluster secret transfers may expose sensitive values if the source, target, or destination is not sufficiently scoped.

Mitigation: Authorize each secret and trusted destination before transfer, protect saved kubeconfigs, and keep secret values out of responses and logs.

Risk: Production cluster changes may affect the wrong environment or resources if the target and intended operation are not verified.

Mitigation: Start with narrowly scoped, read-only access; before changes, verify the exact cluster, namespace, resource, and intended operation.

## Reference(s):

- [ClawHub release](https://clawhub.ai/rohitg00/skills/k8s-multicluster)
- [Argo CD MCP server](https://github.com/argoproj-labs/mcp-for-argocd)
- [Flux MCP server](https://fluxoperator.dev/mcp-server/)
- [Kubernetes Secrets good practices](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python-style tool-call and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use cluster, namespace, and resource names that should be checked against the intended environment.]

## Skill Version(s):

2.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
