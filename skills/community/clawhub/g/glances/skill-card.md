## Description:

Glances - cross-platform system monitoring guidance for installing, running, configuring, and troubleshooting Glances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and administrators use this skill to monitor local or remote systems with Glances, interpret resource metrics, configure alerts, expose Web/API modes, and export monitoring data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged Docker examples and Docker socket mounts can expose host-level control.

Mitigation: Use those examples only in trusted administrative environments after reviewing Docker socket access, host PID/network settings, and least-privilege alternatives.

Risk: Web, API, and server modes can expose system monitoring data if bound to public interfaces.

Mitigation: Bind services to localhost by default and add authentication, firewall rules, SSH tunneling, or other network controls before enabling remote access.

Risk: Persistent service, cron, sudo, sudo pip, and mutable latest-image examples can create durable or hard-to-audit system changes.

Mitigation: Manually review persistence setup, prefer isolated package installation, avoid mutable latest tags for controlled deployments, and confirm commands before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cn-big-cabbage/skills/glances)
- [ClawHub Publisher Profile](https://clawhub.ai/user/cn-big-cabbage)
- [Glances Homepage](https://nicolargo.github.io/glances/)
- [Glances Documentation](https://glances.readthedocs.io/)
- [Glances Docker Hub](https://hub.docker.com/r/nicolargo/glances)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for local monitoring, Web/API modes, Docker runs, service setup, data export, and troubleshooting.]

## Skill Version(s):

0.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
