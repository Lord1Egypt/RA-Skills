## Description: <br>
Use this skill to manage Proxmox VE virtual machines, containers, snapshots, backups, storage, cluster status, HA, pools, firewall inspection, guest-agent checks, and related lifecycle operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and infrastructure teams use this skill to inspect and operate Proxmox VE resources through governed CLI and MCP workflows. It is suited for VM/container lifecycle tasks, snapshots, backups, storage checks, cluster inventory, and operational troubleshooting when the target is explicitly Proxmox VE. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate high-impact Proxmox resources, including VM and container lifecycle actions. <br>
Mitigation: Install only when agent access to Proxmox administration is intended, use least-privilege API tokens scoped to required pools or nodes, and verify dry-run and confirmation behavior for destructive commands. <br>
Risk: Proxmox credentials could grant broad infrastructure access if overprivileged or poorly protected. <br>
Mitigation: Use a dedicated API token, avoid root-equivalent permissions when possible, store secrets outside config files, and protect ~/.proxmox-aiops/.env with chmod 600 when that path is used. <br>
Risk: Repeated async operations or polling mistakes can create confusing infrastructure state. <br>
Mitigation: Poll returned task UPIDs with the provided task-status and task-log workflows rather than re-issuing write operations. <br>
Risk: Disabling TLS verification can hide endpoint impersonation or misconfiguration. <br>
Mitigation: Keep verify_ssl enabled for production targets and disable it only for controlled self-signed lab certificates. <br>


## Reference(s): <br>
- [Proxmox Aiops on ClawHub](https://clawhub.ai/zw008/skills/proxmox-aiops) <br>
- [Proxmox-AIops homepage](https://github.com/AIops-tools/Proxmox-AIops) <br>
- [proxmox-aiops capabilities](references/capabilities.md) <br>
- [proxmox-aiops CLI reference](references/cli-reference.md) <br>
- [proxmox-aiops setup guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration snippets, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MCP and CLI workflows may return Proxmox task UPIDs for asynchronous write operations.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
