## Description: <br>
Integrates with MissionClaw for project management and AI agent orchestration, helping users create projects, manage Kanban tasks, assign work to agents, view org charts, and schedule automated tasks against a local MissionClaw API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sureshchitmil](https://clawhub.ai/user/sureshchitmil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using MissionClaw use this skill to create projects from chat commands, track project status, list projects, and route work to teams through a local MissionClaw instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent project, agent, and scheduled-task changes through a local MissionClaw API without detailed scoping or confirmation in the artifact. <br>
Mitigation: Use only with a trusted local MissionClaw instance, confirm what data each command sends, and ensure projects, assignments, and scheduled tasks can be listed, audited, and removed. <br>


## Reference(s): <br>
- [ClawHub Missionclaw page](https://clawhub.ai/sureshchitmil/missionclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown command responses with project status, project IDs, team lists, and error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or query projects through a local MissionClaw API configured by MISSIONCLAW_URL.] <br>

## Skill Version(s): <br>
1.6.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
