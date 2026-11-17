## Description:

Manage a shared PostgreSQL Docker container for local development environments, including container lifecycle, database creation and removal, cross-instance dumps, and shared Docker network integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pereirajair](https://clawhub.ai/user/pereirajair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage a local PostgreSQL service for development workflows, including starting and stopping the container, creating isolated databases, copying databases with pg_dump, and opening psql sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts a persistent local PostgreSQL database with documented default credentials.

Mitigation: Set a strong POSTGRES_PASSWORD before using real or shared data, and rotate credentials for any existing persisted volume.

Risk: Database data persists in a Docker volume after the container is stopped.

Mitigation: Treat the Docker volume as persistent storage and remove it only when intentional data deletion is acceptable.

Risk: psql provides direct database access.

Mitigation: Use the skill only with local development data unless access, credentials, and data handling have been reviewed.

Risk: The container joins a shared Docker network.

Mitigation: Consider a dedicated Docker network when isolation is required.

## Reference(s):

- [Postgres Manager on ClawHub](https://clawhub.ai/pereirajair/skills/postgres-manager)
- [Publisher profile: pereirajair](https://clawhub.ai/user/pereirajair)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output may include Docker and PostgreSQL lifecycle commands for a local development environment.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
