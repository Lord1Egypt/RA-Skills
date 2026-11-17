## Description:

Multi-service health and uptime monitoring for websites, APIs, SSL certificates, DNS, Docker containers, systemd services, SSH checks, disk usage, incidents, and uptime reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, system administrators, agency operators, and IT teams use this skill to configure and run local health checks, inspect service status, review incidents, and report uptime for managed infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved service targets can be executed through unsafe shell commands.

Mitigation: Review before installing, run under a low-privilege account, add service targets only from trusted sources, and avoid enabling the systemd timer until shell command construction is fixed.

Risk: The ssh_cmd check type runs commands on remote systems.

Mitigation: Restrict SSH checks to trusted hosts, trusted commands, and minimally privileged accounts.

Risk: Telegram notifications may send service names, targets, and health details off-host.

Mitigation: Treat Telegram bot tokens as secrets and enable notifications only when sharing those operational details with Telegram is acceptable.

## Reference(s):

- [Nex HealthCheck ClawHub page](https://clawhub.ai/nexaiguy/skills/nex-healthcheck)
- [Nex AI homepage](https://nex-ai.be)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output and concise Markdown guidance with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local health status, incident history, uptime percentages, SSL expiry warnings, and optional Telegram notification guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
