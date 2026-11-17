## Description:

On-chain credit scoring and soulbound identity for autonomous agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to create soulbound on-chain identities for autonomous agents, query reputation scores, record attestations, compare agents, and generate reputation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a wallet private key for transaction signing.

Mitigation: Use a dedicated testnet-only wallet with minimal funds and avoid exposing mainnet or private asset wallets.

Risk: Identity creation and attestation actions can spend gas.

Mitigation: Require explicit user confirmation before any transaction that creates an identity or records an attestation.

Risk: On-chain identity and reputation data can be permanent and reputation-affecting.

Mitigation: Review all agent identity details and attestation content before signing transactions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/openclaw-agent-reputation)
- [Publisher Profile](https://clawhub.ai/user/zhenstaff)
- [Project Homepage](https://github.com/ZhenRobotics/openclaw-agent-reputation)
- [Documentation](https://github.com/ZhenRobotics/openclaw-agent-reputation/blob/main/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown or text guidance with optional JSON reports and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction hashes, token IDs, credit score metrics, comparison tables, and formatted reputation reports.]

## Skill Version(s):

1.0.0 (source: release metadata and changelog; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
