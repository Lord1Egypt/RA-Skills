## Description: <br>
Logs significant agent activities to a local Mission Claw dashboard with token usage tracking for task, project, status, and progress records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsangwailam](https://clawhub.ai/user/tsangwailam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to record completed or in-progress work, token usage, project context, and service status in a local Mission Claw dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the Mission Claw npm package and the local mclaw binary. <br>
Mitigation: Install only when you intend to run Mission Claw and trust the mission-claw package source. <br>
Risk: Logged task names, project names, details, agent identifiers, and token counts become persistent work records. <br>
Mitigation: Avoid logging secrets, customer data, credentials, or sensitive internal details. <br>
Risk: The CLI communicates with a local daemon for activity logging. <br>
Mitigation: Keep the local daemon bound to trusted local access. <br>


## Reference(s): <br>
- [Mission Claw ClawHub listing](https://clawhub.ai/tsangwailam/mission-claw) <br>
- [Mission Claw repository](https://github.com/tsangwailam/mcclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command arguments for action, agent, project, status, duration, and token counts.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
