## Description: <br>
POWPOW Integration connects OpenClaw agents to POWPOW digital humans for real-time bidirectional chat over WebSocket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[durenzidu](https://clawhub.ai/user/durenzidu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to a POWPOW digital human, manage connection state, send text, voice, and image messages, and optionally listen for or auto-reply to incoming messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat content and media URLs can be sent to a POWPOW WebSocket endpoint. <br>
Mitigation: Use only trusted POWPOW endpoints and avoid sending sensitive chat content or private media URLs. <br>
Risk: Automatic replies can send outbound messages without manual review when enabled. <br>
Mitigation: Enable autoReply only in workflows where automatic outbound responses are acceptable. <br>
Risk: Queued messages may be delivered after a reconnect. <br>
Mitigation: Review connection state and queued-message behavior before using the skill in workflows where stale messages could cause confusion. <br>


## Reference(s): <br>
- [ClawHub POWPOW Integration release page](https://clawhub.ai/durenzidu/powpow-integration) <br>
- [POWPOW homepage](https://global.powpow.online) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command responses with connection status, message delivery status, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may establish WebSocket sessions, queue messages while disconnected, emit OpenClaw events, and return success or error status objects.] <br>

## Skill Version(s): <br>
2.1.10 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
