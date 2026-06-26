## Description: <br>
Manage Proxmox VE clusters via REST API, including nodes, VMs, containers, power states, snapshots, backups, storage, and tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricanwarfare](https://clawhub.ai/user/ricanwarfare) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, infrastructure operators, and administrators use this skill to inspect and manage Proxmox VE clusters from an agent workflow. It supports read-only cluster status checks and high-impact administrative operations such as VM power changes, snapshots, backups, and rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer Proxmox infrastructure, including start, stop, shutdown, reboot, snapshot, backup, deletion, and rollback operations. <br>
Mitigation: Require explicit user confirmation before high-impact operations, especially on production clusters. <br>
Risk: Proxmox API credentials can grant broad infrastructure access if overprivileged or exposed. <br>
Mitigation: Use a least-privilege Proxmox API token and protect credential files with restrictive permissions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ricanwarfare/proxmox-complete) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may return JSON status or error objects; some bash helper commands emit tabular text.] <br>

## Skill Version(s): <br>
1.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
