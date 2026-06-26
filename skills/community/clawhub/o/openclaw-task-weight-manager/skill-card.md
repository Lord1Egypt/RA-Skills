## Description: <br>
Helps an OpenClaw agent manage multiple interleaved conversation threads by identifying the mainline task, weighting side topics, parking distractions, and periodically steering attention back to the highest-priority work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LucasZH7](https://clawhub.ai/user/LucasZH7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to keep one chat organized around a mainline task while lower-priority side topics are classified, parked, and revisited when priorities change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local task notes may capture sensitive project context if the persistence or bootstrap workflow is used. <br>
Mitigation: Review generated markdown files before committing or sharing a workspace, and avoid storing secrets in thread notes. <br>
Risk: Priority weighting can over-focus on a stale mainline or park an urgent interruption when user intent changes. <br>
Mitigation: Accept explicit priority changes from the user and re-run re-weighting when urgency, blockers, or task ownership changes. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/LucasZH7/openclaw-task-weight-manager) <br>
- [Project Homepage](https://github.com/LucasZH7/openclaw-task-weight-manager) <br>
- [OpenClaw Integration Notes](references/integration.md) <br>
- [Usage Patterns](references/usage-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status blocks, human-readable task boards, and optional shell commands for bootstrapping workspace notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local markdown files under task-weight-manager/ and HEARTBEAT.md when the bootstrap script or persistence workflow is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
