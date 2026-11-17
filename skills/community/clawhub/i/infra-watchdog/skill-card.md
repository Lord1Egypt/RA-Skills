## Description:

Self-hosted infrastructure monitoring for HTTP, TCP, SSL, disk, memory, load, Docker, DNS, and custom commands with alerting via OpenClaw messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure operators use this skill to configure local health checks for endpoints, services, containers, system resources, DNS, SSL certificates, and alert delivery from an OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSL certificate and HTTPS checks can falsely report certificates as valid.

Mitigation: Validate SSL behavior before relying on this skill for certificate or HTTPS security monitoring.

Risk: Some advertised monitoring features may be incomplete or inconsistent with the shipped code.

Mitigation: Review configured monitor types and run checks in a controlled environment before operational deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariusfit/skills/infra-watchdog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational monitoring guidance and local command examples that should be reviewed before use.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact/skill.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
