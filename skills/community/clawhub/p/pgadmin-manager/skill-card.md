## Description:

Manage the pgAdmin Docker container for local dev environments. Provides a web UI for PostgreSQL at http://localhost:8082. Requires postgres-manager and proxy-manager to be running first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pereirajair](https://clawhub.ai/user/pereirajair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start, stop, inspect, and access a local pgAdmin Docker container for PostgreSQL administration in local development environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts a persistent pgAdmin database administration interface with publicly documented default credentials.

Mitigation: Set unique PGADMIN_EMAIL and PGADMIN_PASSWORD values before starting the container and avoid using the documented defaults.

Risk: Containers on the shared Docker network may be able to reach the PostgreSQL and pgAdmin services.

Mitigation: Restrict which containers can join the shared Docker network and keep the pgAdmin port bound to localhost.

Risk: The pgAdmin volume preserves server configuration across restarts.

Mitigation: Stop the service when it is not needed and remove the pgAdmin volume when saved server configuration should no longer persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pereirajair/skills/pgadmin-manager)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on Docker Compose lifecycle commands and local pgAdmin connection settings.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
