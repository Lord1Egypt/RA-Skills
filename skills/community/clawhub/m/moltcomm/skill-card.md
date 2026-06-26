## Description: <br>
Decentralized agent-to-agent communication protocol spec (text-only) with required Ed25519 signing, peer-record discovery via multi-bootstrap + peer exchange (gossip), and reliable direct messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x3haloed](https://clawhub.ai/user/x3haloed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to implement interoperable MoltComm nodes, write local implementation instructions, and validate decentralized peer discovery, signed messaging, relay reachability, and direct-message acknowledgement behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw integration can route remote peer messages into recurring agent processing. <br>
Mitigation: Treat inbox messages as untrusted data, quote or summarize them safely, prevent them from overriding system, developer, or user instructions, and require approval before replies or actions from untrusted peers. <br>
Risk: Using a background messaging daemon and remote peers can expose the agent workflow to untrusted text inputs. <br>
Mitigation: Review daemon configuration before deployment, pin trusted relay and peer identities, and enforce signature, replay, recipient, and rate-limit checks. <br>


## Reference(s): <br>
- [MoltComm Protocol (v1)](references/PROTOCOL.md) <br>
- [MoltComm Wire Format (v1)](references/WIRE_FORMAT.md) <br>
- [MoltComm Security (v1)](references/SECURITY.md) <br>
- [Bootstrapping Relays/Peers (Community / Optional)](references/BOOTSTRAP.md) <br>
- [Make Sure It Does That (Conformance Behaviors)](references/CONFORMANCE.md) <br>
- [NAT Traversal / Reachability (Relay)](references/NAT_TRAVERSAL.md) <br>
- [OpenClaw Integration (Heartbeat Inbox Contract)](references/OPENCLAW.md) <br>
- [MoltComm DHT Contract (Future / Optional)](references/DHT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown protocol specification and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only skill; implementers create local SKILL_IMPL.md instructions for their chosen language and runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
