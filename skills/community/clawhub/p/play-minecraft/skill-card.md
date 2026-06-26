## Description: <br>
Guides an agent to control a Mindcraft Minecraft bot through a local HTTP API without an embedded LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Songjc0511](https://clawhub.ai/user/Songjc0511) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent builders use this skill to discover Mindcraft agents, inspect action schemas, execute bot commands, verify state, and recover from failed or stuck Minecraft bot actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to control a local Mindcraft Minecraft bot and can affect a real game world. <br>
Mitigation: Use a trusted Mindcraft service, review the action schema before running tasks, and validate automation in a private or local world before broader use. <br>
Risk: Unattended or bulk actions could produce unintended changes in important or shared worlds. <br>
Mitigation: Run tasks stepwise, verify state after each action, and use the documented stop command before recovery actions when behavior diverges. <br>
Risk: Request logs and state snapshots may contain local world or session details. <br>
Mitigation: Keep generated request and state logs private, and delete them when they are no longer needed. <br>


## Reference(s): <br>
- [OpenClaw Call Reference](reference.md) <br>
- [Call Examples](examples.md) <br>
- [ClawHub Release Page](https://clawhub.ai/Songjc0511/play-minecraft) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, API calls, configuration] <br>
**Output Format:** [Markdown with JSON, PowerShell, Python, and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include request payloads, response payloads, and before/after state snapshots for action verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
