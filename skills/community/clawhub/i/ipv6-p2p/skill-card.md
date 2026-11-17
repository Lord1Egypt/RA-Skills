## Description:

Send/receive direct encrypted P2P messages between OpenClaw agents using Yggdrasil or ULA IPv6 addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jing-yilin](https://clawhub.ai/user/jing-yilin)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to discover peers, exchange encrypted direct messages between agents, inspect P2P status, and diagnose Yggdrasil connectivity issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may participate in a Yggdrasil P2P network, announce itself to bootstrap and discovered peers, and receive inbound P2P messages.

Mitigation: Install only in environments where P2P discovery and inbound messaging are acceptable, and restrict or disable discovery before use in sensitive environments.

Risk: The release evidence notes installation of unpinned external code.

Mitigation: Prefer a pinned, audited package version before installing or deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jing-yilin/skills/ipv6-p2p)
- [Peer Discovery](artifact/references/discovery.md)
- [IPv6 P2P Example Interaction Flows](artifact/references/flows.md)
- [DeClaw project homepage](https://github.com/ReScienceLab/declaw)
- [DeClaw bootstrap node list](https://resciencelab.github.io/DeClaw/bootstrap.json)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Plain text or Markdown responses with P2P tool-call guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include peer addresses, delivery status, discovery results, and connectivity diagnostics.]

## Skill Version(s):

0.1.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
