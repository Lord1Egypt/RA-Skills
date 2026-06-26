## Description: <br>
Create and manage Proxmox Backup Server backups for Proxmox VMs and LXC containers, including guided setup, target registration, backup runs, status checks, and backup listing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maikimolto](https://clawhub.ai/user/maikimolto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, homelab operators, and infrastructure administrators use this skill to configure Proxmox Backup Server storage, register Proxmox VM and LXC backup targets, and run or inspect backups through guided commands and local helper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help administer Proxmox Backup Server workflows and may lead to apt, mount, fstab, SSH, pvesm, and bulk-backup actions. <br>
Mitigation: Review each infrastructure action before approving it and confirm that it matches the intended backup environment. <br>
Risk: The skill needs Proxmox, PBS, and optionally NAS credentials for setup and backup operations. <br>
Mitigation: Use least-privilege accounts, enable TLS verification when possible, protect credentials stored under ~/.openclaw/credentials, and rotate secrets if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maikimolto/proxmox-backup-server-manager) <br>
- [Architecture reference](references/architecture.md) <br>
- [Setup guide](references/setup-guide.md) <br>
- [Proxmox downloads](https://www.proxmox.com/en/downloads) <br>
- [Proxmox Backup Server package repository](http://download.proxmox.com/debian/pbs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON status output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local credential configuration under ~/.openclaw/credentials when setup is approved.] <br>

## Skill Version(s): <br>
1.6.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
