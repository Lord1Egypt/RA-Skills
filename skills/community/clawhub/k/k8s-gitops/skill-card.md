## Description:

Manage GitOps workflows with Flux and ArgoCD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use the skill to inspect GitOps source and application status, troubleshoot Flux and Argo CD deployments, and manage reconciliation workflows across environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The refresh examples use synchronization operations, which may change live workloads instead of only refreshing status.

Mitigation: Verify the installed MCP tool's behavior and use read-only status checks for inspection.

Risk: Synchronization and pruning can change or delete cluster resources.

Mitigation: Explicitly approve the application, cluster, namespace, and pending changes before synchronization; review pruning effects first.

## Reference(s):

- [Kubernetes GitOps release](https://clawhub.ai/rohitg00/skills/k8s-gitops)
- [Argo CD workflows](artifact/ARGOCD.md)
- [Flux workflows](artifact/FLUX.md)
- [Argo CD MCP server](https://github.com/argoproj-labs/mcp-for-argocd)
- [Flux MCP server](https://fluxoperator.dev/mcp-server/)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code]

**Output Format:** [Markdown with YAML manifests and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover Flux CD and Argo CD workflows.]

## Skill Version(s):

2.0.0 (source: release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
