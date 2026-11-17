## Description:

Manages MikroTik routers via the RouterOS API (port 8728/8729). Use when the user wants to configure, monitor, or troubleshoot a MikroTik router -- including interfaces, firewall, DHCP, DNS, routing, queues, VPN, and system management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluemeda](https://clawhub.ai/user/bluemeda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network engineers use this skill to configure, monitor, and troubleshoot MikroTik RouterOS devices through API calls, Python code, and REST examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe connection and installation defaults could expose router credentials or affect sensitive infrastructure.

Mitigation: Review before installing, use a least-privilege MikroTik account, and prefer TLS on port 8729 with certificate and hostname verification enabled.

Risk: Examples may place passwords on command lines or modify system Python packages.

Mitigation: Avoid command-line passwords and install dependencies in an isolated virtual environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for MikroTik RouterOS API and REST workflows; users should review commands before applying them to network infrastructure.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
