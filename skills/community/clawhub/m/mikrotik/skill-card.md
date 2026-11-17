## Description:

Connects to and manages MikroTik RouterOS devices through the RouterOS API, including device status, firewall rules, network configuration, local network scans, and custom RouterOS commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2944721178](https://clawhub.ai/user/2944721178)

### License/Terms of Use:

MIT-0

## Use Case:

Network administrators and developers use this skill to inspect and manage MikroTik RouterOS devices from an agent workflow, including status checks, firewall and network review, API service checks, backups, and custom RouterOS commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network scanning can generate active probe traffic against local subnets and may trigger monitoring or disrupt sensitive environments.

Mitigation: Run scans only on networks you administer, preferably in a lab or isolated management environment, and get explicit approval before scanning production networks.

Risk: Router credentials may be supplied through TOOLS.md, environment variables, or command-line arguments.

Mitigation: Avoid real administrator passwords in plaintext files or command histories, avoid blank or default credentials, and prefer least-privileged RouterOS accounts.

Risk: Custom RouterOS commands and router administration actions can change or expose sensitive network configuration.

Mitigation: Review commands before execution, restrict use to authorized operators, and test administrative workflows on non-production devices first.

## Reference(s):

- [ClawHub Mikrotik skill page](https://clawhub.ai/2944721178/skills/mikrotik)
- [MikroTik RouterOS API documentation](https://help.mikrotik.com/docs/display/ROS/API)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-style text with RouterOS command examples and tabular status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include router status, firewall and network summaries, scan results, API configuration guidance, backup guidance, and command execution results.]

## Skill Version(s):

1.8.5 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
