## Description:

Goodwallet Alpha helps agents use the Goodwallet crypto wallet CLI for balances, sends, swaps, perps trading, Polymarket betting, DeFi yield actions, and signing across EVM, Solana, Bitcoin, Doge, and XRP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gooddollar](https://clawhub.ai/user/gooddollar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a Goodwallet CLI wallet through an agent for wallet inspection, transaction preparation, swaps, market actions, DeFi yield actions, and signing workflows. It is intended for users who can review wallet actions and confirm high-impact commands before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive high-impact wallet actions, including sends, swaps, trades, bets, yield deposits or withdrawals, and signing.

Mitigation: Inspect balances, quotes, or positions before any state-changing action and require explicit user confirmation before executing fund movement, exposure-creating, yield, or signing commands.

Risk: The skill relies on a mutable globally installed Goodwallet CLI and updater path.

Mitigation: Install only if the Goodwallet npm package and update path are trusted, and run the documented update check before wallet operations.

Risk: The skill may use a persistent local wallet profile containing encrypted MPC key shares and auth tokens.

Mitigation: Use the skill only on trusted environments, protect the local Goodwallet configuration directory, and disconnect the wallet when access is no longer needed.

## Reference(s):

- [Goodwallet homepage](https://goodwallet.dev)
- [Goodwallet npm package](https://www.npmjs.com/package/goodwallet)
- [Goodwallet source link from skill metadata](https://github.com/GoodDollar/mpc-wallet-api)
- [ClawHub skill listing](https://clawhub.ai/gooddollar/skills/goodwallet-alpha)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise plain-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet action proposals that require user confirmation before execution.]

## Skill Version(s):

0.5.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
