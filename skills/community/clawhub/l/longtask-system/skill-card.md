## Description: <br>
State-file driven long task manager that splits tasks into sequential subtasks, supports multi-agent collaboration, and provides real-time visual monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-1106](https://clawhub.ai/user/noah-1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate long-running work by defining ordered task JSON steps, dispatching them to one or more agents, recording completion state, and monitoring progress through logs or a generated cockpit view. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent daemon orchestration can continue dispatching agent work from local task JSON after setup. <br>
Mitigation: Use trusted task files, monitor daemon logs and inbox state, and keep a clear stop procedure for the screen or setsid process. <br>
Risk: Subtasks force a new agent conversation, which can drop important constraints from earlier context. <br>
Mitigation: Repeat critical user requirements and safety constraints inside every task step before execution. <br>
Risk: Generated cockpit HTML may render untrusted task content without escaping. <br>
Mitigation: Avoid opening cockpit HTML from untrusted task files until content escaping is fixed or reviewed. <br>


## Reference(s): <br>
- [LongTask System ClawHub page](https://clawhub.ai/noah-1106/longtask-system) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task orchestration instructions, state-file conventions, daemon commands, inbox recovery guidance, and cockpit rendering guidance.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
