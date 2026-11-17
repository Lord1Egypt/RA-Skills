## Description:

Linux Sysadmin helps agents provide Linux system administration guidance across users and permissions, SSH, storage, networking, systemd, firewalls, monitoring, backups, TLS, Ansible, containers, and infrastructure as code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[husttsq](https://clawhub.ai/user/husttsq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and system administrators use this skill to plan, validate, harden, monitor, back up, automate, troubleshoot, and roll back Linux server changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest root-level Linux administration changes.

Mitigation: Review every proposed command and configuration change before execution, especially on production systems.

Risk: Some examples may install remote scripts or unverified binaries.

Mitigation: Prefer package-manager sources or verify checksums and signatures before installing downloaded software.

Risk: Some examples may grant persistent broad privileges such as NOPASSWD sudo or Docker group access.

Mitigation: Replace broad privilege examples with narrowly scoped sudo rules, temporary access, or role-specific permissions.

## Reference(s):

- [Linux Sysadmin Skill](https://clawhub.ai/husttsq/skills/linux-sysadmin)
- [Linux Sysadmin Quick Reference](references/quick_reference.md)
- [User and Permission Management](references/user_permission.md)
- [SSH Management](references/ssh_management.md)
- [Storage and Filesystem Management](references/storage_filesystem.md)
- [Network Configuration](references/network_config.md)
- [systemd Services and Package Management](references/systemd_services.md)
- [Firewall and Security Hardening](references/firewall_security.md)
- [Monitoring and Logging](references/monitoring_logging.md)
- [Backup and Disaster Recovery](references/backup_recovery.md)
- [Certificate and TLS Management](references/certificate_tls.md)
- [Ansible Automation](references/ansible_automation.md)
- [Container Management](references/container_management.md)
- [Infrastructure as Code](references/infrastructure_as_code.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands, configuration snippets, checklists, and rollback steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose privileged Linux administration commands that require human review before execution.]

## Skill Version(s):

3.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
