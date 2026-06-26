## Description: <br>
Send and receive encrypted peer-to-peer messages between OpenClaw agents over Yggdrasil IPv6, with peer discovery, messaging, and connectivity diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jing-yilin](https://clawhub.ai/user/Jing-yilin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to discover reachable OpenClaw peers, exchange direct encrypted messages, share their own P2P address, and diagnose Yggdrasil connectivity issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Active P2P discovery can expose a reachable network identity to bootstrap nodes and discovered peers. <br>
Mitigation: Install and run this skill only when P2P discovery is intentional, and keep controls available to disable discovery or restrict listeners when it is not needed. <br>
Risk: Automatic peer announcements may be broader than users expect in private, corporate, or monitored environments. <br>
Mitigation: Review the discovery behavior and configured bootstrap peers before deployment, and confirm that network visibility matches the environment's security policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jing-yilin/ipv6-p2p) <br>
- [Peer Discovery](references/discovery.md) <br>
- [IPv6 P2P Example Interaction Flows](references/flows.md) <br>
- [DeClaw project homepage](https://github.com/ReScienceLab/declaw) <br>
- [Bootstrap node list](https://resciencelab.github.io/DeClaw/bootstrap.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [Markdown or plain text with P2P tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Yggdrasil or ULA IPv6 addresses, peer aliases, ports, discovery status, inbox counts, and connectivity diagnostics.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
