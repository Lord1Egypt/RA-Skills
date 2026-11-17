## Description:

Enables agents to control Kite AI testnet smart wallets through Telegram/OpenClaw commands for wallet creation, balance checks, transfers, session keys, and spending limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nihaovand](https://clawhub.ai/user/nihaovand)

### License/Terms of Use:


## Use Case:

External users and operators use this skill through Telegram/OpenClaw to manage Kite AI testnet wallet workflows, including creating wallets, checking balances, sending funds, managing session keys, and setting spending limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram commands can exercise high-impact wallet authority without enough in-skill authorization or confirmation.

Mitigation: Enforce authenticated owners and require explicit confirmations before transfers, permission changes, and spending-limit updates.

Risk: Ordinary users may be exposed to operator wallet authority or balances if wallet actions are not scoped to the intended smart wallet.

Mitigation: Use only a low-value testnet private key, hide operator wallet balances, and route user transfers through the intended smart wallet and its limits.

Risk: Wildcard session-key permissions can grant broader authority than intended.

Mitigation: Restrict session keys to specific function selectors and bounded per-session limits before granting access.

## Reference(s):

- [ClawHub Skill Release Page](https://clawhub.ai/nihaovand/skills/kite-agent-smart-wallet-v3)
- [Kite Testnet RPC Endpoint](https://rpc-testnet.gokite.ai)
- [Kite Testnet Faucet](https://faucet.gokite.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Telegram command responses in Markdown with on-chain transaction requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured low-value Kite testnet wallet key and access to the Kite testnet RPC endpoint.]

## Skill Version(s):

3.0.2 (source: server-resolved release metadata; artifact skill.json states 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
