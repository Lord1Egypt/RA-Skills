## Description:

K8s Fta Skill helps agents troubleshoot Kubernetes and k3s cluster failures with fault-tree analysis, kubectl checks, diagnosis reports, and repair recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yejinlei](https://clawhub.ai/user/yejinlei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and Kubernetes administrators use this skill to investigate pod, service, RBAC, DNS, storage, autoscaling, API server, and k3s issues and receive step-by-step diagnosis and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose or run high-impact Kubernetes repair commands against a live cluster.

Mitigation: Require explicit approval for every mutating command, verify the current cluster and namespace, and avoid production or administrator kubeconfigs by default.

Risk: Certificate and etcd troubleshooting can involve sensitive administrator workflows.

Mitigation: Reserve certificate and etcd-key checks for supervised administrator sessions with scoped credentials and rollback planning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yejinlei/skills/k8s-fta-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnosis reports with inline kubectl and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed mutating cluster actions that require explicit user approval and namespace/cluster verification.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
