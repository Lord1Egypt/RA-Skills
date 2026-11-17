## Description:

Virtual machine management with KubeVirt on Kubernetes. Use when creating, managing, or troubleshooting VMs running on Kubernetes clusters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to inspect and manage KubeVirt virtual machines on Kubernetes, including VM lifecycle operations, migration, and storage. It also provides examples for creating VMs and troubleshooting common startup or migration issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The VM creation example contains a shared plaintext password.

Mitigation: Replace it with unique credentials or SSH keys; do not reuse or expose example credentials.

Risk: The data-volume example uses a guest image that security guidance identifies as unsupported.

Mitigation: Select a supported guest image and verify its source before creating the VM.

Risk: VM lifecycle operations can affect workloads and persistent disks in the target cluster.

Mitigation: Confirm the target cluster, namespace, VM, permissions, and acceptable downtime before changes; remove unneeded VMs and disks.

## Reference(s):

- [KubeVirt VM Management on ClawHub](https://clawhub.ai/rohitg00/skills/k8s-kubevirt)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with tool-call examples and YAML VM manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples may require adaptation to the target cluster and supported guest images.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
