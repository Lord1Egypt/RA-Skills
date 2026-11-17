## Description:

Manage MikroTik RouterOS devices via API to view status, firewall rules, network configuration, logs, users, backups, and run custom commands across multiple devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drodecker](https://clawhub.ai/user/drodecker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network administrators use this skill to inspect and manage MikroTik RouterOS devices, including status, firewall, interface, routing, user, log, backup, and custom command workflows across one or more configured routers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Router credentials may grant broad control over network infrastructure.

Mitigation: Use dedicated least-privileged RouterOS accounts, avoid admin or empty passwords, and do not place router passwords in TOOLS.md or command-line arguments.

Risk: Custom commands and lifecycle operations can change, interrupt, or expose router configuration.

Mitigation: Require explicit user approval before custom commands, reboot, shutdown, backup, cleanup, or other high-impact actions.

Risk: Network scanning and unauthenticated or weakly protected connections may expose activity on untrusted networks.

Mitigation: Run scans only on authorized networks and avoid untrusted networks until TLS support and certificate validation are implemented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drodecker/skills/mikrotik-routeros)
- [MikroTik RouterOS API documentation](https://help.mikrotik.com/docs/display/ROS/API)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with RouterOS command paths, Python snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include device-specific command output, RouterOS API paths, and network or credential handling guidance.]

## Skill Version(s):

2026.3.30 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
