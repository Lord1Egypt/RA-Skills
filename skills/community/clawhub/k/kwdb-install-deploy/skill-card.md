## Description:

Triggered when the user wants to install or deploy KaiwuDB (kwdb, kaiwudb). Helps users complete script-based deployment of KaiwuDB clusters, including configuration file modification, installation command execution, cluster initialization, and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwdb](https://clawhub.ai/user/kwdb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to prepare, configure, install, initialize, and check KaiwuDB deployments on Linux hosts or clusters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-supplied KaiwuDB archive may execute installer code with administrative access.

Mitigation: Verify the archive with an official signature or checksum and inspect or stage extracted files before allowing the agent to run installation commands.

Risk: The deployment workflow can use sudo, docker group access, passwordless SSH, and service auto-start across cluster nodes.

Mitigation: Use a dedicated least-privilege deployment account where possible, confirm each node and setting with the operator, and require approval before install, cluster initialization, or auto-start commands.

## Reference(s):

- [KaiwuDB Script Deployment Guide](references/installation_guide.md)
- [KaiwuDB Common Issues and Solutions](references/troubleshooting.md)
- [KWDB Install Deploy on ClawHub](https://clawhub.ai/kwdb/skills/kwdb-install-deploy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation of installation package path, deployment mode, node addresses, ports, security mode, and other deployment settings before execution.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
