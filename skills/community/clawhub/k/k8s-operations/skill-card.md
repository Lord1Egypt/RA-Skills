## Description:

kubectl operations for applying, patching, deleting, and executing commands on Kubernetes resources. Use when modifying resources, running commands in pods, or managing resource lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kubernetes operators use this skill to apply, patch, delete, scale, and inspect resources, manage rollouts, and execute commands in pods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying, patching, deleting, scaling, or restarting resources and executing commands in pods can change or interrupt workloads.

Mitigation: Use appropriately restricted Kubernetes permissions; before each operation, verify the intended cluster, namespace, resource, and action. Compare live state before production applies, avoid force deletion unless necessary, and verify rollout status after changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/rohitg00/skills/k8s-operations)
- [Publisher profile](https://clawhub.ai/user/rohitg00)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with kubectl operation examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations may modify or interrupt Kubernetes workloads.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
