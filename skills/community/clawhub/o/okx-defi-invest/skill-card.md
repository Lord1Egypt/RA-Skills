## Description: <br>
Helps agents discover OKX-aggregated DeFi products, compare yield opportunities, prepare invest, withdraw, collect, lending, borrowing, staking, and liquidity workflows, and route protocol-specific requests to the appropriate DApp skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find DeFi yield products through OKX aggregation and prepare transaction steps for deposits, withdrawals, reward collection, lending, borrowing, staking, and liquidity pool actions. It is intended for DApp-agnostic DeFi requests and explicitly reroutes named-protocol requests to protocol-specific discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare invest, withdraw, collect, approve, and contract-call workflows that may move real assets if signed. <br>
Mitigation: Require the user to review chain, protocol, wallet address, spender, amount, slippage, approval scope, and calldata before signing or broadcasting any step. <br>
Risk: Routing rules conflict with protocol-specific examples and may send named DApp requests through the aggregated OKX flow. <br>
Mitigation: Before any DeFi command, check the original prompt for named protocols or protocol-native tokens and reroute those requests to the DApp-discovery skill. <br>
Risk: Wallet-dependent workflows are high impact and require account-specific addresses and balances. <br>
Mitigation: Resolve the correct wallet address for the target chain, verify token balance before investment, and stop if the wallet is not logged in or funds are insufficient. <br>
Risk: Stale position data can cause incorrect withdrawal or reward-collection parameters. <br>
Mitigation: Fetch fresh position detail immediately before every withdraw or collect action and do not reuse earlier position results. <br>
Risk: High APY products and short-lived Solana transactions can mislead users or fail unexpectedly. <br>
Mitigation: Warn users when APY exceeds 50%, and warn that Solana transactions must be signed and broadcast within about 60 seconds. <br>


## Reference(s): <br>
- [OKX DeFi CLI Command Reference](references/cli-reference.md) <br>
- [OKX Web3](https://web3.okx.com) <br>
- [ClawHub Skill Listing](https://clawhub.ai/ok-james-01/okx-defi-invest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and transaction review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes product tables, APY/TVL interpretation, wallet and address checks, calldata execution sequencing, and risk warnings before signing.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
