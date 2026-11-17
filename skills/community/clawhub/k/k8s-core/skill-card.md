## Description:

Core Kubernetes resource management for pods, namespaces, configmaps, secrets, and nodes. Use when listing, inspecting, or managing fundamental K8s objects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to list, inspect, and manage core Kubernetes resources, including pods, namespaces, ConfigMaps, Secrets, nodes, and events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Secrets and guide potentially disruptive operations, including deletion and node draining.

Mitigation: Use credentials limited to the intended cluster and tasks; verify the cluster context, namespace, and resource before deletion or node draining; keep secret values out of displayed output.

## Reference(s):

- [Core Kubernetes Resources on ClawHub](https://clawhub.ai/rohitg00/skills/k8s-core)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Markdown with Kubernetes resource-operation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keep Secret values out of displayed output.]

## Skill Version(s):

2.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
