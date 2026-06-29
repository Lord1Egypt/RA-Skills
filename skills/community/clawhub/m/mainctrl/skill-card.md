## Description: <br>
MainCtrl is a runtime safety guard for OpenClaw multi-agent workflows that blocks configured destructive tool calls for controlled agents and redirects them toward sub-agent delegation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ifeel-is-a-mouse](https://clawhub.ai/user/ifeel-is-a-mouse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using OpenClaw multi-agent workflows use MainCtrl to keep orchestration agents in read and delegation mode while preserving execution access for configured sub-agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MainCtrl is a workflow guard, not a hard security sandbox, so uncontrolled agents or unsuitable permissions can still allow destructive actions. <br>
Mitigation: Use it as a delegation guard, keep sub-agent permissions appropriate, and verify controlled agents and status before relying on the protection. <br>
Risk: Plugin install, plugin remove, and refresh-memory commands intentionally change the local OpenClaw environment or memory files. <br>
Mitigation: Run those commands only when those local changes are intended, then review MainCtrl status after the operation. <br>


## Reference(s): <br>
- [MainCtrl on ClawHub](https://clawhub.ai/ifeel-is-a-mouse/skills/mainctrl) <br>
- [README.md](artifact/README.md) <br>
- [plugin/README.md](artifact/plugin/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local OpenClaw plugin installation state, MainCtrl state, or workspace memory when the documented commands are executed.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
