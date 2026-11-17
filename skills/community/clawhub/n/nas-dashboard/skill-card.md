## Description:

Generates an alert-first text NAS and HomeLab dashboard covering system health, ZFS pools, disk SMART status, Docker, Frigate, GPU, UPS, backups, updates, and security checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wudi488](https://clawhub.ai/user/wudi488)

### License/Terms of Use:

MIT-0

## Use Case:

NAS, HomeLab, and self-hosted service operators use this skill to collect a daily health report and prioritize issues that need attention. It is best suited for Linux hosts running ZFS, Docker, UPS monitoring, and optional Frigate or NVIDIA GPU workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report may include sensitive infrastructure and security details, especially when delivered to Telegram.

Mitigation: Send reports only to trusted private destinations and treat dashboard output as operationally sensitive.

Risk: Collection depends on passwordless sudo for host, SMART, firewall, SSH, and backup checks.

Mitigation: Use a tightly scoped sudoers policy for the required diagnostics instead of broad passwordless sudo.

Risk: The dashboard can print privileged repair commands for storage, SSH, firewall, updates, and backups.

Mitigation: Review each command manually before execution and confirm it matches the host's storage, network, and backup configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wudi488/skills/nas-dashboard)
- [Packaged skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text dashboard report with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alert-first report intended to stay under 2000 characters, with severity labels and action guidance.]

## Skill Version(s):

3.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
