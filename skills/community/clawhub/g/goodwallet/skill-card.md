## Description:

Crypto wallet for sending, swapping, trading perps, betting on Polymarket, earning DeFi yield, and signing across EVM, Solana, Bitcoin, Doge, and XRP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peteremiljensen](https://clawhub.ai/user/peteremiljensen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate the Goodwallet CLI for wallet balances, token transfers, swaps, perpetual trading, Polymarket betting, DeFi yield, and transaction signing. The skill is intended for workflows where the agent summarizes CLI results and requests confirmation before any command that moves funds or creates exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform real wallet, trading, betting, signing, and fund-movement workflows.

Mitigation: Inspect balances, quotes, or positions before state-changing actions and require explicit user confirmation for sends, swap execution, trades, bets, earn deposits or withdrawals, and signing.

Risk: The skill depends on a broadly triggered, unpinned globally installed CLI.

Mitigation: Install it only for agents that should operate Goodwallet, and verify the package version plus exact command, asset, amount, recipient, and network before approving high-risk prompts.

Risk: Wallet configuration, encrypted MPC key shares, and auth tokens are stored locally.

Mitigation: Avoid exposing internal wallet details in responses, preserve local configuration confidentiality, and use browser OAuth logout when disconnecting the wallet.

## Reference(s):

- [GoodWallet ClawHub skill](https://clawhub.ai/peteremiljensen/skills/goodwallet)
- [GoodWallet homepage](https://goodwallet.etoro.com)
- [goodwallet npm package](https://www.npmjs.com/package/goodwallet)
- [Publisher profile](https://clawhub.ai/user/peteremiljensen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline CLI commands and concise plain-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the globally installed goodwallet CLI and browser OAuth pairing for authentication.]

## Skill Version(s):

1.7.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
