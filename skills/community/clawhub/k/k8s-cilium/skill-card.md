## Description:

Cilium and Hubble network observability for Kubernetes. Use when managing network policies, observing traffic flows, or troubleshooting connectivity with eBPF-based networking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kubernetes operators use this skill to inspect Cilium health and Hubble traffic flows, troubleshoot connectivity, and manage Cilium network policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cilium installation and default-deny or clusterwide policies can disrupt cluster connectivity.

Mitigation: Confirm the target cluster, namespace, and workload labels; review policy changes, test in staging, and keep a rollback plan.

Risk: Hubble flow output may contain sensitive traffic details.

Mitigation: Review flow data for sensitive information and limit its exposure to authorized users.

## Reference(s):

- [Cilium & Hubble Network Observability on ClawHub](https://clawhub.ai/rohitg00/skills/k8s-cilium)
- [Publisher profile: rohitg00](https://clawhub.ai/user/rohitg00)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with tool-call examples and YAML network policy manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover Cilium status and Hubble flow queries, troubleshooting steps, and policy configuration.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
