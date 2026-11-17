## Description:

Create Ubuntu 24.04 LXC containers or full VMs on Proxmox VE. Docker-ready with Compose v2. Handles nesting for Docker-in-LXC, auto-picks next available CTID, and includes post-boot Docker setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to provision Docker-ready Ubuntu hosts on Proxmox VE as LXC containers or full VMs. It is suited for creating base infrastructure that other deployment skills can use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can provision and delete Proxmox containers or VMs over privileged SSH, including destructive teardown commands.

Mitigation: Use it only on non-production or tightly controlled Proxmox systems, require explicit human confirmation before deletion, and prefer a restricted Proxmox account or API token.

Risk: VM creation accepts a password argument and may expose secrets through command history or process listings.

Mitigation: Prefer SSH keys or secret-manager input and avoid passing reusable passwords directly on the command line.

Risk: The setup downloads Docker Compose and Ubuntu cloud images at runtime without pinning or verification.

Mitigation: Pin versions where practical and verify downloaded binaries or images before use.

Risk: Incorrect IDs, names, or host targets could affect the wrong Proxmox resource.

Mitigation: Validate hostnames, CTIDs, VMIDs, and generated names before executing provisioning or teardown commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solomonneas/skills/proxmox-create-vm)
- [Defaults: Proxmox VM/Container Creation](references/defaults.md)
- [Gotchas: Proxmox VM/Container Creation](references/gotchas.md)
- [Docker Compose v2 download](https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64)
- [Ubuntu 24.04 cloud image](https://cloud-images.ubuntu.com/releases/24.04/release/ubuntu-24.04-server-cloudimg-amd64.img)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns container or VM name, CTID or VMID, type, IP address, SSH access details, and Docker setup status when provisioning completes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
