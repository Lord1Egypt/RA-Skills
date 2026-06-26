## Description: <br>
Goodwallet Alpha helps agents use the Goodwallet CLI to inspect crypto wallets, send funds, swap, trade, bet, earn yield, and sign across EVM, Solana, Bitcoin, Doge, and XRP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gooddollar](https://clawhub.ai/user/gooddollar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate Goodwallet through its CLI for wallet checks, quotes, signing, transfers, swaps, trading, betting, and DeFi yield workflows. It is intended for crypto actions that require read-before-write checks and explicit user confirmation before any command that moves funds or creates exposure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate crypto actions that move funds or create market exposure. <br>
Mitigation: Inspect balances, quotes, or positions before write actions, and require explicit user confirmation before send, swap execution, trade, bet, earn, or sign commands. <br>
Risk: The skill asks the agent to install or update a global wallet CLI. <br>
Mitigation: Approve installation and updates yourself, trust the Goodwallet npm package before use, and use the globally installed binary rather than npx. <br>
Risk: Wallet configuration, encrypted MPC key shares, and auth tokens are stored locally while signing depends on GoodDollar-operated services. <br>
Mitigation: Use a trusted device, protect the local Goodwallet config directory, start with small transactions, and carefully review every signing or transaction prompt. <br>


## Reference(s): <br>
- [Goodwallet homepage](https://goodwallet.dev) <br>
- [Goodwallet npm package](https://www.npmjs.com/package/goodwallet) <br>
- [ClawHub skill page](https://clawhub.ai/gooddollar/goodwallet-alpha) <br>
- [GoodDollar publisher profile](https://clawhub.ai/user/gooddollar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline CLI commands and concise plain-language summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet status, quotes, transaction summaries, or confirmation prompts based on Goodwallet CLI output.] <br>

## Skill Version(s): <br>
0.5.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
