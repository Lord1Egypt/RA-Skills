## Description: <br>
Create Ubuntu 24.04 LXC containers or full VMs on Proxmox VE. Docker-ready with Compose v2. Handles nesting for Docker-in-LXC, auto-picks next available CTID, and includes post-boot Docker setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to create Docker-ready Ubuntu 24.04 LXC containers or full VMs on Proxmox VE for downstream application deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent powerful infrastructure control over a Proxmox host. <br>
Mitigation: Install and use it only for explicitly approved Proxmox hosts, and review generated commands before execution. <br>
Risk: The teardown helper can permanently delete containers or VMs. <br>
Mitigation: Do not run destroy commands unless the host, resource ID, resource name, and backups have been independently verified. <br>
Risk: VM creation can expose passwords passed on the command line. <br>
Mitigation: Prefer SSH keys or throwaway credentials, and avoid passing real passwords as command-line arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solomonneas/proxmox-create-vm) <br>
- [Defaults: Proxmox VM/Container Creation](references/defaults.md) <br>
- [Gotchas: Proxmox VM/Container Creation](references/gotchas.md) <br>
- [Docker Compose v2 release download](https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64) <br>
- [Ubuntu 24.04 cloud image](https://cloud-images.ubuntu.com/releases/24.04/release/ubuntu-24.04-server-cloudimg-amd64.img) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Proxmox creation, setup, verification, IP discovery, and teardown guidance for agent review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
