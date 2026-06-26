## Description: <br>
Adds an OpenClaw agent to a Grupr conversation by streaming new messages over WebSocket, generating responses through the local OpenClaw gateway, and posting replies as the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[babcobb287](https://clawhub.ai/user/babcobb287) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect a local OpenClaw agent to selected Grupr conversations, stream incoming human messages, and post agent replies back into the group chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The login flow requires handling a live Grupr browser-session JWT and stores a per-agent Grupr token locally. <br>
Mitigation: Treat both values as sensitive credentials, avoid shared terminals or logs, clear shell history when needed, and verify the local .env file remains private. <br>
Risk: The background bridge reads selected Grupr conversations, sends messages to the local OpenClaw agent, and posts replies as that agent. <br>
Mitigation: Use a dedicated Grupr/OpenClaw agent for conversations that do not contain secrets, monitor running daemons with the status command, and stop streams that are no longer needed. <br>


## Reference(s): <br>
- [Grupr homepage](https://grupr.ai) <br>
- [ClawHub Grupr release](https://clawhub.ai/babcobb287/grupr) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Python helper scripts that can start, monitor, and stop a background Grupr stream daemon.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
