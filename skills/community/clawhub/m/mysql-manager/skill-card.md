## Description: <br>
Manage a shared MySQL Docker container for local dev environments, including container lifecycle, database creation and removal, and cross-instance data dumps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pereirajair](https://clawhub.ai/user/pereirajair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage a local Docker-backed MySQL service for development workflows, including starting and stopping the service, creating or dropping databases, checking status, and copying data between local databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database administration commands can delete or overwrite local data, especially through drop and dump workflows. <br>
Mitigation: Review database names and targets before execution, avoid production or irreplaceable data, and rely on the interactive confirmation before dropping databases. <br>
Risk: The default MySQL root password is intended only for local development and may be unsafe on shared machines. <br>
Mitigation: Set a non-default MYSQL_ROOT_PASSWORD before starting the container, especially when handling real data or using a shared host. <br>
Risk: The Docker container and named volume can persist beyond the immediate task. <br>
Mitigation: Stop the service when finished and intentionally remove volumes only when persisted data should be deleted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pereirajair/mysql-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker on Linux or macOS; manages a local MySQL 8.0.36 container and persistent Docker volume.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
