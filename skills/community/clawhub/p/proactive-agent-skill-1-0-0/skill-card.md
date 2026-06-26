## Description: <br>
Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve. Includes WAL Protocol, Working Buffer, Autonomous Crons, and battle-tested patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Flychicks](https://clawhub.ai/user/Flychicks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add durable working memory, recovery patterns, heartbeat checks, and scheduled proactive routines to AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad persistent logging that could retain private data, credentials, regulated data, or private messages. <br>
Mitigation: Define allowed logging scope before use, exclude secrets and sensitive data by default, and periodically review or delete memory files. <br>
Risk: Scheduled background routines may run checks or automation beyond the user's intended scope. <br>
Mitigation: Require approval for mutating cron tasks and clearly define which files, conversations, and integrations may be checked. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Flychicks/proactive-agent-skill-1-0-0) <br>
- [OpenClaw Proactive Agent homepage](https://lobehub.com/skills/openclaw-skills-proactive-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup patterns, memory file templates, cron examples, and operational best practices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
