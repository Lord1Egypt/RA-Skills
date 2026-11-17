## Description:

Load when an autonomous agent needs to bridge persistent off-chain swarm coordination with on-chain EVM and Robinhood Chain execution, smart contract audits, and token alignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allisonbit](https://clawhub.ai/user/allisonbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide autonomous agents that coordinate off-chain swarm state, cryptographic attestations, and on-chain execution across EVM-compatible networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous blockchain workflows can submit state-changing transactions or token interactions with financial impact.

Mitigation: Use a dedicated keypair, require explicit user approval for transactions, verify ABI interfaces and codehashes, and check allowances before execution.

Risk: Shared swarm coordination may expose or rely on untrusted peer claims.

Mitigation: Scope shared-bus access and treat observations as claims until corroborated through independent replay.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/allisonbit/skills/onchain-execution-and-consensus)
- [Bankr Terminal Agent Record](https://www.swampai.world/agents/bankr-terminal)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, installs, hidden commands, or data exfiltration behavior were identified in the server security review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
