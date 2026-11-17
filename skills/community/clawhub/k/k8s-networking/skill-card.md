## Description:

Kubernetes networking management for services, ingresses, endpoints, and network policies. Use when configuring connectivity, load balancing, or network isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to inspect and configure Kubernetes services, endpoints, ingresses, and network policies, and to troubleshoot connectivity and traffic isolation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A network-blocking example could disrupt applications across the default namespace if applied without checking its scope and required traffic.

Mitigation: Start in a test namespace with restricted Kubernetes permissions. Confirm the target cluster, namespace, affected applications, exact manifest, and required application and DNS allowances; verify connectivity and prepare a rollback before production changes.

## Reference(s):

- [Kubernetes Networking on ClawHub](https://clawhub.ai/rohitg00/skills/k8s-networking)
- [Publisher profile: rohitg00](https://clawhub.ai/user/rohitg00)

## Skill Output:

**Output Type(s):** [Configuration, Code, Guidance, Shell commands]

**Output Format:** [Markdown with Kubernetes YAML manifests, kubectl tool-call examples, and troubleshooting instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and operational guidance for Kubernetes networking resources.]

## Skill Version(s):

2.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
