## Description:

Set up a full local LGTM observability stack (Loki + Grafana + Tempo + Prometheus + Alloy) for FastAPI apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add local logs, metrics, traces, and Grafana dashboards to FastAPI applications without relying on a hosted observability service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: No-login monitoring services may be reachable beyond the intended local development environment.

Mitigation: Bind exposed Docker ports to 127.0.0.1 and disable anonymous Grafana Admin access or add authentication before running the stack.

Risk: Helper scripts accept service names and ports that affect Prometheus target files.

Mitigation: Validate service names and ports before registration, especially on shared machines or shared workspaces.

Risk: Dependency ranges are not pinned to exact reviewed versions.

Mitigation: Use pinned dependencies or a reviewed lockfile before deploying the instrumentation into sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/observability-lgtm)
- [ClawHub publisher profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python snippets, Docker Compose configuration, and service setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Docker and FastAPI observability setup instructions; requires docker and docker-compose.]

## Skill Version(s):

1.2.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
