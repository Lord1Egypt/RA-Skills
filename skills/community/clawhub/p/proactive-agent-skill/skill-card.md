## Description: <br>
Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangkelvin](https://clawhub.ai/user/fangkelvin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent working memory, recovery logs, heartbeat checks, and scheduled automation patterns to an agent. It is intended for configuring proactive agent behavior such as routine checks, context recovery, and repeated maintenance tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory and working logs may retain credentials, tokens, regulated personal data, or confidential business content. <br>
Mitigation: Define what may be remembered before enabling the skill, exclude sensitive data categories, and provide a review and deletion process for saved memory. <br>
Risk: Recurring heartbeats, private account checks, and autonomous cron jobs may run beyond the user's intended scope. <br>
Mitigation: Narrowly specify allowed accounts, folders, checks, and schedules, and maintain a clear way to review, disable, and remove recurring tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fangkelvin/proactive-agent-skill) <br>
- [OpenClaw skill homepage](https://lobehub.com/skills/openclaw-skills-proactive-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides templates and operational patterns for memory files, heartbeat checks, and scheduled tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
