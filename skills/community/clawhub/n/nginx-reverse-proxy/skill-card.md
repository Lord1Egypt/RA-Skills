## Description:

Configures nginx reverse proxy settings for binding a domain to a specified IP address and port.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudswave](https://clawhub.ai/user/cloudswave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate nginx reverse proxy configuration and commands for binding a domain to a target IP address and port, including optional TLS certificate setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live nginx and TLS configuration with root privileges.

Mitigation: Use it only on hosts where privileged nginx and certificate changes are intended, and require manual validation before running generated commands.

Risk: Incorrect domain, target, destination path, certificate command, or reload step could disrupt routing or TLS service.

Mitigation: Review the domain, target IP and port, generated config, destination path, certbot command, nginx test result, and reload step before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloudswave/skills/nginx-reverse-proxy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with nginx configuration and bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privileged commands that write nginx files, request certificates, test nginx configuration, and reload the nginx service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
