## Description: <br>
Autonomously diagnose and fix OpenClaw system errors affecting the UI, channels, gateway, memory, pairing, or heartbeat checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jbauman-26](https://clawhub.ai/user/jbauman-26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to troubleshoot and recover OpenClaw installations when the control UI, messaging channels, gateway, memory plugin, pairing flow, or heartbeat checks fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to restart OpenClaw services, approve pairing, clear cache, or kill processes before asking the user. <br>
Mitigation: Require manual approval before service stops or restarts, process termination, pairing approval, cache clearing, or configuration reloads on production systems or during active sessions. <br>
Risk: Some recovery paths involve credentials, corrupted configuration, or session history where an incorrect action could cause data loss or account disruption. <br>
Mitigation: Escalate before credential resets, significant configuration edits, or any change involving corrupted session files. <br>


## Reference(s): <br>
- [OpenClaw Diagnostics](references/diagnostics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with diagnostic findings, recovery commands, and verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command output interpretation and escalation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
