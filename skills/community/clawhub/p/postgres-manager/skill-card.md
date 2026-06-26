## Description: <br>
Manage a shared PostgreSQL Docker container for local dev environments, including container lifecycle, database creation and removal, and cross-instance dumps via pg_dump. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pereirajair](https://clawhub.ai/user/pereirajair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run and administer a local PostgreSQL Docker service for development workflows. It helps start and stop the service, create or drop development databases, inspect status, open psql, and copy data between databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages a local Docker PostgreSQL service and can start, stop, inspect, and administer containers and databases. <br>
Mitigation: Install and use it only when local PostgreSQL container management is intended, and stop the container when it is no longer needed. <br>
Risk: Database dump and drop workflows can copy or remove local development data. <br>
Mitigation: Review database names before dump or drop commands, keep the documented confirmation step for drops, and avoid targeting the main database. <br>
Risk: The documented default PostgreSQL password is suitable only for local development. <br>
Mitigation: Set POSTGRES_PASSWORD before use on shared systems or when working with real data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pereirajair/postgres-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Docker and PostgreSQL administration guidance; command execution can affect local containers, volumes, and databases.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
