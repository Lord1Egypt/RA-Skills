## Description:

Manage the phpMyAdmin Docker container for local development environments, providing a local web UI for MySQL at http://localhost:8081 after mysql-manager and proxy-manager are running.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pereirajair](https://clawhub.ai/user/pereirajair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start, stop, check, and locate a local phpMyAdmin Docker container for MySQL administration in a ClawHub-managed development stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables local database administration through phpMyAdmin and may use a predictable default MySQL root password.

Mitigation: Set a strong unique MYSQL_ROOT_PASSWORD before starting the container and confirm the connected MySQL container is not using the default secret.

Risk: A running phpMyAdmin container can expose sensitive database controls if network access is broadened.

Mitigation: Keep the phpMyAdmin port bound to localhost, restrict access to the shared Docker network, and stop the container when it is not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pereirajair/skills/phpmyadmin-manager)
- [Publisher profile](https://clawhub.ai/user/pereirajair)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on Docker Compose lifecycle commands and local phpMyAdmin access details.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
