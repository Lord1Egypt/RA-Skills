## Description:

Create and manage Proxmox Backup Server backups for Proxmox VMs and LXC containers, including guided setup for PBS installation, NAS storage, host access, target registration, backup status, and backup listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maikimolto](https://clawhub.ai/user/maikimolto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, homelab administrators, and infrastructure operators use this skill to configure Proxmox Backup Server storage, register Proxmox VM and LXC targets, and run or inspect backups through guided agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Proxmox/PBS credentials and backup configuration for infrastructure systems.

Mitigation: Use a dedicated least-privilege backup account and store configuration files with restrictive permissions.

Risk: TLS verification can be disabled for self-signed Proxmox or PBS certificates.

Mitigation: Prefer trusted certificates or certificate trust configuration and set verify_ssl to true where possible.

Risk: Setup guidance may include privileged commands that install PBS, mount NAS shares, or edit /etc/fstab.

Mitigation: Review generated sudo and fstab commands before running them, and confirm hostnames, storage paths, and mount options.

Risk: Reusable passwords or token secrets may be requested during setup.

Mitigation: Avoid pasting reusable passwords into chat or command lines when a scoped token or one-time setup flow can be used.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maikimolto/skills/proxmox-backup-server-manager)
- [PBS Backup Setup Guide](references/setup-guide.md)
- [PBS Backup Architecture](references/architecture.md)
- [Proxmox Downloads](https://www.proxmox.com/en/downloads)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, local configuration files, and JSON status output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Proxmox/PBS configuration and credentials stored under ~/.openclaw/credentials when configured.]

## Skill Version(s):

1.6.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
