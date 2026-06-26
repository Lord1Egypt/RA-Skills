## Description: <br>
Helps agents manage InsForge backend projects, including authentication, project setup, SQL/database work, edge functions, storage, frontend deployments, secrets, schedules, logs, and documentation lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonychang04](https://clawhub.ai/user/tonychang04) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate InsForge Backend-as-a-Service projects from the command line, especially for database changes, deployment workflows, secret management, scheduled tasks, and troubleshooting logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent make broad administrative changes to databases, secrets, deployments, schedules, storage, and persistent backend resources. <br>
Mitigation: Confirm the target project before mutations, review SQL/import/export/delete/deploy actions, and avoid using --yes unless prompts should be skipped. <br>
Risk: The skill can handle sensitive material such as secret values, API keys, credentials, database dumps, and project configuration. <br>
Mitigation: Treat credentials, API keys, dumps, and .insforge/project.json as sensitive; do not commit or share them publicly. <br>
Risk: Project creation can install additional agent skills into the workspace. <br>
Mitigation: Inspect any agent skills added under .agents/skills/insforge after project creation before relying on them. <br>


## Reference(s): <br>
- [insforge create](references/create.md) <br>
- [insforge login](references/login.md) <br>
- [insforge db query](references/db-query.md) <br>
- [insforge db export](references/db-export.md) <br>
- [insforge db import](references/db-import.md) <br>
- [insforge functions deploy](references/functions-deploy.md) <br>
- [insforge deployments deploy](references/deployments-deploy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash, SQL, JSON, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify local configuration files and call InsForge CLI commands when used by an agent.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence; artifact metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
