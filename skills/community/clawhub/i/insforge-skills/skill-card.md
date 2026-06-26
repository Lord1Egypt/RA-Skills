## Description: <br>
Create and manage InsForge projects using the CLI. Handles authentication, project setup, database management, edge functions, storage, deployments, and secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonychang04](https://clawhub.ai/user/tonychang04) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agents use this skill to administer InsForge Backend-as-a-Service projects through the InsForge CLI, including authentication, project setup, database work, function deployment, hosting deployments, storage, secrets, schedules, and logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authority over live InsForge resources, including databases, secrets, deployments, storage, and schedules. <br>
Mitigation: Require explicit approval before raw SQL, imports, exports, secret reads, deletes, deployments, schedule changes, and any use of --yes. <br>
Risk: Credential and project configuration exposure could leak access tokens, passwords, project IDs, API keys, exports, or deployment archives. <br>
Mitigation: Use masked secret stores for credentials, keep .insforge/project.json private, and keep exports and deployment archives out of logs, chats, and version control. <br>
Risk: Project creation may auto-install additional agent skill content. <br>
Mitigation: Review any auto-installed .agents/skills/insforge/ content before allowing an agent to rely on it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tonychang04/insforge-skills) <br>
- [Publisher profile](https://clawhub.ai/user/tonychang04) <br>
- [insforge create](references/create.md) <br>
- [insforge db export](references/db-export.md) <br>
- [insforge db import](references/db-import.md) <br>
- [insforge db query](references/db-query.md) <br>
- [insforge deployments deploy](references/deployments-deploy.md) <br>
- [insforge functions deploy](references/functions-deploy.md) <br>
- [insforge login](references/login.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, SQL examples, and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide execution of live InsForge CLI operations that affect projects, databases, deployments, storage, secrets, and schedules.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
