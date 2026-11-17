## Description:

Manage a Kite AI smart wallet with Telegram commands for wallet creation, balance checks, session keys, spending limits, and testnet transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nihaovand](https://clawhub.ai/user/nihaovand)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to run a local Telegram bot for Kite AI testnet wallet operations, including creating smart wallets, checking balances, managing session keys, setting spending limits, and sending testnet transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private keys for wallet operations.

Mitigation: Use only a low-value testnet key, keep environment files out of source control, and prefer safer key storage before broader use.

Risk: Telegram commands can change wallet state, including send, session, and limit actions.

Mitigation: Restrict who can message the bot and require explicit confirmation, address validation, ownership verification, and rate limits before enabling those commands.

Risk: The security verdict is suspicious because wallet-changing actions have weak safeguards.

Mitigation: Review the skill carefully before installation and avoid running wallet-changing commands until the safeguards are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nihaovand/skills/kite-agent-smart-wallet-permissionless-protocol-v2)
- [Kite AI Website](https://gokite.ai)
- [Kite AI Documentation](https://docs.gokite.ai)
- [Kite Testnet Explorer](https://testnet.kitescan.ai)
- [Kite Testnet Faucet](https://faucet.gokite.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, environment configuration examples, and Telegram bot text responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can initiate Kite testnet wallet-changing actions when configured with a private key and Telegram bot token.]

## Skill Version(s):

2.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
