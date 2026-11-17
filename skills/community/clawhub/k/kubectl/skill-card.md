## Description:

Execute and manage Kubernetes clusters via kubectl commands. Query resources, deploy applications, debug containers, manage configurations, and monitor cluster health. Use when working with Kubernetes clusters, containers, deployments, or pod diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddevaal](https://clawhub.ai/user/ddevaal)

### License/Terms of Use:

MIT

## Use Case:

Developers and platform engineers use this skill to plan and run kubectl workflows for inspecting Kubernetes resources, deploying updates, debugging pods, managing configuration, and monitoring cluster health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: kubectl commands can modify live Kubernetes clusters, including deployment updates, scaling, deletion, draining, and container execution.

Mitigation: Use a least-privilege kubeconfig, verify the active context and namespace before execution, and require approval for apply, delete, scale, drain, exec, and port-forward actions.

Risk: Cluster configuration, tokens, secrets, and diagnostic logs may contain sensitive data.

Mitigation: Do not paste raw kubeconfig, secrets, tokens, or sensitive logs into chat or tickets; redact sensitive values before sharing output.

Risk: Port-forwarding can expose cluster workloads outside their intended access path.

Mitigation: Prefer localhost-bound port-forwarding and confirm the target pod, service, namespace, and duration before opening access.

## Reference(s):

- [kubectl Command Reference](references/REFERENCE.md)
- [Official kubectl Docs](https://kubernetes.io/docs/reference/kubectl/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/)
- [Agent Skills Specification](https://agentskills.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires kubectl v1.20+ and an active kubeconfig connection; command effects depend on the user's Kubernetes permissions and selected context.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
