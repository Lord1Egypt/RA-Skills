## Description:

Create Ubuntu 24.04 VMs on Windows Hyper-V from cloud images with cloud-init, including sparse VHDX handling, hv_netvsc network configuration, permissions, Secure Boot settings, Docker Compose v2 installation, and SSH access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to create a fresh Docker-ready Ubuntu VM on a Windows Hyper-V host. It is intended as base infrastructure for later application deployment skills or other Docker-based workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive VM credentials through returned connection details or logs.

Mitigation: Provide passwords through environment variables or stdin, prefer explicit SSH public keys, avoid returning or logging passwords, and rotate generated credentials after provisioning.

Risk: The provisioning path requires high-privilege Hyper-V administration and changes VM disk permissions.

Mitigation: Review and harden scripts before use, run only on trusted Hyper-V hosts, use explicit VM names from a safe character set, and reduce the deploy user's privileges where possible.

Risk: The skill downloads VM images and Docker Compose binaries during provisioning.

Mitigation: Use approved pinned versions and verify downloaded images and binaries before creating or trusting the VM.

Risk: The security evidence flags template-injection and path-handling concerns.

Mitigation: Restrict user-supplied VM names and paths to a safe character set and treat created VMs as administrative infrastructure until those issues are fixed.

## Reference(s):

- [Defaults: Hyper-V VM Creation](artifact/references/defaults.md)
- [Gotchas: Hyper-V VM Creation](artifact/references/gotchas.md)
- [Ubuntu 24.04 LTS cloud image](https://cloud-images.ubuntu.com/releases/24.04/release/ubuntu-24.04-server-cloudimg-amd64.img)
- [Docker Compose v2.32.4 binary](https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-x86_64)
- [ClawHub skill page](https://clawhub.ai/solomonneas/skills/hyperv-create-vm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell, PowerShell, and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cloud-init configuration, host provisioning commands, verification commands, and VM connection details.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
