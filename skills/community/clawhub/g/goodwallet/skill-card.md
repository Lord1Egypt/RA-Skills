## Description: <br>
Crypto wallet for sending, swapping, trading perps, betting on Polymarket, earning DeFi yield, and signing across EVM, Solana, Bitcoin, Doge, and XRP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peteremiljensen](https://clawhub.ai/user/peteremiljensen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to interact with the GoodWallet CLI for wallet balances, sends, swaps, perpetual trades, Polymarket bets, DeFi yield actions, and signing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real financial actions, including token transfers, swaps, trades, bets, yield actions, and signing requests. <br>
Mitigation: Inspect balances, quotes, positions, recipients, assets, amounts, markets, and signing requests before approval, and require explicit user confirmation before any state-changing command. <br>
Risk: Wallet configuration, encrypted MPC key shares, and authentication tokens are stored locally on the user's device. <br>
Mitigation: Use only on a trusted device and install only if the user trusts GoodWallet, GoodDollar, and the npm package. <br>
Risk: The skill depends on GoodWallet external services for MPC co-signing and transaction policy enforcement. <br>
Mitigation: Treat service availability and policy responses as part of the approval path, and report failures plainly without automatic retries. <br>


## Reference(s): <br>
- [GoodWallet homepage](https://goodwallet.etoro.com) <br>
- [GoodWallet npm package](https://www.npmjs.com/package/goodwallet) <br>
- [ClawHub GoodWallet listing](https://clawhub.ai/peteremiljensen/goodwallet) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and concise plain-language summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for user confirmation before fund movement, market exposure, yield deposits or withdrawals, and signing actions.] <br>

## Skill Version(s): <br>
1.7.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
