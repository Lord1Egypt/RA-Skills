## Description: <br>
Linux Sysadmin helps agents provide Linux administration guidance across users and permissions, SSH, storage, networking, systemd, firewalls, monitoring, backups, TLS, Ansible, containers, and Infrastructure as Code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[husttsq](https://clawhub.ai/user/husttsq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and site reliability engineers use this skill to plan, execute, verify, and roll back Linux system administration tasks with command examples and operational checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers high-impact Linux administration operations that can change access, networking, storage, services, security posture, and production availability. <br>
Mitigation: Review every generated command, confirm target hosts and files, make backups, and prepare rollback steps before applying changes. <br>
Risk: Bundled audit and management scripts may collect sensitive administrative data or be unsafe if run with excessive privileges. <br>
Mitigation: Avoid running scripts as root unless required, inspect script behavior first, and protect generated audit output as sensitive operational data. <br>
Risk: Commands for SSH, firewall, sudoers, fstab, LVM, and backup recovery can lock out administrators or cause data loss if applied incorrectly. <br>
Mitigation: Validate changes in a test environment where possible, keep an alternate access path, use syntax checks such as visudo or mount -a, and verify backups before destructive actions. <br>


## Reference(s): <br>
- [Quick reference](references/quick_reference.md) <br>
- [User and permission management](references/user_permission.md) <br>
- [SSH management](references/ssh_management.md) <br>
- [Storage and filesystem](references/storage_filesystem.md) <br>
- [Network configuration](references/network_config.md) <br>
- [systemd services](references/systemd_services.md) <br>
- [Firewall and security hardening](references/firewall_security.md) <br>
- [Monitoring and logging](references/monitoring_logging.md) <br>
- [Backup and recovery](references/backup_recovery.md) <br>
- [Certificate and TLS operations](references/certificate_tls.md) <br>
- [Ansible automation](references/ansible_automation.md) <br>
- [Container management](references/container_management.md) <br>
- [Infrastructure as Code](references/infrastructure_as_code.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, checklists, and reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference bundled audit scripts and operational runbooks; generated commands require human review before execution.] <br>

## Skill Version(s): <br>
3.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
