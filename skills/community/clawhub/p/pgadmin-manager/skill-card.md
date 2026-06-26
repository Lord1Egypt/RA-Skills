## Description: <br>
Manage the pgAdmin Docker container for local dev environments and provide a localhost web UI for PostgreSQL at http://localhost:8082. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pereirajair](https://clawhub.ai/user/pereirajair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to start, stop, inspect, and access a local pgAdmin container for PostgreSQL database management in a Docker-based development environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default pgAdmin password is weak even though the service is bound to localhost. <br>
Mitigation: Set a strong PGADMIN_PASSWORD before starting the container. <br>
Risk: Saved pgAdmin server configurations persist in the pgadmin_data Docker volume. <br>
Mitigation: Avoid storing sensitive production database connections and remove the pgadmin_data volume when saved configurations should no longer persist. <br>
Risk: The skill starts a Docker container from the dpage/pgadmin4:8.6 image. <br>
Mitigation: Install and run it only when you trust the Docker image and need a local pgAdmin instance. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/pereirajair/pgadmin-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Docker lifecycle guidance for pgAdmin, including access URL, login settings, prerequisites, and persistence notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
