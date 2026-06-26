## Description: <br>
Provides a three-layer local memory system that helps an agent retain user preferences, feedback, project context, and references to external systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinnzen](https://clawhub.ai/user/sinnzen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they want an agent to organize durable local notes about user background, work preferences, project state, and external-system pointers. It is intended for local memory workflows where entries can be reviewed against current project state before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist personal, project, and external-system context without explicit consent, retention, or deletion controls. <br>
Mitigation: Use a MEMORY_WORKSPACE directory you control, avoid storing secrets or regulated/confidential data, and periodically review or delete stored memory files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sinnzen/memory-hierarchy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown memory entries and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local memory files under MEMORY_WORKSPACE or the default local OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
