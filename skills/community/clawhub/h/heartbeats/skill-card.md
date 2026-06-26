## Description: <br>
Guidelines for proactive behavior, periodic checks, and memory maintenance using heartbeats and cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FlayZz](https://clawhub.ai/user/FlayZz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure proactive heartbeat checks, choose between heartbeat polls and cron jobs, and maintain compact long-term memory notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages unattended checks across private accounts, workspace files, and project state. <br>
Mitigation: Restrict which accounts, directories, and files the agent may inspect before enabling heartbeat behavior. <br>
Risk: The skill permits proactive memory edits and repository changes, including commits and pushes. <br>
Mitigation: Require explicit approval before commits, pushes, deletions, or long-term memory updates, and periodically review HEARTBEAT.md, MEMORY.md, and memory/heartbeat-state.json. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with optional JSON state and file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update HEARTBEAT.md, MEMORY.md, memory/heartbeat-state.json, documentation, and repository state when the agent is allowed to act proactively.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
