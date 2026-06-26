## Description: <br>
Deploy a chat and collaboration hub with four agents for group chat, threaded conversations, moderation, translation, and archival workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a four-agent, self-hosted collaboration hub with a chat server, moderator, translator, and archive bot. It guides installation, host naming, trust handshakes, data flows, and example message exchange commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted pilotctl, clawhub, or pilot-* packages could affect the deployed chat hub. <br>
Mitigation: Verify tool and package provenance before installation, and deploy only between nodes you control. <br>
Risk: Translation, moderation, and archive flows can expose or retain sensitive conversation content. <br>
Mitigation: Define retention periods, backup protection, access controls, redaction rules, and user notice or consent before using the hub for real conversations. <br>
Risk: Trust handshakes determine which nodes can exchange chat, moderation, translation, and archive messages. <br>
Mitigation: Review handshake targets and verify trust state with pilotctl trust before sending operational messages. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-chat-collaboration-hub-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON manifest examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance assumes pilotctl, clawhub, pilot-protocol, and a running daemon are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
