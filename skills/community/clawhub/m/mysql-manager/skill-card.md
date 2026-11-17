## Description:

Manage a shared MySQL Docker container for local dev environments, including container lifecycle, database creation and removal, and cross-instance data dumps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pereirajair](https://clawhub.ai/user/pereirajair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate a local shared MySQL container for development workflows, create or remove databases, inspect status, and copy data between local database instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships with an unsafe default MySQL root password for local Docker use.

Mitigation: Set MYSQL_ROOT_PASSWORD to a strong non-default value before first start and rotate any volume that was initialized with the default secret.

Risk: Create, dump, and drop operations can change or delete shared local database data.

Mitigation: Review the target database name before running mutation commands, keep the drop confirmation prompt in place, and avoid using this against data that is not backed up.

Risk: The MySQL container joins a Docker network that other containers can access.

Mitigation: Avoid sharing the Docker network with untrusted containers and use the localhost-only host port binding for local access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pereirajair/skills/mysql-manager)
- [Skill instructions](artifact/SKILL.md)
- [Docker Compose configuration](artifact/docker-compose.yml)
- [MySQL manager shell runner](artifact/run.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are guidance for running Docker and MySQL administration commands; command execution can mutate local database state.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
