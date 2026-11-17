## Description:

Read-only API reference for NexusWeb3 safety protocols 21-30 on Base mainnet, covering kill switch status, KYA verification, audit logs, bounties, licensing, milestones, subscriptions, insolvency, referrals, and collectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexusweb3dev](https://clawhub.ai/user/nexusweb3dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to find Base mainnet contract addresses, view functions, and example calls for NexusWeb3 safety and compliance protocols. It is intended for read-oriented agent assistance around protocol status, verification, audit logs, and related on-chain reference data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is presented as read-only but includes examples for transactions that can move funds, alter permissions, or create persistent token approvals.

Mitigation: Use it as reference material by default; require explicit user confirmation, verified contract addresses, and exact bounded amounts before any write transaction is prepared or submitted.

Risk: Some documented on-chain actions are irreversible or persistent, including permanent kill-switch actions, non-transferable collective membership tokens, and token approvals.

Mitigation: Review current protocol state, transaction intent, allowance size, and recovery options before acting; avoid unlimited USDC approvals unless the user deliberately accepts the continuing allowance risk.

## Reference(s):

- [NexusWeb3 Protocols](https://github.com/nexusweb3dev/nexusweb3-protocols)
- [ClawHub Skill Page](https://clawhub.ai/nexusweb3dev/skills/nexusweb3-safety)
- [Base Mainnet RPC](https://mainnet.base.org)
- [BaseScan](https://basescan.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with Solidity-style call examples and network configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no credentials or downloads are required for documented read operations.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
