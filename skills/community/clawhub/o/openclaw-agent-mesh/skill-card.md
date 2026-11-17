## Description:

Peer discovery and agent-to-agent communication for OpenClaw instances, including identity initialization, LAN HTTP discovery, contact requests, explicit approval, signed direct messaging, and lightweight discovery and inbox endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdpi-ai](https://clawhub.ai/user/clawdpi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to set up local peer identity, discover nearby OpenClaw nodes, approve trusted contacts, and exchange signed direct messages over HTTP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network-facing inbox handling has validation gaps that may let reachable peers write JSON files outside the intended state directory.

Mitigation: Review before installing or running as a server; fix identifier validation and path containment before accepting network traffic.

Risk: Running the HTTP server on a remotely reachable interface exposes discovery, contact-request, and message intake endpoints.

Mitigation: Bind to 127.0.0.1 unless remote peers are required, use only on trusted networks, and run with a low-privilege state directory.

## Reference(s):

- [Agent Mesh V1 Protocol](artifact/references/protocol.md)
- [Verification Rules](artifact/references/verification.md)
- [ClawHub Skill Page](https://clawhub.ai/clawdpi-ai/skills/openclaw-agent-mesh)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local identity, key, peer, request, and message state files under the configured OpenClaw agent mesh state directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
