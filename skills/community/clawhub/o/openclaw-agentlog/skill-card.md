## Description: <br>
OpenClaw AgentLog records OpenClaw agent sessions, tool activity, reasoning snippets, responses, token usage, and trace handoffs to an AgentLog backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hobo0cn](https://clawhub.ai/user/hobo0cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add AgentLog observability to OpenClaw agents, including automatic session evidence capture, trace lifecycle management, and handoff support between agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive agent activity may be captured and stored by the AgentLog backend. <br>
Mitigation: Deploy only with a trusted backend, review data retention controls, and disable or redact reasoning and tool capture when sensitive prompts, outputs, or file paths may be present. <br>
Risk: Installation can modify the OpenClaw runtime through postinstall or dist patching behavior. <br>
Mitigation: Review or disable patching before production use, confirm the remote target, keep backups, and test rollback before enabling it on a gateway. <br>
Risk: Trace and session data may expose workspace activity and command results. <br>
Mitigation: Limit access to trace storage, avoid using the skill in high-sensitivity workspaces without approval, and verify which event hooks are enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hobo0cn/openclaw-agentlog) <br>
- [OpenClaw plugin manifest](artifact/openclaw.plugin.json) <br>
- [OpenClaw plugin schema](https://openclaw.ai/schemas/plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [OpenClaw plugin hooks and TypeScript APIs with JSON trace/span payloads and shell-based installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records may include prompts, reasoning snippets, tool arguments, tool outputs, file paths, command results, token usage, and session metadata.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
