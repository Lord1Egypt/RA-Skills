## Description:

Initialize and configure Traefik reverse proxy with Docker, including Docker Compose setup, path-prefix or host-based routing, dashboard access, metrics, logging, and tracing options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[le-shi](https://clawhub.ai/user/le-shi)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up a Traefik v3 reverse proxy with Docker Compose, configure service routing, and enable operational features such as dashboard access, logs, metrics, and tracing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default templates expose sensitive Docker and dashboard access patterns that require review before installation.

Mitigation: Use a Docker socket proxy or file provider instead of mounting /var/run/docker.sock directly, disable api.insecure, keep the dashboard off public networks, and require authentication and HTTPS.

Risk: Administrative routes can become reachable from unintended networks if deployed without access controls.

Mitigation: Restrict admin routes by IP allowlist or VPN and review route exposure before starting Traefik.

Risk: Unpinned images or helper dependencies can change behavior over time.

Mitigation: Pin container images and helper dependencies before production use.

## Reference(s):

- [Traefik Configuration Examples](references/examples.md)
- [Traefik Features](references/features.md)
- [Traefik Configuration Summary](references/summary.md)
- [Docker Compose Template](assets/docker-compose.yml)
- [Traefik Dynamic Configuration Template](assets/traefik-dynamic.yml)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Docker Compose and Traefik dynamic configuration templates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
