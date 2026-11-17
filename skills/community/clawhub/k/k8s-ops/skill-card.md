## Description:

Kubernetes operations plugin for cluster management, monitoring, troubleshooting, and security auditing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to inspect, manage, troubleshoot, and audit Kubernetes clusters through OpenClaw tools backed by kubectl access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cluster administration actions may use broad Kubernetes authority.

Mitigation: Use a least-privileged kubeconfig or ServiceAccount and test in a non-production cluster before production use.

Risk: Cluster-admin binding guidance can grant full cluster control.

Mitigation: Avoid cluster-admin bindings unless full cluster control is intentional and approved.

Risk: Remote Kubernetes manifests and SSH host configuration can introduce supply-chain or credential exposure risk.

Mitigation: Pin and inspect remote manifests before applying them, prefer SSH keys, and avoid plaintext SSH passwords.

Risk: Weakly scoped tool parameters may allow unsafe Kubernetes operations.

Mitigation: Require clear per-tool input validation and human review before trusting the skill for production operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cn-big-cabbage/skills/k8s-ops)
- [Project Homepage](https://github.com/CN-big-cabbage/k8s-ops-agent)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Text or JSON results with Kubernetes commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires kubectl and valid, appropriately scoped Kubernetes credentials.]

## Skill Version(s):

2.1.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
