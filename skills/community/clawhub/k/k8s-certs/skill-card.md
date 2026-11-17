## Description:

Kubernetes certificate management with cert-manager. Use when managing TLS certificates, configuring issuers, or troubleshooting certificate issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kubernetes engineers use this skill to inspect, create, and troubleshoot cert-manager certificates, issuers, certificate requests, and ingress TLS configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cluster-wide cert-manager installation and cluster write operations may affect resources beyond the requested certificate changes.

Mitigation: Confirm the target cluster, namespace, and requested changes before enabling writes; approve installation separately and review a pinned official release manifest.

Risk: Certificate issuance sends the configured email address and domain names to Let's Encrypt.

Mitigation: Check the email address and domain names before issuance, and use a staging issuer for tests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/rohitg00/skills/k8s-certs)
- [cert-manager installation manifest](https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Python tool-call examples and YAML manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
