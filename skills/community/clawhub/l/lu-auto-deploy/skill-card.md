## Description:

Lu Auto Deploy helps agents generate Docker deployment commands, Docker Compose templates, and configuration guidance for common self-hosted services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesson1222-ship-it](https://clawhub.ai/user/jesson1222-ship-it)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and self-hosting administrators use this skill to draft Docker commands and compose files for monitoring, media, utility, and security services. It is most useful when the user wants repeatable deployment templates or batch deployment guidance for a Docker host or NAS-style environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Docker templates may expose powerful services, administrative interfaces, broad host mounts, or Docker socket access.

Mitigation: Review every command before execution, bind sensitive services to localhost or a private admin network, avoid exposing Portainer directly, avoid raw Docker socket access where possible, and narrow File Browser mounts to a dedicated directory.

Risk: Some templates use mutable container image tags such as latest, which can change behavior over time.

Mitigation: Pin image versions or digests before deployment and require an explicit dry run before any deployment is executed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jesson1222-ship-it/skills/lu-auto-deploy)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Docker CLI and Docker Compose code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service templates, generated configuration files, deployment steps, and update guidance.]

## Skill Version(s):

1.0.0 (source: release metadata, artifact metadata, and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
