## Description: <br>
OpenClaw Agent Mesh helps OpenClaw instances discover approved peers, establish trust, and exchange signed direct messages over a lightweight HTTP JSON workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClawdPI-AI](https://clawhub.ai/user/ClawdPI-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to initialize local OpenClaw mesh identities, discover nearby OpenClaw nodes, approve contact requests, and exchange verified direct messages between trusted peers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose a local HTTP service for peer discovery, contact requests, and direct-message intake. <br>
Mitigation: Run the server only on networks and peers you control or explicitly trust, keep it on localhost unless remote peer access is required, and prefer HTTPS endpoints. <br>
Risk: The skill stores private keys, peer data, contact requests, and inbound messages in local state. <br>
Mitigation: Protect the state directory and private key with restrictive permissions, and periodically audit or delete stored inbound network data. <br>
Risk: Discovery results alone do not establish trust between agents. <br>
Mitigation: Require explicit contact approval before accepting direct messages and verify signatures, timestamps, and message IDs before storing inbound messages. <br>


## Reference(s): <br>
- [Agent Mesh V1 Protocol](references/protocol.md) <br>
- [Verification Rules](references/verification.md) <br>
- [OpenClaw Agent Mesh on ClawHub](https://clawhub.ai/ClawdPI-AI/openclaw-agent-mesh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON file descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or inspect local mesh state files under the configured OpenClaw agent mesh state directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
