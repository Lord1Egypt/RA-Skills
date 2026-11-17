## Description:

Debug Kubernetes pods, nodes, and workloads. Use when pods are failing, containers crash, nodes are unhealthy, or users mention debugging, troubleshooting, or diagnosing Kubernetes issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to diagnose failing Kubernetes pods, unhealthy nodes, and workload issues through cluster status, events, logs, metrics, network, and storage checks. It provides troubleshooting guidance and diagnostic workflows for Kubernetes clusters accessed through kubectl-mcp-server tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Node-repair instructions may affect workloads without clearly requiring user approval or safety checks.

Mitigation: Start with a read-only Kubernetes account and explicitly select the intended cluster and namespace. Require approval before cleanup, process termination, or workload changes. Preserve relevant logs and confirm maintenance is complete before uncordoning a node.

## Reference(s):

- [Common Errors](references/COMMON-ERRORS.md)
- [Troubleshooting Decision Tree](references/DECISION-TREE.md)
- [Safely drain a node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Code]

**Output Format:** [Markdown troubleshooting guidance with diagnostic results, kubectl/MCP tool calls, and optional shell or Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cluster-, namespace-, and context-dependent; advanced diagnostics require the cilium, diagnostics, istio, policy, and security toolsets.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
