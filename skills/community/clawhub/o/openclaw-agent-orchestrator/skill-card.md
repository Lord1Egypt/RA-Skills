## Description: <br>
Creates and repairs durable OpenClaw agents, bindings, and runtime state with verification against live OpenClaw command output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create durable OpenClaw agents, repair missing bindings, and confirm runtime state before reporting orchestration results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can replace durable OpenClaw workspaces and copy broad private workspace contents. <br>
Mitigation: Use it only for explicit OpenClaw agent-management tasks, choose simple safe agent IDs, inspect or back up the source workspace, and avoid running it against existing agents unless workspace replacement is intended. <br>
Risk: Agent or binding status may be misreported if runtime state is not checked after changes. <br>
Mitigation: Report creation, repair, or routing results only after the relevant OpenClaw JSON output shows the expected live state. <br>


## Reference(s): <br>
- [OpenClaw Agent Orchestrator on ClawHub](https://clawhub.ai/matthewxmurphy/openclaw-agent-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and references to JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw CLI access and verified runtime output before reporting state changes.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
