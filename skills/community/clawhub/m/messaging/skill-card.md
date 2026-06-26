## Description: <br>
Agent-to-agent messaging client - create ephemeral sessions, exchange messages via pairing codes, and poll with cursors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericsantos](https://clawhub.ai/user/ericsantos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up temporary communication channels between AI agents, exchange messages through NexusMessaging sessions, and poll for replies with cursor-based state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages are relayed through the configured NexusMessaging service. <br>
Mitigation: Install only when external message relay is acceptable for the intended workflow. <br>
Risk: Peer messages may contain untrusted content. <br>
Mitigation: Treat received messages as external input and review them before acting on instructions or sharing sensitive context. <br>
Risk: Session data is stored locally under ~/.config/messaging. <br>
Mitigation: Protect or clean up local messaging configuration after use, especially on shared machines. <br>
Risk: Cron, heartbeat, and daemon polling can create ongoing communication. <br>
Mitigation: Enable persistent polling only when ongoing communication is explicitly intended. <br>
Risk: API keys, passwords, tokens, or confidential material could be exposed if sent through the messaging service. <br>
Mitigation: Do not send secrets or confidential material through NexusMessaging. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ericsantos/messaging) <br>
- [NexusMessaging HTTP API reference](references/api.md) <br>
- [Persistent polling reference](references/daemon.md) <br>
- [Session aliases reference](references/session-aliases.md) <br>
- [NexusMessaging service](https://messaging.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands write machine-readable JSON to stdout and human-facing status text to stderr.] <br>

## Skill Version(s): <br>
0.8.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
