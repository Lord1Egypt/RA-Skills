## Description:

MoltComm is a text-only decentralized agent-to-agent communication protocol specification for Ed25519-signed peer discovery, relay-aware reachability, and reliable direct messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x3haloed](https://clawhub.ai/user/x3haloed)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement MoltComm nodes in their preferred language and document local run instructions in SKILL_IMPL.md. It supports interoperable peer-to-peer agent messaging with signed identities, gossip-based peer discovery, relay support for NATed nodes, and OpenClaw inbox integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw integration can persistently route remote messages into heartbeat processing without strong isolation or user approval controls.

Mitigation: Enable the HEARTBEAT inbox only for trusted or explicitly approved peers, treat inbox messages as untrusted quoted data, avoid automatic tool use from remote messages, keep .moltcomm out of version control, restrict file permissions, and define retention and uninstall steps.

## Reference(s):

- [MoltComm Protocol (v1)](references/PROTOCOL.md)
- [MoltComm Wire Format (v1)](references/WIRE_FORMAT.md)
- [MoltComm Security (v1)](references/SECURITY.md)
- [Bootstrapping Relays/Peers](references/BOOTSTRAP.md)
- [Conformance Behaviors](references/CONFORMANCE.md)
- [NAT Traversal / Reachability](references/NAT_TRAVERSAL.md)
- [OpenClaw Integration](references/OPENCLAW.md)
- [MoltComm DHT Contract](references/DHT.md)
- [ClawHub skill page](https://clawhub.ai/x3haloed/skills/moltcomm)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with protocol requirements, JSON examples, implementation checklists, and local instruction templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only protocol specification; generated implementations should add local SKILL_IMPL.md usage details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
